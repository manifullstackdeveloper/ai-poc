O_API_KEY = ""

from langchain.llms import OpenAI

llm = OpenAI(model_name="....", openai_api_key=O_API_KEY)

print(llm("Tell me  about LLM?"))


H_API_KEY ="..."

from langchain import HuggingFaceHub

llm = HuggingFaceHub(repo_id = "....", huggingfacehub_api_token = H_API_KEY)

print(llm("Tell me about LLM?"))