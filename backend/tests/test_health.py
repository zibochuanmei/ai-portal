from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_propagates_request_id() -> None:
    response = client.get("/health", headers={"X-Request-ID": "test-trace-001"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-trace-001"


def test_visible_agents() -> None:
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    assert len(response.json()) >= 1
