import requests
import base64
import json

BASE_URL = "http://127.0.0.1:8000"

def encode_auth(username, password):
    token = f"{username}:{password}"
    return base64.b64encode(token.encode()).decode()

def test_login():
    print("🔵 Testing /login endpoint...")

    headers = {
        "Authorization": f"Basic {encode_auth('Peter', 'pete123')}"
    }

    response = requests.get(f"{BASE_URL}/login", headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_test_endpoint():
    print("\n🔵 Testing /test endpoint...")

    headers = {
        "Authorization": f"Basic {encode_auth('Bruce', 'securepass')}"
    }

    response = requests.get(f"{BASE_URL}/test", headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_chat_stub():
    print("\n🔵 Testing /chat endpoint (stub)...")

    headers = {
        "Authorization": f"Basic {encode_auth('Sam', 'financepass')}"
    }

    payload = {"message": "What is the Q4 revenue?"}

    response = requests.post(f"{BASE_URL}/chat", headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_login()
    test_test_endpoint()
    test_chat_stub()
