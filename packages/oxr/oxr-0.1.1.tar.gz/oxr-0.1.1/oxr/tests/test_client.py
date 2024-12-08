from __future__ import annotations

import datetime as dt
from decimal import Decimal

import pytest
import responses
from responses import matchers

import oxr

_BASE_RESPONSE = {
    "disclaimer": "https://openexchangerates.org/terms/",
    "license": "https://openexchangerates.org/license/",
    "timestamp": 1717622400,
}


@pytest.fixture
def client() -> oxr.Client:
    return oxr.Client("app_id")


@responses.activate
def test_latest(client: oxr.Client) -> None:
    resp = {
        "base": "USD",
        "rates": {"EUR": 0.85, "JPY": 110.0},
        **_BASE_RESPONSE,
    }
    responses.get(
        "https://openexchangerates.org/api/latest.json",
        json=resp,
        match=[
            matchers.query_param_matcher(
                {"app_id": "app_id", "base": "USD", "show_alternative": False}
            )
        ],
    )
    resp = client.latest()
    assert resp.base == "USD"
    assert resp.rates == {"EUR": Decimal("0.85"), "JPY": Decimal("110.0")}


@responses.activate
def test_historical(client: oxr.Client) -> None:
    resp = {
        "base": "USD",
        "rates": {"EUR": 0.85, "JPY": 110.0},
        **_BASE_RESPONSE,
    }
    responses.get(
        "https://openexchangerates.org/api/historical/2021-01-01.json",
        json=resp,
        match=[
            matchers.query_param_matcher(
                {
                    "app_id": "app_id",
                    "base": "USD",
                    "show_alternative": False,
                    "symbols": "EUR,JPY",
                }
            )
        ],
    )
    resp = client.historical(dt.date(2021, 1, 1), symbols=["EUR", "JPY"])
    assert resp.base == "USD"
    assert resp.rates == {"EUR": Decimal("0.85"), "JPY": Decimal("110.0")}


@responses.activate
def test_time_series(client: oxr.Client) -> None:
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
    responses.get(
        "https://openexchangerates.org/api/time-series.json",
        json=resp,
        match=[
            matchers.query_param_matcher(
                {
                    "app_id": "app_id",
                    "base": "USD",
                    "show_alternative": False,
                    "symbols": "EUR,JPY",
                    "start": "2021-01-01",
                    "end": "2021-01-31",
                }
            )
        ],
    )
    resp = client.time_series(dt.date(2021, 1, 1), dt.date(2021, 1, 31), symbols=["EUR", "JPY"])
    assert resp.start_date == dt.date(2021, 1, 1)
    assert resp.end_date == dt.date(2021, 1, 31)
    assert resp.base == "USD"
    assert resp.rates == {
        dt.date(2021, 1, 1): {"EUR": Decimal("0.85"), "JPY": Decimal("110.0")},
        dt.date(2021, 1, 2): {"EUR": Decimal("0.86"), "JPY": Decimal("111.0")},
    }


@responses.activate
def test_convert(client: oxr.Client) -> None:
    resp = {
        "query": {"from": "USD", "to": "EUR", "amount": 100.0},
        "meta": {"rate": 0.85, "timestamp": 1717622400},
        "response": 85.0,
        **_BASE_RESPONSE,
    }
    responses.get(
        "https://openexchangerates.org/api/convert.json",
        json=resp,
        match=[
            matchers.query_param_matcher(
                {"app_id": "app_id", "from": "USD", "to": "EUR", "amount": 100.0}
            )
        ],
    )
    resp = client.convert(100, "USD", "EUR")
    assert resp.meta.rate == Decimal("0.85")
    assert resp.amount == Decimal("85.0")
    assert resp.meta.time == dt.datetime(2024, 6, 5, 21, 20, tzinfo=dt.timezone.utc)


@responses.activate
def test_ohlc(client: oxr.Client) -> None:
    resp = {
        "base": "USD",
        "start_time": "2021-01-01T00:00:00",
        "end_time": "2021-01-01T23:59:59Z",
        "rates": {"USD": {"open": 0.85, "high": 0.86, "low": 0.84, "close": 0.85, "average": 0.85}},
        **_BASE_RESPONSE,
    }
    responses.get(
        "https://openexchangerates.org/api/ohlc.json",
        json=resp,
        match=[
            matchers.query_param_matcher(
                {
                    "app_id": "app_id",
                    "base": "USD",
                    "show_alternative": False,
                    "period": "1d",
                    "start_time": "2021-01-01T00:00:00",
                    "symbols": "USD",
                }
            )
        ],
    )
    resp = client.ohlc(dt.datetime(2021, 1, 1), "1d", symbols=["USD"])
    assert resp.base == "USD"
    assert resp.start_time == dt.datetime(2021, 1, 1, 0, 0)
    assert resp.rates["USD"].open == Decimal("0.85")
    assert resp.rates["USD"].high == Decimal("0.86")
    assert resp.rates["USD"].low == Decimal("0.84")
    assert resp.rates["USD"].close == Decimal("0.85")
    assert resp.rates["USD"].average == Decimal("0.85")
