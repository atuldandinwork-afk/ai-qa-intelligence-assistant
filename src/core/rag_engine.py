from src.core.vector_db import VectorDB

class RAGEngine:
    def __init__(self, persist_dir="vectorstore"):
        self.vdb = VectorDB(persist_dir)
        self.vdb.create_collection()  # if empty, create; you'll replace when loading existing

    def query(self, question: str, k: int = 3):
        res = self.vdb.query(question, k)
        docs = res.get("documents", [[]])[0]
        # naive combination
        return "\n\n".join(docs)