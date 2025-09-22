import pytest
from pathlib import Path
from src.components.document_loader import DocumentLoader
import pandas as pd

def test_document_loader_initialization():
    """Test if DocumentLoader initializes correctly"""
    loader = DocumentLoader(
        docs_dir="data/policy_documents/",
        metadata_path="data/pr_metadata.csv"
    )
    assert isinstance(loader.docs_dir, Path)
    assert not loader.metadata_df.empty

def test_load_documents_with_valid_files(tmp_path, sample_metadata_df):
    """Test loading documents with valid PDF files"""
    # Create a more valid PDF file
    pdf_path = tmp_path / "Test Policy.pdf"
    with open(pdf_path, 'wb') as f:
        f.write(b'''%PDF-1.7
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]>>endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000052 00000 n
0000000101 00000 n
trailer<</Size 4/Root 1 0 R>>
startxref
149
%%EOF''')
    
    # Save sample metadata
    metadata_path = tmp_path / "test_metadata.csv"
    sample_metadata_df.to_csv(metadata_path, index=False)
    
    loader = DocumentLoader(str(tmp_path), str(metadata_path))
    documents = loader.load_documents()
    
    assert len(documents) > 0
    assert all(doc.metadata.get('policy_title') for doc in documents)

def test_load_documents_with_no_matching_metadata(tmp_path):
    """Test loading documents with no matching metadata"""
    # Create empty metadata CSV
    metadata_path = tmp_path / "empty_metadata.csv"
    pd.DataFrame(columns=['policy_title']).to_csv(metadata_path, index=False)
    
    loader = DocumentLoader(str(tmp_path), str(metadata_path))
    documents = loader.load_documents()
    
    assert len(documents) == 0

def test_load_documents_with_missing_files():
    """Test loading documents from empty directory"""
    loader = DocumentLoader("nonexistent_dir/", "data/pr_metadata.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_documents()