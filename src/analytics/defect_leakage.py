import pandas as pd
from datetime import timedelta
from pathlib import Path

DATA_PATH = Path("src/data/documents")
SPRINT_DAYS = 14


def load_defect_data():
    file_path = DATA_PATH / "defects.csv"
    if not file_path.exists():
        raise FileNotFoundError("defects.csv not found")

    df = pd.read_csv(file_path)
    df["Created_Date"] = pd.to_datetime(df["Created_Date"])
    return df


def assign_sprints(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign sprint numbers based on Created_Date.
    """
    start_date = df["Created_Date"].min()
    df["Sprint_Number"] = (
        (df["Created_Date"] - start_date).dt.days // SPRINT_DAYS
    ) + 1
    return df


def defect_leakage_trend(last_n_sprints: int = 4):
    """
    Computes production defect trend over last N sprints.
    """
    df = load_defect_data()
    df = assign_sprints(df)

    # Production vs pre-production
    production_sources = ["Production", "Monitoring"]
    df["Is_Production"] = df["Detected_By"].isin(production_sources)

    # Aggregate by sprint
    trend = (
        df.groupby("Sprint_Number")["Is_Production"]
        .sum()
        .reset_index(name="Production_Defects")
    )

    # Filter last N sprints
    max_sprint = trend["Sprint_Number"].max()
    trend = trend[trend["Sprint_Number"] >= max_sprint - last_n_sprints + 1]

    # Direction analysis
    start = int(trend.iloc[0]["Production_Defects"])
    end = int(trend.iloc[-1]["Production_Defects"])

    direction = (
        "improving" if end < start else
        "worsening" if end > start else
        "stable"
    )

    summary = {
        "start_sprint": int(trend.iloc[0]["Sprint_Number"]),
        "end_sprint": int(trend.iloc[-1]["Sprint_Number"]),
        "start_production_defects": start,
        "end_production_defects": end,
        "direction": direction,
    }

    return trend, summary
