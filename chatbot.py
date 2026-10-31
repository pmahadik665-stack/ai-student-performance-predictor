"""AI Academic Assistant: rule-based intent matching over the student's own data."""
import recommendation as rec


def reply(msg, stu=None, pred=None):
    m = msg.lower()
    has = stu is not None
    inp = stu.inputs() if has else None
    if any(w in m for w in ("hello", "hi ", "hey")) or m.strip() in ("hi", "hey"):
        return "Hello! I can help with your attendance, study plan, weak subjects, career, scholarship and placement readiness."
    if not has:
        return "Sign in as a student to get personalised answers."
    if "attend" in m: return rec.attendance_advice(inp["attendance"])
    if "weak" in m or "subject" in m:
        w = rec.weak_subjects(inp)
        return "Weak areas: " + ", ".join(f"{k} ({v}%)" for k, v in w) if w else "No weak areas found. Great work!"
    if "plan" in m or "study" in m: return " ".join(rec.study_plan(inp, pred.predicted_pct if pred else 60)[:3])
    if "career" in m or "job" in m: return "Suggested careers: " + ", ".join(rec.career(inp, pred.predicted_pct if pred else 60))
    if "scholar" in m: return rec.scholarship(inp, pred.predicted_pct if pred else 60)
    if "place" in m: p = rec.placement(inp, pred.predicted_pct if pred else 60); return f"Placement readiness: {p['level']} ({p['score']}/100)."
    if "risk" in m or "grade" in m or "predict" in m or "score" in m:
        return (f"Your latest prediction: {pred.predicted_pct}% (grade {pred.grade}), risk {pred.risk}." if pred
                else "You have no predictions yet. Open the AI Prediction page.")
    if "forecast" in m or "next sem" in m:
        f = rec.forecast(inp, pred.predicted_pct if pred else 60); return f"Next-semester forecast: {f['next']}% ({f['trend']})."
    return "Try asking about: attendance, weak subjects, study plan, career, scholarship, placement, risk or forecast."
