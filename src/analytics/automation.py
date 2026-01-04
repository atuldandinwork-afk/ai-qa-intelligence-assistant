import pandas as pd
from pathlib import Path

DATA_PATH = Path("src/data/documents")


def load_automation_data():
    file_path = DATA_PATH / "automation_metrics.csv"
    if not file_path.exists():
        raise FileNotFoundError("automation_metrics.csv not found")

    return pd.read_csv(file_path)


def automation_summary():
    """
    Returns high-level automation metrics.
    """
    df = load_automation_data()

    summary = {
        "total_test_cases": int(df["Total_Test_Cases"].sum()),
        "total_automated": int(df["Automated_Test_Cases"].sum()),
        "total_pending": int(df["Pending_Automation"].sum()),
        "overall_coverage_percent": round(
            (df["Automated_Test_Cases"].sum() / df["Total_Test_Cases"].sum()) * 100, 2
        ),
        "lowest_coverage_module": df.loc[
            df["Automation_Coverage_%"].idxmin(), "Module"
        ],
        "highest_coverage_module": df.loc[
            df["Automation_Coverage_%"].idxmax(), "Module"
        ],
        "overall_coverage_percent": float(
        round(
        (df["Automated_Test_Cases"].sum() / df["Total_Test_Cases"].sum()) * 100, 2
        )
    ),

    }

    return summary
