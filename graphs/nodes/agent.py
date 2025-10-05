from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from tools.metadata_tool import lookup_policy_metadata
from common.config import load_config
from common.llm import get_llm

_cfg = load_config()
_TOOLS = [lookup_policy_metadata]

def agent_node(state):
    """Run ReAct agent; store tool output if called."""
    llm = get_llm()
    agent = create_react_agent(llm, _TOOLS)

    sys = SystemMessage(content=(
        "You are a helpful policy assistant. Use retrieved context to answer.\n"
        "If the user asks about policy status, managers, business owner, or review cycle, "
        "call the tool `lookup_policy_metadata` with a short query (typically a policy title).\n"
        "Do not fabricate metadata. Keep answers concise.\n\n"
        f"Retrieved context:\n{state['context']}\n"
    ))
    messages = [sys] + state["messages"]

    result = agent.invoke({"messages": messages})
    new_messages = result["messages"]

    tool_called = False
    metadata_text = state.get("metadata_text", "")
    for msg in reversed(new_messages):
        if isinstance(msg, ToolMessage):
            tool_called = True
            metadata_text = msg.content
            # print("[NOTIFY] Metadata tool was invoked by the agent.")
            break

    return {
        "messages": new_messages,
        "metadata_text": metadata_text,
        "tool_called": tool_called or state.get("tool_called", False),
    }
