from data_loader import load_all_documents
from embedding import EmbeddingPipeline
from vectorstore import FaissVectorStore
from search import RAGSearch

if __name__ == "__main__":
    # docs = load_all_documents("./data/pdf_documents")
    store = FaissVectorStore("faiss_store")
    # store.build_from_documents(docs)
    store.load()
    # print(store.query("types is machine learning", top_k=3))

    rag_search=RAGSearch()
    query = "What is Machine Learning"
    summary = rag_search.search_and_summarize(query, top_k=3)

    print("Summary:", summary)