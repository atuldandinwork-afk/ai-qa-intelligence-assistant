import pandas as pd
from src.agents.state import AgentState

RISK_FILE = "src/data/predictions/module_risk_predictions.csv"


def risk_agent(state: AgentState) -> AgentState:
    df = pd.read_csv(RISK_FILE)

    high_risk = (
        df[df["risk_probability"] > 0.6]
        .sort_values("risk_probability", ascending=False)
        .head(3)
    )

    if high_risk.empty:
        state["risk_result"] = "No high-risk modules detected for the upcoming sprint."
        return state

    response = "High risk modules for the upcoming sprint:\n"

    for _, row in high_risk.iterrows():
        response += (
            f"- {row['Module']} (Sprint {row['Sprint_Number']}): "
            f"{round(row['risk_probability'] * 100)}% risk. "
            f"{row['risk_explanation']}\n"
        )

    state["risk_result"] = response
    return state
