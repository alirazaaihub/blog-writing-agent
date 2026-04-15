# ✍️ Blog Writing Agent

An autonomous AI agent that writes full, well-structured blog posts on any topic — and if the topic needs current information, it **searches the web automatically** before writing.

---

## 🚀 What It Does

Give it any topic. It thinks, plans, researches (if needed), and writes a complete blog post — saved as a Markdown file.

- Decides on its own whether the topic needs web research
- Plans the blog structure with sections and bullet points
- Writes all sections **in parallel** using LangGraph's fanout pattern
- Saves the final blog as a `.md` file automatically

**Example:**
> Input: `"Latest trends in Agentic AI 2025"`  
> → Agent decides: needs web research  
> → Searches DuckDuckGo for 2–5 queries  
> → Plans 4–6 blog sections  
> → Writes all sections simultaneously  
> → Saves `Latest_trends_in_Agentic_AI_2025.md`

---

## ✨ Features

- 🔀 **Smart Router** — decides if topic needs live web research or not
- 🌐 **Web Research** — fetches real-time data via DuckDuckGo automatically
- 🗂️ **AI Planner** — creates a structured outline with sections and bullet points
- ⚡ **Parallel Writing** — all blog sections written simultaneously using LangGraph `Send`
- 🔗 **Source Linking** — includes clickable `[source](url)` links in blog content
- 💾 **Auto Save** — final blog saved as a `.md` file automatically
- 🧠 **Structured Outputs** — uses Pydantic models for reliable LLM outputs

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | LangGraph |
| LLM | Groq (llama-3.1-8b-instant) |
| Web Search | DuckDuckGo (via LangChain) |
| Structured Output | Pydantic + LangChain |
| Output Format | Markdown (.md) |
| Language | Python 3.11+ |

---

## ⚙️ How It Works

```
User gives a Topic
        ↓
┌──────────────────┐
│     Router       │  → Needs web research? Yes / No
└────────┬─────────┘
         ↓
┌──────────────────┐         ┌──────────────────┐
│  Research Node   │ (if yes)│   Skip Research  │ (if no)
│  DuckDuckGo      │         └────────┬─────────┘
└────────┬─────────┘                  │
         └──────────┬─────────────────┘
                    ↓
         ┌──────────────────┐
         │  Planner Node    │  → Creates 4–6 section outline
         └────────┬─────────┘
                  ↓
     ┌────────────────────────┐
     │   Fanout (Parallel)    │  → Sends each section to a separate worker
     └──┬──────┬──────┬───────┘
        ↓      ↓      ↓
    Worker  Worker  Worker   → Each writes one section in Markdown
        ↓      ↓      ↓
     ┌────────────────────────┐
     │    Reducer Node        │  → Sorts + merges all sections
     └────────────────────────┘
                  ↓
        Final Blog (.md file)
```

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/alirazaaihub/blog-writing-agent.git
cd blog-writing-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Open `agent.py` and replace the API key:

```python
GROQ_API_KEY = "your_groq_api_key_here"
```

Or better, use a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

And load it with:

```python
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

Get your free Groq API key at: https://console.groq.com

---

## ▶️ Usage

**Option 1 — Edit topic in code:**

```python
# At the bottom of agent.py
run("Your blog topic here")
```

Then run:

```bash
python agent.py
```

**Option 2 — Import and call:**

```python
from agent import run

run("Top 10 Python libraries for AI in 2025")
```

**Output:**

```
Blog saved as: Top_10_Python_libraries_for_AI_in_2025.md
```

The `.md` file will be saved in your project root directory.

---

## 📁 Project Structure

```
blog-writing-agent/
│
├── agent.py              # Full LangGraph blog writing agent
├── requirements.txt      # Project dependencies
├── .env                  # API keys (do not commit)
├── .env.example          # Template for environment variables
└── README.md
```

---

## 📋 Dependencies

```
langchain
langchain-groq
langchain-community
langgraph
pydantic
duckduckgo-search
python-dotenv
```

Install all:

```bash
pip install langchain langchain-groq langchain-community langgraph pydantic duckduckgo-search python-dotenv
```

---

## 🧩 Key Concepts Used

| Concept | How It's Used |
|--------|----------------|
| **LangGraph StateGraph** | Controls full agent flow from router to final output |
| **Smart Router** | LLM decides if topic needs web research using structured output |
| **DuckDuckGo Search** | Fetches real-time web results for research-needed topics |
| **AI Planner** | LLM generates structured blog outline using Pydantic model |
| **Fanout Pattern** | `Send()` API writes all sections in parallel — faster output |
| **Reducer Node** | Collects parallel outputs, sorts by section ID, merges into final blog |
| **Structured Outputs** | Pydantic `BaseModel` ensures reliable, parseable LLM responses |
| **Markdown Output** | Final blog saved as `.md` file with clickable source links |

---

## 📝 Sample Output Structure

```markdown
# Latest Trends in Agentic AI 2025

## Introduction
...

## What Are AI Agents?
...

## Top Frameworks in 2025
...

## Real-World Use Cases
...

## Challenges and Limitations
...

## Conclusion
...
```

---

## 🙋 About

Built by **Ali raza** — an 18-year-old self-taught AI developer from Pakistan.  
This is part of my Agentic AI portfolio built using LangChain, LangGraph, and Groq.

📌 [LinkedIn](https://www.linkedin.com/in/ali-raza-7124a0403/) • [GitHub](https://github.com/alirazaaihub)

---

## 📄 License

MIT License — feel free to use and modify.
