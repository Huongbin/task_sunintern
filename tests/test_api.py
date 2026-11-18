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


def test_task_crud() -> None:
    create_response = client.post(
        "/tasks",
        json={"title": "Test task", "description": "Test description"},
    )
    assert create_response.status_code == 201

    task = create_response.json()
    task_id = task["id"]

    list_response = client.get("/tasks?skip=0&limit=20")
    assert list_response.status_code == 200
    assert any(item["id"] == task_id for item in list_response.json())

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated task", "description": "Updated description"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated task"

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
