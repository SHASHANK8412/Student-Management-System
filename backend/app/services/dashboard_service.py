from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.attendance import AttendanceRecord
from app.models.fee import FeeInvoice
from app.models.payment import Payment
from app.models.student import Student
from app.schemas.dashboard import DashboardKPI, DashboardResponse, SeriesPoint


class DashboardService:
    def __init__(self, session: Session):
        self.session = session

    def build(self) -> DashboardResponse:
        total_students = self.session.scalar(select(func.count(Student.id)).where(Student.is_deleted.is_(False))) or 0
        active_students = self.session.scalar(select(func.count(Student.id)).where(Student.is_deleted.is_(False), Student.status == "Active")) or 0
        total_collection = self.session.scalar(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.is_deleted.is_(False))) or 0
        pending_fees = self.session.scalar(select(func.coalesce(func.sum(FeeInvoice.balance_amount), 0)).where(FeeInvoice.is_deleted.is_(False), FeeInvoice.balance_amount > 0)) or 0
        todays_collection = self.session.scalar(select(func.coalesce(func.sum(Payment.amount), 0)).where(func.date(Payment.payment_date) == func.current_date())) or 0
        monthly_revenue = total_collection
        students_due_today = self.session.scalar(select(func.count(FeeInvoice.id)).where(FeeInvoice.is_deleted.is_(False), FeeInvoice.due_date == func.current_date(), FeeInvoice.balance_amount > 0)) or 0
        overdue_students = self.session.scalar(select(func.count(FeeInvoice.id)).where(FeeInvoice.is_deleted.is_(False), FeeInvoice.balance_amount > 0, FeeInvoice.due_date < func.current_date())) or 0

        kpi = DashboardKPI(
            total_students=int(total_students),
            active_students=int(active_students),
            total_collection=float(total_collection),
            pending_fees=float(pending_fees),
            todays_collection=float(todays_collection),
            monthly_revenue=float(monthly_revenue),
            students_due_today=int(students_due_today),
            overdue_students=int(overdue_students),
        )
        return DashboardResponse(
            kpi=kpi,
            monthly_collection=[SeriesPoint(label="Jan", value=0), SeriesPoint(label="Feb", value=0), SeriesPoint(label="Mar", value=0)],
            class_wise_revenue=[SeriesPoint(label="Class 10", value=0), SeriesPoint(label="Class 9", value=0)],
            payment_trends=[SeriesPoint(label="Cash", value=0), SeriesPoint(label="UPI", value=0)],
            due_distribution=[SeriesPoint(label="Paid", value=0), SeriesPoint(label="Partial", value=0), SeriesPoint(label="Overdue", value=0)],
            recent_activity=[],
            upcoming_due_dates=[],
        )
