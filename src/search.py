
import os
from dotenv import load_dotenv
from vectorstore import FaissVectorStore
from langchain_groq import ChatGroq

load_dotenv()


class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "openai/gpt-oss-20b",
    ):
        # Local embedding model + FAISS index
        self.vectorstore = FaissVectorStore(
            persist_dir=persist_dir,
            embedding_model=embedding_model,
        )

        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents

            docs = load_all_documents("data/pdf_documents")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()

        # Hosted LLM through Groq API
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is missing from your .env file")

        self.llm = ChatGroq(
            api_key=groq_api_key,
            model=llm_model,
            temperature=0.1,
        )

        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)

        texts = [
            result["metadata"].get("text", "")
            for result in results
            if result.get("metadata")
            and result["metadata"].get("text")
        ]

        if not texts:
            return "No relevant documents found."

        context = "\n\n".join(texts)

        prompt = f"""
You are a helpful assistant answering questions from documents.

Use only the supplied context. Do not invent facts.
If the context does not answer the question, say so.
Answer clearly and concisely.

Context:
{context}

Question:
{query}

Answer:
"""

        response = self.llm.invoke(prompt)
        return response.content


if __name__ == "__main__":
    rag_search = RAGSearch()

    query = "What is the attention mechanism?"
    answer = rag_search.search_and_summarize(query, top_k=3)

    print("Answer:", answer)
