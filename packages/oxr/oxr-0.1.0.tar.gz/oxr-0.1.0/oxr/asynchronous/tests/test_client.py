from __future__ import annotations

import datetime as dt
import urllib.parse
from typing import Any

import pytest
from aioresponses import aioresponses

import oxr.asynchronous

_BASE_RESPONSE = {
    "disclaimer": "https://openexchangerates.org/terms/",
    "license": "https://openexchangerates.org/license/",
}


@pytest.fixture
def client() -> oxr.asynchronous.Client:
    return oxr.asynchronous.Client("app_id")


def _construct_url(base_url: str, params: dict[str, Any]) -> str:
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"


@pytest.mark.asyncio
async def test_latest(client: oxr.asynchronous.Client):
    resp = {
        "base": "USD",
        "rates": {"EUR": 0.85, "JPY": 110.0},
        **_BASE_RESPONSE,
    }
    url = _construct_url(
        "https://openexchangerates.org/api/latest.json",
        {"app_id": "app_id", "base": "USD", "show_alternative": "false"},
    )
    with aioresponses() as m:
        m.get(url, payload=resp)  # type: ignore
        response = await client.latest()
        assert response["base"] == "USD"
        assert response["rates"] == {"EUR": 0.85, "JPY": 110.0}


@pytest.mark.asyncio
async def test_historical(client: oxr.asynchronous.Client):
    resp = {
        "base": "USD",
        "rates": {"EUR": 0.85, "JPY": 110.0},
        **_BASE_RESPONSE,
    }
    url = _construct_url(
        "https://openexchangerates.org/api/historical/2021-01-01.json",
        {
            "app_id": "app_id",
            "base": "USD",
            "show_alternative": "false",
            "symbols": "EUR,JPY",
        },
    )
    with aioresponses() as m:
        m.get(url, payload=resp)  # type: ignore
        response = await client.historical(dt.date(2021, 1, 1), symbols=["EUR", "JPY"])
        assert response["base"] == "USD"
        assert response["rates"] == {"EUR": 0.85, "JPY": 110.0}


@pytest.mark.asyncio
async def test_time_series(client: oxr.asynchronous.Client):
    resp = {
        "base": "USD",
        "start_date": "2021-01-01",
        "end_date": "2021-01-31",
        "rates": {
            "2021-01-01": {"EUR": 0.85, "JPY": 110.0},
            "2021-01-02": {"EUR": 0.86, "JPY": 111.0},
        },
        **_BASE_RESPONSE,
    }
    url = _construct_url(
        "https://openexchangerates.org/api/time-series.json",
        {
            "app_id": "app_id",
            "base": "USD",
            "show_alternative": "false",
            "symbols": "EUR,JPY",
            "start": "2021-01-01",
            "end": "2021-01-31",
        },
    )
    with aioresponses() as m:
        m.get(url, payload=resp)  # type: ignore
        response = await client.time_series(
            dt.date(2021, 1, 1), dt.date(2021, 1, 31), symbols=["EUR", "JPY"]
        )
        assert response["start_date"] == "2021-01-01"
        assert response["end_date"] == "2021-01-31"
        assert response["base"] == "USD"
        assert response["rates"] == {
            "2021-01-01": {"EUR": 0.85, "JPY": 110.0},
            "2021-01-02": {"EUR": 0.86, "JPY": 111.0},
        }


@pytest.mark.asyncio
async def test_convert(client: oxr.asynchronous.Client):
    resp = {
        "query": {"from": "USD", "to": "EUR", "amount": 100},
        "meta": {"rate": 0.85},
        "response": 85.0,
        **_BASE_RESPONSE,
    }
    url = _construct_url(
        "https://openexchangerates.org/api/convert.json",
        {"app_id": "app_id", "from": "USD", "to": "EUR", "amount": 100},
    )
    with aioresponses() as m:
        m.get(url, payload=resp)  # type: ignore
        response = await client.convert(100, "USD", "EUR")
        assert response["query"] == {"from": "USD", "to": "EUR", "amount": 100}
        assert response["meta"] == {"rate": 0.85}
        assert response["response"] == 85.0


@pytest.mark.asyncio
async def test_ohlc(client: oxr.asynchronous.Client):
    resp = {
        "base": "USD",
        "start_time": "2021-01-01T00:00:00",
        "end_time": "2021-01-01T23:59:59Z",
        "rates": {"USD": {"open": 0.85, "high": 0.86, "low": 0.84, "close": 0.85, "average": 0.85}},
        **_BASE_RESPONSE,
    }
    url = _construct_url(
        "https://openexchangerates.org/api/ohlc.json",
        {
            "app_id": "app_id",
            "base": "USD",
            "show_alternative": "false",
            "period": "1d",
            "start_time": "2021-01-01T00:00:00",
            "symbols": "USD",
        },
    )
    with aioresponses() as m:
        m.get(url, payload=resp)  # type: ignore
        response = await client.ohlc(dt.datetime(2021, 1, 1), "1d", symbols=["USD"])
        assert response["base"] == "USD"
        assert response["start_time"] == "2021-01-01T00:00:00"
        assert response["rates"] == {
            "USD": {"open": 0.85, "high": 0.86, "low": 0.84, "close": 0.85, "average": 0.85}
        }
