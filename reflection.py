from langchain.prompts import PromptTemplate
from llm import llm
from db.schema import get_schema

reflection_prompt = PromptTemplate(
    input_variables=["schema", "plan", "sql", "error"],
    template="""
Fix the SQL query based on the error.
Only output corrected SQL.
"""
)

def reflection_agent(plan, sql, error):
    return llm.predict(
        reflection_prompt.format(
            schema=get_schema(),
            plan=plan,
            sql=sql,
            error=error
        )
    )
