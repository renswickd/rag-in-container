import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import streamlit as st
from frontend.components.styles import load_css
from frontend.components.header import render_header
from frontend.components.chat_interface import render_chat_interface
from frontend.utils.session_manager import initialize_session_state

def main():
    st.set_page_config(
        page_title="Policy Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Load and apply CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Render components
    render_header()
    render_chat_interface()

if __name__ == "__main__":
    main()