import streamlit as st
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
import tempfile
import os

st.set_page_config(page_title="📄 PDF Chatbot (Ollama)", layout="wide")
st.title("📚 Chat with a PDF using Local LLM (Ollama)")

# Step 1: Select your local model
model_choice = st.selectbox("Choose your local model", ["llama2", "mistral", "gemma"])
llm = Ollama(model=model_choice)

# Step 2: Upload a PDF file
uploaded_pdf = st.file_uploader("📄 Upload a PDF file", type=["pdf"])

retriever = None

if uploaded_pdf:
    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    # Load and split PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    # Embeddings + Vector DB
    embeddings = OllamaEmbeddings(model=model_choice)
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

# Step 3: Ask a question
user_input = st.chat_input("Ask something from the PDF...")

if user_input:
    if not retriever:
        st.warning("⚠️ Please upload a PDF first.")
    else:
        prompt = PromptTemplate.from_template("""
        Use the following context to answer the question.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )

        with st.spinner("Reading PDF and answering..."):
            answer = qa_chain.run(user_input)

        st.chat_message("user").write(user_input)
        st.chat_message("ai").write(answer)
