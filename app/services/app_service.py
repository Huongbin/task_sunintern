class AppService:
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name

    def get_status_message(self) -> str:
        return f"{self.app_name} is running"
