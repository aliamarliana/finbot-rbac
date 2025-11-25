# Role-Based RAG Chatbot for FinTech — Codebasics GenAI Project Challenge

This project is a full, production-ready implementation of a **Role-Based Access Control (RBAC) RAG Chatbot**, built for the [[Codebasics GenAI Resume Project Challenge](https://codebasics.io/challenges/codebasics-gen-ai-data-science-resume-project-challenge/19)].

The system solves a real-world FinTech problem:  
Different departments (Finance, HR, Marketing, Engineering, Executives) cannot quickly access the right information, causing delays and inefficiencies.  
To address this, the chatbot provides **secure, role-based**, context-rich answers using a RAG pipeline powered entirely by **open-source models**.

---

# 🚩 Problem Statement

FinSolve Technologies faces:

- Slow cross-team communication  
- Difficulty accessing important documents  
- Department silos (Finance, HR, Marketing, Engineering)  
- Inefficient decision-making  
- Risk of unauthorized data access  

They need a chatbot that:

✅ understands natural language  
✅ retrieves information securely  
✅ limits answers based on user roles  
✅ cites source documents  
✅ provides accurate, context-aware responses  

This project delivers exactly that.

---

# 🎯 Solution Overview

The system uses **RAG + RBAC**, meaning:

### 🔐 Role-Based Access Control  
Each user (Finance, HR, Marketing, Engineering, C-Level, Employee) can only access the documents assigned to their department.

### 🔎 Retrieval-Augmented Generation  
When a user asks a question:

1. The system retrieves only the documents they are allowed to see  
2. Uses embeddings to find the most relevant chunks  
3. Sends them to an LLM  
4. Generates a clear, contextual answer  
5. Includes source references  

Everything is managed safely using metadata filtering and LangChain retrievers.

---

# 🧱 Architecture

```text
┌────────────┐
│    User    │
└──────┬─────┘
       │
       ▼
┌────────────────────┐
│    Streamlit UI    │
└──────┬─────────────┘
       │ HTTP Request
       ▼
┌────────────────────┐
│   FastAPI Backend  │
│ (Auth + RBAC + API)│
└──────┬─────────────┘
       │ Calls RAG
       ▼
┌────────────────────┐
│   RAG Pipeline     │
│ (Retriever + LLM)  │
└──────┬─────────────┘
       │
       ├──────────────►  HuggingFace LLM  
       │                (Mistral-7B Instruct)
       │
       └──────────────►  ChromaDB Vector Store
                        (Embeddings + Metadata)
```


### Components:

- **Streamlit UI**
  - Chat interface  
  - Role display  
  - Chat history  
  - Admin panel  

- **FastAPI Backend**
  - Authentication  
  - RBAC filtering  
  - RAG endpoint  
  - Document ingestion endpoint  
  - Logging  

- **RAG Pipeline**
  - Text chunking  
  - Embedding generation  
  - Vector search (Chroma)  
  - LLM generation  

---

# 🧰 Tech Stack

## 🔹 Backend
- **FastAPI**
- **LangChain**
- **ChromaDB** (vector store)
- **SentenceTransformers** (embeddings)
  - `all-MiniLM-L6-v2`
- **HuggingFace Inference API** (LLM)
  - `mistralai/Mistral-7B-Instruct-v0.3`

## 🔹 Frontend
- **Streamlit**

## 🔹 Data
- Official Codebasics RAG Challenge dataset  
- Markdown, CSV (HR data), and metadata

## 🔹 Dev Tools
- Python 3.10
- venv
- dotenv

---

# 🔐 Roles Supported

| Role          | Access Level |
|---------------|--------------|
| Finance       | Financial reports, expenses, reimbursements |
| Marketing     | Campaigns, KPIs, performance metrics |
| HR            | Employee data, attendance, payroll |
| Engineering   | Technical docs, architecture, guidelines |
| C-Level       | Full access |
| Employee      | General policy documents |

---

# 📝 Example Users

| Username | Password     | Role        |
|----------|--------------|-------------|
| Tony     | password123  | engineering |
| Bruce    | securepass   | marketing   |
| Sam      | financepass  | finance     |
| Peter    | pete123      | engineering |
| Sid      | sidpass123   | marketing   |
| Natasha  | hrpass123    | hr          |
| Admin    | admin123     | admin       |

---

# 🧭 What I Have Learn

- Retrieval Augmented Generation (RAG)
- RBAC security in AI systems  
- LangChain retrievers  
- HuggingFace LLM integration  
- Embeddings + Vector Databases  
- API + UI integration  
- FinTech use case modeling  
- Full-stack AI development  

---

# 🌟 Project Outcome

This repository demonstrates my ability to:

⚡ Build a real-world AI application  
⚡ Work with open-source LLMs  
⚡ Implement secure information systems  
⚡ Architect a complete RAG pipeline  
⚡ Deploy a production-ready AI microservice  

---

# 📸 User Interface Preview

Below is a quick look at the front-end experience of the Role-Based RAG Chatbot.
The UI is designed to be clean, simple, and intuitive, allowing users to authenticate, select their role, and chat seamlessly with the system.

### 🏠 Main Chat Interface (with Sidebar)
This is the primary screen where authenticated users interact with the chatbot, ask questions, and view generated answers.
<img width="591" height="591" alt="image" src="https://github.com/user-attachments/assets/27156529-27b6-4f74-917b-6026c3d90601" />

### 🔐 Sidebar — User Login Panel

Users authenticate here with their username and password.
After login, Role-Based Access Control (RBAC) automatically restricts or grants access to department-specific information.

<img width="582" height="535" alt="image" src="https://github.com/user-attachments/assets/aa502d86-98ed-4a9c-b424-d6d4d835556a" />
