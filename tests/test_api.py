from fastapi.testclient import TestClient

from passportpal.config import Settings


def test_health_is_ok(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["app"] == "passportpal"
    assert response.json()["env"] == "ci"
    assert response.json()["version"] == "dev"


def test_git_sha_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("GIT_SHA", "3f2c1ab")

    settings = Settings(app_env="ci")

    assert settings.git_sha == "3f2c1ab"


def test_ready(client: TestClient):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["database"] is True


def test_documents(client: TestClient):
    response = client.get("/v1/documents")

    assert response.status_code == 200
    assert response.json()["total"] == 20
    assert len(response.json()["items"]) == 20


def test_get_existing_document(client: TestClient):
    response = client.get("/v1/documents/PP001")

    assert response.status_code == 200
    assert response.json()["id"] == "PP001"
    assert response.json()["full_name"] == "Aarav Sharma"


def test_get_missing_document(client: TestClient):
    response = client.get("/v1/documents/PP999")

    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert "PP999" in response.json()["detail"]


def test_search_by_nationality(client: TestClient):
    response = client.get("/v1/documents", params={"q": "Indian"})

    assert response.status_code == 200
    assert response.json()["total"] == 8


def test_search_is_case_insensitive(client: TestClient):
    response = client.get("/v1/documents", params={"q": "meera"})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["full_name"] == "Meera Krishnan"


def test_search_with_no_results(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"q": "UnknownPerson"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


def test_document_limit(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"limit": 5},
    )

    assert response.status_code == 200
    assert len(response.json()["items"]) == 5
    assert response.json()["limit"] == 5


def test_document_offset(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"offset": 2, "limit": 2},
    )

    assert response.status_code == 200
    assert response.json()["items"][0]["id"] == "PP003"
    assert response.json()["items"][1]["id"] == "PP004"


def test_offset_beyond_available_records(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"offset": 100},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 20
    assert response.json()["items"] == []


def test_invalid_zero_limit(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"limit": 0},
    )

    assert response.status_code == 422


def test_limit_above_maximum(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"limit": 101},
    )

    assert response.status_code == 422


def test_negative_offset(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"offset": -1},
    )

    assert response.status_code == 422


def test_query_exceeding_maximum_length(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"q": "a" * 201},
    )

    assert response.status_code == 422


def test_query_at_maximum_length(client: TestClient):
    response = client.get(
        "/v1/documents",
        params={"q": "a" * 200},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 0
