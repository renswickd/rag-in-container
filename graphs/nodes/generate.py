from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from common.config import load_config
from common.llm import get_llm

_cfg = load_config()


def generate_node(state):
    """Compose final answer from retrieved context + optional metadata."""
    llm = get_llm()

    user_query = next((m.content for m in state["messages"] if isinstance(m, HumanMessage)), "")
    meta_block = state.get("metadata_text", "").strip()
    meta_section = f"\n\n[Metadata]\n{meta_block}" if meta_block else ""

    sys = SystemMessage(content=(
        "You are a precise policy assistant. Write a concise, tailored answer.\n"
        "Use the retrieved snippets as supporting evidence and include metadata if provided.\n"
        "If metadata contradicts snippets, trust metadata for status/owner/manager/review cadence.\n"
        "Avoid hallucinations. If unsure, say so and propose next steps.\n"
        f"\n[Retrieved Snippets]\n{state['context']}{meta_section}"
    ))
    human = HumanMessage(content=user_query)

    resp: AIMessage = llm.invoke([sys, human])
    return {"messages": [resp]}
