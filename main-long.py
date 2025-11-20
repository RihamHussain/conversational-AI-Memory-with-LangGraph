from langgraph.graph import StateGraph, START
from State import State
from Nodes import NodeGraph
from My_Graph import build_long_term_graph




if __name__ == "__main__":
    compiled_graph = build_long_term_graph()

    # Every long-term conversation must use a thread_id
    config = {"configurable": {"thread_id": "long-term-session-1"}}

    # Start the conversation. If memory exists, it will load automatically
    print("\n🔵 Starting long-term memory chatbot...")
    final_state = compiled_graph.invoke(State(messages=[], summary=""), config=config)

    print("\n🟢 Conversation finished and saved permanently to long_memory.db\n")
