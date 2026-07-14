from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.fee import FeeInvoice, FeeStructure
from app.repositories.base import BaseRepository


class FeeStructureRepository(BaseRepository[FeeStructure]):
    def __init__(self, session: Session):
        super().__init__(session, FeeStructure)


class FeeInvoiceRepository(BaseRepository[FeeInvoice]):
    def __init__(self, session: Session):
        super().__init__(session, FeeInvoice)

    def overdue(self):
        return select(FeeInvoice).where(FeeInvoice.is_deleted.is_(False), FeeInvoice.balance_amount > 0)
