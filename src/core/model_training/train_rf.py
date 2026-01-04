import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

DATA_FILE = Path("src/data/documents/test_execution_data.csv")
MODEL_PATH = Path("src/data/models/automation_rf.pkl")

def train_rf():
    if not DATA_FILE.exists():
        raise FileNotFoundError(DATA_FILE)
    df = pd.read_csv(DATA_FILE)
    # basic sanity: ensure columns exist
    features = ["Sprint", "Total_Test_Cases", "Pending_Automation", "Defects_Found_By_Automation"]
    for c in features:
        if c not in df.columns:
            raise ValueError(f"Missing column {c} in {DATA_FILE}")
    df = df.dropna(subset=features + ["Automation_Coverage_%"])
    X = df[features]
    y = df["Automation_Coverage_%"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Saved RF model to", MODEL_PATH)

if __name__ == "__main__":
    train_rf()
