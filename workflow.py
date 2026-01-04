from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from agents.planner import planner_agent
from agents.sql_writer import sql_writer_agent
from agents.reflection import reflection_agent
from agents.analyzer import analyzer_agent
from tools.sql_executor import run_sql_safe

class SQLAgentState(TypedDict):
    question: str
    plan: Optional[str]
    sql: Optional[str]
    result: Optional[List]
    error: Optional[str]
    retries: int

def planner_node(state):
    return {"plan": planner_agent(state["question"]), "retries": 0}

def writer_node(state):
    return {"sql": sql_writer_agent(state["plan"])}

def executor_node(state):
    res = run_sql_safe(state["sql"])
    if res["success"]:
        return {"result": res["data"], "error": None}
    return {"error": res["error"], "retries": state["retries"] + 1}

def reflection_node(state):
    return {"sql": reflection_agent(state["plan"], state["sql"], state["error"])}

def analyzer_node(state):
    return {"final_answer": analyzer_agent(state["question"], state["result"])}

graph = StateGraph(SQLAgentState)
graph.set_entry_point("planner")
graph.add_node("planner", planner_node)
graph.add_node("writer", writer_node)
graph.add_node("executor", executor_node)
graph.add_node("reflection", reflection_node)
graph.add_node("analyzer", analyzer_node)

graph.add_edge("planner", "writer")
graph.add_edge("writer", "executor")

def route(state):
    if state["error"] is None:
        return "analyzer"
    elif state["retries"] < 2:
        return "reflection"
    return END

graph.add_conditional_edges("executor", route, {
    "analyzer": "analyzer",
    "reflection": "reflection",
    END: END
})

graph.add_edge("reflection", "executor")
graph.add_edge("analyzer", END)

agent = graph.compile()
