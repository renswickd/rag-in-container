import pytest
from src.components.document_processor import DocumentProcessor
from langchain.schema import Document

def test_document_processor_initialization():
    """Test if DocumentProcessor initializes with default values"""
    processor = DocumentProcessor()
    assert processor.text_splitter._chunk_size == 1000  # Note the underscore
    assert processor.text_splitter._chunk_overlap == 200

def test_process_documents_with_valid_input(sample_documents):
    """Test processing documents with valid input"""
    processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    processed_docs = processor.process_documents(sample_documents)
    
    assert len(processed_docs) > 0
    assert all(isinstance(doc, Document) for doc in processed_docs)
    assert all(len(doc.page_content) <= 100 for doc in processed_docs)

def test_process_documents_preserves_metadata(sample_documents):
    """Test if metadata is preserved after processing"""
    processor = DocumentProcessor()
    processed_docs = processor.process_documents(sample_documents)
    
    original_metadata = sample_documents[0].metadata
    for doc in processed_docs:
        assert doc.metadata == original_metadata

def test_process_empty_documents():
    """Test processing empty document list"""
    processor = DocumentProcessor()
    processed_docs = processor.process_documents([])
    assert len(processed_docs) == 0