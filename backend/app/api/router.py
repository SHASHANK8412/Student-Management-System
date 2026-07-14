from fastapi import APIRouter

from app.api.v1.endpoints import attendance, auth, dashboard, fees, payments, reports, search, settings, students, users

api_router = APIRouter()
api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(students.router, prefix="/students", tags=["Students"])
api_v1_router.include_router(fees.router, prefix="/fees", tags=["Fees"])
api_v1_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_v1_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_v1_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_v1_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_v1_router.include_router(search.router, prefix="/search", tags=["Search"])
api_v1_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
