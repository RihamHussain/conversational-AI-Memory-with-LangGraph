from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from State import State
from Nodes import NodeGraph


class Graph(StateGraph):
    def __init__(self):
        # Initialize the StateGraph with our State TypedDict
        
        super().__init__(State)

        self.node_graph = NodeGraph()
        self.compiled_graph = None

        # Short-term memory: LangGraph's in-memory checkpointer
        # This stores checkpoints (state snapshots) in RAM during the run
        self.checkpointer = InMemorySaver()

    def build_graph(self):
        # Define nodes
        self.add_node("ask_question", self.node_graph.ask_question)
        self.add_node("chatbot", self.node_graph.chatbot)
        self.add_node("ask_another_question", self.node_graph.ask_another_question)

        # Define edges
        self.add_edge(START, "ask_question")
        self.add_edge("ask_question", "chatbot")
        self.add_edge("chatbot", "ask_another_question")

        # Conditional routing from "ask_another_question"
        self.add_conditional_edges(
            source="ask_another_question",
            path=self.node_graph.routing_function,
        )

    def run(self):
        # Build and compile the graph with a checkpointer
        self.build_graph()
        self.compiled_graph = self.compile(checkpointer=self.checkpointer)
        return self.compiled_graph

    
    def test_graph(self):
        """
        Runs one conversation and prints the latest StateSnapshot.
        """

        if self.compiled_graph is None:
            raise RuntimeError("Graph not compiled. Call run() first.")

        # LangGraph requires a thread_id when using a checkpointer.
        # This identifies the conversation thread in the checkpoint store.
        config = {"configurable": {"thread_id": "demo-thread"}}

        # Our State has: messages, summary
        initial_state = State(messages=[], summary="")

        # Run the graph once (ask → chatbot → ask_another_question → route)
        final_state = self.compiled_graph.invoke(initial_state, config=config)

        # --- StateSnapshot: latest checkpoint for this thread ---
        # This returns a StateSnapshot object (values, next, metadata, etc.) 
        snapshot = self.compiled_graph.get_state(config)

        print("\n--- Latest StateSnapshot (from checkpointer) ---")
        # snapshot.values contains the current state (our State dict)
        print("State values:", snapshot.values)
        print("Next nodes:", snapshot.next)
        print("Created at:", snapshot.created_at)
        print("-----------------------------------------------\n")

        return final_state

def build_long_term_graph():
    # Create persistent SQLite-backed memory
        checkpointer = SqliteSaver.from_file("long_memory.db")

        graph = StateGraph(State)
        node_graph = NodeGraph()

        # Register nodes
        graph.add_node("ask_question", node_graph.ask_question)
        graph.add_node("chatbot", node_graph.chatbot)
        graph.add_node("ask_another_question", node_graph.ask_another_question)

        # Connect nodes
        graph.add_edge(START, "ask_question")
        graph.add_edge("ask_question", "chatbot")
        graph.add_edge("chatbot", "ask_another_question")
        graph.add_conditional_edges(
            source="ask_another_question",
            path=node_graph.routing_function,
        )

        # Compile with persistent checkpointer
        return graph.compile(checkpointer=checkpointer)