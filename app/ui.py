# app/ui.py
import streamlit as st
import requests
import base64
from typing import List

# -------------------------
# Config
# -------------------------
API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000")  # override in HF Space secrets if backend hosted externally
CHAT_ENDPOINT = f"{API_BASE}/chat"
LOGIN_ENDPOINT = f"{API_BASE}/"  # we reuse Basic Auth via /chat

# -------------------------
# Utils
# -------------------------
def encode_basic_auth(username: str, password: str) -> str:
    token = f"{username}:{password}"
    return base64.b64encode(token.encode()).decode()

def call_chat(username: str, password: str, message: str, top_k: int=5, max_new_tokens: int=300, temperature: float=0.2, timeout: int=60):
    headers = {"Authorization": f"Basic {encode_basic_auth(username, password)}", "Content-Type": "application/json"}
    payload = {"message": message, "top_k": top_k, "max_new_tokens": max_new_tokens, "temperature": temperature}
    resp = requests.post(CHAT_ENDPOINT, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

# -------------------------
# Page layout & session state
# -------------------------
st.set_page_config(page_title="FinSolve RBAC Chatbot", layout="wide")
st.title("🤖 FinSolve RBAC Chatbot — Production UI")

if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Sidebar: login / info
# -------------------------
with st.sidebar:
    st.header("👤 Login (Demo)")
    st.session_state.username = st.text_input("Username", value=st.session_state.username)
    st.session_state.password = st.text_input("Password", value=st.session_state.password, type="password")

    st.markdown("---")
    st.write("When deployed, set `API_BASE` in Space secrets to your backend URL.")
    if st.button("Clear history"):
        st.session_state.history = []

# -------------------------
# Controls (top)
# -------------------------
col1, col2, col3 = st.columns([4,1,1])
with col1:
    query = st.text_input("Ask a question", key="query_input")
with col2:
    top_k = st.selectbox("Top K", [1,2,3,4,5,10], index=4)
with col3:
    temperature = st.slider("Temp", 0.0, 1.0, 0.2, step=0.05)

if st.button("Send"):
    if not st.session_state.username or not st.session_state.password:
        st.warning("Please login in the sidebar first.")
    elif not query.strip():
        st.warning("Write a question first.")
    else:
        try:
            res = call_chat(st.session_state.username, st.session_state.password, query, top_k=top_k, temperature=float(temperature))
            answer = res.get("answer", "No answer")
            sources = res.get("sources", [])
            # Append to history
            st.session_state.history.append({"role":"user","text": query})
            st.session_state.history.append({"role":"assistant","text": answer, "sources": sources})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------
# Conversation display
# -------------------------
st.markdown("## Conversation")
for msg in st.session_state.history[::-1]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")
        if msg.get("sources"):
            st.markdown("**Sources:**")
            for s in msg["sources"]:
                st.write("-", s)
