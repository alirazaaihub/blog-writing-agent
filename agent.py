from pathlib import Path
from typing import TypedDict, List
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from pydantic import BaseModel



# 1) Schemas (Structured Output)

class RouterOutput(BaseModel):
    needs_research: bool
    queries: List[str]


class Task(BaseModel):
    id: int
    title: str
    bullets: List[str]


class Plan(BaseModel):
    tasks: List[Task]



# 2) State

from typing import TypedDict, List, Annotated
import operator

class State(TypedDict):
    topic: str
    needs_research: bool
    queries: List[str]
    evidence: List[dict]
    tasks: List[dict]
    sections: Annotated[List[tuple[int, str]], operator.add]  
    final: str


# 3) LLM

GROQ_API_KEY = "Enter api key"


llm = ChatGroq(groq_api_key=GROQ_API_KEY,
               model="llama-3.1-8b-instant")

router_llm = llm.with_structured_output(RouterOutput)
planner_llm = llm.with_structured_output(Plan)



# 4) Router

def router_node(state: State):
    decision = router_llm.invoke(
        f"""
Decide if this topic needs web research.

Topic: {state['topic']}

- If latest/trending → needs_research = true
- Otherwise false
- Generate 2–5 search queries if needed
"""
    )

    return {
        "needs_research": decision.needs_research,
        "queries": decision.queries,
    }


def route_next(state: State):
    return "research" if state["needs_research"] else "planner"



# 5) Research

def research_node(state: State):
    tool = DuckDuckGoSearchAPIWrapper()

    evidence = []

    for q in state["queries"]:
        results = tool.results(q, max_results=5)  

        for r in results:
            if r.get("link"):
                evidence.append({
                    "title": r.get("title"),
                    "url": r.get("link"),   
                    "snippet": r.get("snippet"),
                })

    return {"evidence": evidence}



# 6) Planner

def planner_node(state: State):
    plan = planner_llm.invoke(
        f"""
Create a blog outline.

Topic: {state['topic']}

- Create 4–6 sections
- Each section must have:
  - id
  - title
  - 2–4 bullets
"""
    )

    return {
        "tasks": [t.model_dump() for t in plan.tasks]
    }


# 7) Fanout (Dynamic Workers)

def fanout(state: State):
    return [
        Send("worker", {
            "task": t,
            "topic": state["topic"],
            "evidence": state["evidence"]
        })
        for t in state["tasks"]
    ]



# 8) Worker

def worker_node(payload: dict):
    task = payload["task"]

    evidence_text = "\n".join(
        f"{e['title']} ({e['url']})"
        for e in payload["evidence"][:5]
    )

    prompt = f"""
Write a detailed blog section in Markdown.

## {task['title']}

Topic: {payload['topic']}

Cover:
{task['bullets']}

Use sources where relevant:
{evidence_text}

Rules:
- Add links like [source](url)
- Clear explanation
"""

    content = llm.invoke([HumanMessage(content=prompt)]).content

    return {"sections": [(task["id"], content)]}



# 9) Reducer

def reducer_node(state: State):
    sections = sorted(state["sections"], key=lambda x: x[0])

    body = "\n\n".join([s for _, s in sections])

    final = f"# {state['topic']}\n\n{body}"

    filename = f"{state['topic'].replace(' ', '_')}.md"
    Path(filename).write_text(final, encoding="utf-8")

    print(f"\nBlog saved as: {filename}")

    return {"final": final}



# 10) Graph

g = StateGraph(State)

g.add_node("router", router_node)
g.add_node("research", research_node)
g.add_node("planner", planner_node)
g.add_node("worker", worker_node)
g.add_node("reducer", reducer_node)

g.add_edge(START, "router")

g.add_conditional_edges(
    "router",
    route_next,
    {
        "research": "research",
        "planner": "planner"
    }
)

g.add_edge("research", "planner")

g.add_conditional_edges("planner", fanout, ["worker"])

g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()



# 11) Runner

def run(topic: str):
    return app.invoke({
        "topic": topic,
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "tasks": [],
        "sections": [],
        "final": ""
    })



# 12) Run

if __name__ == "__main__":
    run("enter your topic ")
