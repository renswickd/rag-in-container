import pytest
from src.components.embedding_manager import EmbeddingManager

def test_embedding_manager_initialization(test_persist_dir):
    """Test if EmbeddingManager initializes correctly"""
    manager = EmbeddingManager(test_persist_dir)
    assert manager.persist_directory == test_persist_dir
    assert manager.embedding_function is not None

def test_embed_and_store_documents(test_persist_dir, sample_documents):
    """Test embedding and storing documents"""
    manager = EmbeddingManager(test_persist_dir)
    manager.embed_and_store(sample_documents)
    
    assert manager.vectorstore is not None
    
    # Test if documents can be retrieved
    results = manager.similarity_search("test policy")
    assert len(results) > 0

def test_similarity_search_with_no_documents(test_persist_dir):
    """Test similarity search when no documents are stored"""
    manager = EmbeddingManager(test_persist_dir)
    results = manager.similarity_search("test query")
    assert len(results) == 0

def test_get_relevant_documents(test_persist_dir, sample_documents):
    """Test getting relevant documents"""
    manager = EmbeddingManager(test_persist_dir)
    manager.embed_and_store(sample_documents)
    
    results = manager.get_relevant_documents("test policy", k=2)
    assert len(results) <= 2