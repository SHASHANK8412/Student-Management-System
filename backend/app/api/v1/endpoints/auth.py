from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import permissions_for_role
from app.core.security import create_access_token, create_password_hash, create_refresh_token, hash_token, verify_password
from app.core.dependencies import get_current_user
from app.models.user import EmailVerificationToken, PasswordResetToken, RefreshToken, Role, User
from app.schemas.auth import AuthResponse, AuthUser, ForgotPasswordRequest, LoginRequest, RefreshTokenRequest, ResetPasswordRequest, VerifyEmailRequest
from app.schemas.common import MessageResponse, TokenPair

router = APIRouter()


def _build_auth_user(user: User) -> AuthUser:
    return AuthUser(
        id=user.id,
        public_id=user.public_id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role.name,
        permissions=user.role.permissions or permissions_for_role(user.role.name),
        is_active=user.is_active,
        is_verified=user.is_verified,
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).join(Role).filter(User.email == payload.email.lower(), User.is_deleted.is_(False)).one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    permissions = user.role.permissions or permissions_for_role(user.role.name)
    access_token = create_access_token(user.public_id, user.role.name, permissions)
    refresh_token, refresh_hash, expires_at = create_refresh_token(user.public_id)
    db.add(RefreshToken(user_id=user.id, token_hash=refresh_hash, expires_at=expires_at))
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return AuthResponse(
        tokens=TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,
        ),
        user=_build_auth_user(user),
    )


@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    token_hash = hash_token(payload.refresh_token)
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked_at.is_(None)).one_or_none()
    if not stored or stored.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = db.get(User, stored.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    permissions = user.role.permissions or permissions_for_role(user.role.name)
    return TokenPair(
        access_token=create_access_token(user.public_id, user.role.name, permissions),
        refresh_token=payload.refresh_token,
        expires_in=30 * 60,
    )


@router.post("/logout", response_model=MessageResponse)
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token_hash = hash_token(payload.refresh_token)
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).one_or_none()
    if stored:
        stored.revoked_at = datetime.now(timezone.utc)
    db.commit()
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=AuthUser)
def me(current_user: User = Depends(get_current_user)):
    return _build_auth_user(current_user)


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower(), User.is_deleted.is_(False)).one_or_none()
    if user:
        raw_token, token_hash, expires_at = create_refresh_token(user.public_id)
        db.add(PasswordResetToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at))
        db.commit()
    return MessageResponse(message="If the account exists, a reset link has been generated")


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = hash_token(payload.token)
    token = db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash, PasswordResetToken.used_at.is_(None)).one_or_none()
    if not token or token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
    user = db.get(User, token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    user.password_hash = create_password_hash(payload.new_password)
    token.used_at = datetime.now(timezone.utc)
    db.commit()
    return MessageResponse(message="Password reset successfully")


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    token_hash = hash_token(payload.token)
    token = db.query(EmailVerificationToken).filter(EmailVerificationToken.token_hash == token_hash, EmailVerificationToken.verified_at.is_(None)).one_or_none()
    if not token or token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification token")
    user = db.get(User, token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    user.is_verified = True
    token.verified_at = datetime.now(timezone.utc)
    db.commit()
    return MessageResponse(message="Email verified successfully")
