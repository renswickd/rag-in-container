from typing import List
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class EmbeddingManager:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        # Initialize HuggingFace embeddings with all-MiniLM model
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vectorstore = None
        
    def embed_and_store(self, documents: List[Document]):
        """
        Create embeddings and store in ChromaDB
        """
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_function,
            persist_directory=self.persist_directory,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search for the query
        """
        if not self.vectorstore:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function
            )
        return self.vectorstore.similarity_search(query, k=k)

    def get_relevant_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Alternative method name for compatibility with newer LangChain versions
        """
        return self.similarity_search(query, k=k)


if __name__ == "__main__":
    # Example usage
    # from document_loader import DocumentLoader
    # from document_processor import DocumentProcessor

    # loader = DocumentLoader(docs_dir="data/policy_documents/", metadata_path="data/pr_metadata.csv")
    # docs = loader.load_documents()
    # print(f"Loaded {len(docs)} documents for embedding.")

    # processor = DocumentProcessor()
    # processed_docs = processor.process_documents(docs)
    # print(f"Processed into {len(processed_docs)} document chunks.")

    embedding_manager = EmbeddingManager(persist_directory="chromadb")
    # embedding_manager.embed_and_store(processed_docs)
    # print("Embedded documents and stored in Chroma DB.")

    # Test similarity search
    query = "I am not sure what choose for cloud security? Should I go with SSO or MFA?"
    results = embedding_manager.similarity_search(query, k=3)
    print(f"Top 3 similar documents for query: '{query}'")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Metadata: {doc.metadata}")
        print(f"Content: {doc.page_content[:500]}")