"""Rule-based AI recommendation engine: weak subjects, study plan, career, forecast, scholarship, placement."""
import math


def components(i):
    return {"Attendance": i["attendance"], "Internal Exams": i["internal"], "Assignments": i["assignment"],
            "Project Work": i["project"], "Practical / Lab": i["practical"],
            "Study Habits": min(100, i["study_hours"] * 12.5), "Academic Base (CGPA)": i["prev_cgpa"] * 10}


def weak_subjects(i, limit=60):
    return sorted([(k, round(v)) for k, v in components(i).items() if v < limit], key=lambda x: x[1])


def attendance_advice(att):
    if att >= 85: return "Excellent attendance. Keep it above 85% to stay eligible for attendance rewards."
    if att >= 75: return "Attendance is safe but close to the limit. Avoid skipping more than 2 classes a month."
    need = math.ceil(4 * (75 - att))
    return (f"Attendance is {att:.0f}%, below the 75% requirement. Attend the next {need} classes "
            "in a row (no absences) to cross 75%.")


def study_plan(i, pct):
    weak = [w[0] for w in weak_subjects(i)]
    hrs = 2 if pct >= 80 else 3 if pct >= 65 else 4 if pct >= 50 else 5
    plan = [f"Target {max(hrs, math.ceil(i['study_hours']))} focused study hours per day, in 50-minute blocks.",
            "Mon/Wed/Fri: concept revision and previous-year questions.",
            "Tue/Thu: solve numericals, lab record work and assignments.",
            "Sat: one full mock internal test, then review mistakes. Sun: rest + 1 hour planning."]
    if weak: plan.insert(1, "Priority focus areas: " + ", ".join(weak[:3]) + ".")
    if i["assignment"] < 60: plan.append("Submit every assignment 2 days before the deadline.")
    return plan


def career(i, pct):
    strong = max([("project", i["project"]), ("practical", i["practical"]), ("internal", i["internal"])],
                 key=lambda x: x[1])[0]
    base = {"project": ["Software Developer", "Product Engineer", "Full-Stack Developer"],
            "practical": ["Embedded / Hardware Engineer", "QA & Test Engineer", "Network Engineer"],
            "internal": ["Data Analyst", "Researcher / Higher Studies (M.Tech / MBA)", "Business Analyst"]}[strong]
    if pct >= 80 and i["prev_cgpa"] >= 8: base = base + ["Data Scientist / ML Engineer"]
    return base


def forecast(i, pct):
    delta = 0.25 * (i["attendance"] - 75) / 5 + 1.2 * (i["study_hours"] - 3) + 0.1 * (i["assignment"] - 60) / 5
    nxt = max(0, min(100, pct + max(-8, min(8, delta))))
    return {"next": round(nxt, 1), "low": round(max(0, nxt - 4), 1), "high": round(min(100, nxt + 4), 1),
            "trend": "Improving" if nxt > pct + 0.5 else "Declining" if nxt < pct - 0.5 else "Stable"}


def scholarship(i, pct):
    if pct >= 85 and i["prev_cgpa"] >= 8.5 and i["attendance"] >= 85:
        return "Eligible: Merit Scholarship (full tuition waiver)"
    if pct >= 75 and i["prev_cgpa"] >= 7.5 and i["attendance"] >= 75:
        return "Eligible: Merit-cum-Means Scholarship (partial waiver)"
    if pct >= 60 and i["attendance"] >= 75:
        return "Not eligible yet. Raise performance above 75% and CGPA above 7.5 to qualify."
    return "Not eligible. Minimum 75% attendance and 60% predicted score are required."


def placement(i, pct):
    s = 0.4 * pct + 0.2 * i["project"] + 0.15 * i["practical"] + 0.1 * i["attendance"] + 0.15 * i["prev_cgpa"] * 10
    lvl = "Ready" if s >= 75 else "Almost Ready" if s >= 62 else "Needs Preparation"
    return {"score": round(s, 1), "level": lvl}


def all_insights(i, res, rank=None):
    return {"weak": weak_subjects(i), "attendance": attendance_advice(i["attendance"]),
            "plan": study_plan(i, res["pct"]), "career": career(i, res["pct"]),
            "forecast": forecast(i, res["pct"]), "scholarship": scholarship(i, res["pct"]),
            "placement": placement(i, res["pct"]), "rank": rank}
