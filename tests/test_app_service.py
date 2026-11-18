from app.repositories.sample_repository import SampleRepository
from app.services.app_service import AppService


def test_app_service_returns_running_message() -> None:
    service = AppService(SampleRepository())

    assert service.get_status_message() == "TaskSunIntern API is running"
