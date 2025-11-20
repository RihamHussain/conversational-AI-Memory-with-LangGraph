import requests
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal
from State import State


class NodeGraph:
    # -------------------------- Node 1 --------------------------
    def ask_question(self, state: State) -> State:
        print(f"\n-------> ENTERING ask_question:")
        print("What is your question?")

        return State(messages=[HumanMessage(input())])

    # -------------------------- Node 2 --------------------------
    def chatbot(self, state: State) -> State:
        print("\n-------> ENTERING chatbot:")

        # Take the last user message as the prompt
        prompt = state["messages"][0].content

        # Call local Ollama server with DeepSeek-R1
        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "deepseek-r1:8b",
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            # Ollama /api/generate returns the text in the "response" field
            answer = (data.get("response") or "").strip()

            if not answer:
                answer = "[Ollama returned an empty response.]"

        except Exception as e:
            answer = f"[Error talking to Ollama on 127.0.0.1:11434 with model 'deepseek-r1:8b': {e}]"

        print(answer)
        return State(messages=[AIMessage(content=answer)])

    # -------------------------- Node 3 --------------------------
    def ask_another_question(self, state: State) -> State:
        print(f"\n-------> ENTERING ask_another_question:")
        print("Would you like to ask one more question (yes/no)?")

        return State(messages=[HumanMessage(input())])

    # Define Routing Function:
    def routing_function(self, state: State) -> Literal["ask_question", "__end__"]:
        if state["messages"][0].content.lower().strip() == "yes":
            return "ask_question"
        else:
            return "__end__"
