import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path("src/data/documents")
DEFECT_FILE = DATA_DIR / "defects.csv"


def handle_defect_question(query: str):
    """
    Handles all DF_xxxx defect-specific questions.
    """

    df = pd.read_csv(DEFECT_FILE)

    # Normalize column names defensively
    df.columns = [c.strip() for c in df.columns]

    # Extract defect ID (e.g. DF_005, DF_0007)
    match = re.search(r"(df_\d+)", query.lower())
    if not match:
        return {
            "text": "Defect ID not found in the question.",
            "analytics": False,
            "visual": False,
        }

    defect_id = match.group(1).upper()

    defect = df[df["Defect_ID"].str.upper() == defect_id]

    if defect.empty:
        return {
            "text": f"No defect found with ID {defect_id}.",
            "analytics": False,
            "visual": False,
        }

    row = defect.iloc[0]

    q = query.lower()

    # -----------------------------
    # RCA
    # -----------------------------
    if "rca" in q or "root cause" in q:
        rca = row.get("RCA", "")
        if pd.isna(rca) or str(rca).strip() == "":
            rca = "RCA not recorded."
        return {
            "text": f"RCA for defect {defect_id}: {rca}",
            "analytics": False,
            "visual": False,
        }

    # -----------------------------
    # STATUS
    # -----------------------------
    if "status" in q:
        return {
            "text": f"Defect {defect_id} is currently in '{row['Status']}' status.",
            "analytics": False,
            "visual": False,
        }

    # -----------------------------
    # FULL DEFECT SUMMARY (DEFAULT)
    # -----------------------------
    text = (
        f"Defect {defect_id} details:\n"
        f"• Module: {row['Module']}\n"
        f"• Environment: {row['Environment']}\n"
        f"• Severity: {row['Severity']}\n"
        f"• Status: {row['Status']}\n"
        f"• Detected By: {row['Detected_By']}\n"
        f"• Summary: {row['Summary']}"
    )

    return {
        "text": text,
        "analytics": False,
        "visual": False,
    }
