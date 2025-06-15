import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "CodeCraft AI" in response.text

def test_run_python_code():
    response = client.post(
        "/api/run",
        json={"code": "print('Hello, World!')", "language": "python"}
    )
    assert response.status_code == 200
    assert "Hello, World!" in response.json()["output"]

def test_invalid_language():
    response = client.post(
        "/api/run",
        json={"code": "console.log('test')", "language": "invalid"}
    )
    assert response.status_code == 400
    assert "Unsupported language" in response.json()["detail"]
