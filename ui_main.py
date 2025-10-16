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
from pipeline.document_tracker import DocumentTracker

def main():
    st.set_page_config(
        page_title="Policy Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Initialize document tracker
    if "doc_tracker" not in st.session_state:
        st.session_state.doc_tracker = DocumentTracker()
    
    # Load and apply CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Render ingestion controls in sidebar
    render_ingestion_sidebar(st.session_state.doc_tracker)
    
    # Main content area
    with st.container():
        # Render header and chat interface
        render_header()
        render_chat_interface()

if __name__ == "__main__":
    main()