# Developer Guide

## Backend structure

- `app/core`: config, database, security, and authorization helpers
- `app/models`: SQLAlchemy ORM models
- `app/schemas`: Pydantic request and response contracts
- `app/repositories`: persistence access helpers
- `app/services`: business logic
- `app/api/v1/endpoints`: FastAPI route handlers
- `alembic/versions`: schema migrations

## Frontend structure

- `src/api`: Axios-based API clients
- `src/components`: reusable layout, charts, and UI primitives
- `src/context`: auth and theme state
- `src/pages`: route-level screens
- `src/styles`: global Tailwind and theme tokens

## Conventions

- Use typed request and response models.
- Keep business rules in services instead of route handlers.
- Use `useQuery` for server state and `react-hook-form` plus `zod` for forms.
