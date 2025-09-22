import pytest
from pathlib import Path
import pandas as pd
from langchain.schema import Document

@pytest.fixture
def sample_metadata_df():
    return pd.DataFrame({
        'policy_title': ['Test Policy'],
        'published_status': ['PUBLISHED'],
        'managers': ['Test Manager'],
        'business_owner': ['Test Owner'],
        'review_cycle': ['Annual']
    })

@pytest.fixture
def sample_documents():
    return [
        Document(
            page_content="This is a test policy document content.",
            metadata={
                'policy_title': 'Test Policy',
                'published_status': 'PUBLISHED',
                'business_owner': 'Test Owner'
            }
        )
    ]

@pytest.fixture
def test_persist_dir(tmp_path):
    return str(tmp_path / "test_chromadb")