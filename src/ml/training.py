from pathlib import Path
import joblib
import pandas as pd

from src.ml.dataset_builder import build_ml_dataset
from sklearn.model_selection import train_test_split


df = build_ml_dataset()

# Binary target
df["unstable"] = (df["pass_rate"] < 0.7).astype(int)


FEATURES = [
    "pass_rate",
    "flaky_tests",
    "automation_coverage",
    "pending_automation",
    "auto_detected_defects",
    "prod_detected_defects",
]

X = df[FEATURES]
y = df["unstable"]

print("X shape:", X.shape)
print("y shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42,
)

model.fit(X_train, y_train)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report,
)

y_pred = model.predict(X_test)

coef_df = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": model.coef_[0],
}).sort_values(by="coefficient", ascending=False)

# Predict probability of instability
df["risk_probability"] = model.predict_proba(X)[:, 1]

#print(df[["Module", "Sprint_Number", "risk_probability"]].head())


def explain_risk(row):
    reasons = []

    if row["pass_rate"] < 0.7:
        reasons.append("low pass rate")

    if row["prod_detected_defects"] > 0:
        reasons.append("production defects detected")

    if row["pending_automation"] > 50:
        reasons.append("high pending automation backlog")

    if row["automation_coverage"] < 60:
        reasons.append("low automation coverage")

    if not reasons:
        return "Overall execution and automation health is stable."

    return "Risk driven by " + ", ".join(reasons) + "."

df["risk_explanation"] = df.apply(explain_risk, axis=1)

#print(df[["Module", "Sprint_Number", "risk_probability", "risk_explanation"]].head())



OUTPUT_FILE = "src/data/predictions/module_risk_predictions.csv"
df.to_csv(OUTPUT_FILE, index=False)

MODEL_DIR = Path("src/ml/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, "src/ml/models/risk_model.pkl")
print("✅ Model saved to src/ml/models/risk_model.pkl")

print(f"Risk predictions saved to {OUTPUT_FILE}")




