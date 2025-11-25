# tests/test_day2.py
import requests
import base64
import time

BASE = "http://127.0.0.1:8000"

def auth_header(username, password):
    token = f"{username}:{password}"
    import base64
    return {"Authorization": "Basic " + base64.b64encode(token.encode()).decode()}

def run_ingest():
    print("Requesting ingest as Admin...")
    h = auth_header("Admin", "adminpw")
    r = requests.post(BASE + "/ingest", headers=h)
    print("Status:", r.status_code, "Resp:", r.json())

def test_query_as_finance():
    print("Query as Sam (finance)...")
    h = auth_header("Sam", "financepass")
    payload = {"question": "What is the quarterly financial summary?", "top_k": 3}
    r = requests.post(BASE + "/query", json=payload, headers=h)
    print("Status:", r.status_code)
    print(r.json())

def test_query_as_employee():
    print("Query as employee (no permission to finance docs)...")
    # create a lightweight 'employee' user if not in DB else use existing
    h = auth_header("Tony", "password123")  # Tony is engineering in DB
    payload = {"question": "Tell me about company policies", "top_k": 3}
    r = requests.post(BASE + "/query", json=payload, headers=h)
    print("Status:", r.status_code)
    print(r.json())

if __name__ == "__main__":
    # Wait a bit (if server was just started)
    time.sleep(1)
    run_ingest()
    time.sleep(3)
    test_query_as_finance()
    test_query_as_employee()
