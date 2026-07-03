from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    errors: Any = None
    timestamp: datetime = Field(default_factory=utc_now)


def success_response(
    message: str,
    data: T | None = None,
) -> ApiResponse[T]:
    return ApiResponse(
        success=True,
        message=message,
        data=data,
        errors=None,
    )


def error_response(
    message: str,
    errors: Any = None,
) -> ApiResponse[None]:
    return ApiResponse(
        success=False,
        message=message,
        data=None,
        errors=errors,
    )
