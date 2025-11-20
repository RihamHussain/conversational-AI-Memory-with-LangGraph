import requests
def test_ollama_deepseek():
    """
    Simple connectivity test for local Ollama + DeepSeek-R1:8b.
    """
    print("Testing connection to Ollama (DeepSeek-R1:8b)...")

    try:
        resp = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "deepseek-r1:8b",
                "prompt": "Hello from the LangGraph test script. Please reply very briefly.",
                "stream": False,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        answer = (data.get("response") or "").strip()
        print("\n--- SUCCESS ---")
        print("Ollama is running and DeepSeek-R1 responded with:\n")
        print(answer)
        print("\n-----------------\n")
    except Exception as e:
        print("\n--- ERROR ---")
        print("Failed to connect to Ollama / DeepSeek-R1.")
        print(f"Details: {e}")
        print("-----------------\n")


if __name__ == "__main__":
    test_ollama_deepseek()
