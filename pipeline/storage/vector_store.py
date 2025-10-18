from pathlib import Path
from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:
    def __init__(
        self, 
        persist_directory: str,
        collection_name: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.db = self._init_db()

    def _init_db(self) -> Chroma:
        """Initialize or load existing Chroma DB"""
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )

    def add_documents(self, documents: List) -> None:
        """Add documents to vector store"""
        try:
            if not documents:
                raise ValueError("No documents provided")
                
            # Add documents and persist
            self.db.add_documents(documents)
            # self.db.persist()
            print(f"Successfully added and persisted {len(documents)} documents")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

    def reset(self) -> None:
        """Reset the vector store"""
        self.db._client.delete_collection(self.collection_name)
        self.db = self._init_db()

    def get_stats(self) -> dict:
        """Get vector store statistics"""
        return {
            "total_documents": self.db._collection.count(),
            "collection_name": self.collection_name
        }