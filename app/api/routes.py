from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_app_service
from app.repositories.task_repository import TaskRepository
from app.schemas.common import (
    HealthResponse,
    MessageResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
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


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TaskResponse]:
    repository = TaskRepository(db)
    tasks = await repository.get_all()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    repository = TaskRepository(db)
    task = await repository.create(data.title, data.description)
    return TaskResponse.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    repository = TaskRepository(db)
    task = await repository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task = await repository.update(task, data.title, data.description)
    return TaskResponse.model_validate(task)


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    repository = TaskRepository(db)
    task = await repository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await repository.delete(task)
