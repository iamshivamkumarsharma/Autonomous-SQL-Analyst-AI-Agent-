from langchain.prompts import PromptTemplate
from llm import llm

analyzer_prompt = PromptTemplate(
    input_variables=["question", "result"],
    template="""
Explain SQL results in business language.
"""
)

def analyzer_agent(question, result):
    return llm.predict(
        analyzer_prompt.format(
            question=question,
            result=result
        )
    )
