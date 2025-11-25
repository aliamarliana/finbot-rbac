# tests/test_day4.py
import requests
import base64
import time

BASE = "http://127.0.0.1:8000"

def auth_header(user, pwd):
    tok = f"{user}:{pwd}"
    return {"Authorization": "Basic " + base64.b64encode(tok.encode()).decode()}

def test_ingest_admin():
    print("Ingest as Admin...")
    r = requests.post(BASE + "/ingest", headers=auth_header("Admin", "adminpw"), timeout=300)
    print(r.status_code, r.json())

def test_query(role_user, role_pass, q):
    print(f"Query as {role_user}: {q}")
    r = requests.post(BASE + "/chat", headers=auth_header(role_user, role_pass), json={"message": q}, timeout=120)
    print(r.status_code)
    print(r.json())

if __name__ == "__main__":
    time.sleep(1)
    test_ingest_admin()
    time.sleep(5)
    test_query("Sam","financepass","Summarize the quarterly financial report.")
    test_query("Tony","password123","What's in the employee handbook?")
    test_query("Natasha","hrpass123","List payroll info for employees.")
