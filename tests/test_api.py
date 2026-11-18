from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200


def test_documents(client: TestClient):
    response = client.get("/v1/documents")
    assert response.status_code in [200, 401, 403, 422]
