import pandas as pd
from pathlib import Path

DATA_FILE = Path("src/data/documents/defects.csv")


def get_defect_by_id(defect_id: str) -> dict | None:
    """
    Deterministic lookup for a defect by ID.
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError("defects.csv not found")

    df = pd.read_csv(DATA_FILE)

    defect_id = defect_id.strip().upper()

    row = df[df["Defect_ID"].str.upper() == defect_id]

    if row.empty:
        return None

    r = row.iloc[0]

    return {
        "Defect_ID": r["Defect_ID"],
        "Module": r["Module"],
        "Environment": r["Environment"],
        "Status": r["Status"],
        "Severity": r["Severity"],
        "RCA": (
            r["RCA"]
            if pd.notna(r.get("RCA"))
            else "RCA not yet identified"
        ),
        "Detected_By": r.get("Detected_By", "Unknown"),
        "Summary": r.get("Summary", ""),
    }
