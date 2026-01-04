from src.agents.state import AgentState
from src.analytics.automation import automation_summary
from src.analytics.execution import execution_stability_trend
from src.analytics.defects import defect_summary


def analytics_agent(state: AgentState) -> AgentState:
    query = state["query"].lower()

    responses = []

    if "automation" in query or "coverage" in query:
        summary = automation_summary()
        responses.append(
            f"Automation coverage is {summary['overall_coverage_percent']}% across all modules."
        )

    if "execution" in query or "pass rate" in query or "stability" in query:
        _, summary = execution_stability_trend(last_n_sprints=4)
        responses.append(
            f"Execution stability is {summary['direction']}. "
            f"Pass rate is {summary['end_pass_rate_percent']}%."
        )

    if "defect" in query or "dre" in query:
        summary = defect_summary()
        responses.append(
            f"Defect Removal Efficiency is {summary['dre_percent']}%. "
            f"{summary['pre_production_defects']} defects were caught before production."
        )

    state["analytics_result"] = " ".join(responses)
    return state
