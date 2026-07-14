ROLE_SUPER_ADMIN = "Super Admin"
ROLE_PRINCIPAL = "Principal"
ROLE_ACCOUNTANT = "Accountant"
ROLE_RECEPTIONIST = "Receptionist"

PERMISSIONS = {
    ROLE_SUPER_ADMIN: {
        "users:read",
        "users:write",
        "students:read",
        "students:write",
        "fees:read",
        "fees:write",
        "payments:read",
        "payments:write",
        "attendance:read",
        "attendance:write",
        "reports:read",
        "settings:read",
        "settings:write",
    },
    ROLE_PRINCIPAL: {
        "students:read",
        "students:write",
        "fees:read",
        "payments:read",
        "attendance:read",
        "reports:read",
        "settings:read",
    },
    ROLE_ACCOUNTANT: {
        "students:read",
        "fees:read",
        "fees:write",
        "payments:read",
        "payments:write",
        "reports:read",
    },
    ROLE_RECEPTIONIST: {
        "students:read",
        "students:write",
        "payments:read",
        "payments:write",
        "attendance:read",
        "attendance:write",
    },
}


def permissions_for_role(role: str) -> list[str]:
    return sorted(PERMISSIONS.get(role, set()))
