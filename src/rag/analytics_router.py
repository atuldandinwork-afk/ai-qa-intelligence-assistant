def detect_intent(query: str) -> dict:
    """
    Detects whether the query is:
    - informational (RAG only)
    - analytical (needs numeric processing)
    - visual (needs chart)
    """

    q = query.lower()

    analytics_keywords = [
        "trend",
        "over time",
        "last sprint",
        "coverage",
        "execution rate",
        "defect rate",
        "dre",
        "automation progress",
    ]

    visual_keywords = [
        "show",
        "plot",
        "graph",
        "chart",
        "visualize",
    ]

    is_analytics = any(k in q for k in analytics_keywords)
    is_visual = any(k in q for k in visual_keywords)

    return {
        "analytics": is_analytics,
        "visual": is_visual,
    }
