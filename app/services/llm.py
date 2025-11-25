# app/services/llm.py
import os
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.llms import HuggingFaceHub

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

# Prompt template: system + context + user question
SYSTEM_PROMPT = """
You are FinSolve Assistant, a secure role-based company assistant. Only use the provided context to answer the user's question.
Respect role-based access: do not invent or reveal information not present in the context or outside the user's permitted departments.
Provide a concise helpful answer and at the end include "Sources:" followed by source file names and chunk ids.
"""

PROMPT_TMPL = SYSTEM_PROMPT + "\n\nCONTEXT:\n{context}\n\nUser Question:\n{question}\n\nAnswer:"
prompt = PromptTemplate(input_variables=["context", "question"], template=PROMPT_TMPL)

def get_hf_llm(max_new_tokens: int = 300, temperature: float = 0.2):
    """
    Returns a LangChain HuggingFaceHub LLM wrapper that calls the Inference API.
    """
    if not HF_TOKEN:
        raise ValueError("HF_API_TOKEN not found in environment. Set it in .env")

    llm = HuggingFaceHub(
        repo_id=HF_MODEL,
        huggingfacehub_api_token=HF_TOKEN,
        model_kwargs={"temperature": temperature, "max_new_tokens": max_new_tokens}
    )
    return llm

def generate_answer(context_chunks: str, question: str, max_new_tokens: int = 300, temperature: float = 0.2):
    """
    Calls the HuggingFaceHub LLM via LangChain and returns text response.
    """
    llm = get_hf_llm(max_new_tokens=max_new_tokens, temperature=temperature)
    final_prompt = prompt.format(context=context_chunks, question=question)
    output = llm(final_prompt)
    return output
