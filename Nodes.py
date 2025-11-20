import requests
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal
from State import State
from Summarizer import summarize_messages


class NodeGraph:

    # -------------------------- Node 1 --------------------------
    def ask_question(self, state: State) -> State:
        print("\n-------> ENTERING ask_question:")
        print("What is your question?")

        user_msg = HumanMessage(input())
        return State(messages=[user_msg], summary=state.get("summary", ""))

    # -------------------------- Node 2 --------------------------
    def chatbot(self, state: State) -> State:
        print("\n-------> ENTERING chatbot:")

        summary = state.get("summary", "")
        messages = list(state["messages"])
        user_message = messages[-1].content

        # Build DeepSeek context (SAFE: no f-strings)
        recent_messages_text = ""
        for m in messages:
            role = "User" if m.type == "human" else "Assistant"
            recent_messages_text += "{}: {}\n".format(role, m.content)

        context = (
            "Conversation summary:\n{}\n\n"
            "Recent messages:\n{}\n\n"
            "User question: {}\n\n"
            "Using the summary as memory, answer the user.\n"
        ).format(summary, recent_messages_text, user_message)

        # Call Ollama DeepSeek
        resp = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "deepseek-r1:8b",
                "prompt": context,
                "stream": False,
            },
            timeout=120,
        )

        answer = resp.json().get("response", "").strip()
        print(answer)

        # Add assistant reply to message list
        messages.append(AIMessage(content=answer))

        # ------------------ MEMORY LOGIC ------------------
        if len(messages) > 6:
            print("\n[Memory is long → summarizing...]\n")
            new_summary = summarize_messages(messages, summary)
            summary = new_summary
            messages = messages[-3:]  # keep last 3 messages only

        return State(messages=messages, summary=summary)

    # -------------------------- Node 3 --------------------------
    def ask_another_question(self, state: State) -> State:
        print("\n-------> ENTERING ask_another_question:")
        print("Would you like to ask one more question (yes/no)?")
        user_msg = HumanMessage(input())
        return State(messages=[user_msg], summary=state["summary"])

    # -------------------------- Routing --------------------------
    def routing_function(self, state: State) -> Literal["ask_question", "__end__"]:
        if state["messages"][0].content.lower().strip() == "yes":
            return "ask_question"
        return "__end__"
