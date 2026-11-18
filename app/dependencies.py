from app.repositories.sample_repository import SampleRepository
from app.services.app_service import AppService


def get_app_name() -> str:
    from app.config import settings

    return settings.app_name


def get_app_service() -> AppService:
    return AppService(SampleRepository())
