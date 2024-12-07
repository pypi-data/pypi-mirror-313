from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Iterable
from types import TracebackType
from typing import Any, cast

import aiohttp
from typing_extensions import Self

from oxr import _exceptions, exceptions, responses
from oxr._base import BaseClient
from oxr._types import Currency, Endpoint, Period


def _encode_params(params: dict[str, Any]) -> dict[str, Any]:
    """yarl does not encode booleans as strings."""
    return {
        key: "true" if value is True else "false" if value is False else value
        for key, value in params.items()
    }


class Client(BaseClient, contextlib.AbstractAsyncContextManager["Client"]):
    """A asynchronous client for the Open Exchange Rates API."""

    _session: aiohttp.ClientSession | None = None

    async def _get(
        self,
        endpoint: Endpoint,
        query_params: dict[str, Any],
        path_params: list[str] | None = None,
    ) -> dict[str, Any]:
        url = self._prepare_url(endpoint, path_params)
        session = self._get_session()
        async with session.get(
            url,
            params=_encode_params({"app_id": self._app_id, **query_params}),
        ) as response:
            resp_json = await response.json()
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError as error:
                msg = resp_json.get("message", "")
                print("Error message is", msg)
                exc = _exceptions.get(error.status, msg)
                if exc is not None:
                    raise exc from error
                raise exceptions.Error(error) from None  # pragma: no cover
            return resp_json

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def currencies(self) -> responses.Currencies:
        """Get a list of available currencies."""
        return cast(responses.Currencies, await self._get("currencies", {}))

    async def latest(
        self,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.Rates:
        """Get the latest exchange rates.

        Args:
            base: The base currency.
            symbols: The target currencies.
            show_alternative: Whether to show alternative currencies.
                Such as black market and digital currency rates.
        """
        params = {
            "app_id": self._app_id,
            "base": base or self._base,
            "show_alternative": show_alternative,
        }
        if symbols is not None:
            params["symbols"] = ",".join(symbols)
        return cast(responses.Rates, await self._get("latest", params))

    async def historical(
        self,
        date: dt.date,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.Rates:
        params = {
            "base": base or self._base,
            "show_alternative": show_alternative,
        }
        if symbols is not None:
            params["symbols"] = ",".join(symbols)
        return cast(
            responses.Rates, await self._get("historical", params, path_params=[date.isoformat()])
        )

    async def convert(
        self,
        amount: float,
        from_: str,
        to: str,
    ) -> responses.Conversion:
        params = {"from": from_, "to": to, "amount": amount}
        return cast(responses.Conversion, await self._get("convert", params))

    async def time_series(
        self,
        start: dt.date,
        end: dt.date,
        symbols: Iterable[Currency] | None = None,
        base: str | None = None,
        show_alternative: bool = False,
    ) -> responses.TimeSeries:
        params = {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "show_alternative": show_alternative,
        }
        params["base"] = base or self._base
        if symbols is not None:
            params["symbols"] = ",".join(symbols)
        return cast(responses.TimeSeries, await self._get("time-series", params))

    async def ohlc(
        self,
        start_time: dt.datetime,
        period: Period,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.OHLC:
        params = {
            "start_time": start_time.isoformat(),
            "period": period,
            "show_alternative": show_alternative,
        }
        params["base"] = base or self._base
        if symbols is not None:
            params["symbols"] = ",".join(symbols)
        return cast(responses.OHLC, await self._get("ohlc", params))

    async def usage(self) -> dict[str, Any]:
        """Get the usage statistics for the API key."""
        return await self._get("usage", {})

    async def __aenter__(self) -> Self:
        """Entire client session."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit client session."""
        if self._session is not None:
            return await self.close()

    async def close(self) -> None:
        """Close the client session."""
        if self._session is not None:
            await self._session.close()
            self._session = None
