from dataclasses import dataclass


@dataclass(frozen=True)
class SampleStatus:
    name: str

    @classmethod
    def default(cls) -> "SampleStatus":
        return cls(name="TaskSunIntern API")
