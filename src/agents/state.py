from typing import TypedDict, Optional


class AgentState(TypedDict):
    query: str
    intent: Optional[str]

    analytics_result: Optional[str]
    risk_result: Optional[str]
    rag_context: Optional[str]

    final_answer: Optional[str]



