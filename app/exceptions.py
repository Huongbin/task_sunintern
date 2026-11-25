from fastapi import HTTPException


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=404, detail=detail)
