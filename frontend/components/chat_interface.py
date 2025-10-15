import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from frontend.utils.reference_formatter import format_references

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

def render_chat_interface():
    """Render the chat interface with messages and input"""
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