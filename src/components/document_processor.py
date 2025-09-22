from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks while preserving metadata
        """
        processed_documents = []
        for doc in documents:
            splits = self.text_splitter.split_text(doc.page_content)
            for split in splits:
                processed_documents.append(
                    Document(
                        page_content=split,
                        metadata=doc.metadata
                    )
                )
        return processed_documents
    
if __name__ == "__main__":
    # use the documents from document_loader.py for testing
    from document_loader import DocumentLoader

    loader = DocumentLoader(docs_dir="data/policy_documents/", metadata_path="data/pr_metadata.csv")
    docs = loader.load_documents()
    print(f"Loaded {len(docs)} documents for processing.")

    processor = DocumentProcessor()
    processed_docs = processor.process_documents(docs)
    print(f"Processed into {len(processed_docs)} document chunks.")
    for doc in processed_docs[:2]:   
        print(f"Metadata: {doc.metadata}")
        print(f"Content: {doc.page_content[:500]}")   
        print("------------------\n")