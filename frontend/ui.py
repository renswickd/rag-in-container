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

# Sample prompts for quick access
SAMPLE_PROMPTS = {
    "Cloud Access": "What are the requirements for accessing cloud services?",
    "Data Privacy": "What are the key points in the Data Privacy Policy?",
    "Policy Ownership": "Who is responsible for maintaining the Security Policy?",
    "Review Cycles": "How often are policies reviewed?",
    "Incident Response": "What steps should I take during a security incident?",
    "Data Sharing": "What's the process for sharing data with vendors?",
}

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
    
    # Split context into individual document references
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
    # Add user message to history
    current_message = HumanMessage(content=query)
    st.session_state.conversation_history.append(current_message)
    
    # Prepare initial state
    init_state = {
        "messages": st.session_state.conversation_history.copy(),
        "context": "",
        "metadata_text": "",
        "tool_called": False,
    }
    
    # Get response from RAG pipeline
    final_state = st.session_state.app.invoke(
        init_state,
        config={"configurable": {"thread_id": "streamlit-session"}},
    )
    
    # Extract response and context
    msgs = final_state["messages"]
    ai_msgs = [m for m in msgs if isinstance(m, AIMessage)]
    response = ai_msgs[-1].content if ai_msgs else "(no response)"
    
    # Add assistant's response to history
    st.session_state.conversation_history.append(AIMessage(content=response))
    
    # Get context for references
    context = final_state.get("context", "")
    
    return response, context

def main():
    st.set_page_config(
        page_title="Policy Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Title and description
    st.title("📚 Policy Assistant")
    st.markdown("""
    Get instant answers about company policies. Ask questions in natural language or 
    use the sample prompts below.
    """)
    
    # Sidebar with sample prompts
    with st.sidebar:
        st.header("📝 Sample Prompts")
        for title, prompt in SAMPLE_PROMPTS.items():
            if st.button(f"▶️ {title}"):
                st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Main chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about policies..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get response and references
        with st.spinner("Thinking..."):
            response, context = process_query(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
            
            # Display references in expandable section
            with st.expander("📚 View References", expanded=False):
                st.markdown(format_references(context))
            
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()