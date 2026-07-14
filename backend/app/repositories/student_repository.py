from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.repositories.base import BaseRepository


class StudentRepository(BaseRepository[Student]):
    def __init__(self, session: Session):
        super().__init__(session, Student)

    def search(self, query: str):
        pattern = f"%{query}%"
        return select(Student).where(
            Student.is_deleted.is_(False),
            or_(
                Student.student_name.ilike(pattern),
                Student.father_name.ilike(pattern),
                Student.parent_name.ilike(pattern),
                Student.admission_number.ilike(pattern),
                Student.phone.ilike(pattern),
                Student.aadhar_number.ilike(pattern),
                Student.class_name.ilike(pattern),
            ),
        )
