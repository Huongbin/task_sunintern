def get_app_name() -> str:
    from app.config import settings

    return settings.app_name
