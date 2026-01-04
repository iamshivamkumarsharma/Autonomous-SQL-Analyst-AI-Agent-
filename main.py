from graph.workflow import agent

response = agent.invoke({
    "question": "Show total revenue by product category",
    "plan": None,
    "sql": None,
    "result": None,
    "error": None,
    "retries": 0
})

print(response.get("final_answer"))
