from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from ..storage.document_store import DocumentStore
from ..utils.document_tracker import DocumentTracker

class DocumentLoader:
    def __init__(self, tracker: DocumentTracker, doc_store: DocumentStore):
        self.tracker = tracker
        self.doc_store = doc_store

    def load_documents(self, pdf_dir: Path) -> List:
        """Load unprocessed PDF documents"""
        docs = []
        unprocessed = self.tracker.get_unprocessed_files(pdf_dir)
        
        for file_path in sorted(unprocessed):
            try:
                loader = PyPDFLoader(str(file_path))
                documents = loader.load()
                
                # Archive the document
                archived_path = self.doc_store.archive_document(file_path)
                
                # Update tracker
                self.tracker.register_document(file_path, archived_path)
                
                docs.extend(documents)
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
                
        return docs