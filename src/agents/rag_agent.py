from src.rag.query_engine import QAQueryEngine

# Initialize RAG engine once (important for performance)
_rag_engine = QAQueryEngine()


def rag_agent(state: dict) -> dict:
    """
    Fallback RAG agent.
    Uses vector search + LLM to answer unstructured questions.
    """

    query = state.get("query", "")
    if not query:
        state["rag_context"] = "No query provided."
        return state

    try:
        answer = _rag_engine.answer(query)
        state["rag_context"] = answer
    except Exception as e:
        state["rag_context"] = "I don't know."

    return state
