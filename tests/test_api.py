from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json()["message"] == f"{settings.app_name} is running"


def test_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_not_found() -> None:
    response = client.get("/api/v1/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
