# AI-Powered Student Performance Prediction and Academic Analytics System

Flask web app (dark glassmorphism UI generated from Python strings) plus a CustomTkinter desktop client, sharing one SQLite database, one ML module and one PDF engine.

## Run
```bash
python -m venv venv && venv\Scripts\activate        # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
python app.py                  # web app -> http://127.0.0.1:5000
python desktop_app.py          # optional CustomTkinter client
python model.py                # optional: retrain from the command line
```
First run creates `student.db`, `student_data.csv` (600 synthetic records), `model.pkl`, and seeds 30 students.

| Role | Login | Password |
|---|---|---|
| Admin | admin@college.edu (or ID `ADMIN`) | admin123 |
| Student | student@college.edu (or ID `S1001`) | student123 |

## Files
| File | Purpose |
|---|---|
| app.py | Routes, auth, prediction workflow, admin, seeding |
| ui.py | Every page (HTML/CSS/JS) as Python strings used with `render_template_string` |
| model.py | Dataset generator, 4 models, comparison, best-model selection, Joblib save, prediction |
| database.py | SQLAlchemy tables: users, students, predictions, reports, notifications, achievements |
| analytics.py | 8 Plotly charts and 5 Matplotlib/Seaborn figures |
| report_generator.py | ReportLab PDF with college header, QR code, recommendations, timestamp |
| recommendation.py | Risk, weak subjects, study plan, career, forecast, scholarship, placement, attendance advice |
| chatbot.py | Rule-based academic assistant |
| desktop_app.py | CustomTkinter GUI: splash, login, register, dashboards, prediction, reports, model training |
| DOCUMENTATION.md | Full project report with UML, Gantt, SRS, testing |

## Viva cheat sheet
- **Which model is used?** All four are trained on an 80/20 split; the one with the highest R2 is saved to `model.pkl`.
- **How is "success probability" computed?** Normal CDF of (predicted % - 40) / model RMSE.
- **Risk rule:** High if predicted < 50% or attendance < 65%; Medium if predicted < 60% or attendance < 75%; else Low.
- **Is the dataset real?** No. It is synthetic (see `generate_dataset`). To use real data, replace `student_data.csv` with the same columns and click *Re-train models*.
