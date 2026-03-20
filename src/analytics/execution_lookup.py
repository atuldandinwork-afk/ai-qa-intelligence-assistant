import pandas as pd
from pathlib import Path

DATA_DIR = Path("src/data/documents")
TEST_EXEC_FILE = DATA_DIR / "test_execution_results.csv"


def load_test_cases():
    df = pd.read_csv(TEST_EXEC_FILE)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    return df



# def get_execution_by_test_case(test_case_id: str):
#     df = load_test_cases()
#     print("Available columns:", df.columns.tolist())

import pandas as pd
from pathlib import Path

EXECUTION_FILE = Path("src/data/documents/test_execution_results.csv")

def get_execution_by_test_case(test_case_id: str):
    df = pd.read_csv(EXECUTION_FILE)

    # ✅ Normalize column names once
    df.columns = [c.strip().lower() for c in df.columns]

    if "test_case_id" not in df.columns:
        raise ValueError("Execution file missing test_case_id column")

    tc_df = df[df["test_case_id"] == test_case_id]

    if tc_df.empty:
        return None

    linked_defects = (
        tc_df["linked_defect"]
        .dropna()
        .unique()
        .tolist()
        if "linked_defect" in tc_df.columns
        else []
    )

    return {
        "test_case_id": test_case_id,
        "total_executions": int(len(tc_df)),
        "passed": int((tc_df["status"] == "Pass").sum()),
        "failed": int((tc_df["status"] == "Fail").sum()),
        "latest_status": str(tc_df.sort_values("execution_date").iloc[-1]["status"]),
        "linked_defects": linked_defects,
    }
