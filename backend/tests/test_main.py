from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Code audit ai API" in response.json()["message"]

def test_api_scans():
    response = client.get("/api/v1/scans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
