from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# THIS LINE CAN BE REPLEACE with different AI models...
########################################################################################################
llm = Ollama(model="llama3")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################


# Define a simple LangChain prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are an expert AI. Answer the following question: {question}"
)

# Create LLM Chain
chain = LLMChain(llm=llm, prompt=prompt)


# Ask a question
response = chain.run("What are the different AI models?")

print(response)