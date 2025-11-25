# scripts/ingest.py
import math
import os
from app.utils.loader import discover_documents
from app.services.vectorstore import VectorStore

# Sliding-window chunker
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200):
    if not text:
        return []
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= L:
            break
        start = end - overlap
    return chunks

def build_docs_for_vectorstore(documents):
    out = []
    for d in documents:
        dept = d["department"]
        src = d["source"]
        content = d["content"]
        chunks = chunk_text(content, chunk_size=800, overlap=200)
        for idx, c in enumerate(chunks):
            doc_id = f"{dept}::{src}::chunk-{idx}"
            metadata = {
                "department": dept,
                "source": src,
                "chunk_id": idx
            }
            out.append({"id": doc_id, "content": c, "metadata": metadata})
    return out

if __name__ == "__main__":
    print("Starting ingestion process (LangChain + Chroma) ...")
    docs = discover_documents()
    print(f"Discovered {len(docs)} source files.")
    vs = VectorStore()
    prepared = build_docs_for_vectorstore(docs)
    print(f"Prepared {len(prepared)} chunks to index.")
    BATCH = 64
    for i in range(0, len(prepared), BATCH):
        batch = prepared[i:i+BATCH]
        vs.add_documents(batch)
        print(f"Indexed batch {i//BATCH + 1} / {math.ceil(len(prepared)/BATCH)}")
    print("Ingestion complete. Persistence in", os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))
