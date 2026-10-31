"""AI-Powered Student Performance Prediction and Academic Analytics System - Flask app.
The whole UI is generated from Python strings (render_template_string). Run:  python app.py"""
import os, io, json, csv
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, redirect, url_for, flash, render_template_string, jsonify, send_file, abort, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from jinja2 import DictLoader
from database import db, User, Student, Prediction, Report, Notification, Achievement
import model as ml, analytics as an, recommendation as rec, chatbot as bot
from report_generator import build_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get("SECRET_KEY", "change-me-in-production"),
                  SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(BASE_DIR, "student.db"))
db.init_app(app)
lm = LoginManager(app); lm.login_view = "login"

FIELDS = [("attendance", "Attendance %", 0, 100), ("study_hours", "Study hours per day", 0, 16),
          ("internal", "Internal score", 0, 100), ("assignment", "Assignment score", 0, 100),
          ("prev_cgpa", "Previous CGPA", 0, 10), ("project", "Project marks", 0, 100),
          ("practical", "Practical marks", 0, 100)]
COLLEGE = "Goa College of Engineering & Technology"


@lm.user_loader
def load_user(uid): return db.session.get(User, int(uid))


def admin_required(f):
    @wraps(f)
    @login_required
    def w(*a, **k):
        if not current_user.is_admin: abort(403)
        return f(*a, **k)
    return w


@app.before_request
def touch():
    if current_user.is_authenticated and not request.path.startswith("/api/chat"):
        current_user.last_seen = datetime.utcnow(); db.session.commit()


@app.context_processor
def inject():
    unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).count() if current_user.is_authenticated else 0
    return dict(college=COLLEGE, unread=unread)


def read_inputs(form):
    out = {}
    for k, label, lo, hi in FIELDS:
        try: v = float(form.get(k, ""))
        except ValueError: raise ValueError(f"{label} must be a number.")
        if not lo <= v <= hi: raise ValueError(f"{label} must be between {lo} and {hi}.")
        out[k] = v
    return out


def run_prediction(stu, inp):
    """Predict, persist, update student record, raise notifications and award badges."""
    res = ml.predict(inp)
    for k, v in inp.items(): setattr(stu, k, v)
    p = Prediction(student_id=stu.id, predicted_pct=res["pct"], grade=res["grade"], success_prob=res["prob"],
                   risk=res["risk"], category=res["category"], status=res["status"], model_name=res["model"],
                   inputs=json.dumps(inp))
    db.session.add(p)
    uid = stu.user_id
    def note(t, m, k):
        if uid: db.session.add(Notification(user_id=uid, title=t, message=m, kind=k))
    note("Prediction ready", f"Predicted {res['pct']}% (grade {res['grade']}), risk {res['risk']}.", "prediction")
    if inp["attendance"] < 75: note("Attendance warning", rec.attendance_advice(inp["attendance"]), "attendance")
    if res["risk"] == "High": note("At-risk alert", "Early warning: your predicted score is in the risk zone. Review your study plan.", "suggestion")
    w = rec.weak_subjects(inp)
    if w: note("Improvement suggestion", f"Focus on {w[0][0]} ({w[0][1]}%) this week.", "suggestion")
    have = {a.badge for a in stu.achievements}
    for badge, ok in [("Top Performer", res["pct"] >= 85), ("Attendance Star", inp["attendance"] >= 90),
                      ("Academic Excellence", inp["prev_cgpa"] >= 8.5 and res["pct"] >= 80)]:
        if ok and badge not in have:
            db.session.add(Achievement(student_id=stu.id, badge=badge))
            note("Badge earned", f"You earned the {badge} badge!", "prediction")
    db.session.commit()
    return p, res


def insights_for(p):
    inp = json.loads(p.inputs)
    res = {"pct": p.predicted_pct}
    return inp, rec.all_insights(inp, res, ml.percentile_rank(p.predicted_pct))


def page(name, **ctx): return render_template_string(T[name], **ctx)


# ------------------------------------------------------------------ public pages
@app.route("/")
def landing(): return page("landing")


@app.route("/api/demo", methods=["POST"])
def api_demo():
    d = request.get_json(force=True)
    try:
        cg = float(d.get("prev_cgpa", 7)); inp = {"attendance": float(d["attendance"]), "study_hours": float(d["study_hours"]),
              "internal": float(d["internal"]), "assignment": float(d["assignment"]), "prev_cgpa": cg,
              "project": 40 + cg * 4, "practical": 38 + cg * 4.5}
    except (KeyError, ValueError): return jsonify(error="Invalid input"), 400
    return jsonify(ml.predict(inp))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("home"))
    if request.method == "POST":
        ident = request.form.get("identifier", "").strip()
        u = User.query.filter((User.email == ident.lower()) | (User.student_code == ident.upper())).first()
        if u and u.check_password(request.form.get("password", "")):
            login_user(u, remember=bool(request.form.get("remember")))
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else url_for("home"))
        flash("Incorrect email / Student ID or password.", "bad")
    return page("login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form; email = f.get("email", "").strip().lower(); roll = f.get("roll_no", "").strip().upper()
        if not (f.get("name") and email and roll and len(f.get("password", "")) >= 6):
            flash("Fill every field. Password needs at least 6 characters.", "bad")
        elif User.query.filter_by(email=email).first() or Student.query.filter_by(roll_no=roll).first():
            flash("That email or roll number is already registered.", "bad")
        else:
            u = User(name=f["name"].strip(), email=email); u.set_password(f["password"]); db.session.add(u); db.session.flush()
            u.student_code = f"S{1000 + u.id}"
            db.session.add(Student(user_id=u.id, name=u.name, roll_no=roll, email=email, department=f.get("department", "CSE"),
                                   semester=int(f.get("semester", 1))))
            db.session.commit(); flash(f"Account created. Your Student ID is {u.student_code}.", "ok")
            return redirect(url_for("login"))
    return page("signup", depts=ml.DEPTS)


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        u = User.query.filter_by(email=request.form.get("email", "").strip().lower()).first()
        s = u.student if u else None
        if u and s and s.roll_no == request.form.get("roll_no", "").strip().upper() and len(request.form.get("password", "")) >= 6:
            u.set_password(request.form["password"]); db.session.commit()
            flash("Password updated. You can sign in now.", "ok"); return redirect(url_for("login"))
        flash("Email and roll number do not match, or the new password is too short.", "bad")
    return page("forgot")


@app.route("/logout")
@login_required
def logout(): logout_user(); return redirect(url_for("landing"))


@app.route("/home")
@login_required
def home(): return redirect(url_for("admin") if current_user.is_admin else url_for("dashboard"))


# ------------------------------------------------------------------ student pages
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin: return redirect(url_for("admin"))
    s = current_user.student or abort(404)
    last = s.latest
    perf = round(0.4 * (last.predicted_pct if last else 50) + 0.3 * s.attendance + 0.3 * s.prev_cgpa * 10, 1)
    series = [p.predicted_pct for p in reversed(s.predictions[:12])]
    return page("dashboard", s=s, last=last, perf=perf, history=s.predictions[:8],
                trend=an.trend_chart(series) if series else None)


@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    stu = current_user.student
    result = None
    if request.method == "POST":
        try:
            inp = read_inputs(request.form)
            name, roll = request.form.get("name", "").strip(), request.form.get("roll_no", "").strip().upper()
            if not current_user.is_admin: stu = current_user.student
            else:
                if not (name and roll): raise ValueError("Student name and roll number are required.")
                stu = Student.query.filter_by(roll_no=roll).first() or Student(name=name, roll_no=roll)
                db.session.add(stu); db.session.flush()
            p, res = run_prediction(stu, inp)
            _, ins = insights_for(p)
            result = dict(p=p, res=res, ins=ins)
        except ValueError as e: flash(str(e), "bad")
    return page("predict", stu=stu, fields=FIELDS, result=result, form=request.form)


@app.route("/analytics")
@login_required
def analytics():
    df, b = an.load_df(), ml.load_bundle()
    s = current_user.student
    preds = [p.predicted_pct for p in reversed(s.predictions)] if s else None
    return page("analytics", charts=an.plotly_charts(df, b, preds))


@app.route("/leaderboard")
@login_required
def leaderboard():
    rows = [(s, s.latest) for s in Student.query.all() if s.latest]
    rows.sort(key=lambda r: r[1].predicted_pct, reverse=True)
    return page("leaderboard", rows=rows[:25])


@app.route("/notifications")
@login_required
def notifications():
    items = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created.desc()).limit(50).all()
    shown = [(n, n.is_read) for n in items]
    for n in items: n.is_read = True
    db.session.commit()
    return page("notifications", items=shown)


@app.route("/reports")
@login_required
def reports():
    q = Prediction.query.order_by(Prediction.created.desc())
    if not current_user.is_admin: q = q.filter_by(student_id=current_user.student.id)
    return page("reports", preds=q.limit(40).all())


def _owned(pid):
    p = db.session.get(Prediction, pid) or abort(404)
    if not current_user.is_admin and p.student.user_id != current_user.id: abort(403)
    return p


@app.route("/report/<int:pid>/pdf")
@login_required
def report_pdf(pid):
    p = _owned(pid); inp, ins = insights_for(p)
    pdf = build_report(p.student, p, ins, inp, request.host_url)
    fn = f"report_{p.student.roll_no}_{p.id}.pdf"
    if not Report.query.filter_by(prediction_id=p.id).first():
        db.session.add(Report(student_id=p.student_id, prediction_id=p.id, filename=fn)); db.session.commit()
    return send_file(io.BytesIO(pdf), mimetype="application/pdf", as_attachment=bool(request.args.get("dl")), download_name=fn)


@app.route("/report/<int:pid>/print")
@login_required
def report_print(pid): return page("print", p=_owned(pid))


@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    s = current_user.student
    return jsonify(reply=bot.reply((request.get_json(force=True) or {}).get("msg", ""), s, s.latest if s else None))


# ------------------------------------------------------------------ admin
def admin_metrics():
    ps = Prediction.query.all(); b = ml.load_bundle()
    latest = [s.latest.predicted_pct for s in Student.query.all() if s.latest]
    return dict(students=Student.query.count(), preds=len(ps), avg=round(sum(latest) / len(latest), 1) if latest else 0,
                acc=b["best"]["accuracy"], active=User.query.filter(User.last_seen > datetime.utcnow() - timedelta(minutes=15)).count())


@app.route("/admin")
@admin_required
def admin():
    q = request.args.get("q", "").strip()
    qs = Student.query
    if q: qs = qs.filter(Student.name.ilike(f"%{q}%") | Student.roll_no.ilike(f"%{q}%") | Student.department.ilike(f"%{q}%"))
    return page("admin", m=admin_metrics(), students=qs.order_by(Student.id.desc()).limit(100).all(), q=q, depts=ml.DEPTS)


@app.route("/admin/add", methods=["POST"])
@admin_required
def admin_add():
    f = request.form; email = f.get("email", "").strip().lower(); roll = f.get("roll_no", "").strip().upper()
    if not (f.get("name") and email and roll): flash("Name, email and roll number are required.", "bad")
    elif User.query.filter_by(email=email).first() or Student.query.filter_by(roll_no=roll).first():
        flash("Email or roll number already exists.", "bad")
    else:
        u = User(name=f["name"], email=email); u.set_password(f.get("password") or "student123"); db.session.add(u); db.session.flush()
        u.student_code = f"S{1000 + u.id}"
        db.session.add(Student(user_id=u.id, name=f["name"], roll_no=roll, email=email, department=f.get("department", "CSE"),
                               semester=int(f.get("semester") or 1)))
        db.session.commit(); flash(f"Student added with ID {u.student_code}.", "ok")
    return redirect(url_for("admin"))


@app.route("/admin/edit/<int:sid>", methods=["GET", "POST"])
@admin_required
def admin_edit(sid):
    s = db.session.get(Student, sid) or abort(404)
    if request.method == "POST":
        try:
            for k, v in read_inputs(request.form).items(): setattr(s, k, v)
            s.name, s.department = request.form["name"], request.form.get("department", s.department)
            s.semester = int(request.form.get("semester", s.semester)); db.session.commit()
            flash("Student updated.", "ok"); return redirect(url_for("admin"))
        except ValueError as e: flash(str(e), "bad")
    return page("edit", s=s, fields=FIELDS, depts=ml.DEPTS)


@app.route("/admin/delete/<int:sid>", methods=["POST"])
@admin_required
def admin_delete(sid):
    s = db.session.get(Student, sid) or abort(404)
    u = s.user
    if u:
        Notification.query.filter_by(user_id=u.id).delete(); db.session.delete(s); db.session.delete(u)
    else: db.session.delete(s)
    db.session.commit(); flash("Student deleted.", "ok"); return redirect(url_for("admin"))


@app.route("/admin/model", methods=["GET", "POST"])
@admin_required
def admin_model():
    if request.method == "POST":
        if request.form.get("regen"): ml.generate_dataset(seed=int(datetime.now().timestamp()) % 10000)
        ml.train_all(); flash("Models retrained and the best one was saved to model.pkl.", "ok")
        return redirect(url_for("admin_model"))
    b = ml.load_bundle(); df = an.load_df()
    return page("model", b=b, imgs=an.mpl_images(df, b))


@app.route("/admin/export")
@admin_required
def admin_export():
    out = io.StringIO(); w = csv.writer(out); w.writerow(["roll_no", "name", "department", "semester"] + ml.FEATURES + ["latest_pct"])
    for s in Student.query.all(): w.writerow([s.roll_no, s.name, s.department, s.semester] + [getattr(s, k) for k in ml.FEATURES] + [s.latest.predicted_pct if s.latest else ""])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=students_export.csv"})


@app.route("/admin/clear-predictions", methods=["POST"])
@admin_required
def admin_clear():
    Report.query.delete(); Prediction.query.delete(); Achievement.query.delete(); db.session.commit()
    flash("All predictions, reports and badges were cleared.", "ok"); return redirect(url_for("admin"))


@app.errorhandler(403)
def e403(e): return page("err", code=403, msg="You do not have access to this page."), 403


@app.errorhandler(404)
def e404(e): return page("err", code=404, msg="That page does not exist."), 404


# ------------------------------------------------------------------ seed data
def seed():
    db.create_all()
    if not os.path.exists(ml.CSV): ml.generate_dataset()
    if not os.path.exists(ml.PKL): ml.train_all()
    if User.query.first(): return
    a = User(name="Administrator", email="admin@college.edu", role="admin", student_code="ADMIN"); a.set_password("admin123")
    db.session.add(a)
    import pandas as pd
    for i, r in pd.read_csv(ml.CSV).head(30).iterrows():
        u = User(name=r["name"], email="student@college.edu" if i == 0 else f"{r['roll_no'].lower()}@college.edu", student_code=f"S{1001 + i}")
        u.set_password("student123"); db.session.add(u); db.session.flush()
        s = Student(user_id=u.id, name=r["name"], roll_no=r["roll_no"], email=u.email, department=r["department"], semester=int(r["semester"]))
        db.session.add(s); db.session.flush()
        run_prediction(s, {k: float(r[k]) for k in ml.FEATURES})
    db.session.commit()




def bootstrap():
    with app.app_context(): seed()


# ------------------------------------------------------------------ UI (Jinja strings)
from ui import T   # noqa: E402  (templates live in ui.py as Python strings; still no HTML/CSS files)
app.jinja_env.loader = DictLoader(T)

if __name__ == "__main__":
    bootstrap()
    app.run(debug=False)
