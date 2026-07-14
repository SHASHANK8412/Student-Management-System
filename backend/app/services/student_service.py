from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.repositories.student_repository import StudentRepository


class StudentService:
    def __init__(self, session: Session):
        self.session = session
        self.students = StudentRepository(session)

    def create(self, student: Student) -> Student:
        self.session.add(student)
        self.session.flush()
        return student

    def update(self, student: Student, payload: dict) -> Student:
        for key, value in payload.items():
            setattr(student, key, value)
        self.session.flush()
        return student

    def list_students(self, search: str | None = None) -> Select:
        if search:
            return self.students.search(search)
        return select(Student).where(Student.is_deleted.is_(False)).order_by(Student.student_name.asc())
