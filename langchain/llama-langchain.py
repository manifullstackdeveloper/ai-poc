from langchain_community.llms import Ollama

# THIS LINE CAN BE REPLEACE with different AI models...
########################################################################################################
llm = Ollama(model="llama3")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################

# one ask, one response
#print(llm.invoke("What is LLAMA vs OLLAMA?"))

# multi ask and multi response
response = llm.generate(["What is Langchain and Llamaindex?", "What is hugging face?"])

print(response)