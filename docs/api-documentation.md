# API Documentation

## Authentication

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `POST /api/v1/auth/verify-email`

## Core modules

- Students: `GET/POST/PATCH/DELETE /api/v1/students`
- Fees: `GET/POST /api/v1/fees/structures`, `GET/POST /api/v1/fees/invoices`
- Payments: `GET/POST /api/v1/payments`, `POST /api/v1/payments/refunds`
- Attendance: `GET/POST/DELETE /api/v1/attendance`
- Reports: `GET /api/v1/reports/collection`, `GET /api/v1/reports/pending-fees`, `GET /api/v1/reports/student-ledger`
- Settings: `GET/POST /api/v1/settings/*`
- Search: `GET /api/v1/search/global?q=...`
- Dashboard: `GET /api/v1/dashboard`

## Authorization

Every protected endpoint uses JWT authentication and permission checks derived from the signed-in user role.
