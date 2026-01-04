from langchain.prompts import PromptTemplate
from llm import llm
from db.schema import get_schema

planner_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are a senior data analyst.

Database schema:
{schema}

User question:
{question}

Create a step-by-step SQL plan.
"""
)

def planner_agent(question):
    return llm.predict(
        planner_prompt.format(
            schema=get_schema(),
            question=question
        )
    )
