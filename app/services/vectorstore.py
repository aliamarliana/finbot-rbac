# app/services/vectorstore.py
import os
from typing import List, Dict
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

from dotenv import load_dotenv
load_dotenv()

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
COLLECTION_NAME = "company_docs"

class VectorStore:
    def __init__(self, persist_directory: str = PERSIST_DIR, collection_name: str = COLLECTION_NAME):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        # Use langchain HuggingFaceEmbeddings wrapper (under the hood uses sentence-transformers)
        self.hf_emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # LangChain embedding wrapper supports embedding of a single string or list
        return [self.hf_emb.embed_query(t) for t in texts]

    def add_documents(self, docs: List[Dict]):
        """
        docs: list of {"id": str, "content": str, "metadata": {...}}
        We'll embed doc contents in batches and add them to Chroma with embeddings.
        """
        contents = [d["content"] for d in docs]
        metadatas = [d.get("metadata", {}) for d in docs]
        ids = [d["id"] for d in docs]
        # get embeddings
        embeddings = self.embed_texts(contents)
        # Add to chroma
        self.collection.add(documents=contents, metadatas=metadatas, ids=ids, embeddings=embeddings)

    def query(self, query_text: str, n_results: int = 5, where: Dict = None):
        """
        Query using embeddings and optional metadata filter (where)
        where should follow chromadb's filter format e.g. {"department": {"$in": ["finance","general"]}}
        Returns list of dicts: id, document, metadata, distance
        """
        q_emb = self.hf_emb.embed_query(query_text)
        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=n_results,
            where=where
        )
        output = []
        if results and len(results.get("ids", [])) > 0:
            ids = results.get("ids")[0]
            docs = results.get("documents")[0]
            metadatas = results.get("metadatas")[0]
            distances = results.get("distances", [[None]])[0]
            for _id, doc, meta, dist in zip(ids, docs, metadatas, distances):
                output.append({
                    "id": _id,
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                })
        return output
