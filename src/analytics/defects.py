import pandas as pd
from pathlib import Path

DATA_PATH = Path("src/data/documents")
DEFECT_FILE = DATA_PATH / "defects.csv"

def load_defect_data():
    """
    Loads defect data from CSV.
    """
    file_path = DATA_PATH / "defects.csv"
    if not file_path.exists():
        raise FileNotFoundError("defects.csv not found in src/data/documents")

    return pd.read_csv(file_path)


def defect_summary():
    """
    Computes core defect metrics including DRE.
    """
    df = load_defect_data()

    if "Detected_By" not in df.columns:
        raise ValueError(
            f"'Detected_By' column not found. Available columns: {df.columns.tolist()}"
        )

    # Define production detection sources
    production_sources = ["Production", "Monitoring"]

    prod = df[df["Detected_By"].isin(production_sources)].shape[0]
    pre_prod = df.shape[0] - prod

    dre = round(
        (pre_prod / (pre_prod + prod)) * 100, 2
    ) if (pre_prod + prod) > 0 else 0

    return {
        "total_defects": int(df.shape[0]),
        "pre_production_defects": int(pre_prod),
        "production_defects": int(prod),
        "dre_percent": dre,
        "logic_used": "Detected_By (Production vs Non-Production)",
    }

def get_defect_by_id(query: str) -> dict:
    """
    Retrieve defect details by defect ID (e.g., DF_005).
    """

    # Extract defect ID from query
    match = re.search(r"\b(df_\d+)\b", query.lower())
    if not match:
        return {
            "text": "No defect ID found in the question.",
            "analytics": False,
            "visual": False,
        }

    defect_id = match.group(1).upper()

    # Load defect data
    df = pd.read_csv(DEFECT_FILE)

    # Normalize column names just in case
    df.columns = [c.strip() for c in df.columns]

    # Locate defect
    row = df[df["Defect_ID"] == defect_id]

    if row.empty:
        return {
            "text": f"No defect found with ID {defect_id}.",
            "analytics": False,
            "visual": False,
        }

    defect = row.iloc[0]

    # Build a deterministic response
    text = (
        f"Defect {defect_id} details:\n"
        f"- Module: {defect['Module']}\n"
        f"- Environment: {defect['Environment']}\n"
        f"- Status: {defect['Status']}\n"
        f"- Severity: {defect['Severity']}\n"
        f"- Assigned To: {defect['Assigned_To']}\n"
        f"- RCA: {defect.get('RCA', 'Not provided')}\n"
        f"- Summary: {defect['Summary']}"
    )

    return {
        "text": text,
        "analytics": True,
        "visual": False,
    }