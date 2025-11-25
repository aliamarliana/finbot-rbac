# app/main.py
import logging
import os
from typing import Dict
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from app.utils.loader import discover_documents
from scripts.ingest import build_docs_for_vectorstore
from app.services.vectorstore import VectorStore
from app.services.rag import answer_query_with_rag, allowed_departments

# -------------------------
# Logging
# -------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("finbot")

# -------------------------
# App & Auth
# -------------------------
app = FastAPI(title="FinSolve RBAC Chatbot - Day 4 (Production-ready)")

security = HTTPBasic()

# Dummy user DB (demo only)
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},
    "Admin": {"password": "adminpw", "role": "c_level"}
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        logger.warning("Authentication failed for user=%s", username)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}

# -------------------------
# Request/Response Models
# -------------------------
class ChatRequest(BaseModel):
    message: str
    top_k: int = 5
    max_new_tokens: int = 300
    temperature: float = 0.2

# -------------------------
# Health & Root
# -------------------------
@app.get("/")
def root():
    return {"message": "FinSolve RBAC Chatbot - Day 4 (Production-ready)"}

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Ingest endpoint (admin-only)
# -------------------------
@app.post("/ingest")
def run_ingest(user=Depends(authenticate)):
    if user["role"] != "c_level":
        logger.warning("Unauthorized ingest attempt by %s", user["username"])
        raise HTTPException(status_code=403, detail="Only c_level can run ingest.")
    try:
        docs = discover_documents()
        prepared = build_docs_for_vectorstore(docs)
        vs = VectorStore()
        BATCH = 64
        import math
        for i in range(0, len(prepared), BATCH):
            batch = prepared[i:i+BATCH]
            vs.add_documents(batch)
            logger.info("Indexed batch %d/%d", i//BATCH + 1, math.ceil(len(prepared)/BATCH))
        logger.info("Ingestion completed: %d chunks", len(prepared))
        return {"status": "ingested", "chunks_indexed": len(prepared)}
    except Exception as e:
        logger.exception("Ingest failed")
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Chat endpoint (RBAC + RAG + LLM)
# -------------------------
@app.post("/chat")
def chat_endpoint(req: ChatRequest, user=Depends(authenticate)):
    logger.info("Chat request by user=%s role=%s q=%s", user["username"], user["role"], req.message[:50])
    try:
        res = answer_query_with_rag(req.message, user["role"], top_k=req.top_k,
                                    max_new_tokens=req.max_new_tokens, temperature=req.temperature)
        return {
            "user": user["username"],
            "role": user["role"],
            "question": req.message,
            "answer": res["answer"],
            "sources": res["sources"],
            "retrieved_count": len(res.get("retrieved", []))
        }
    except Exception as e:
        logger.exception("Chat failed")
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Global exception handler (clean JSON)
# -------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
