# app/services/rag.py
from typing import List
from app.services.vectorstore import VectorStore
from app.services.llm import generate_answer

# RBAC mapping (simple single-role metadata)
ROLE_ACCESS = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "employee": ["general"],
    "c_level": ["finance", "marketing", "hr", "engineering", "general"]
}

vs = VectorStore()

def allowed_departments(role: str):
    return ROLE_ACCESS.get(role, ["general"])

def retrieve_for_role(query: str, role: str, top_k: int = 5):
    allowed = allowed_departments(role)
    where = {"department": {"$in": allowed}}
    results = vs.query(query_text=query, n_results=top_k, where=where)
    return results

def build_context_from_results(results: List[dict]):
    """
    Combine retrieved chunks into a context block, and produce a sources summary.
    Returns (context_text, sources_list)
    """
    pieces = []
    sources = []
    for r in results:
        meta = r.get("metadata", {})
        dept = meta.get("department", "unknown")
        src = meta.get("source", "unknown")
        chunk_id = meta.get("chunk_id", "0")
        text = r.get("document", "")
        # Add small header and text
        header = f"[{dept} | {src} | chunk-{chunk_id}]"
        pieces.append(header + "\n" + text + "\n")
        sources.append(f"{src}#chunk-{chunk_id}")
    context = "\n---\n".join(pieces)
    return context, list(dict.fromkeys(sources))  # dedupe preserving order

def answer_query_with_rag(question: str, role: str, top_k: int = 5, max_new_tokens: int = 300, temperature: float = 0.2):
    # retrieve
    results = retrieve_for_role(question, role, top_k=top_k)
    if not results:
        return {
            "answer": "No relevant documents found for your role.",
            "sources": [],
            "retrieved": []
        }
    context, sources = build_context_from_results(results)
    # generate
    answer_text = generate_answer(context, question, max_new_tokens=max_new_tokens, temperature=temperature)
    return {
        "answer": answer_text,
        "sources": sources,
        "retrieved": results
    }
