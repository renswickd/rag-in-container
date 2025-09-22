import pytest
from src.components.embedding_manager import EmbeddingManager
from main import QueryEngine

@pytest.fixture
def query_engine(test_persist_dir):
    embedding_manager = EmbeddingManager(test_persist_dir)
    return QueryEngine(embedding_manager)

@pytest.fixture
def setup_vectorstore(test_persist_dir, sample_documents):
    embedding_manager = EmbeddingManager(test_persist_dir)
    embedding_manager.embed_and_store(sample_documents)
    return embedding_manager

def test_query_engine_initialization(query_engine):
    """Test if QueryEngine initializes correctly"""
    assert query_engine.embedding_manager is not None
    assert query_engine.llm is not None
    assert query_engine.qa_chain is not None

def test_format_context(query_engine, sample_documents):
    """Test context formatting"""
    context = query_engine._format_context(sample_documents)
    assert isinstance(context, str)
    assert "Test Policy" in context
    assert "Test Owner" in context

def test_process_query_with_no_relevant_docs(query_engine):
    """Test query processing when no relevant documents found"""
    response = query_engine.process_query("irrelevant query")
    assert "couldn't find any relevant information" in response.lower()

def test_process_query_maintains_chat_history(query_engine, setup_vectorstore):
    """Test if chat history is maintained"""
    query_engine.embedding_manager = setup_vectorstore
    query_engine.process_query("test query")
    assert len(query_engine.chat_history) == 1