import os
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langsmith import traceable
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env", verbose=True, override=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@traceable(run_type="llm", metadata={"ls_provider": "ollama", "model": "mistral"})
def create_qa_agent(pdf_path, model_name="mistral"):
    """
    Create a question-answering agent for a specific PDF document.

    Args:
        pdf_path (str): Path to the PDF file
        model_name (str): Name of the Ollama model to use

    Returns:
        qa_chain: A QA chain that can answer questions about the PDF
    """
    persist_directory = "./data/chroma_db"

    # Check if the Chroma store already exists
    if os.path.exists(persist_directory):
        logging.info("Loading existing Chroma store...")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model=model_name))
    else:
        logging.info("Creating new Chroma store...")
        # 1. Load the PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        logging.info(f"Loaded {len(pages)} pages from the PDF.")

        # 2. Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        splits = text_splitter.split_documents(pages)
        logging.info(f"Split the document into {len(splits)} chunks.")

        # 3. Create embeddings and store them
        embeddings = OllamaEmbeddings(model=model_name)
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        for i, chunk in enumerate(tqdm(splits, desc="Processing chunks"), 1):
            vectorstore.add_documents([chunk], embedding=embeddings)
        logging.info(f"Stored {len(splits)} chunks in the vectorstore.")

    # 4. Create the LLM
    llm = Ollama(model=model_name)

    # 5. Create a custom prompt template
    prompt_template1 = """
    You are a helpful AI assistant that answers questions based on the provided PDF document.
    Use only the context provided to answer the question. If you don't know the answer or
    can't find it in the context, say so. Answer in few shot
    """

    prompt_template = """
    You are a software principal engineer. 
    Use your knowledge base to answer questions about your profile only which is in the pdf and reply answer in few shots in one or two sentences. 
    Do not answer outside my profile. can't find it in the context, say so. Answer in few shot
    At the end of the answer please add my signature 
    Don not proivde all the details. Try to answer in one or two sentences or less than 8 words
    Thanks - Mani Alagarsamy
    
    Context: {context}

    Question: {question}

    Answer: Let me answer from my profile. Every response should end with my signature -Thanks - Mani Alagarsamy"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # 6. Create and return the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain

@traceable(run_type="chain")
def ask_question(qa_chain, question):
    """
    Ask a question to the QA chain and get the response.

    Args:
        qa_chain: The QA chain created by create_qa_agent
        question (str): The question to ask

    Returns:
        dict: Response containing the answer and source documents
    """
    try:
        response = qa_chain({"query": question})
        return {
            "answer": response["result"],
            "sources": [doc.page_content for doc in response["source_documents"]]
        }
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {
            "error": f"An error occurred: {str(e)}",
            "answer": None,
            "sources": None
        }

def main():
    # Ensure Ollama is running and the model is pulled
    # You can pull the model using: ollama pull mistral

    # Replace with your PDF path
    PDF_PATH = "/Users/mani/Downloads/test/mani-poc.pdf"

    if not os.path.exists(PDF_PATH):
        logging.error(f"The file {PDF_PATH} does not exist.")
        return

    # Create the QA agent
    qa_agent = create_qa_agent(PDF_PATH)

    # Ask questions from the user
    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        logging.info(f"Question: {question}")
        result = ask_question(qa_agent, question)
        if result.get("error"):
            logging.error(result['error'])
        else:
            logging.info(f"Answer: {result['answer']}")
            logging.info("Sources used:")
            #for i, source in enumerate(result['sources'], 1):
             #   logging.info(f"Source {i}: {source[:200] + '...' if len(source) > 200 else source}")

if __name__ == "__main__":
    main()