"""Professional PDF report (ReportLab): college header, student details, prediction, grade analysis,
recommendations, QR code, date & time."""
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

COLLEGE = "Goa College of Engineering & Technology"
NAVY, PURPLE = colors.HexColor("#0b1030"), colors.HexColor("#6d28d9")


def _qr(text, size=70):
    w = qr.QrCodeWidget(text); b = w.getBounds()
    d = Drawing(size, size, transform=[size / (b[2] - b[0]), 0, 0, size / (b[3] - b[1]), 0, 0]); d.add(w); return d


def _tbl(rows, widths, head=True):
    t = Table(rows, colWidths=widths)
    st = [("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#c9cde0")), ("FONTSIZE", (0, 0), (-1, -1), 9),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ROWBACKGROUNDS", (0, 1 if head else 0), (-1, -1),
                                                    [colors.white, colors.HexColor("#f3f4fb")])]
    if head: st += [("BACKGROUND", (0, 0), (-1, 0), PURPLE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
    t.setStyle(TableStyle(st)); return t


def build_report(stu, pred, ins, inputs, verify_url="http://localhost:5000"):
    """stu: Student, pred: Prediction, ins: dict from recommendation.all_insights, inputs: dict. Returns bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=12 * mm, bottomMargin=14 * mm,
                            title=f"Academic Report - {stu.name}")
    S = getSampleStyleSheet()
    h2 = ParagraphStyle("h2", parent=S["Heading2"], textColor=PURPLE, spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("b", parent=S["BodyText"], fontSize=9.5, leading=13)
    head = Table([[Paragraph(f"<font color='white' size=16><b>{COLLEGE}</b></font><br/><font color='#8be9fd' size=9>"
                             "AI-Powered Student Performance Prediction &amp; Academic Analytics System</font>", body),
                   Paragraph("<font color='white' size=9>Academic Prediction Report<br/>" +
                             datetime.now().strftime("%d %b %Y, %I:%M %p") + "</font>", body)]], colWidths=[125 * mm, 50 * mm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                              ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    el = [head, Spacer(1, 8), Paragraph("Student Details", h2),
          _tbl([["Name", stu.name, "Roll No", stu.roll_no], ["Department", stu.department, "Semester", str(stu.semester)],
                ["Email", stu.email or "-", "Model Used", pred.model_name]], [28 * mm, 60 * mm, 28 * mm, 59 * mm], head=False),
          Paragraph("Prediction Results", h2),
          _tbl([["Predicted %", "Grade", "Success Probability", "Risk Level", "Category"],
                [f"{pred.predicted_pct}%", pred.grade, f"{pred.success_prob}%", pred.risk, pred.category]], [35 * mm] * 5),
          Paragraph("Input Parameters &amp; Grade Analysis", h2)]
    names = {"attendance": "Attendance %", "study_hours": "Study hours/day", "internal": "Internal score",
             "assignment": "Assignment score", "prev_cgpa": "Previous CGPA", "project": "Project marks", "practical": "Practical marks"}
    el.append(_tbl([["Parameter", "Value"]] + [[names[k], str(inputs[k])] for k in names], [90 * mm, 85 * mm]))
    weak = ", ".join(f"{k} ({v}%)" for k, v in ins["weak"]) or "None. All areas are above 60%."
    f = ins["forecast"]
    el += [Spacer(1, 4), Paragraph(f"<b>Weak areas:</b> {weak}", body),
           Paragraph(f"<b>Next-semester forecast:</b> {f['next']}% ({f['low']}-{f['high']}), trend {f['trend']}", body),
           Paragraph(f"<b>Placement readiness:</b> {ins['placement']['level']} ({ins['placement']['score']}/100)", body),
           Paragraph(f"<b>Scholarship:</b> {ins['scholarship']}", body)]
    if ins.get("rank"): el.append(Paragraph(f"<b>Estimated rank:</b> {ins['rank'][0]} of {ins['rank'][1]} students", body))
    el.append(Paragraph("Recommendations", h2))
    for line in [ins["attendance"]] + ins["plan"] + ["Career suggestions: " + ", ".join(ins["career"])]:
        el.append(Paragraph("&bull; " + line, body))
    el += [Spacer(1, 12), Table([[_qr(f"{verify_url}|{stu.roll_no}|{pred.id}|{pred.predicted_pct}"),
                                  Paragraph("Scan to verify this report.<br/>Generated automatically; predictions are "
                                            "estimates based on a machine-learning model and are not official results.", body)]],
                                colWidths=[30 * mm, 145 * mm])]
    doc.build(el); return buf.getvalue()
