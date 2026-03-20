# AI QA Intelligence Assistant

Starter project for a RAG + ML + prediction + LoRA-capable QA assistant.
Open this folder in VS Code. Use the included scripts to ingest documents and run the minimal Gradio UI.

Structure:
- src/ingestion: document loaders + chunking
- src/core: rag_engine, vector_db, llm wrapper
- src/ui: Gradio app
- data/documents: your existing files (place them here)

## FastAPI endpoint

A small server is provided in `src/api/server.py` that exposes analytics functions via HTTP.

Start the server:

```powershell
uvicorn src.api.server:app --reload
```

Endpoints:

- `GET /execution/{test_case_id}`  
  Returns execution details for the given test case id (e.g. `TC_0108`).

- `POST /execution`  
  JSON body `{ "test_case_id": "TC_0108" }`.

You can call these using Postman, curl, or any REST client.

### Query endpoint (Gradio-style)

- `POST /query`  
  JSON body: `{ "query": "<your question>" }`  
  Returns a JSON object with `text` (the answer) and, if a visualization is generated, `figure_base64` containing a base64‑encoded PNG.  

Example using curl:

```powershell
curl -X POST http://127.0.0.1:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query":"Show execution trend"}'
```

Decode the `figure_base64` string to view the chart in any image viewer or embed it in HTML.
