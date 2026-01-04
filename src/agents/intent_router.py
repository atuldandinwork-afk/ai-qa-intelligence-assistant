# src/agents/intent_router.py

def route_intent(query: str) -> str:
    q = query.lower()

    # Risk / prediction intent
    if any(k in q for k in [
        "risk", "risky", "unstable", "next sprint", "prediction"
    ]):
        return "risk"

    # Analytics intent
    if any(k in q for k in [
        "automation", "coverage", "execution", "pass rate",
        "trend", "defect", "dre", "stability", "flaky"
    ]):
        return "analytics"

    # Default fallback
    return "rag"
