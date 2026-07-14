from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings

settings = get_settings()


def ensure_upload_dir() -> Path:
    path = Path(settings.upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_local_file_url(filename: str) -> str:
    return f"/{settings.upload_dir}/{filename}"


def unique_filename(original_name: str) -> str:
    suffix = Path(original_name).suffix
    return f"{uuid4().hex}{suffix}"
