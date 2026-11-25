from app.config import settings
from app.services.app_service import AppService


def test_app_service_returns_running_message() -> None:
    service = AppService(app_name=settings.app_name)

    assert service.get_status_message() == f"{settings.app_name} is running"
