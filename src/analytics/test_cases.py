import pandas as pd
from pathlib import Path

DATA_DIR = Path("src/data/documents")
TEST_CASES_FILE = DATA_DIR / "test_cases.csv"


def load_test_cases():
    df = pd.read_csv(TEST_CASES_FILE)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def get_test_case_by_id(test_case_id: str):
    df = load_test_cases()
    #print("Available columns:", df.columns.tolist())

    test_case_id = test_case_id.upper().strip()
    row = df[df["test_case_id"] == test_case_id]

    if row.empty:
        return None

    r = row.iloc[0]

    return {
        "Test_Case_ID": r["test_case_id"],
        "Title": r["title"],
        "Module": r["module"],
        "Priority": r["priority"],
        "Automated": r["automated"],
        "Created_By": r["created_by"],
        "Created_Date": r["created_date"],
        "Last_Updated": r["last_updated"],
    }
