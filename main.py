import os
import sys
from rich.console import Console
from langchain_core.messages import HumanMessage, AIMessage
from graphs.policy_graph import build_graph
from common.logger_util import init_logger

console = Console()
APP = build_graph()

def chat_loop(thread_id: str = "dev-thread-001"):
    console.print("[bold green]Policy Assistant (dev) — type 'exit' to quit[/bold green]")
    
    # Initialize conversation history
    conversation_history = []
    
    while True:
        try:
            user = console.input("[bold cyan]You:[/bold cyan] ").strip()
            if not user:
                continue
            if user.lower() in {"exit", "quit"}:
                break

            # Add user message to history
            current_message = HumanMessage(content=user)
            conversation_history.append(current_message)

            init_state = {
                "messages": conversation_history.copy(),  # Use full history
                "context": "",
                "metadata_text": "",
                "tool_called": False,
            }
            
            final_state = APP.invoke(
                init_state,
                config={"configurable": {"thread_id": thread_id}},
            )
            
            msgs = final_state["messages"]
            ai_msgs = [m for m in msgs if isinstance(m, AIMessage)]
            resp = ai_msgs[-1].content if ai_msgs else "(no response)"

            # Add assistant's response to history
            conversation_history.append(AIMessage(content=resp))
            
            console.print(f"[bold magenta]Assistant:[/bold magenta] {resp}\n")
            
        except KeyboardInterrupt:
            print()
            break

if __name__ == "__main__":
    # tid = sys.argv[1] if len(sys.argv) > 1 else "dev-thread-001"
    # print(f"Thread ID: {tid}")

    session_id = os.getenv("SESSION_ID", None)  # or None
    logger, session_path = init_logger(name="policy", session_id=session_id, level=20)
    
    chat_loop(session_id)
