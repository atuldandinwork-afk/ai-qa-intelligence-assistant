# AI QA Intelligence Assistant

Starter project for a RAG + ML + prediction + LoRA-capable QA assistant.
Open this folder in VS Code. Use the included scripts to ingest documents and run the minimal Gradio UI.

Structure:
- src/ingestion: document loaders + chunking
- src/core: rag_engine, vector_db, llm wrapper
- src/ui: Gradio app
- data/documents: your existing files (place them here)
