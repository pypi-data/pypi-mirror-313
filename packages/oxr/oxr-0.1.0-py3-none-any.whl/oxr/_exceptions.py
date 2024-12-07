from __future__ import annotations

from typing import Final

from oxr.exceptions import (
    Error,
    InvalidAppID,
    InvalidCurrency,
    InvalidDate,
    InvalidDateRange,
    NoAccessError,
)

_EXCEPTION_MAPPING: Final[dict[tuple[int, str], type[Error]]] = {
    (403, "not_allowed"): NoAccessError,
    (401, "invalid_app_id"): InvalidAppID,
    (400, "invalid_currency"): InvalidCurrency,
    (400, "invalid_date"): InvalidDate,
    (400, "invalid_date_range"): InvalidDateRange,
}


def get(code: int, message: str) -> type[Error] | None:
    """Get the error class for the given code and message."""
    return _EXCEPTION_MAPPING.get((code, message), None)
