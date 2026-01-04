import pandas as pd
from pathlib import Path

DATA_PATH = Path("src/data/documents")


def load_trend_data():
    file_path = DATA_PATH / "automation_trend_metrics.csv"
    if not file_path.exists():
        raise FileNotFoundError("automation_trend_metrics.csv not found")

    return pd.read_csv(file_path)


def automation_trend(last_n_sprints=4):
    """
    Computes weighted automation coverage trend over last N sprints.
    """
    df = load_trend_data()

    # Normalize sprint number (e.g., "Sprint 4" -> 4)
    df["Sprint_Number"] = (
        df["Sprint"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(int)
    )

    # Aggregate per sprint (WEIGHTED)
    sprint_summary = (
        df.groupby("Sprint_Number")
          .agg({
              "Automated_Test_Cases": "sum",
              "Total_Test_Cases": "sum"
          })
          .reset_index()
    )

    sprint_summary["Automation_Coverage_%"] = (
        sprint_summary["Automated_Test_Cases"]
        / sprint_summary["Total_Test_Cases"]
    ) * 100

    sprint_summary = sprint_summary.sort_values("Sprint_Number")
    trend_df = sprint_summary.tail(last_n_sprints)

    trend_summary = {
        "start_sprint": int(trend_df.iloc[0]["Sprint_Number"]),
        "end_sprint": int(trend_df.iloc[-1]["Sprint_Number"]),
        "start_coverage": round(float(trend_df.iloc[0]["Automation_Coverage_%"]), 2),
        "end_coverage": round(float(trend_df.iloc[-1]["Automation_Coverage_%"]), 2),
        "delta": round(
            float(trend_df.iloc[-1]["Automation_Coverage_%"])
            - float(trend_df.iloc[0]["Automation_Coverage_%"]),
            2,
        ),
        "direction": (
            "improving"
            if trend_df.iloc[-1]["Automation_Coverage_%"]
               > trend_df.iloc[0]["Automation_Coverage_%"]
            else "declining"
        )
    }

    return trend_df, trend_summary
