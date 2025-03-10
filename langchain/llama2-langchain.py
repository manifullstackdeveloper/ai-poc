# Install dependencies if not already
# pip install langchain ollama

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

# 1. Load the model using Ollama
# THIS LINE CAN BE REPLEACE with different AI models...
########################################################################################################
llm = Ollama(model="llama2")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################
# Replace with 'llama3' once available via `ollama pull llama3`

# 2. Define a prompt template
prompt1 = PromptTemplate.from_template("what is the famouse dish in {location}.")

# 3. Create the chain using the modern LangChain pipe style
chain1 = prompt1 | llm

#final_answer = chain1.invoke({"location": "Madurai, TamilNadu"})

#print(final_answer)

prompt2 = PromptTemplate.from_template("Then Provide recipes for top 2 items: \n  {dish}.")

# 3. Create the chain using the modern LangChain pipe style
chain2 = prompt2 | llm


final_chain = chain1 | chain2

result = final_chain.invoke({"location": "Madurai, TamilNadu"})

print(result)