import pandas as pd
from pathlib import Path
import joblib

from src.ml.dataset_builder import build_ml_dataset

# -----------------------------
# Configuration
# -----------------------------
OUTPUT_DIR = Path("src/data/predictions")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "module_risk_predictions.csv"

MODEL_PATH = Path("src/ml/models/risk_model.pkl")

FEATURE_COLUMNS = [
    "pass_rate",
    "flaky_tests",
    "automation_coverage",
    "pending_automation",
    "auto_detected_defects",
    "prod_detected_defects",
]

# -----------------------------
# Load dataset
# -----------------------------
df = build_ml_dataset()
if df is None or df.empty:
    raise RuntimeError("ML dataset is empty. Cannot run prediction.")

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load(MODEL_PATH)

# -----------------------------
# Prepare features
# -----------------------------
X = df[FEATURE_COLUMNS]

# -----------------------------
# Predict risk probability
# -----------------------------
df["risk_probability"] = model.predict_proba(X)[:, 1]

# -----------------------------
# Generate explanations (rule-based)
# -----------------------------
def explain_risk(row):
    reasons = []

    if row["pass_rate"] < 0.7:
        reasons.append("low pass rate")
    if row["pending_automation"] > 20:
        reasons.append("high pending automation backlog")
    if row["prod_detected_defects"] > 0:
        reasons.append("production defects detected")

    if not reasons:
        return "Risk within acceptable limits"

    return "Risk driven by " + ", ".join(reasons)

df["risk_explanation"] = df.apply(explain_risk, axis=1)

# -----------------------------
# Build final risk DataFrame
# -----------------------------
df_risk = df[
    [
        "Module",
        "Sprint_Number",
        "risk_probability",
        "risk_explanation",
    ]
].copy()

# -----------------------------
# Persist predictions (Step 6A.4.3)
# -----------------------------
df_risk.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Risk predictions saved to {OUTPUT_FILE}")


