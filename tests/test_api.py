from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "TaskSunIntern API is running"


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_not_found() -> None:
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
