from __future__ import annotations

from typing import ClassVar


class Error(Exception):
    """Base exception class for `openexchangerates`."""

    code: ClassVar[int | None] = None


class InvalidCurrency(Error):
    """Raised when an invalid currency is provided."""

    code = 400


class InvalidDate(Error):
    """Raised when an invalid date is provided."""

    code = 400


class InvalidDateRange(Error):
    """Raised when an invalid date range is provided."""

    code = 400


class InvalidAppID(Error):
    """Raised when an invalid App ID is provided."""

    code = 401


class NoAccessError(Error):
    """Raised when the App ID does not have access to the requested resource or endpoint."""

    code = 403
