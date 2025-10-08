from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from tools.metadata_tool import lookup_policy_metadata
from common.config import load_config
from common.llm import get_llm

_TOOLS = [lookup_policy_metadata]

def agent_node(state):
    """Run ReAct agent; store tool output if called."""
    print("----- NODE CALL: agent_node -----")
    llm = get_llm()
    agent = create_react_agent(llm, _TOOLS)

    # Get conversation history
    messages = state["messages"]
    user_messages = [m for m in messages if isinstance(m, HumanMessage)]
    current_query = user_messages[-1].content if user_messages else ""

    sys = SystemMessage(content=(
        "You are a helpful policy assistant. Use retrieved context to answer.\n"
        "For questions about policy ownership, status, managers, or review cycle, "
        "use the lookup_policy_metadata tool.\n"
        "Consider the conversation history for follow-up questions about specific policies.\n"
        "Do not fabricate metadata. Keep answers concise and accurate.\n\n"
        f"Retrieved context:\n{state['context']}\n"
    ))
    
    agent_messages = [sys] + state["messages"]
    result = agent.invoke({"messages": agent_messages})
    new_messages = result["messages"]
    # print(f"[DEBUG] - new_messages: {new_messages}")

    tool_called = False
    metadata_text = state.get("metadata_text", "")
    for msg in reversed(new_messages):
        if isinstance(msg, ToolMessage):
            tool_called = True
            metadata_text = msg.content
            break

    return {
        "messages": new_messages,
        "metadata_text": metadata_text,
        "tool_called": tool_called or state.get("tool_called", False),
    }
