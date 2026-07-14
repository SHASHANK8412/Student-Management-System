from pydantic import BaseModel


class DashboardKPI(BaseModel):
    total_students: int
    active_students: int
    total_collection: float
    pending_fees: float
    todays_collection: float
    monthly_revenue: float
    students_due_today: int
    overdue_students: int


class SeriesPoint(BaseModel):
    label: str
    value: float


class DashboardResponse(BaseModel):
    kpi: DashboardKPI
    monthly_collection: list[SeriesPoint]
    class_wise_revenue: list[SeriesPoint]
    payment_trends: list[SeriesPoint]
    due_distribution: list[SeriesPoint]
    recent_activity: list[str]
    upcoming_due_dates: list[str]
