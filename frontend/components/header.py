import streamlit as st

def render_header():
    """Render the application header"""
    st.markdown("<h1 class='main-header'>📚 Policy Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    Ask questions about company policies and get instant answers with references to source documents.
    """)