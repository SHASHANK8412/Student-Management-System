from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.router import api_v1_router
from app.core.config import get_settings
from app.core.database import Base, engine, SessionLocal
from app.core.permissions import ROLE_ACCOUNTANT, ROLE_PRINCIPAL, ROLE_RECEPTIONIST, ROLE_SUPER_ADMIN, permissions_for_role
from app.models.user import Role
from app.core.security import create_password_hash
from app.models.user import Role, User

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.rate_limit_per_minute}/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_roles = {role.name for role in db.query(Role).all()}
        seeded = [
            (ROLE_SUPER_ADMIN, "Full system access"),
            (ROLE_PRINCIPAL, "Principal access"),
            (ROLE_ACCOUNTANT, "Accounting access"),
            (ROLE_RECEPTIONIST, "Reception access"),
        ]
        for role_name, description in seeded:
            if role_name not in existing_roles:
                db.add(Role(name=role_name, description=description, permissions=permissions_for_role(role_name)))
        db.commit()

        admin_role = db.query(Role).filter(Role.name == ROLE_SUPER_ADMIN).one()
        admin_user = db.query(User).filter(User.email == settings.default_admin_email).one_or_none()
        if admin_user is None:
            db.add(
                User(
                    full_name=settings.default_admin_full_name,
                    email=settings.default_admin_email,
                    phone=None,
                    password_hash=create_password_hash(settings.default_admin_password),
                    role_id=admin_role.id,
                    is_active=True,
                    is_verified=True,
                )
            )
        else:
            admin_user.full_name = settings.default_admin_full_name
            admin_user.password_hash = create_password_hash(settings.default_admin_password)
            admin_user.role_id = admin_role.id
            admin_user.is_active = True
            admin_user.is_verified = True
        db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", default_response_class=ORJSONResponse, lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(api_v1_router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response


@app.get("/")
def root():
    return {"message": "Student Fee Management System API"}


@app.get("/health")
def health():
    return {"status": "ok"}
