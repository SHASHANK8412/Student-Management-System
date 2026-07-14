# Troubleshooting Guide

## Backend does not start

- Confirm the database URL points to a reachable PostgreSQL instance.
- Verify that `SECRET_KEY` is set.
- Check that the required Python packages are installed.

## Frontend cannot reach the API

- Ensure `VITE_API_BASE_URL` ends with `/api/v1`.
- Confirm CORS allows the frontend origin.
- Check browser network logs for 401 or 500 responses.

## Migrations fail

- Confirm the `alembic.ini` connection string matches `.env`.
- Run migrations from the `backend/` directory.
- Verify the PostgreSQL user has schema creation privileges.

## Login fails after deployment

- Check that the access token and refresh token are stored in local storage.
- Ensure cookie or header policies are not stripping the `Authorization` header.
