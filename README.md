# AI QA Intelligence Assistant

> A RAG-powered, multi-agent QA intelligence system that answers natural language questions about your test suite — covering automation coverage, defect trends, execution stability, flaky tests, and sprint risk prediction.

Built by a QA engineer with 16+ years of experience who got tired of waiting for dashboards to tell him what he already knew was wrong.

---

## What it does

Most QA dashboards show you *what happened*. This assistant tells you *what it means* and *what to watch next sprint*.

Ask it anything:

```
"Which modules are risky next sprint?"
→ Risk agent scores modules by defect density, execution instability, and automation gaps

"Are there flaky tests?"
→ Identifies flaky test cases from execution history with failure rate analysis

"Show automation trend over last 4 sprints"
→ Returns a chart + natural language summary of coverage direction

"What is defect removal efficiency?"
→ RAG retrieves context, LLM explains the metric with your actual data

"Is execution stable?"
→ Execution stability trend with pass/fail variance across sprints
```

---

## Architecture

```
User Query
    │
    ▼
Intent Router  ──────────────────────────────────────┐
    │                                                 │
    ├── "analytics"  →  Analytics Agent               │
    │       ├── automation_summary()                  │
    │       ├── automation_trend()                    │
    │       ├── defect_summary()                      │
    │       ├── defect_leakage_trend()                │
    │       └── execution_stability_trend()           │
    │                                                 │
    ├── "risk"       →  Risk Agent                    │
    │       └── module risk scoring (ML)              │
    │                                                 │
    └── "rag"        →  RAG Engine                    │
            ├── ChromaDB vector store                 │
            ├── sentence-transformers embeddings      │
            └── OpenAI LLM response generation        │
                                                      │
Orchestrator assembles final_answer ◄─────────────────┘
    │
    ▼
Gradio UI  /  FastAPI endpoint
```

---

## Key capabilities

**Multi-agent orchestration** — an intent router classifies every query and dispatches to the right agent. Analytics questions go to the analytics agent, risk questions to the risk agent, conceptual questions to the RAG engine.

**Risk prediction** — the risk agent scores test modules using execution instability, defect density, and automation gaps to flag what needs attention before the next sprint starts.

**RAG over QA knowledge** — document ingestion pipeline (LangChain + ChromaDB + sentence-transformers) lets you ask conceptual questions about QA metrics and get answers grounded in your own documentation.

**Execution intelligence** — tracks test case execution history, surfaces flaky tests, and measures stability trends across sprints.

**Defect analytics** — defect leakage trend, defect removal efficiency, production escape rate — all queryable in plain English.

**Visualization** — matplotlib charts returned via API as base64 PNG, embedded directly in the Gradio UI.

---

## Tech stack

| Layer | Technology |
|---|---|
| LLM | OpenAI GPT (via LangChain) |
| Vector store | ChromaDB |
| Embeddings | sentence-transformers |
| Agent orchestration | Custom LangGraph-style state machine |
| API | FastAPI + Uvicorn |
| UI | Gradio |
| Analytics | pandas, scikit-learn, matplotlib |
| Testing | pytest, pytest-asyncio |

---

## Getting started

**Prerequisites:** Python 3.10+, an OpenAI API key

```bash
# Clone the repo
git clone https://github.com/atuldandinwork-afk/ai-qa-intelligence-assistant.git
cd ai-qa-intelligence-assistant

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY=your_key_here

# Ingest your documents
python src/ingestion/ingest.py

# Launch the Gradio UI
python src/ui/app.py

# Or start the FastAPI server
uvicorn src.api.server:app --reload
```

---

## API reference

### Query endpoint

```bash
POST /query
Content-Type: application/json

{ "query": "Which modules are risky next sprint?" }
```

Response:
```json
{
  "text": "Modules ranked by risk: Login (high), Checkout (medium)...",
  "figure_base64": "<base64 PNG if visualization was generated>"
}
```

### Execution lookup

```bash
GET  /execution/{test_case_id}     # e.g. /execution/TC_0108
POST /execution  { "test_case_id": "TC_0108" }
```

---

## Project structure

```
ai-qa-intelligence-assistant/
├── src/
│   ├── agents/
│   │   ├── orchestrator.py        # Main agent loop
│   │   ├── intent_router.py       # Query classification
│   │   ├── analytics_agent.py     # Analytics dispatch
│   │   └── risk_agent.py          # Module risk scoring
│   ├── analytics/
│   │   ├── automation.py          # Automation coverage
│   │   ├── automation_trend.py    # Sprint-over-sprint trend
│   │   ├── defects.py             # Defect summary
│   │   ├── defect_leakage.py      # Production escape rate
│   │   ├── execution.py           # Stability + flaky tests
│   │   ├── execution_lookup.py    # Test case lookup
│   │   ├── defect_lookup.py       # Defect record lookup
│   │   └── visuals.py             # matplotlib chart generation
│   ├── rag/
│   │   ├── query_engine.py        # ChromaDB + LLM query
│   │   ├── unified_handler.py     # Routes to analytics or RAG
│   │   └── analytics_router.py    # Intent detection
│   ├── ingestion/                 # Document loaders + chunking
│   ├── api/
│   │   └── server.py              # FastAPI endpoints
│   └── ui/
│       └── app.py                 # Gradio interface
├── data_generator/                # Synthetic QA data generation
├── chroma/                        # Vector store (local)
├── db/                            # SQLite / structured data
├── tests/                         # pytest test suite
├── requirements.txt
└── pytest.ini
```

---

## Roadmap

- [ ] RAGAS integration for RAG pipeline evaluation (faithfulness, answer relevance, context recall)
- [ ] Hallucination detection layer
- [ ] Benchmark suite with 50 curated QA question-answer pairs
- [ ] GitHub Actions CI — auto-run evals on every push
- [ ] LLM eval score dashboard in README
- [ ] LoRA fine-tuning on QA-domain data
- [ ] Hugging Face Spaces deployment for live demo

---

## Why I built this

I've spent 16+ years in software testing. The hardest part was never finding bugs — it was communicating risk to stakeholders in time to do something about it. Dashboards show the past. This assistant reasons about it.

This project is my transition from writing tests to building the intelligence layer that makes testing smarter.

---

## Author

**Atul Dandin** — Senior QA Engineer → AI Quality Specialist

[GitHub](https://github.com/atuldandinwork-afk) · [LinkedIn](https://linkedin.com/in/your-profile)

---

## License

MIT
