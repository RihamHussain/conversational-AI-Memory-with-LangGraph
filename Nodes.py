import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from typing import Literal
from State import State
class NodeGraph():
    # Define the Nodes
    # -------------------------- Node 1 --------------------------
    def ask_question(self, state: State) -> State:
        
        print(f"\n-------> ENTERING ask_question:")
        
        print("What is your question?")
        
        return State(messages = [HumanMessage(input())])

    # -------------------------- Node 2 --------------------------
    def chatbot(self, state: State) -> State:
        print("\n-------> ENTERING chatbot:")
        load_dotenv()

        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-flash-latest")

        prompt = state["messages"][0].content
        response = model.generate_content(prompt)

        print(response.text)

        from langchain_core.messages import AIMessage
        return State(messages=[AIMessage(content=response.text)])



    # -------------------------- Node 3 --------------------------

    def ask_another_question(self, state: State) -> State:
        
        print(f"\n-------> ENTERING ask_another_question:")
        
        print("Would you like to ask one more question (yes/no)?")
        
        return State(messages = [HumanMessage(input())])

    # Define Routing Function:

    def routing_function(self, state: State) -> Literal["ask_question", "__end__"]:
        
        if state["messages"][0].content == "yes":
            return "ask_question"
        else:
            return "__end__"
        
