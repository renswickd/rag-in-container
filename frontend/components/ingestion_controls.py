import streamlit as st
from pathlib import Path
from pipeline.document_tracker import DocumentTracker
from pipeline.ingestion.processor import process_documents
from typing import Optional

def render_ingestion_sidebar(tracker: Optional[DocumentTracker] = None):
    """Render ingestion controls in the sidebar"""
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Status Section
        st.subheader("Status", divider="gray")
        total_docs = len(tracker.get_processed_files()) if tracker else 0
        st.metric("Total Documents", f"{total_docs}")
        
        # Document List
        if tracker and total_docs > 0:
            with st.expander("📑 Processed Documents"):
                for doc_path in tracker.get_processed_files():
                    st.text(Path(doc_path).name)
        
        # Controls Section
        st.subheader("Controls", divider="gray")
        
        # Vector DB Stats
        if st.button("🔄 Refresh Stats"):
            # Add vector DB stats refresh logic here
            pass
        
        # Dangerous Operations
        st.subheader("Maintenance", divider="gray")
        with st.expander("⚠️ Reset"):
            if st.button("Reset Vector DB", type="primary"):
                st.warning("This will delete all embedded documents!")
                if st.button("Confirm Reset"):
                    # Add reset logic here
                    st.success("Vector DB reset successfully")