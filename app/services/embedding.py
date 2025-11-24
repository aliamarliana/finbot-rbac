from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb

def init_vector_store(documents):
    client = chromadb.Client()
    collection = client.get_or_create_collection("company_docs")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    for dept, docs in documents.items():
        for doc in docs:
            content = doc["content"]
            source = doc["source"]

            embedding = model.encode(content).tolist()

            collection.add(
                documents=[content],
                ids=[f"{dept}_{source}"],
                metadatas=[{"department": dept, "source": source}]
            )

    print("Vector store initialized.")
    return collection
