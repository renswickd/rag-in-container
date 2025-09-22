import os
import warnings
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import pandas as pd
from pathlib import Path

# Suppress PDF-related warnings
warnings.filterwarnings('ignore', category=UserWarning, message='.*?wrong pointing.*?')

class DocumentLoader:
    def __init__(self, docs_dir: str, metadata_path: str):
        self.docs_dir = Path(docs_dir)
        self.metadata_df = pd.read_csv(metadata_path)
    
    def load_documents(self) -> List[Document]:
        """
        Load PDF documents and merge with metadata from CSV
        """
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.docs_dir}")
            
        documents = []
        for pdf_path in self.docs_dir.glob("*.pdf"):
            try:
                loader = PyPDFLoader(str(pdf_path))
                pdf_documents = loader.load()
                
                # Get metadata for this document
                doc_metadata = self.metadata_df[
                    self.metadata_df['policy_title'] == pdf_path.name.rstrip('.pdf')
                ].to_dict('records')
                
                if doc_metadata:
                    for doc in pdf_documents:
                        doc.metadata.update(doc_metadata[0])
                        documents.append(doc)
                        
            except Exception as e:
                print(f"Error loading {pdf_path}: {str(e)}")
                continue
                
        return documents
    
if __name__ == "__main__":

    # Example usage
    loader = DocumentLoader(docs_dir="data/policy_documents/", metadata_path="data/pr_metadata.csv")
    docs = loader.load_documents()
    print(f"Loaded {len(docs)} documents with metadata.")
    for doc in docs[:2]:
        print(doc.metadata)