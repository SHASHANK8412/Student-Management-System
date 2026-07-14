from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import APIModel, TokenPair


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class VerifyEmailRequest(BaseModel):
    token: str


class AuthUser(APIModel):
    id: int
    public_id: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: str
    permissions: list[str]
    is_active: bool
    is_verified: bool


class AuthResponse(BaseModel):
    tokens: TokenPair
    user: AuthUser
