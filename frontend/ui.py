import os
import streamlit as st
from typing import List
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from graphs.policy_graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage
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

def format_references(context: str) -> str:
    """Format reference documents for display"""
    if not context:
        return "No references available"
    
    references = context.split("\n\n")
    formatted_refs = []
    
    for ref in references:
        if "[Source:" in ref:
            source = ref.split("[Source:")[1].split("]")[0].strip()
            content = ref.split("]")[1].strip()
            formatted_refs.append(f"📄 **{source}**\n{content}")
    
    return "\n\n".join(formatted_refs)

def process_query(query: str) -> tuple[str, str]:
    """Process user query and return response with references"""
    current_message = HumanMessage(content=query)
    st.session_state.conversation_history.append(current_message)
    
    init_state = {
        "messages": st.session_state.conversation_history.copy(),
        "context": "",
        "metadata_text": "",
        "tool_called": False,
    }
    
    final_state = st.session_state.app.invoke(
        init_state,
        config={"configurable": {"thread_id": "streamlit-session"}},
    )
    
    msgs = final_state["messages"]
    ai_msgs = [m for m in msgs if isinstance(m, AIMessage)]
    response = ai_msgs[-1].content if ai_msgs else "(no response)"
    
    st.session_state.conversation_history.append(AIMessage(content=response))
    context = final_state.get("context", "")
    
    return response, context

def main():
    st.set_page_config(
        page_title="Policy Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            color: #1E88E5;
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-container {
            padding: 1rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 5rem;  /* Space for input box */
        }
        .stExpander {
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        /* Fixed input container at bottom */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem 5rem;
            border-top: 1px solid #e0e0e0;
            z-index: 1000;
        }
        /* Adjust main content padding */
        .main-content {
            padding-bottom: 80px;  /* Height of input container */
        }
        /* Style chat messages */
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 class='main-header'>📚 Policy Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    Ask questions about company policies and get instant answers with references to source documents.
    """)
    
    # Main content area with messages
    with st.container():
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "context" in message:
                    with st.expander("📑 View Source Documents", expanded=False):
                        st.markdown(format_references(message["context"]))
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Fixed input container at bottom
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    if prompt := st.chat_input("Ask about policies...", key="chat_input"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get response
        with st.spinner("Searching policies..."):
            response, context = process_query(prompt)
        
        # Add assistant response with context
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "context": context
        })
        
        # Rerun to update UI
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()