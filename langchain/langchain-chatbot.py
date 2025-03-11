from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load local LLaMA model via Ollama
llm = Ollama(model="llama2")  # or "llama3", "mistral", etc.

# Add memory for back-and-forth chatting
memory = ConversationBufferMemory()

# Create conversation chain
chat = ConversationChain(llm=llm, memory=memory, verbose=True)

# Chat loop
print("🤖 Start chatting with your local LLaMA! (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = chat.run(user_input)
    print("LLaMA:", response)
