from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_app_name
from app.schemas.common import HealthResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=MessageResponse)
def read_root(app_name: Annotated[str, Depends(get_app_name)]) -> MessageResponse:
    return MessageResponse(message=f"{app_name} is running")


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
