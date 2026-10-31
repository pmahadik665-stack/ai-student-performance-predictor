"""Machine-learning module: dataset generation, training, comparison, best-model selection, Joblib persistence."""
import os, math
import numpy as np, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE = os.path.dirname(os.path.abspath(__file__))
CSV, PKL = os.path.join(BASE, "student_data.csv"), os.path.join(BASE, "model.pkl")
FEATURES = ["attendance", "study_hours", "internal", "assignment", "prev_cgpa", "project", "practical"]
DEPTS = ["CSE", "ECE", "MECH", "CIVIL", "IT"]
PASS_MARK = 40.0
_cache = {}


def generate_dataset(n=600, seed=42, path=CSV):
    """Synthetic but realistic dataset. final_pct = weighted blend of inputs + noise."""
    r = np.random.default_rng(seed)
    att = r.normal(78, 13, n).clip(35, 100)
    sh = r.normal(3.5, 1.5, n).clip(0.5, 10)
    cg = r.normal(7.0, 1.1, n).clip(4, 10)
    internal = (0.5 * cg * 10 + 0.3 * att + 5 + r.normal(0, 8, n)).clip(20, 100)
    assign = (45 + sh * 6 + r.normal(0, 10, n)).clip(20, 100)
    proj = (40 + cg * 4 + r.normal(0, 8, n)).clip(30, 100)
    prac = (38 + cg * 4.5 + r.normal(0, 8, n)).clip(30, 100)
    final = (0.15 * att + 1.0 * sh + 0.20 * internal + 0.10 * assign + 2.5 * cg + 0.10 * proj
             + 0.10 * prac - 0.25 * np.maximum(0, 75 - att) + 0.03 * (internal - 60) * (sh - 3)
             + r.normal(0, 3, n)).clip(10, 100)
    first = ["Aarav", "Diya", "Rohan", "Sneha", "Kabir", "Meera", "Arjun", "Ananya", "Vihaan", "Isha",
             "Rahul", "Priya", "Karan", "Neha", "Aditya", "Pooja", "Siddharth", "Riya", "Nikhil", "Tanvi"]
    last = ["Naik", "Desai", "Fernandes", "Kamat", "Shetty", "Gaonkar", "Borkar", "Prabhu", "Dessai", "Rane"]
    dept = r.choice(DEPTS, n)
    df = pd.DataFrame({
        "name": [f"{r.choice(first)} {r.choice(last)}" for _ in range(n)],
        "roll_no": [f"{d[:2]}{23000 + i}" for i, d in enumerate(dept)],
        "department": dept, "semester": r.integers(1, 9, n),
        "attendance": att.round(1), "study_hours": sh.round(1), "internal": internal.round(1),
        "assignment": assign.round(1), "prev_cgpa": cg.round(2), "project": proj.round(1),
        "practical": prac.round(1), "final_pct": final.round(1)})
    df.to_csv(path, index=False)
    return df


def grade_for(p):
    for cut, g in [(90, "O"), (80, "A+"), (70, "A"), (60, "B+"), (50, "B"), (40, "C")]:
        if p >= cut: return g
    return "F"


def train_all(path=CSV, save=True):
    """Train 4 models, compare, auto-select best by R2, save with Joblib. Returns the bundle."""
    df = pd.read_csv(path) if os.path.exists(path) else generate_dataset()
    X, y = df[FEATURES], df["final_pct"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, random_state=42),
    }
    results, fitted = [], {}
    for name, m in models.items():
        m.fit(Xtr, ytr)
        pred = m.predict(Xte)
        mae, mse, r2 = mean_absolute_error(yte, pred), mean_squared_error(yte, pred), r2_score(yte, pred)
        results.append({"model": name, "accuracy": round(float(max(0, 100 * (1 - mae / yte.mean()))), 2),
                        "mae": round(float(mae), 3), "mse": round(float(mse), 3), "rmse": round(math.sqrt(mse), 3),
                        "r2": round(float(r2), 4)})
        fitted[name] = m
    best = max(results, key=lambda r: r["r2"])
    bm = fitted[best["model"]]
    imp = (bm.feature_importances_ if hasattr(bm, "feature_importances_")
           else np.abs(bm.coef_) / np.abs(bm.coef_).sum())
    bundle = {"model": bm, "name": best["model"], "features": FEATURES, "metrics": results,
              "best": best, "rmse": best["rmse"], "importances": dict(zip(FEATURES, map(float, imp))),
              "y_test": yte.tolist(), "y_pred": bm.predict(Xte).tolist(), "rows": len(df)}
    if save: joblib.dump(bundle, PKL)
    _cache.clear()
    return bundle


def load_bundle():
    if "b" not in _cache:
        try:
            b = joblib.load(PKL)
            b["model"].predict(pd.DataFrame([[0] * len(b["features"])], columns=b["features"]))
        except Exception:  # missing, corrupt or saved by another scikit-learn version -> retrain
            b = train_all()
        _cache["b"] = b
    return _cache["b"]


def predict(inp):
    b = load_bundle()
    X = pd.DataFrame([[float(inp[f]) for f in FEATURES]], columns=FEATURES)
    pct = float(np.clip(b["model"].predict(X)[0], 0, 100))
    prob = 0.5 * (1 + math.erf((pct - PASS_MARK) / (max(b["rmse"], 1e-6) * math.sqrt(2))))
    att = float(inp["attendance"])
    risk = "High" if (pct < PASS_MARK + 10 or att < 65) else "Medium" if (pct < 60 or att < 75) else "Low"
    cat = ("Excellent" if pct >= 85 else "Good" if pct >= 70 else "Average" if pct >= 55 else "Needs Improvement")
    return {"pct": round(pct, 1), "grade": grade_for(pct), "prob": round(prob * 100, 1), "risk": risk,
            "category": cat, "status": "Pass" if pct >= PASS_MARK else "Fail", "model": b["name"]}


def percentile_rank(pct):
    """Estimated rank among the training population (Student Ranking Prediction)."""
    df = pd.read_csv(CSV)
    return int((df["final_pct"] > pct).sum()) + 1, len(df)


if __name__ == "__main__":
    b = train_all()
    for m in b["metrics"]: print(m)
    print("Best:", b["name"])
