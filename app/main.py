from typing import Dict
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.utils.loader import load_all_documents
from app.services.embedding import init_vector_store

app = FastAPI()
security = HTTPBasic()

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},  # fixed typo
}

# Load dataset (Day 1)
DOCUMENTS = load_all_documents()

# Initialize vector DB (Day 1)
VECTOR_STORE = init_vector_store(DOCUMENTS)


# Authentication
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"username": username, "role": user["role"]}


@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Chat endpoint (to be fully implemented on Day 3)
@app.post("/chat")
def query(message: str, user=Depends(authenticate)):
    return {
        "user": user["username"],
        "role": user["role"],
        "message_received": message,
        "response": "RAG pipeline not implemented yet — Day 3.",
    }
