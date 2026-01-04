from langchain.prompts import PromptTemplate
from llm import llm
from db.schema import get_schema

sql_writer_prompt = PromptTemplate(
    input_variables=["schema", "plan"],
    template="""
Write a SQL SELECT query based on the plan.
Only output SQL.
"""
)

def sql_writer_agent(plan):
    return llm.predict(
        sql_writer_prompt.format(
            schema=get_schema(),
            plan=plan
        )
    )
