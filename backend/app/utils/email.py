from app.core.config import get_settings

settings = get_settings()


def build_verification_email(link: str) -> str:
    return f"Please verify your email by visiting: {link}"


def build_password_reset_email(link: str) -> str:
    return f"Reset your password using this link: {link}"
