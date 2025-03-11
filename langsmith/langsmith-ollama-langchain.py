from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langsmith import traceable

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_PROJECT"] = "ollama-test"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Load local model using Ollama
########################################################################################################
llm = Ollama(model="llama2")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################

# Build prompt
prompt = PromptTemplate.from_template("{question}?")

# Define the chain
chain = prompt | llm

# Trace the call using LangSmith
@traceable
def ask_question(question):
    return chain.invoke(question)


# running the QA chain in a loop until the user types "exit"
while True:
    question = input("Question: ")
    if question.lower() == "exit":
        break
    answer =  ask_question(question)

    print(f"\nAnswer: {answer}\n")