from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session: Session):
        super().__init__(session, Payment)

    def by_student(self, student_id: int):
        return select(Payment).where(Payment.student_id == student_id, Payment.is_deleted.is_(False)).order_by(Payment.payment_date.desc())
