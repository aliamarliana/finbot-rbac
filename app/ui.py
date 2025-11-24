import streamlit as st
import requests
import base64

API_URL = "http://127.0.0.1:8000"


# -------------------------
# Helper Functions
# -------------------------

def encode_basic_auth(username, password):
    token = f"{username}:{password}"
    return base64.b64encode(token.encode()).decode()


def login_user(username, password):
    try:
        headers = {"Authorization": f"Basic {encode_basic_auth(username, password)}"}
        response = requests.get(f"{API_URL}/login", headers=headers)

        if response.status_code == 200:
            data = response.json()
            return True, data["role"]
        else:
            return False, None

    except Exception as e:
        return False, None


def send_message(message, username, password):
    headers = {"Authorization": f"Basic {encode_basic_auth(username, password)}"}
    payload = {"message": message}

    response = requests.post(f"{API_URL}/chat", headers=headers, json=payload)
    return response.json()


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(page_title="RBAC RAG Chatbot", layout="centered")

st.title("🤖 Role-Based RAG Chatbot")
st.write("Secure, role-specific access to organizational knowledge.")

# -------------------------
# Session State Initialization
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Login Screen
# -------------------------
if not st.session_state.authenticated:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        ok, role = login_user(username, password)

        if ok:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.role = role

            st.success(f"Logged in as {username} ({role})")
            st.rerun()
        else:
            st.error("Invalid username or password. Try again.")

    st.stop()  # Stops rendering further if not logged in


# -------------------------
# Sidebar Info
# -------------------------
with st.sidebar:
    st.header("👤 User Info")
    st.write(f"**Username:** {st.session_state.username}")
    st.write(f"**Role:** {st.session_state.role}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()


# -------------------------
# Chat Interface
# -------------------------

st.subheader("💬 Chat with your AI Assistant")

# Display messages
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.chat_message("user").markdown(msg["text"])
    else:
        st.chat_message("assistant").markdown(msg["text"])

# Input box at the bottom
user_input = st.chat_input("Ask a question...")

if user_input:
    # Store user's message
    st.session_state.messages.append({"sender": "user", "text": user_input})

    # Send to FastAPI backend
    response = send_message(
        user_input,
        st.session_state.username,
        st.session_state.password
    )

    bot_reply = response.get("response", "No response received.")

    st.session_state.messages.append({"sender": "assistant", "text": bot_reply})
    st.rerun()
