from app.schemas.base import BaseSchema


class MessageResponse(BaseSchema):
    message: str


class HealthResponse(BaseSchema):
    status: str
