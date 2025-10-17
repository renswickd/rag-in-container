from pathlib import Path
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..storage.vector_store import VectorStore

class DocumentProcessor:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def process_documents(self, documents: List) -> bool:
        """Process documents and add to vector store"""
        if not documents:
            print("No documents to process")
            return False
            
        try:
            # Split documents into chunks
            chunks = self.splitter.split_documents(documents)
            
            if not chunks:
                print("No chunks created from documents")
                return False
            
            # Add to vector store
            self.vector_store.add_documents(chunks)
            print(f"Successfully added {len(chunks)} chunks to vector store")
            
            return True
            
        except Exception as e:
            print(f"Error processing documents: {e}")
            return False