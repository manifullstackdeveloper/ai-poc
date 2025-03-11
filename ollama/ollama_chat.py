import streamlit as st
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Set page config
st.set_page_config(page_title="💬 Chat with LLaMA (Ollama)", layout="wide")

# Title
st.title("🦙 Chat with Local LLaMA using Ollama")

# Session state to store conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ConversationBufferMemory()
    st.session_state.chat_chain = ConversationChain(
        llm=Ollama(model="llama2"),  # Replace with 'llama3' or others
        memory=st.session_state.chat_history,
        verbose=False
    )

# Input box
user_input = st.chat_input("Say something to LLaMA...")

# Process input and display response
if user_input:
    with st.spinner("Thinking..."):
        response = st.session_state.chat_chain.run(user_input)

    # Show chat messages
    st.chat_message("user").write(user_input)
    st.chat_message("ai").write(response)
