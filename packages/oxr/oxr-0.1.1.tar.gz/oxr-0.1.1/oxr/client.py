from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import Any, Iterable

import pydantic
import requests

from oxr import _exceptions, exceptions, responses
from oxr._base import BaseClient
from oxr._types import Currency, Endpoint, Period


class Client(BaseClient):
    """A client for the Open Exchange Rates API."""

    def _get(
        self,
        endpoint: Endpoint,
        query_params: dict[str, Any],
        path_params: list[str] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request to the API."""
        url = self._prepare_url(endpoint, path_params)
        response = requests.get(
            url,
            params={"app_id": self._app_id, **query_params},
            timeout=self._timeout,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            msg = response.json().get("message", "")
            exc = _exceptions.get(response.status_code, msg)
            if exc is not None:
                raise exc from error
            raise exceptions.Error(error) from None  # pragma: no cover

        return response.json()

    def currencies(self) -> responses.Currencies:
        currency_validator = pydantic.TypeAdapter(responses.Currencies)
        return currency_validator.validate_python(self._get("currencies", {}))

    def latest(
        self,
        base: str | None = None,
        symbols: Iterable[Currency] | None = None,
        show_alternative: bool = False,
    ) -> responses.Rates:
        params = {"base": base or self._base, "show_alternative": show_alternative}
        if symbols is not None:
            params["symbols"] = ",".join(symbols)

        self._get("latest", params)
        return responses.Rates.model_validate(self._get("latest", params))

    def historical(
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
        return responses.Rates.model_validate(
            self._get("historical", params, path_params=[date.isoformat()]),
        )

    def convert(
        self,
        amount: float | Decimal,
        from_: str,
        to: str,
    ) -> responses.Conversion:
        params = {"from": from_, "to": to, "amount": float(amount)}
        return responses.Conversion.model_validate(self._get("convert", params))

    def time_series(
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
        return responses.TimeSeries.model_validate(self._get("time-series", params))

    def ohlc(
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
        return responses.OHLC.model_validate(self._get("ohlc", params))

    def usage(self) -> dict[str, Any]:
        return self._get("usage", {})
