from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from chromadb import PersistentClient

class VectorDB:
    def __init__(self, persist_dir: str):
        self.persist_dir = persist_dir
        self.embedding = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        self.client = PersistentClient(path=persist_dir)
        self.collection_name = "langchain"

    def create_collection(self):
        collections = self.client.list_collections()
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(name=self.collection_name)

    def add_documents(self, documents):
        if not documents:
            raise ValueError("No documents to index")

        self.vectordb = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding,
            persist_directory=self.persist_dir,
            collection_name=self.collection_name,
        )

    def persist(self):
        # Chroma persists automatically, but we keep this for clarity
        pass
