from pydantic import EmailStr

from app.schemas.base import BaseSchema


class RegisterRequest(BaseSchema):
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseSchema):
    id: int
    full_name: str
    email: str
    is_active: bool
