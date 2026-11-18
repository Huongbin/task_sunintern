from app.repositories.sample_repository import SampleRepository


class AppService:
    def __init__(self, repository: SampleRepository) -> None:
        self.repository = repository

    def get_status_message(self) -> str:
        return f"{self.repository.get_status().name} is running"
