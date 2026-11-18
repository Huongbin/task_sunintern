from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root() -> dict:
    return {"message": "TaskSunIntern API is running"}


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
