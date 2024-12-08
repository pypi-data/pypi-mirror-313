from __future__ import annotations

import abc
import datetime as dt
from collections.abc import Awaitable
from decimal import Decimal
from typing import Any, Final, Iterable

from oxr import responses
from oxr._types import Currency, Endpoint, Period

_BASE_URL: Final = "https://openexchangerates.org/api"


class BaseClient(abc.ABC):
    def __init__(
        self,
        app_id: str,
        *,
        base: Currency = "USD",
        base_url: str = _BASE_URL,
        timeout: float = 5,
    ) -> None:
        """Initialize the client.

        Args:
            app_id: The app id for the API.
            base: The base currency to use across the client.
            base_url: The base URL for the API.
                Unless you are using a custom endpoint, or for testing
                purposes, you should not need to change this.
            timeout: The request timeout in seconds.
        """
        self._app_id = app_id
        self._base = base
        self._base_url = base_url
        self._timeout = timeout

    def _prepare_url(self, endpoint: Endpoint, path_params: list[str] | None) -> str:
        base_url = f"{self._base_url}/{endpoint}"
        url_paths = "/".join(path_params) if path_params else ""
        return f"{base_url}/{url_paths}.json" if url_paths else f"{base_url}.json"

    @abc.abstractmethod
    def _get(
        self,
        endpoint: Endpoint,
        query_params: dict[str, Any],
        path_params: list[str] | None = None,
    ) -> dict[str, Any] | Awaitable[dict[str, Any]]:
        """Make a GET request to the API."""

    @abc.abstractmethod
    def latest(
        self,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.Rates | Awaitable[responses.Rates]:
        """Get the latest exchange rates.

        Args:
            base: The base currency.
            symbols: The target currencies.
            show_alternative: Whether to show alternative currencies.
                Such as black market and digital currency rates.
        """

    @abc.abstractmethod
    def currencies(self) -> responses.Currencies | Awaitable[responses.Currencies]:
        """Get a mapping of available currency codes to names."""

    @abc.abstractmethod
    def historical(
        self,
        date: dt.date,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.Rates | Awaitable[responses.Rates]:
        """Get historical exchange rates.

        Args:
            date: The date of the rates.
            base: The base currency.
            symbols: The target currencies.
            show_alternative: Whether to show alternative currencies.
                Such as black market and digital currency rates.
        """

    @abc.abstractmethod
    def convert(
        self,
        amount: float | Decimal,
        from_: str,
        to: str,
    ) -> responses.Conversion | Awaitable[responses.Conversion]:
        """Convert an amount between two currencies.

        Args:
            amount: The amount to convert.
            from_: The source currency.
            to: The target currency.
            date: The date of the rates to use.
        """

    @abc.abstractmethod
    def time_series(
        self,
        start: dt.date,
        end: dt.date,
        symbols: Iterable[Currency] | None = None,
        base: str | None = None,
        show_alternative: bool = False,
    ) -> responses.TimeSeries | Awaitable[responses.TimeSeries]:
        """Get historical exchange rates for a range of dates.

        Args:
            start: The start date of the range.
            end: The end date of the range.
            symbols: The target currencies.
            base: The base currency.
            show_alternative: Whether to show alternative currencies.
                Such as black market and digital currency rates.
        """

    @abc.abstractmethod
    def ohlc(
        self,
        start_time: dt.datetime,
        period: Period,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.OHLC | Awaitable[responses.OHLC]:
        """Get the latest open, low, high, and close rates for a currency.

        Args:
            base: The base currency.
            symbols: The target currencies.
            show_alternative: Whether to show alternative currencies.
                Such as black market and digital currency rates.
        """
