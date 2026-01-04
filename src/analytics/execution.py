import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = Path("src/data/documents")
SPRINT_DAYS = 14


# -----------------------------
# Load execution data
# -----------------------------
def load_execution_data():
    file_path = DATA_PATH / "test_execution_results.csv"
    if not file_path.exists():
        raise FileNotFoundError("test_execution_results.csv not found")

    df = pd.read_csv(file_path)

    if "Execution_Date" not in df.columns:
        raise ValueError("Execution_Date column missing in test_execution_results.csv")

    if "Status" not in df.columns:
        raise ValueError("Status column missing in test_execution_results.csv")

    df["Execution_Date"] = pd.to_datetime(df["Execution_Date"])
    return df


# -----------------------------
# Assign sprints from dates
# -----------------------------
def assign_sprints(df: pd.DataFrame) -> pd.DataFrame:
    start_date = df["Execution_Date"].min()

    df["Sprint_Number"] = (
        (df["Execution_Date"] - start_date).dt.days // SPRINT_DAYS
    ) + 1

    return df


# -----------------------------
# Execution stability trend
# -----------------------------
def execution_stability_trend(last_n_sprints: int = 4):
    """
    Computes pass-rate trend over the last N sprints.
    """
    df = load_execution_data()
    df = assign_sprints(df)

    df["Is_Pass"] = df["Status"].str.lower() == "pass"

    trend_df = (
        df.groupby("Sprint_Number")["Is_Pass"]
        .mean()
        .reset_index(name="Pass_Rate")
        .sort_values("Sprint_Number")
    )

    max_sprint = trend_df["Sprint_Number"].max()
    trend_df = trend_df[
        trend_df["Sprint_Number"] >= max_sprint - last_n_sprints + 1
    ]

    # Handle edge case: single sprint
    start_rate = round(trend_df.iloc[0]["Pass_Rate"] * 100, 2)
    end_rate = round(trend_df.iloc[-1]["Pass_Rate"] * 100, 2)

    if end_rate > start_rate:
        direction = "improving"
    elif end_rate < start_rate:
        direction = "degrading"
    else:
        direction = "stable"

    summary = {
        "start_sprint": int(trend_df.iloc[0]["Sprint_Number"]),
        "end_sprint": int(trend_df.iloc[-1]["Sprint_Number"]),
        "start_pass_rate_percent": start_rate,
        "end_pass_rate_percent": end_rate,
        "direction": direction,
    }

    return trend_df, summary


# -----------------------------
# Flaky test detection
# -----------------------------
def flaky_tests(min_pass_rate: float = 0.3, max_pass_rate: float = 0.8):
    """
    Identifies flaky tests based on intermittent pass/fail behavior.
    """
    df = load_execution_data()

    required_cols = {"Test_Case_ID", "Module", "Status"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns for flakiness detection: {missing}")

    df["Is_Pass"] = df["Status"].str.lower() == "pass"

    stats = (
        df.groupby(["Test_Case_ID", "Module"])["Is_Pass"]
        .mean()
        .reset_index(name="Pass_Rate")
    )

    flaky_df = stats[
        (stats["Pass_Rate"] >= min_pass_rate) &
        (stats["Pass_Rate"] <= max_pass_rate)
    ].sort_values("Pass_Rate")

    return flaky_df


# -----------------------------
# Visualization helpers
# -----------------------------
def plot_execution_stability(trend_df):
    fig, ax = plt.subplots()

    ax.plot(
        trend_df["Sprint_Number"],
        trend_df["Pass_Rate"] * 100,
        marker="o",
        linewidth=2
    )

    ax.set_title("Execution Pass Rate Trend")
    ax.set_xlabel("Sprint")
    ax.set_ylabel("Pass Rate (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)

    return fig
