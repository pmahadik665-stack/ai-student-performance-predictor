"""Analytics: interactive Plotly charts (web) and Matplotlib/Seaborn figures (web + desktop)."""
import io, base64
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
import model as ml

NEON, PURPLE = "#22d3ee", "#8b5cf6"


def load_df():
    import os
    if not os.path.exists(ml.CSV): ml.generate_dataset()
    df = pd.read_csv(ml.CSV)
    df["grade"] = df["final_pct"].apply(ml.grade_for)
    return df


# ---------------- Plotly (imported lazily so desktop app works without it) ----------------
def _html(fig, h=340):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=h, margin=dict(l=40, r=15, t=40, b=40), font=dict(family="Inter, sans-serif"))
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"displayModeBar": False})


def plotly_charts(df, bundle, preds=None):
    import plotly.express as px, plotly.graph_objects as go
    seq = [PURPLE, NEON, "#f472b6", "#34d399", "#fbbf24"]
    c = {}
    c["Attendance vs Marks"] = _html(px.scatter(df, x="attendance", y="final_pct", color="department",
                                                color_discrete_sequence=seq, opacity=.75, title="Attendance vs Marks"))
    sem = df.groupby("semester")["prev_cgpa"].mean().reset_index()
    f = px.line(sem, x="semester", y="prev_cgpa", markers=True, title="CGPA Trend by Semester")
    f.update_traces(line_color=NEON)
    if preds:
        f.add_trace(go.Scatter(x=list(range(1, len(preds) + 1)), y=[p / 10 for p in preds], name="You (predicted/10)",
                               mode="lines+markers", line=dict(color=PURPLE)))
    c["CGPA Trend"] = _html(f)
    top = df.nlargest(10, "final_pct").iloc[::-1]
    c["Student Ranking"] = _html(px.bar(top, x="final_pct", y="name", orientation="h", title="Top 10 Students",
                                        color="final_pct", color_continuous_scale=[PURPLE, NEON]))
    d = df.groupby("department")["final_pct"].mean().reset_index()
    c["Department Performance"] = _html(px.bar(d, x="department", y="final_pct", color="department",
                                               color_discrete_sequence=seq, title="Department Average %"))
    cols = ml.FEATURES + ["final_pct"]
    c["Performance Heatmap"] = _html(px.imshow(df[cols].corr().round(2), text_auto=True, aspect="auto",
                                               color_continuous_scale="Viridis", title="Feature Correlation"), 380)
    s = df.assign(h=df["study_hours"].round()).groupby("h")["final_pct"].mean().reset_index()
    c["Study Hours Analysis"] = _html(px.area(s, x="h", y="final_pct", title="Average Marks by Study Hours / day")
                                      .update_traces(line_color=NEON, fillcolor="rgba(34,211,238,.2)"))
    f = px.scatter(x=bundle["y_test"], y=bundle["y_pred"], title=f"Prediction Accuracy ({bundle['name']})",
                   labels={"x": "Actual %", "y": "Predicted %"}, opacity=.8)
    f.add_shape(type="line", x0=10, y0=10, x1=100, y1=100, line=dict(color=PURPLE, dash="dash"))
    c["Prediction Accuracy"] = _html(f)
    g = df["grade"].value_counts().reindex(["O", "A+", "A", "B+", "B", "C", "F"]).fillna(0).reset_index()
    g.columns = ["grade", "count"]
    c["Grade Distribution"] = _html(px.bar(g, x="grade", y="count", title="Grade Distribution", color="count",
                                           color_continuous_scale=[PURPLE, NEON]))
    return c


def trend_chart(preds):
    import plotly.graph_objects as go
    f = go.Figure(go.Scatter(x=list(range(1, len(preds) + 1)), y=preds, mode="lines+markers",
                             line=dict(color=NEON, width=3), fill="tozeroy", fillcolor="rgba(139,92,246,.18)"))
    f.update_layout(title="Predicted % over time", yaxis_range=[0, 100])
    return _html(f, 260)


# ---------------- Matplotlib / Seaborn (Figure objects, no pyplot -> safe for web and Tk) ----------------
def _style(fig, ax):
    fig.patch.set_facecolor("#0b1030"); ax.set_facecolor("#0b1030")
    for s in ax.spines.values(): s.set_color("#444a70")
    ax.tick_params(colors="#c8cde6"); ax.xaxis.label.set_color("#c8cde6")
    ax.yaxis.label.set_color("#c8cde6"); ax.title.set_color("white")


def fig_attendance(df):
    f = Figure(figsize=(5, 3.4)); a = f.subplots()
    sns.scatterplot(data=df, x="attendance", y="final_pct", hue="department", ax=a, s=18, palette="cool", legend=False)
    a.set_title("Attendance vs Score"); _style(f, a); f.tight_layout(); return f


def fig_study(df):
    f = Figure(figsize=(5, 3.4)); a = f.subplots()
    sns.regplot(data=df, x="study_hours", y="final_pct", ax=a, scatter_kws={"s": 12, "alpha": .5, "color": "#22d3ee"},
                line_kws={"color": "#8b5cf6"})
    a.set_title("Study Hours vs Score"); _style(f, a); f.tight_layout(); return f


def fig_importance(bundle):
    imp = pd.Series(bundle["importances"]).sort_values()
    f = Figure(figsize=(5, 3.4)); a = f.subplots()
    sns.barplot(x=imp.values, y=imp.index, ax=a, color="#8b5cf6")
    a.set_title(f"Feature Importance ({bundle['name']})"); _style(f, a); f.tight_layout(); return f


def fig_comparison(bundle):
    m = pd.DataFrame(bundle["metrics"])
    f = Figure(figsize=(5, 3.4)); a = f.subplots()
    sns.barplot(data=m, x="model", y="r2", ax=a, color="#22d3ee")
    a.set_title("Model Comparison (R2)"); a.tick_params(axis="x", rotation=15); a.set_ylim(0, 1)
    _style(f, a); f.tight_layout(); return f


def fig_passfail(df):
    p = (df["final_pct"] >= ml.PASS_MARK).sum(); n = len(df) - p
    f = Figure(figsize=(5, 3.4)); a = f.subplots()
    a.pie([p, n], labels=["Pass", "Fail"], colors=["#34d399", "#f87171"], autopct="%1.1f%%", textprops={"color": "white"})
    a.set_title("Pass / Fail"); f.patch.set_facecolor("#0b1030"); a.title.set_color("white"); f.tight_layout(); return f


def to_b64(fig):
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=110, facecolor=fig.get_facecolor())
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def mpl_images(df, bundle):
    return {"Attendance vs Score": to_b64(fig_attendance(df)), "Study Hours vs Score": to_b64(fig_study(df)),
            "Feature Importance": to_b64(fig_importance(bundle)), "Model Comparison": to_b64(fig_comparison(bundle)),
            "Pass / Fail": to_b64(fig_passfail(df))}
