import requests
from langchain_core.messages import HumanMessage, AIMessage
from typing import Literal
from State import State
from Summarizer import summarize_messages


class NodeGraph:

    # -------------------------- NODE 1 --------------------------
    def ask_question(self, state: State) -> State:
        print("\n-------> ENTERING ask_question:")
        print("What is your question?")

        user_input = input()

        # Append user message to history
        messages = list(state.get("messages", []))
        messages.append(HumanMessage(content=user_input))

        return State(messages=messages, summary=state.get("summary", ""))

    # -------------------------- NODE 2 --------------------------
    def chatbot(self, state: State) -> State:
        print("\n-------> ENTERING chatbot:")

        messages = list(state["messages"])
        summary = state.get("summary", "")

        recent_text = ""
        for m in messages:
            role = "User" if m.type == "human" else "Assistant"
            recent_text += "{}: {}\n".format(role, m.content)

        context = (
            "Conversation summary:\n{}\n\n"
            "Recent conversation:\n{}\n\n"
            "Using the summary as memory, answer the last user question.\n"
        ).format(summary, recent_text)

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "deepseek-r1:8b", "prompt": context, "stream": False},
            timeout=120,
        )

        answer = response.json().get("response", "").strip()
        print(answer)

        # Append AI message to history
        messages.append(AIMessage(content=answer))

        # ---- APPLY MEMORY / SUMMARY LOGIC ----
        if len(messages) > 6:
            print("\n[Summarizing memory...]\n")
            new_summary = summarize_messages(messages, summary)
            summary = new_summary
            messages = messages[-3:]  # keep last 3 messages after summarizing

        return State(messages=messages, summary=summary)

    # -------------------------- NODE 3 --------------------------
    def ask_another_question(self, state: State) -> State:
        print("\n-------> ENTERING ask_another_question:")
        print("Would you like to ask one more question (yes/no)?")

        answer = input()
        messages = list(state["messages"])
        messages.append(HumanMessage(content=answer))

        return State(messages=messages, summary=state["summary"])

    # -------------------------- ROUTER --------------------------
    def routing_function(self, state: State) -> Literal["ask_question", "__end__"]:
        last_msg = state["messages"][-1].content.lower().strip()
        return "ask_question" if last_msg == "yes" else "__end__"
