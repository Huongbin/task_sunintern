from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_app_service, get_current_user
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.common import (
    HealthResponse,
    MessageResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.security import create_access_token, hash_password, verify_password
from app.services.app_service import AppService

router = APIRouter()


@router.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(
    data: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    repository = UserRepository(db)

    if await repository.get_by_email(str(data.email)):
        raise HTTPException(status_code=400, detail="Email already exists")

    return await repository.create(
        full_name=data.full_name,
        email=str(data.email),
        password_hash=hash_password(data.password),
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    user = await UserRepository(db).get_by_email(str(data.email))

    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[TaskResponse]:
    repository = TaskRepository(db)
    tasks = await repository.get_all(skip=skip, limit=limit)
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
