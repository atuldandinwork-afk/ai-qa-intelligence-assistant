# src/ml/features.py

import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------
# Severity mapping (Option B)
# -------------------------------
SEVERITY_MAP = {
    "Blocker": 5,
    "Critical": 4,
    "Major": 3,
    "High": 3,
    "Minor": 2,
    "Medium": 2,
    "Trivial": 1,
    "Low": 1,
}


# -------------------------------
# Data paths
# -------------------------------
DATA_DIR = Path("src/data/documents")

DEFECTS_FILE = DATA_DIR / "defects.csv"
AUTOMATION_FILE = DATA_DIR / "automation_metrics.csv"
EXECUTION_FILE = DATA_DIR / "test_execution_results.csv"

df = pd.read_csv(DEFECTS_FILE)
print("Columns found:", df.columns.tolist())
df["severity_score"] = (
    df["Severity"]
    .astype(str)
    .str.strip()
    .map(SEVERITY_MAP)
)

print("severity_score created:", df["severity_score"].head())

if df["severity_score"].isna().any():
    unknown = df.loc[df["severity_score"].isna(), "Severity"].unique()
    raise ValueError(f"Unknown severity values found: {unknown}")

df["is_prod"] = df["Environment"].str.lower().eq("production")

features = (
    df.groupby("Module")
      .agg(
          total_defects=("Defect_ID", "count"),
          prod_defects=("is_prod", "sum"),
          avg_severity=("severity_score", "mean"),
      )
      .reset_index()
)


def build_defect_features() -> pd.DataFrame:
    df = pd.read_csv(DEFECTS_FILE)

    # Map severity to numeric score
    df["severity_score"] = (
        df["Severity"]
        .astype(str)
        .str.strip()
        .map(SEVERITY_MAP)
    )

    if df["severity_score"].isna().any():
        unknown = df.loc[df["severity_score"].isna(), "Severity"].unique()
        raise ValueError(f"Unknown severity values found: {unknown}")

    # Identify production defects
    df["is_prod"] = df["Environment"].astype(str).str.lower().eq("production")

    # Aggregate by module
    features = (
        df.groupby("Module")
          .agg(
              total_defects=("Defect_ID", "count"),
              prod_defects=("is_prod", "sum"),
              avg_severity=("severity_score", "mean"),
          )
          .reset_index()
    )

    return features

def build_execution_features() -> pd.DataFrame:
        df = pd.read_csv(EXECUTION_FILE)

        # -----------------------------
        # Normalize sprint to numeric
        # -----------------------------
        df["Sprint_Number"] = df["Sprint"].str.extract(r"(\d+)").astype(int)

        # -----------------------------
        # Pass / Fail flag
        # -----------------------------
        df["is_pass"] = df["Status"].str.lower().eq("pass")

        # -----------------------------
        # Total executions per module + sprint
        # -----------------------------
        exec_counts = (
            df.groupby(["Module", "Sprint_Number"])
            .size()
            .reset_index(name="total_executions")
        )

        # -----------------------------
        # Pass rate per module + sprint
        # -----------------------------
        pass_rate = (
            df.groupby(["Module", "Sprint_Number"])["is_pass"]
            .mean()
            .reset_index(name="pass_rate")
        )

        # -----------------------------
        # Flaky tests detection
        # -----------------------------
        flaky = (
            df.groupby(["Module", "Sprint_Number", "Test_Case_ID"])["Status"]
            .nunique()
            .reset_index(name="status_variants")
        )

        flaky_tests = (
            flaky[flaky["status_variants"] > 1]
            .groupby(["Module", "Sprint_Number"])
            .size()
            .reset_index(name="flaky_tests")
        )

        # -----------------------------
        # Merge all execution features
        # -----------------------------
        features = (
            exec_counts
            .merge(pass_rate, on=["Module", "Sprint_Number"], how="left")
            .merge(flaky_tests, on=["Module", "Sprint_Number"], how="left")
        )

        features["flaky_tests"] = features["flaky_tests"].fillna(0).astype(int)

        return features


def build_automation_features() -> pd.DataFrame:
    df = pd.read_csv(AUTOMATION_FILE)

    print("Automation columns:", df.columns.tolist())

    df = df[
        [
            "Module",
            "Automation_Coverage_%",
            "Pending_Automation",
            "Defects_Found_By_Automation",
            "Defects_Found_In_Production",
        ]
    ]

    df = df.rename(columns={
        "Automation_Coverage_%": "automation_coverage",
        "Pending_Automation": "pending_automation",
        "Defects_Found_By_Automation": "auto_detected_defects",
        "Defects_Found_In_Production": "prod_detected_defects",
    })

    return df
   

if __name__ == "__main__":
    df_auto = build_automation_features()
    print(df_auto)