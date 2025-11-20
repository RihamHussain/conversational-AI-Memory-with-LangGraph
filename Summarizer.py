import requests

def summarize_messages(messages, previous_summary=""):
    text = ""

    # Convert LangChain messages to readable text
    for msg in messages:
        role = "User" if msg.type == "human" else "Assistant"
        text += f"{role}: {msg.content}\n"

    prompt = (
        "You are a memory-summarizing assistant.\n"
        "Summarize the following conversation in a concise, factual way.\n"
        "Do NOT hallucinate or add unrelated information.\n\n"
        "Previous summary:\n"
        "{}\n\n"
        "Conversation:\n"
        "{}\n\n"
        "Write the improved summary:\n"
    ).format(previous_summary, text)

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "deepseek-r1:8b", "prompt": prompt, "stream": False},
        timeout=120,
    )

    data = response.json()
    return (data.get("response") or "").strip()
