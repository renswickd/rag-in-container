import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import streamlit as st
from frontend.components.styles import load_css
from frontend.components.header import render_header
from frontend.components.chat_interface import render_chat_interface
from frontend.components.ingestion_controls import render_ingestion_sidebar
from frontend.utils.session_manager import initialize_session_state
from pipeline.utils.document_tracker import DocumentTracker
from pipeline.storage.document_store import DocumentStore
from pipeline.storage.vector_store import VectorStore

def main():
    st.set_page_config(
        page_title="Policy Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Initialize storage components if not in session state
    if "doc_tracker" not in st.session_state:
        st.session_state.doc_tracker = DocumentTracker()
    
    if "doc_store" not in st.session_state:
        archive_path = Path("data/archived_docs")
        st.session_state.doc_store = DocumentStore(archive_path)
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = VectorStore(
            persist_directory="chroma_db",
            collection_name="docs"
        )
    
    # Load and apply CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Render ingestion controls in sidebar
    render_ingestion_sidebar(
        tracker=st.session_state.doc_tracker,
        vector_store=st.session_state.vector_store,
        doc_store=st.session_state.doc_store
    )
    
    # Main content area
    with st.container():
        # Render header and chat interface
        render_header()
        render_chat_interface()

if __name__ == "__main__":
    main()