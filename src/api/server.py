from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.analytics.execution_lookup import get_execution_by_test_case
from src.rag.unified_handler import handle_query, _get_rag_engine
from src.ui.plotters import (
    render_execution_trend,
    render_automation_coverage,
    render_defect_distribution,
)

import io, base64
from typing import Optional


def fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.read()
    return base64.b64encode(img_bytes).decode("utf-8")

app = FastAPI(
    title="AI QA Intelligence Assistant API",
    description="Simple endpoints exposing analytics functions",
    version="0.1",
)

# allow all origins for testing with Postman, browser, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


from pydantic import BaseModel


class ExecutionRequest(BaseModel):
    test_case_id: str


@app.get("/execution/{test_case_id}")
def read_execution(test_case_id: str):
    """Return execution summary for a given test case id via path parameter."""
    result = get_execution_by_test_case(test_case_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No data found for {test_case_id}")
    return result


@app.post("/execution")
def read_execution_post(req: ExecutionRequest):
    """Return execution summary for a given test case id via POST JSON body."""
    result = get_execution_by_test_case(req.test_case_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {req.test_case_id}",
        )
    return result


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    text: Optional[str]
    figure_base64: Optional[str]


# new models for retrieval debugging
class RetrieveRequest(BaseModel):
    query: str
    top_k: Optional[int] = 2


class RetrieveResponse(BaseModel):
    documents: str
    answer: str


@app.post("/query", response_model=QueryResponse)
def run_query(req: QueryRequest):
    """Run the unified handler and optionally return a visualization as base64 PNG."""
    result = handle_query(req.query)
    if result is None:
        return {"text": "I don't know.", "figure_base64": None}

    text = result.get("text", "")
    fig_str = None
    if result.get("visual"):
        vt = result.get("visual_type")
        payload = result.get("visual_payload")
        if vt == "execution_trend":
            fig = render_execution_trend(payload)
        elif vt == "automation_coverage":
            fig = render_automation_coverage(payload)
        elif vt == "defect_distribution":
            fig = render_defect_distribution(payload)
        else:
            fig = None

        if fig is not None:
            fig_str = fig_to_base64(fig)

    return {"text": text, "figure_base64": fig_str}


# ------------------------------------------------------------------
# endpoint for retrieving raw documents used by the RAG pipeline
# useful for debugging or inspection
# ------------------------------------------------------------------
@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve_documents(req: RetrieveRequest):
    """Return the documents retrieved from the vector store and generate an answer based on them."""
    engine = _get_rag_engine()
    if engine is None:
        raise HTTPException(status_code=500, detail="RAG engine not available")

    docs = engine.retrieve(req.query, top_k=req.top_k)
    answer = engine.answer_with_context(req.query, docs)
    return {"documents": docs, "answer": answer}


@app.get("/")
def root():
    return {"message": "AI QA Intelligence Assistant API is running"}
