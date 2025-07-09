import os
import re
from io import StringIO
from pathlib import Path

import pandas as pd
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Extract raw text and tables
def extract_text_and_tables_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() + "\n"

    table_blocks = re.findall(r'(?:(?:\d+%?\s+){2,}.*?)(?=\n\S|\Z)', raw_text, re.DOTALL)
    cleaned_tables = []

    for block in table_blocks:
        try:
            df = pd.read_csv(StringIO(block), sep=r'\s{2,}', engine='python')
            cleaned_tables.append(df)
        except Exception:
            continue

    return raw_text, cleaned_tables

# Load and process PDFs
def load_pdf_and_create_vectorstore(pdf_paths):
    all_pages = []

    for path in pdf_paths:
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        all_pages.extend(pages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_pages)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

# Build conversational QA chain
def get_qa_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )
    return qa_chain
