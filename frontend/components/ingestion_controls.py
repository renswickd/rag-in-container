import streamlit as st
from pathlib import Path
from pipeline.utils.document_tracker import DocumentTracker
from pipeline.storage.vector_store import VectorStore
from pipeline.storage.document_store import DocumentStore
from pipeline.ingestion.loader import DocumentLoader
from pipeline.ingestion.processor import DocumentProcessor
from typing import Optional

def render_ingestion_sidebar(
    tracker: DocumentTracker,
    vector_store: VectorStore,
    doc_store: DocumentStore
):
    """Render ingestion controls in the sidebar"""
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Status Section
        st.subheader("Status", divider="gray")
        stats = vector_store.get_stats()
        st.metric("Total Documents", f"{stats['total_documents']}")
        
        # Document List
        processed_files = tracker.get_processed_files()
        if processed_files:
            with st.expander("📑 Processed Documents"):
                for doc_path in processed_files:
                    st.text(Path(doc_path).name)
        
        # Vector DB Stats
        if st.button("🔄 Refresh Stats"):
            st.experimental_rerun()
        
        # Dangerous Operations
        st.subheader("Maintenance", divider="gray")
        with st.expander("⚠️ Reset"):
            if st.button("Reset Vector DB", type="primary"):
                st.warning("This will delete all embedded documents!")
                if st.button("Confirm Reset"):
                    vector_store.reset()
                    st.success("Vector DB reset successfully")
                    st.experimental_rerun()