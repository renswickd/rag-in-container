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
        try:
            # Get all PDF files in directory
            pdf_files = list(pdf_dir.glob("**/temp_uploads/*.pdf"))
            
            for file_path in pdf_files:
                try:
                    # Load document
                    loader = PyPDFLoader(str(file_path))
                    documents = loader.load()
                    
                    if documents:
                        # Archive the document
                        archived_path = self.doc_store.archive_document(file_path)
                        
                        # Update tracker with archived path
                        self.tracker.register_document(file_path, archived_path)
                        
                        # Add metadata to documents
                        for doc in documents:
                            doc.metadata.update({
                                "source": str(file_path.name),
                                "archived_path": str(archived_path)
                            })
                        
                        docs.extend(documents)
                        
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
                    
            return docs
            
        except Exception as e:
            print(f"Error scanning directory {pdf_dir}: {e}")
            return []