import operator
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage

from graphs.nodes.retrieve import retrieve_node
from graphs.nodes.agent import agent_node
from graphs.nodes.generate import generate_node

class GraphState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    context: str
    metadata_text: str
    tool_called: bool

def build_graph():
    g = StateGraph(GraphState)
    g.add_node("retrieve", retrieve_node)
    g.add_node("agent", agent_node)
    g.add_node("generate", generate_node)

    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "agent")
    g.add_edge("agent", "generate")
    g.add_edge("generate", END)

    memory = MemorySaver()
    return g.compile(checkpointer=memory)
