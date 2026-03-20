import re
import pandas as pd

from src.analytics.defects import defect_summary, load_defect_data
from src.analytics.execution import execution_stability_trend, flaky_tests
from src.analytics.automation import automation_summary
from src.rag.query_engine import QAQueryEngine
from src.analytics.defects import get_defect_by_id
from src.analytics.defect_lookup import get_defect_by_id
from src.analytics.execution_lookup import get_execution_by_test_case
from src.analytics.traceability import trace_test_case




# Optional: risk predictions file
RISK_FILE = "src/data/predictions/module_risk_predictions.csv"

# Initialize RAG engine when first needed.  This avoids import-time
# failures if the langchain-openai integration isn't installed or if the
# environment (API key, vectorstore) isn't yet configured.
_rag_engine = None

def _get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        try:
            _rag_engine = QAQueryEngine()
        except ImportError as exc:
            # log and leave engine as None; callers can degrade gracefully
            print("WARNING: failed to initialize RAG engine:", exc)
            _rag_engine = None
    return _rag_engine


def handle_query(query: str) -> dict:
    q = query.lower().strip()

    # =================================================
    # 1️⃣ DEFECT LOOKUP (DF_XXXX)
    # =================================================
    match_df = re.search(r"\bdf_\d+\b", q)
    if match_df:
        defect_id = match_df.group().upper()
        defect = get_defect_by_id(defect_id)

        if not defect:
            return {
                "text": f"No defect found with ID {defect_id}.",
                "analytics": True,
                "visual": False,
            }

        if "rca" in q:
            return {
                "text": f"RCA for {defect_id}: {defect.get('RCA') or 'Not documented.'}",
                "analytics": True,
                "visual": False,
            }

        text = (
            f"Defect {defect['Defect_ID']} belongs to module {defect['Module']}.\n"
            f"Severity: {defect['Severity']}\n"
            f"Status: {defect['Status']}\n"
            f"Detected by: {defect['Detected_By']}\n"
            f"Summary: {defect['Summary']}"
        )

        return {
            "text": text,
            "analytics": True,
            "visual": False,
        }

    # =================================================
    # 2️⃣ TEST CASE TRACEABILITY (TC_XXXX)
    # =================================================
    match_tc = re.search(r"\btc_\d+\b", q)
    if match_tc:
        tc_id = match_tc.group().upper()
        trace = trace_test_case(tc_id)

        if not trace:
            return {
                "text": f"No trace data found for {tc_id}.",
                "analytics": True,
                "visual": False,
            }

        exec_data = trace["execution"]
        defects = trace["defects"]

        text = (
            f"{tc_id} execution summary:\n"
            f"- Total executions: {exec_data['total_executions']}\n"
            f"- Latest status: {exec_data['latest_status']}\n"
        )

        if defects:
            text += "\nLinked defects:\n"
            for d in defects:
                text += f"- {d['Defect_ID']} ({d['Severity']}, {d['Status']})\n"
        else:
            text += "\nNo linked defects."

        return {
            "text": text.strip(),
            "analytics": True,
            "visual": False,
        }

    # =================================================
    # 3️⃣ RISK ANALYTICS
    # =================================================
    if any(k in q for k in ["risk", "risky", "next sprint"]):
        if not pd.io.common.file_exists(RISK_FILE):
            return {
                "text": "Risk predictions are not available yet.",
                "analytics": True,
                "visual": False,
            }

        df = pd.read_csv(RISK_FILE)
        high_risk = df[df["risk_probability"] > 0.6]

        if high_risk.empty:
            return {
                "text": "No high-risk modules predicted.",
                "analytics": True,
                "visual": False,
            }

        modules = ", ".join(high_risk["Module"].unique())
        return {
            "text": f"High-risk modules for the next sprint: {modules}.",
            "analytics": True,
            "visual": False,
        }

    # =================================================
    # 4️⃣ EXECUTION ANALYTICS
    # =================================================
    if any(k in q for k in ["execution", "pass rate", "stability", "flaky"]):
        trend_df, summary = execution_stability_trend(last_n_sprints=4)

        text = (
            f"Execution stability is {summary['direction']}. "
            f"Pass rate is {summary['end_pass_rate_percent']}% "
            f"in Sprint {summary['end_sprint']}."
        )

        flaky = flaky_tests()
        if len(flaky) > 0:
            text += f" {len(flaky)} flaky tests were identified."

        return {
            "text": text,
            "analytics": True,
            "visual": True,
            "visual_type": "execution_trend",
            "visual_payload": trend_df,
        }

    # =================================================
    # 5️⃣ AUTOMATION ANALYTICS
    # =================================================
    if any(k in q for k in ["automation", "coverage"]):
        summary = automation_summary()

        return {
            "text": f"Automation coverage is {summary['overall_coverage_percent']}%.",
            "analytics": True,
            "visual": False,
        }

    # =================================================
    # 6️⃣ DEFECT METRICS (DRE)
    # =================================================
    if any(k in q for k in ["dre", "defect removal"]):
        summary = defect_summary()

        return {
            "text": f"DRE is {summary['dre_percent']}%.",
            "analytics": True,
            "visual": False,
        }

    # =================================================
    # 7️⃣ RAG FALLBACK (LAST)
    # =================================================
    # fallback to RAG if none of the analytic rules matched
    engine = _get_rag_engine()
    if engine is None:
        return {
            "text": "I don't know.",
            "analytics": False,
            "visual": False,
        }

    try:
        answer = engine.answer(query)
        return {
            "text": answer,
            "analytics": False,
            "visual": False,
        }
    except Exception:
        return {
            "text": "I don't know.",
            "analytics": False,
            "visual": False,
        }



def handle_rag_question(query: str):
    context = _rag_engine.retrieve_knowledge(query)
    answer = _rag_engine.answer_with_context(query, context)

    return {
        "text": answer,
        "analytics": False,
        "visual": False,
    }

def handle_project_info_question(query: str):
        """
        Handles project-level and people/entity questions
        using ONLY org_project_info.md context.
        """
        context = _rag_engine.retrieve(
            query=query,
            top_k=2,
            metadata_filter={"doc_type": "project_info"},
        )

        if not context.strip():
            return {
                "text": "I don't know.",
                "analytics": False,
                "visual": False,
            }

        prompt = f"""
    You are answering a factual project information question.

    Use ONLY the information provided below.
    Answer clearly and directly.
    Do NOT infer or add extra information.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

        answer = _rag_engine.llm.invoke(prompt)

        return {
            "text": answer.content,
            "analytics": False,
            "visual": False,
        }



