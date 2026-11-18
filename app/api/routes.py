from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_app_service
from app.schemas.common import HealthResponse, MessageResponse
from app.services.app_service import AppService

router = APIRouter()


@router.get("/", response_model=MessageResponse)
def read_root(
    service: Annotated[AppService, Depends(get_app_service)],
) -> MessageResponse:
    return MessageResponse(message=service.get_status_message())


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
