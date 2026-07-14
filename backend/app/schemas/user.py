from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import APIModel


class RoleRead(APIModel):
    id: int
    name: str
    description: str | None = None
    permissions: list[str]
    is_active: bool


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    phone: str | None = None
    password: str = Field(min_length=8, max_length=128)
    role_id: int


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=200)
    phone: str | None = None
    role_id: int | None = None
    is_active: bool | None = None
    is_verified: bool | None = None


class UserRead(APIModel):
    id: int
    public_id: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: RoleRead
    is_active: bool
    is_verified: bool
    last_login_at: datetime | None = None
