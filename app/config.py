from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskSunIntern API"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./task.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
