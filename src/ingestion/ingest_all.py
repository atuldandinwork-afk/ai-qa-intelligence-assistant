from src.ingestion.loaders.file_loader import load_documents_from_folder, load_file
from src.core.vector_db import VectorDB
from pathlib import Path


DATA_FOLDER = Path("src/data/documents")
PERSIST_DIR = str(Path("vectorstore").absolute())

def run_ingest_and_index():
    print(f"Recursively loading documents from {DATA_FOLDER}")

    docs = []
    for file_path in DATA_FOLDER.rglob("*"):
        if file_path.suffix.lower() in [".md", ".txt", ".csv", ".json"]:
            docs.extend(load_file(file_path))

    print(f"Loaded {len(docs)} chunks. Initializing vector DB...")

    vdb = VectorDB(persist_dir=PERSIST_DIR)
    vdb.create_collection()
    vdb.add_documents(docs)
    vdb.persist()

    print("Indexing complete. Persisted to", PERSIST_DIR)

if __name__ == "__main__":
    run_ingest_and_index()
    print("Writing vectors to:", PERSIST_DIR)

