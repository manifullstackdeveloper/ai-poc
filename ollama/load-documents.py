from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("/Users/mani/Downloads/test", glob="**/*.pdf")
document = loader.load()
print(len(document))

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(document)


from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

vectorstore = Chroma.from_documents(
    documents=all_splits,
    embedding=OllamaEmbeddings(model="llama3", show_progress=True),
    persist_directory="./chroma_db",
)

from langchain import hub
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama3")

retriever = vectorstore.as_retriever()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


import os
os.environ["LANGCHAIN_API_KEY"] = ""

rag_prompt = hub.pull("rlm/rag-prompt")

qa_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)


# running the QA chain in a loop until the user types "exit"
while True:
    question = input("Question: ")
    if question.lower() == "exit":
        break
    answer = qa_chain.invoke(question)

    print(f"\nAnswer: {answer}\n")