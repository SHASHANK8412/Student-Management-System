from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import Role, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(select(User).where(User.email == email, User.is_deleted.is_(False))).scalar_one_or_none()

    def list_roles(self) -> list[Role]:
        return self.session.execute(select(Role).where(Role.is_active.is_(True))).scalars().all()
