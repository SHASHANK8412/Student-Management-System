from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.attendance import AttendanceRecord
from app.schemas.attendance import AttendanceCreate, AttendanceRead
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AttendanceRead], dependencies=[Depends(require_permissions("attendance:read"))])
def list_attendance(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), student_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(AttendanceRecord).where(AttendanceRecord.is_deleted.is_(False))
    if student_id:
        stmt = stmt.where(AttendanceRecord.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(AttendanceRecord.attendance_date.desc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("attendance:write"))])
def create_attendance(payload: AttendanceCreate, db: Session = Depends(get_db)):
    existing = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == payload.student_id, AttendanceRecord.attendance_date == payload.attendance_date).one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attendance already recorded for this date")
    record = AttendanceRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{attendance_id}", response_model=MessageResponse, dependencies=[Depends(require_permissions("attendance:write"))])
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.get(AttendanceRecord, attendance_id)
    if not record or record.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    record.is_deleted = True
    db.commit()
    return MessageResponse(message="Attendance deleted")
