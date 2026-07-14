from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.core.permissions import ROLE_SUPER_ADMIN
from app.core.security import create_password_hash
from app.models.user import Role, User
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.schemas.user import RoleRead, UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("/roles", response_model=list[RoleRead], dependencies=[Depends(require_permissions("users:read"))])
def list_roles(db: Session = Depends(get_db)):
    return db.execute(select(Role).order_by(Role.name.asc())).scalars().all()


@router.get("", response_model=PaginatedResponse[UserRead], dependencies=[Depends(require_permissions("users:read"))])
def list_users(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), search: str | None = None, db: Session = Depends(get_db)):
    stmt = select(User).where(User.is_deleted.is_(False))
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(User.full_name.ilike(pattern) | User.email.ilike(pattern))
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("users:write"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    role = db.get(Role, payload.role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    user = User(full_name=payload.full_name, email=payload.email.lower(), phone=payload.phone, password_hash=create_password_hash(payload.password), role_id=role.id, is_verified=role.name == ROLE_SUPER_ADMIN)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permissions("users:read"))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permissions("users:write"))])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=MessageResponse, dependencies=[Depends(require_permissions("users:write"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_deleted = True
    db.commit()
    return MessageResponse(message="User deleted")
