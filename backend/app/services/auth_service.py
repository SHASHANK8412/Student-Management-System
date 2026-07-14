from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.permissions import permissions_for_role
from app.core.security import create_access_token, create_password_hash, create_refresh_token, decode_token, hash_token, verify_password
from app.models.user import EmailVerificationToken, PasswordResetToken, RefreshToken, Role, User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.users = UserRepository(session)

    def login(self, email: str, password: str) -> tuple[User, str, str, datetime]:
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        role_name = user.role.name
        permissions = permissions_for_role(role_name)
        access_token = create_access_token(user.public_id, role_name, permissions)
        raw_refresh_token, token_hash, expires_at = create_refresh_token(user.public_id)
        self.session.add(RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at))
        user.last_login_at = datetime.now(timezone.utc)
        self.session.flush()
        return user, access_token, raw_refresh_token, expires_at

    def register_user(self, full_name: str, email: str, password: str, phone: str | None, role: Role) -> User:
        user = User(full_name=full_name, email=email.lower(), phone=phone, password_hash=create_password_hash(password), role_id=role.id)
        self.session.add(user)
        self.session.flush()
        self.session.add(EmailVerificationToken(user_id=user.id, token_hash=hash_token(f"verify-{user.public_id}"), expires_at=datetime.now(timezone.utc)))
        return user

    def refresh(self, refresh_token: str) -> User:
        token_hash = hash_token(refresh_token)
        stored = self.session.query(RefreshToken).filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked_at.is_(None)).one_or_none()
        if not stored or stored.expires_at < datetime.now(timezone.utc):
            raise ValueError("Invalid refresh token")
        user = self.session.get(User, stored.user_id)
        if not user:
            raise ValueError("User not found")
        return user
