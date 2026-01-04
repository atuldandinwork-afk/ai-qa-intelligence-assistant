from src.agents.state import AgentState


def intent_router(state: AgentState) -> AgentState:
    query = state["query"].lower()

    if any(k in query for k in ["risk", "unstable", "next sprint"]):
        state["intent"] = "risk"

    elif any(k in query for k in [
        "automation",
        "coverage",
        "execution",
        "pass rate",
        "defect",
        "dre",
        "trend"
    ]):
        state["intent"] = "analytics"

    else:
        state["intent"] = "rag"

    return state
