"""CustomTkinter desktop client (viva demo). Same database, models and PDF engine as the web app.
Pages: Splash, Login, Registration, Student Dashboard, Admin Dashboard, Prediction Window, Reports Window.
Run:  python desktop_app.py"""
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app import app, bootstrap, db, User, Student, Prediction, run_prediction, insights_for, admin_metrics
import model as ml, analytics as an
from report_generator import build_report

ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("blue")
LABELS = {"attendance": "Attendance %", "study_hours": "Study hours / day", "internal": "Internal score", "assignment": "Assignment score",
          "prev_cgpa": "Previous CGPA", "project": "Project marks", "practical": "Practical marks"}


def table(parent, cols, rows, h=10):
    t = ttk.Treeview(parent, columns=cols, show="headings", height=h)
    for c in cols: t.heading(c, text=c); t.column(c, width=100, anchor="center")
    for r in rows: t.insert("", "end", values=r)
    return t


def show_fig(parent, fig):
    c = FigureCanvasTkAgg(fig, master=parent); c.draw(); c.get_tk_widget().pack(fill="both", expand=True)


class DesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__(); self.title("EduPredict AI - Desktop"); self.geometry("1150x700"); self.user = None
        self.ctx = app.app_context(); self.ctx.push(); bootstrap(); self.splash()

    def clear(self):
        for w in self.winfo_children(): w.destroy()

    # 1. Splash
    def splash(self):
        self.clear(); ctk.CTkLabel(self, text="EduPredict AI", font=("Segoe UI", 40, "bold")).pack(pady=(220, 4))
        ctk.CTkLabel(self, text="Student Performance Prediction and Academic Analytics").pack()
        bar = ctk.CTkProgressBar(self, width=360); bar.pack(pady=24); bar.set(0)
        def step(v=0):
            bar.set(v)
            self.after(40, lambda: step(v + .04)) if v < 1 else self.login_page()
        step()

    # 2. Login
    def login_page(self):
        self.clear(); f = ctk.CTkFrame(self, width=380); f.pack(pady=120, ipadx=30, ipady=20)
        ctk.CTkLabel(f, text="Sign in", font=("Segoe UI", 26, "bold")).pack(pady=14)
        ident = ctk.CTkEntry(f, placeholder_text="Email or Student ID", width=280); ident.pack(pady=6)
        pw = ctk.CTkEntry(f, placeholder_text="Password", show="*", width=280); pw.pack(pady=6)
        def go():
            i = ident.get().strip()
            u = User.query.filter((User.email == i.lower()) | (User.student_code == i.upper())).first()
            if u and u.check_password(pw.get()): self.user = u; self.admin_page() if u.is_admin else self.student_page()
            else: messagebox.showerror("Sign in failed", "Incorrect email / Student ID or password.")
        ctk.CTkButton(f, text="Sign in", command=go, width=280).pack(pady=10)
        ctk.CTkButton(f, text="Create account", fg_color="transparent", command=self.register_page).pack()
        ctk.CTkLabel(f, text="Demo: student@college.edu / student123   |   admin@college.edu / admin123", font=("Segoe UI", 10)).pack(pady=6)

    # 3. Registration
    def register_page(self):
        self.clear(); f = ctk.CTkFrame(self); f.pack(pady=70, ipadx=30, ipady=14)
        ctk.CTkLabel(f, text="Student registration", font=("Segoe UI", 24, "bold")).pack(pady=10)
        e = {}
        for k, ph in [("name", "Full name"), ("email", "Email"), ("roll", "Roll number"), ("pw", "Password (min 6)")]:
            e[k] = ctk.CTkEntry(f, placeholder_text=ph, width=300, show="*" if k == "pw" else ""); e[k].pack(pady=5)
        dept = ctk.CTkOptionMenu(f, values=ml.DEPTS, width=300); dept.pack(pady=5)
        def save():
            n, em, r, p = (e[k].get().strip() for k in ("name", "email", "roll", "pw"))
            if not (n and em and r and len(p) >= 6): return messagebox.showwarning("Missing details", "Fill every field. Password needs 6+ characters.")
            if User.query.filter_by(email=em.lower()).first() or Student.query.filter_by(roll_no=r.upper()).first():
                return messagebox.showerror("Already registered", "That email or roll number already exists.")
            u = User(name=n, email=em.lower()); u.set_password(p); db.session.add(u); db.session.flush(); u.student_code = f"S{1000 + u.id}"
            db.session.add(Student(user_id=u.id, name=n, roll_no=r.upper(), email=em.lower(), department=dept.get())); db.session.commit()
            messagebox.showinfo("Registered", f"Your Student ID is {u.student_code}"); self.login_page()
        ctk.CTkButton(f, text="Register", command=save, width=300).pack(pady=10)
        ctk.CTkButton(f, text="Back", fg_color="transparent", command=self.login_page).pack()

    # shared shell
    def shell(self, items):
        self.clear(); side = ctk.CTkFrame(self, width=200); side.pack(side="left", fill="y")
        ctk.CTkLabel(side, text="EduPredict AI", font=("Segoe UI", 18, "bold")).pack(pady=18)
        for t, c in items: ctk.CTkButton(side, text=t, command=c, fg_color="transparent", anchor="w").pack(fill="x", padx=8, pady=2)
        ctk.CTkButton(side, text="Logout", fg_color="#b91c1c", command=self.login_page).pack(side="bottom", pady=16, padx=8, fill="x")
        self.body = ctk.CTkFrame(self, fg_color="transparent"); self.body.pack(side="left", fill="both", expand=True, padx=16, pady=12)

    def reset_body(self):
        for w in self.body.winfo_children(): w.destroy()

    # 4. Student dashboard
    def student_page(self):
        self.shell([("Dashboard", self.student_page), ("New prediction", lambda: self.predict_window(self.user.student)),
                    ("Graphs", self.graphs), ("Reports", lambda: self.reports_window(self.user.student)), ])
        s = self.user.student; l = s.latest; self.reset_body()
        ctk.CTkLabel(self.body, text=f"Welcome, {s.name}", font=("Segoe UI", 26, "bold")).pack(anchor="w")
        row = ctk.CTkFrame(self.body); row.pack(fill="x", pady=10)
        for t, v in [("CGPA", s.prev_cgpa), ("Attendance", f"{s.attendance:.0f}%"), ("Latest prediction", f"{l.predicted_pct}%" if l else "-"),
                     ("Risk", l.risk if l else "-")]:
            c = ctk.CTkFrame(row); c.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(c, text=t).pack(pady=(8, 0)); ctk.CTkLabel(c, text=str(v), font=("Segoe UI", 22, "bold")).pack(pady=(0, 8))
        table(self.body, ("Date", "Predicted %", "Grade", "Pass %", "Risk"),
              [(p.created.strftime("%d %b %H:%M"), p.predicted_pct, p.grade, p.success_prob, p.risk) for p in s.predictions[:12]]).pack(fill="x")

    # 5. Admin dashboard
    def admin_page(self):
        self.shell([("Dashboard", self.admin_page), ("Predict", lambda: self.predict_window(None)), ("Model training", self.model_window),
                    ("Graphs", self.graphs), ("Reports", lambda: self.reports_window(None))])
        self.reset_body(); m = admin_metrics()
        ctk.CTkLabel(self.body, text="Admin dashboard", font=("Segoe UI", 26, "bold")).pack(anchor="w")
        row = ctk.CTkFrame(self.body); row.pack(fill="x", pady=10)
        for t, v in [("Students", m["students"]), ("Predictions", m["preds"]), ("Avg score", f"{m['avg']}%"), ("Accuracy", f"{m['acc']}%"), ("Active", m["active"])]:
            c = ctk.CTkFrame(row); c.pack(side="left", expand=True, fill="x", padx=4)
            ctk.CTkLabel(c, text=t).pack(pady=(8, 0)); ctk.CTkLabel(c, text=str(v), font=("Segoe UI", 20, "bold")).pack(pady=(0, 8))
        bar = ctk.CTkFrame(self.body, fg_color="transparent"); bar.pack(fill="x")
        q = ctk.CTkEntry(bar, placeholder_text="Search name / roll / dept", width=260); q.pack(side="left", padx=4)
        holder = ctk.CTkFrame(self.body); holder.pack(fill="both", expand=True, pady=8)
        def fill(*_):
            for w in holder.winfo_children(): w.destroy()
            t = q.get().strip().lower()
            rows = [s for s in Student.query.all() if t in f"{s.name} {s.roll_no} {s.department}".lower()]
            self.tree = table(holder, ("ID", "Roll", "Name", "Dept", "Attendance", "Latest %"),
                              [(s.id, s.roll_no, s.name, s.department, f"{s.attendance:.0f}", s.latest.predicted_pct if s.latest else "-") for s in rows], 14)
            self.tree.pack(fill="both", expand=True)
        def add():
            w = ctk.CTkToplevel(self); w.title("Add student"); w.geometry("320x340"); e = {}
            for k in ("name", "email", "roll"): e[k] = ctk.CTkEntry(w, placeholder_text=k.title(), width=260); e[k].pack(pady=8)
            def ok():
                n, em, r = e["name"].get().strip(), e["email"].get().strip().lower(), e["roll"].get().strip().upper()
                if not (n and em and r): return messagebox.showwarning("Missing", "All fields required.", parent=w)
                if User.query.filter_by(email=em).first() or Student.query.filter_by(roll_no=r).first(): return messagebox.showerror("Duplicate", "Email or roll exists.", parent=w)
                u = User(name=n, email=em); u.set_password("student123"); db.session.add(u); db.session.flush(); u.student_code = f"S{1000 + u.id}"
                db.session.add(Student(user_id=u.id, name=n, roll_no=r, email=em)); db.session.commit(); w.destroy(); fill()
            ctk.CTkButton(w, text="Add (password: student123)", command=ok).pack(pady=12)
        def delete():
            sel = self.tree.selection()
            if sel and messagebox.askyesno("Delete", "Delete the selected student and all their data?"):
                s = db.session.get(Student, int(self.tree.item(sel[0])["values"][0])); u = s.user
                db.session.delete(s); db.session.delete(u) if u else None; db.session.commit(); fill()
        ctk.CTkButton(bar, text="Search", width=80, command=fill).pack(side="left"); ctk.CTkButton(bar, text="Add student", command=add).pack(side="left", padx=6)
        ctk.CTkButton(bar, text="Delete selected", fg_color="#b91c1c", command=delete).pack(side="left"); fill()

    # 6. Prediction window
    def predict_window(self, stu):
        w = ctk.CTkToplevel(self); w.title("AI Prediction"); w.geometry("560x640"); e = {}
        if stu is None:
            for k, ph in (("name", "Student name"), ("roll", "Roll number")): e[k] = ctk.CTkEntry(w, placeholder_text=ph, width=300); e[k].pack(pady=5)
        for k, lab in LABELS.items():
            e[k] = ctk.CTkEntry(w, placeholder_text=lab, width=300); e[k].pack(pady=5)
            if stu: e[k].insert(0, str(getattr(stu, k)))
        out = ctk.CTkLabel(w, text="", justify="left", font=("Segoe UI", 14)); out.pack(pady=10)
        def go():
            try: inp = {k: float(e[k].get()) for k in LABELS}
            except ValueError: return messagebox.showerror("Invalid input", "Every field must be a number.", parent=w)
            s = stu
            if s is None:
                n, r = e["name"].get().strip(), e["roll"].get().strip().upper()
                if not (n and r): return messagebox.showwarning("Missing", "Name and roll number are required.", parent=w)
                s = Student.query.filter_by(roll_no=r).first() or Student(name=n, roll_no=r); db.session.add(s); db.session.flush()
            p, r = run_prediction(s, inp)
            out.configure(text=f"Predicted: {r['pct']}%   Grade: {r['grade']}\nPass probability: {r['prob']}%\nRisk: {r['risk']}   Category: {r['category']}\n"
                               + ("EARLY WARNING: student is at risk." if r["risk"] == "High" else ""))
        ctk.CTkButton(w, text="Predict", command=go, width=300).pack(pady=8)

    # 7. Reports window
    def reports_window(self, stu):
        w = ctk.CTkToplevel(self); w.title("Reports"); w.geometry("700x420")
        ps = (stu.predictions if stu else Prediction.query.order_by(Prediction.created.desc()).limit(50).all())
        t = table(w, ("ID", "Student", "Date", "Predicted %", "Grade"), [(p.id, p.student.name, p.created.strftime("%d %b %H:%M"), p.predicted_pct, p.grade) for p in ps], 12)
        t.pack(fill="both", expand=True, padx=10, pady=10)
        def export():
            sel = t.selection()
            if not sel: return messagebox.showinfo("Select a row", "Pick a prediction first.", parent=w)
            p = db.session.get(Prediction, int(t.item(sel[0])["values"][0])); inp, ins = insights_for(p)
            path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"report_{p.student.roll_no}_{p.id}.pdf", parent=w)
            if path: open(path, "wb").write(build_report(p.student, p, ins, inp)); messagebox.showinfo("Saved", path, parent=w)
        ctk.CTkButton(w, text="Export selected as PDF", command=export).pack(pady=8)

    # model training window + graphs
    def model_window(self):
        w = ctk.CTkToplevel(self); w.title("Model training"); w.geometry("1000x640")
        box = ctk.CTkFrame(w); box.pack(fill="both", expand=True)
        def draw(b):
            for c in box.winfo_children(): c.destroy()
            table(box, ("Model", "Accuracy %", "MAE", "MSE", "RMSE", "R2", "Selected"),
                  [(m["model"], m["accuracy"], m["mae"], m["mse"], m["rmse"], m["r2"], "YES" if m["model"] == b["name"] else "") for m in b["metrics"]], 5).pack(fill="x", padx=10, pady=8)
            tabs = ctk.CTkTabview(box); tabs.pack(fill="both", expand=True, padx=10)
            for n, f in [("Feature importance", an.fig_importance(b)), ("Comparison", an.fig_comparison(b))]: show_fig(tabs.add(n), f)
        def retrain(): draw(ml.train_all())
        ctk.CTkButton(w, text="Re-train models", command=retrain).pack(pady=6); draw(ml.load_bundle())

    def graphs(self):
        self.reset_body(); df, b = an.load_df(), ml.load_bundle(); tabs = ctk.CTkTabview(self.body); tabs.pack(fill="both", expand=True)
        for n, f in [("Attendance vs Score", an.fig_attendance(df)), ("Study Hours vs Score", an.fig_study(df)), ("Feature Importance", an.fig_importance(b)),
                     ("Model Comparison", an.fig_comparison(b)), ("Pass / Fail", an.fig_passfail(df))]: show_fig(tabs.add(n), f)


if __name__ == "__main__":
    DesktopApp().mainloop()
