from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from common.config import load_config
from common.llm import get_llm

_cfg = load_config()


def generate_node(state):
    """Compose final answer from retrieved context + optional metadata."""
    print("----- NODE CALL: generate_node -----")
    llm = get_llm()

    # Get conversation history
    messages = state["messages"]
    user_messages = [m for m in messages if isinstance(m, HumanMessage)]
    current_query = user_messages[-1].content if user_messages else ""
    
    # Get previous context if any
    previous_context = ""
    if len(user_messages) > 1:
        previous_responses = [m for m in messages if isinstance(m, AIMessage)]
        if previous_responses:
            previous_context = "\n".join([r.content for r in previous_responses[:-1]])

    meta_block = state.get("metadata_text", "").strip()
    meta_section = f"\n\n[Metadata]\n{meta_block}" if meta_block else ""
    
    context_block = state.get("context", "").strip()

    sys = SystemMessage(content=(
        "You are a precise policy assistant. Write a concise, tailored answer.\n"
        "Use the retrieved snippets as supporting evidence and include metadata if provided.\n"
        "If metadata contradicts snippets, trust metadata for status/owner/manager/review cadence.\n"
        "Consider previous conversation context when answering follow-up questions.\n"
        "Avoid hallucinations. If unsure, say so and propose next steps.\n"
        f"\n[Previous Context]\n{previous_context}\n"
        f"\n[Retrieved Snippets]\n{context_block}{meta_section}"
    ))
    
    human = HumanMessage(content=current_query)
    resp: AIMessage = llm.invoke([sys, human])
    
    # Format response with markdown
    response_text = resp.content
    if not context_block and not meta_block:
        response_text += "\n\n*Note: No relevant information was found in the policy documents.*"
        
    return {"messages": [AIMessage(content=response_text)]}
