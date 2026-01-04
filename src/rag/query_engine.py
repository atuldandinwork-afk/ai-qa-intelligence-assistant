import collections
from urllib import response
from dotenv import load_dotenv
load_dotenv()

from chromadb import PersistentClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate


class QAQueryEngine:
    def __init__(
        self,
        persist_dir="vectorstore",
        llm_model="gpt-4o-mini",
    ):
        print("Using Chroma persist dir:", persist_dir)

        # Embeddings
        self.embedder = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # Chroma
        self.client = PersistentClient(path=persist_dir)

        collections = self.client.list_collections()
        if not collections:
            raise RuntimeError("No Chroma collections found. Did ingestion run?")

        self.collection = self.client.get_collection(collections[0].name)
        print(f"Using Chroma collection: {collections[0].name}")

        # LLM
        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=0.2,
        )

        # Prompt
        self.prompt = PromptTemplate(
            template="""
You are a senior QA and Test Engineering expert.

Answer the question using ONLY the information provided in the context.
If the answer is not present in the context, say exactly: "I don't know.
Use the context below to answer the question. Do not repeat headings. Summarize.
Answer using exact facts from the context.
Do not infer.
Do not generalize."

Context:
{context}

Question:
{question}

Answer:
""",
            input_variables=["context", "question"],
        )

    # ---- Internal helper ----
    def _retrieve_context(self, question: str, top_k: int = 2) -> str:
        query_embedding = self.embedder.embed_query(question)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents"],
        )

        documents = results.get("documents", [[]])[0]
        return "\n\n".join(documents)

    # ---- Public interface ----
    # def retrieve(self, question: str, top_k: int = 2) -> str:
    #     query_embedding = self.embedder.embed_query(question)

    #     results = self.collection.query(
    #         query_embeddings=[query_embedding],
    #         n_results=top_k,
    #         include=["documents"],
    #     )

    #     docs = results.get("documents", [[]])[0]
    #     print("DEBUG: Retrieved documents:", len(docs))

    #     return "\n\n".join(docs)
    
    def retrieve(self, query: str, top_k: int = 2, metadata_filter: dict | None = None) -> str:
        query_embedding = self.embedder.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=metadata_filter,
            include=["documents"],
        )

        documents = results.get("documents", [[]])[0]
        print("DEBUG: Retrieved documents:", len(documents))
        print("DEBUG: Retrieved documents content:", documents)
        return "\n\n".join(documents)

    def answer(self, question: str) -> str:
        context = self.retrieve(question)

        prompt_text = self.prompt.format(
            context=context,
            question=question,
        )

        response = self.llm.invoke(prompt_text)
        return response.content
    
    def retrieve_knowledge(self, question: str, top_k: int = 2) -> str:
        query_embedding = self.embedder.embed_query(question)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"doc_type": "knowledge"},
            include=["documents"]
        )

        documents = results.get("documents", [[]])[0]
        return "\n\n".join(documents)
    

    def answer_with_context(self, question: str, context: str) -> str:
        prompt = f"""
    You are a QA expert assistant.

    Use ONLY the context below to answer the question.
    Use the context below to answer the question. Do not repeat headings. Summarize.
    If the answer is not present, say "I don't know"
    Answer using exact facts from the context.
    Do not infer.
    Do not generalize.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
        response = self.llm.invoke(prompt)
        return response.content.strip()
    

   



    
    

    


    

    
