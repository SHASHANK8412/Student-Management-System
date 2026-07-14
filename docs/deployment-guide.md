# Deployment Guide

## Frontend on Vercel

- Connect the repository to Vercel.
- Set the project root to `frontend/`.
- Add `VITE_API_BASE_URL` to the environment variables.
- Deploy from the `main` branch.

## Backend on Render

- Create a web service from `backend/`.
- Use the build command `pip install -r requirements.txt`.
- Use the start command `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Add `DATABASE_URL`, `SECRET_KEY`, and the email settings.

## PostgreSQL on Neon

- Provision a Neon database.
- Copy the connection string into `DATABASE_URL`.
- Run Alembic migrations after deployment.

## HTTPS and custom domain

- Point DNS to Vercel and Render as appropriate.
- Enable managed TLS in both platforms.
- Update `CORS_ORIGINS` and `FRONTEND_URL` to the production domain.
