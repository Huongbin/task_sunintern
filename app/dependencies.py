from app.config import settings
from app.services.app_service import AppService


def get_app_service() -> AppService:
    return AppService(app_name=settings.app_name)
