import os
from langgraph.graph import START, StateGraph
from State import State
from Nodes import NodeGraph

class Graph(StateGraph):
    def __init__(self):
        super().__init__(State)    # <--- IMPORTANT
        self.node_graph = NodeGraph()
        self.compiled_graph = None

    def build_graph(self):
        self.add_node("ask_question", self.node_graph.ask_question)
        self.add_node("chatbot", self.node_graph.chatbot)
        self.add_node("ask_another_question", self.node_graph.ask_another_question)

        self.add_edge(START, "ask_question")
        self.add_edge("ask_question", "chatbot")
        self.add_edge("chatbot", "ask_another_question")
        self.add_conditional_edges(source = "ask_another_question", 
                                    path = self.node_graph.routing_function)
    
    def run(self):
        self.build_graph()
        self.compiled_graph = self.compile()
        return self.compiled_graph
    
    def test_graph(self):
        self.compiled_graph.invoke(State(messages = []))