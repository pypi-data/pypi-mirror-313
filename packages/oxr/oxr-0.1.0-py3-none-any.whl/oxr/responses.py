from __future__ import annotations

from typing import TypedDict

from typing_extensions import TypeAlias

from oxr._types import Currency


class _Base(TypedDict):
    """The base response from the API."""

    disclaimer: str
    license: str


class Rates(_Base):
    """The response for the latest and historical endpoints."""

    timestamp: int
    base: Currency
    rates: dict[Currency, float]


# Functional typed dict to use 'from' as a key.
_ConversionRequest = TypedDict(
    "_ConversionRequest",
    {"query": str, "from": Currency, "to": Currency, "amount": float},
)


class _ConversionMeta(TypedDict):
    timestamp: int
    rate: float


class Conversion(_Base):
    """The response for the convert endpoint."""

    query: _ConversionRequest
    meta: _ConversionMeta
    response: float


class TimeSeries(_Base):
    """The response for the time series endpoint."""

    start_date: str
    end_date: str
    base: Currency
    rates: dict[str, dict[Currency, float]]


class _OHLCRates(TypedDict):
    open: float
    high: float
    low: float
    close: float
    average: float


class OHLC(_Base):
    """The response for the olhc endpoint."""

    start_time: str
    end_time: str
    base: Currency
    rates: dict[Currency, _OHLCRates]


Currencies: TypeAlias = "dict[Currency, str]"
