"""Database layer: SQLite via Flask-SQLAlchemy. Tables: users, students, predictions, reports, notifications, achievements."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_code = db.Column(db.String(20), unique=True)          # "Student ID" login
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default="student")           # student | admin
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship("Student", backref="user", uselist=False)

    def set_password(self, p): self.password_hash = generate_password_hash(p)
    def check_password(self, p): return check_password_hash(self.password_hash, p)
    @property
    def is_admin(self): return self.role == "admin"


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(80), nullable=False)
    roll_no = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120))
    department = db.Column(db.String(40), default="CSE")
    semester = db.Column(db.Integer, default=1)
    attendance = db.Column(db.Float, default=75)
    study_hours = db.Column(db.Float, default=3)
    internal = db.Column(db.Float, default=60)
    assignment = db.Column(db.Float, default=60)
    prev_cgpa = db.Column(db.Float, default=7)
    project = db.Column(db.Float, default=60)
    practical = db.Column(db.Float, default=60)
    predictions = db.relationship("Prediction", backref="student", cascade="all, delete-orphan",
                                  order_by="Prediction.created.desc()")
    achievements = db.relationship("Achievement", backref="student", cascade="all, delete-orphan")
    reports = db.relationship("Report", backref="student", cascade="all, delete-orphan")

    @property
    def latest(self): return self.predictions[0] if self.predictions else None
    def inputs(self):
        return {k: getattr(self, k) for k in
                ("attendance", "study_hours", "internal", "assignment", "prev_cgpa", "project", "practical")}


class Prediction(db.Model):
    __tablename__ = "predictions"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    predicted_pct = db.Column(db.Float)
    grade = db.Column(db.String(4))
    success_prob = db.Column(db.Float)
    risk = db.Column(db.String(10))
    category = db.Column(db.String(30))
    status = db.Column(db.String(10))                              # Pass | Fail
    model_name = db.Column(db.String(40))
    inputs = db.Column(db.Text)                                    # JSON snapshot
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    prediction_id = db.Column(db.Integer, db.ForeignKey("predictions.id"))
    filename = db.Column(db.String(120))
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(80))
    message = db.Column(db.String(300))
    kind = db.Column(db.String(20))                                # prediction | attendance | suggestion
    is_read = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Achievement(db.Model):
    __tablename__ = "achievements"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    badge = db.Column(db.String(40))
    created = db.Column(db.DateTime, default=datetime.utcnow)
