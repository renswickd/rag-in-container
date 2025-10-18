import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from graphs.policy_graph import build_graph
from common.logger_util import init_logger

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "app" not in st.session_state:
        st.session_state.app = build_graph()
    if "logger" not in st.session_state:
        logger, _ = init_logger(name="policy-ui")
        st.session_state.logger = logger