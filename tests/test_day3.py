# tests/test_day3.py
import requests
import base64
import time

BASE = "http://127.0.0.1:8000"

def auth_header(user, pwd):
    tok = f"{user}:{pwd}"
    return {"Authorization": "Basic " + base64.b64encode(tok.encode()).decode()}

def ingest_as_admin():
    print("Calling /ingest as Admin...")
    r = requests.post(BASE + "/ingest", headers=auth_header("Admin", "adminpw"), timeout=300)
    print("Status:", r.status_code, r.text)

def chat_as_user(user, pwd, q):
    print(f"\nChat as {user}: {q}")
    r = requests.post(BASE + "/chat", headers=auth_header(user, pwd), json={"message": q}, timeout=120)
    print("Status:", r.status_code)
    try:
        print(r.json())
    except Exception:
        print(r.text)

if __name__ == "__main__":
    time.sleep(1)
    ingest_as_admin()
    time.sleep(5)
    chat_as_user("Sam", "financepass", "Summarize the quarterly financial report.")
    chat_as_user("Bruce", "securepass", "Summarize the marketing campaign performance.")
    chat_as_user("Tony", "password123", "What is listed in the employee handbook?")
