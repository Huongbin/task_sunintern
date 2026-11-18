from app.models.sample import SampleStatus


class SampleRepository:
    def get_status(self) -> SampleStatus:
        return SampleStatus.default()
