from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from langchain_core.messages import convert_to_openai_messages

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_PROJECT"] = "ollama-test"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Connect to the LangSmith client

client = Client()

oai_client = OpenAI(
    api_key= ""
)
# Define the prompt

prompt = ChatPromptTemplate([
("system", "You are a helpful chatbot."),
("user", "{question}"),
])

# Push the prompt

client.pull_prompt("my-prompt")


formatted_prompt = prompt.invoke({"question": "What is the color of the sky?"})

print(formatted_prompt)

response = oai_client.chat.completions.create(
model="gpt-4o",
messages=convert_to_openai_messages(formatted_prompt.messages),
)