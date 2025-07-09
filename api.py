from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from main import load_pdf_and_create_vectorstore, get_qa_chain

# Load secrets from .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Paths to your PDF files
pdf_paths = [
    "pdfs/Conditions_Generales_2025_AAV.pdf",
    "pdfs/DIP_AAV_2025.pdf"
]

# Init FastAPI
app = FastAPI()

# Create vectorstore and QA chain at startup
vectorstore = load_pdf_and_create_vectorstore(pdf_paths)
qa_chain = get_qa_chain(vectorstore)

# Request schema
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query, request: Request):
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = qa_chain.invoke({"question": query.question, "chat_history": []})
    return {
    "answer": result["answer"],
    "sources": [doc.metadata.get("source", "") for doc in result["source_documents"]]
}
