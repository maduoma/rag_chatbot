from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.models import ChatRequest, ChatResponse
from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_text
from app.vectorstore.embeddings import embed_chunks
from app.vectorstore.faiss_store import get_faiss_store, add_to_faiss, retrieve_chunks
from app.llm.rag_chain import generate_answer
import os

router = APIRouter()

DATA_RAW = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw'))

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(DATA_RAW, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        text = load_document(file_path)
        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)
        add_to_faiss(chunks, embeddings)
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        retrieved_chunks = retrieve_chunks(request.query)
        answer = generate_answer(request.query, retrieved_chunks)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
