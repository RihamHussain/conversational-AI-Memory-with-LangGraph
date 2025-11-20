# LangGraph Course Practice Project  
Building AI Workflows with Python, LangGraph, and Google Gemini

This repository contains my implementation and practice code while studying **AI Workflow Orchestration using LangGraph**.  
It includes examples of:

- Defining graph states  
- Creating custom nodes  
- Building flow logic  
- Integrating LLMs (here, Google Gemini FREE API)  
- Running interactive graphs in Python

This project was completed **as part of my learning journey** while taking the LangGraph training section inside the 365 Data Science Pathway.

---

## 🏆 Certificate
I completed the course at **365 Data Science**, and earned the following certificate:

👉 **Course Certificate:**  
https://learn.365datascience.com/certificates/CC-C99648477B/

This repository documents my hands-on implementation of the concepts covered in the course.

---

## 🚀 Project Overview

This project demonstrates:

- How to define a `State` in LangGraph  
- How to create custom graph nodes (e.g., chatbot, question prompt)  
- How to compile and run a LangGraph workflow  
- How to use Google Gemini's FREE API instead of paid OpenAI calls  
- How to integrate an LLM into a graph-based workflow  
- How to run the graph interactively from a Python script  

The project is intentionally simple and focuses on **core concepts** rather than production-level orchestration.

---

## 📁 Folder Structure

```

.
├── main.py               # Entry point to run the graph
├── My_Graph.py           # Graph definition, node linking, and compilation
├── Nodes.py              # Custom node logic (Ask Question, Chatbot)
├── State.py              # Shared TypedDict state object
├── requirements.txt      # Dependencies
├── .env                  # API keys (ignored by Git)
├── .gitignore            # Git ignored files
└── 03-XX *.ipynb         # Jupyter notebooks from the course

````

---

## 🔧 Installation & Setup

### 1️⃣ Create and activate a Conda environment

```bash
conda create --name langgraph_env python=3.11
conda activate langgraph_env
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add your API key to `.env`

Create a file named `.env`:

```
GEMINI_API_KEY=YOUR_KEY_HERE
```

> ❗ Never commit `.env` to GitHub.
> This project includes a `.gitignore` to protect it.

### 4️⃣ Run the project

```bash
python main.py
```

---

## 🧠 How It Works

### **State Definition**

The project uses a TypedDict-based state:

```python
class State(TypedDict):
    messages: Sequence[BaseMessage]
```

### **Nodes**

Two main nodes exist:

* `ask_question`
  Prompts the user for input.

* `chatbot`
  Sends the user input to **Google Gemini FREE API** and returns an AI message.

### **Graph Logic**

`My_Graph.py` builds the LangGraph workflow:

1. Start → `ask_question`
2. Next → `chatbot`
3. End

Everything is managed with:

```python
graph = StateGraph(State)
graph.add_node(...)
graph.add_edge(...)
```

---

## ☁ Google Gemini Integration (Free API)

This project uses:

* `google-generativeai`
* Model: `gemini-1.5-flash-latest`

The Gemini client is configured like this:

```python
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

---

## 🧪 Example Output

```
-------> ENTERING ask_question:
What is your question?
▶ what is AI?

-------> ENTERING chatbot:
Artificial intelligence (AI) refers to...
```

---

## 🛡 Git Ignore Protections

This project includes a `.gitignore` configured to protect:

* `.env`
* Conda artifacts
* VS Code temp files
* Jupyter checkpoints
* Compiled Python files

---

## 📚 Acknowledgment

This project reflects my learning progress while practicing LangGraph concepts from the 365 Data Science platform.
It is not an official reproduction of course materials, but an independent implementation of the techniques covered.

---

## 📬 Contact

If you'd like help, feedback, or collaboration on LangGraph, LLM workflows, or AI engineering, feel free to reach out!

You can find me on:

* LinkedIn: [@riham-a-hussain](https://www.linkedin.com/in/riham-a-hussain/)