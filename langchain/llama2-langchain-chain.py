from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

# THIS LINE CAN BE REPLEACE with different AI models...
########################################################################################################
llm = Ollama(model="llama2")
# 1. llm = OpenAI(model_name="...", openai_api_key=API_KEY)
# 2. llm = HuggingFaceHub(repo_id = "..."", huggingfacehub_api_token = API_KEY)
########################################################################################################

# Step 1: Generate a blog title
prompt1 = PromptTemplate.from_template("Write a blog title about {topic}")
chain1 = prompt1 | llm

# Step 2: Write a blog post from the title
prompt2 = PromptTemplate.from_template("Write a short blog post using this title: {input}")
chain2 = prompt2 | llm

# Chain them together
final_chain = chain1 | chain2

# Run the full pipeline
output = final_chain.invoke({"topic": "Diffusion Models"})
print(output)
