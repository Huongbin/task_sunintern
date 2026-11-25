from datetime import datetime

from app.schemas.base import BaseSchema


class MessageResponse(BaseSchema):
    message: str


class HealthResponse(BaseSchema):
    status: str


class TaskCreate(BaseSchema):
    title: str
    description: str | None = None


class TaskUpdate(BaseSchema):
    title: str
    description: str | None = None


class TaskResponse(BaseSchema):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
