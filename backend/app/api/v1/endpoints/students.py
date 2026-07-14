from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.student import Student
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate

router = APIRouter()


@router.get("", response_model=PaginatedResponse[StudentRead], dependencies=[Depends(require_permissions("students:read"))])
def list_students(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), search: str | None = None, class_name: str | None = None, section: str | None = None, status: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.is_deleted.is_(False))
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            Student.student_name.ilike(pattern)
            | Student.father_name.ilike(pattern)
            | Student.parent_name.ilike(pattern)
            | Student.admission_number.ilike(pattern)
            | Student.phone.ilike(pattern)
            | Student.aadhar_number.ilike(pattern)
            | Student.class_name.ilike(pattern)
        )
    if class_name:
        stmt = stmt.where(Student.class_name == class_name)
    if section:
        stmt = stmt.where(Student.section == section)
    if status:
        stmt = stmt.where(Student.status == status)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(Student.student_name.asc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("students:write"))])
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.admission_number == payload.admission_number).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admission number already exists")
    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/{student_id}", response_model=StudentRead, dependencies=[Depends(require_permissions("students:read"))])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student or student.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.patch("/{student_id}", response_model=StudentRead, dependencies=[Depends(require_permissions("students:write"))])
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student or student.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", response_model=MessageResponse, dependencies=[Depends(require_permissions("students:write"))])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student or student.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student.is_deleted = True
    db.commit()
    return MessageResponse(message="Student deleted")
