from src.agents.intent_router import route_intent
from src.agents.risk_agent import risk_agent
from src.agents.analytics_agent import analytics_agent
from src.agents.rag_agent import rag_agent


def orchestrate(state: dict) -> dict:
    """
    Central orchestrator for agentic reasoning.
    Mutates and returns shared state.
    """

    query = state.get("query", "")
    if not query:
        state["final_answer"] = "No query provided."
        return state

    # 1) Route intent
    intent = route_intent(query)
    state["intent"] = intent

    # 2) Invoke appropriate agent
    if intent == "risk":
        state = risk_agent(state)

    elif intent == "analytics":
        state = analytics_agent(state)

    else:  # rag fallback
        state = rag_agent(state)

    # 3) Synthesize final answer
    # Each agent is responsible for writing its own result
    if state.get("risk_result"):
        state["final_answer"] = state["risk_result"]

    elif state.get("analytics_result"):
        state["final_answer"] = state["analytics_result"]

    elif state.get("rag_context"):
        state["final_answer"] = state["rag_context"]

    else:
        state["final_answer"] = "I don't know."

    return state
