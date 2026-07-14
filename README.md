# Student Fee Management System

A production-oriented student fee management platform for schools, colleges, and tuition centers. The application is split into a FastAPI backend, a React 19 + Vite frontend, and PostgreSQL persistence.

## Stack

- Frontend: React 19, Vite, TypeScript, Tailwind CSS, React Router, Axios, React Hook Form, Zod, TanStack Query, Framer Motion, Recharts, React Hot Toast
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, JWT, bcrypt
- Database: PostgreSQL
- Deployment: Docker, GitHub Actions, Vercel, Render, Neon

## What is included

- Secure login, refresh tokens, password reset, and email verification flow
- Role-based access control for Super Admin, Principal, Accountant, and Receptionist
- Student, fee, payment, attendance, dashboard, reports, settings, and global search modules
- Dark/light UI with glassmorphism, responsive layout, and animated dashboard cards
- Dockerfiles, docker-compose, Nginx config, and CI/CD workflow
- Alembic setup and an initial schema migration

## Repository Layout

- `backend/` FastAPI app, SQLAlchemy models, services, repositories, Alembic, and tests
- `frontend/` React app, reusable UI, routes, API client, and dashboard pages
- `docs/` installation, development, API, deployment, and troubleshooting guides
- `.github/workflows/ci.yml` GitHub Actions pipeline
- `docker-compose.yml` local stack orchestration

## Quick Start

### Backend

1. Create a virtual environment.
2. Install dependencies from `backend/requirements.txt`.
3. Set the variables from `.env.example`.
4. Run migrations with Alembic.
5. Start the API with `uvicorn app.main:app --reload` from `backend/`.

### Frontend

1. Install dependencies in `frontend/`.
2. Set `VITE_API_BASE_URL`.
3. Run `npm run dev`.

### Docker

Run `docker compose up --build` from the repository root.

## API

Swagger UI is available at `/docs` when the backend is running. OpenAPI is generated automatically by FastAPI.

## Deployment

- Frontend: deploy the `frontend/` app to Vercel.
- Backend: deploy the `backend/` app to Render.
- Database: provision PostgreSQL on Neon.
- Local containers: use `docker compose` and the provided Nginx config.

## Notes

- The codebase uses soft delete columns and timestamp audit fields on core models.
- The backend seeds the four required roles on startup.
- The frontend expects the backend API to be available under `/api/v1`.
