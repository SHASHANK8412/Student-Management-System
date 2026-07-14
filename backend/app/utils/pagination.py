from dataclasses import dataclass
from math import ceil

from pydantic import BaseModel

from app.schemas.common import PaginationMeta


def build_pagination_meta(page: int, page_size: int, total: int) -> PaginationMeta:
    total_pages = ceil(total / page_size) if total else 0
    return PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages)
