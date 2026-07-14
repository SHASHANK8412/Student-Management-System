# Installation Guide

## Backend

1. Open `backend/`.
2. Create a Python 3.13 environment.
3. Install packages with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and update the values.
5. Run `alembic upgrade head`.
6. Start the app with `uvicorn app.main:app --reload`.

## Frontend

1. Open `frontend/`.
2. Run `npm install`.
3. Set `VITE_API_BASE_URL` in a local `.env` file.
4. Start the dev server with `npm run dev`.

## Docker

Run `docker compose up --build` from the repository root to start PostgreSQL, the API, and the frontend container.
