"""Test endpoints that don't require a paid plan."""

from __future__ import annotations

import datetime as dt
import os

import pytest

import oxr
import oxr.exceptions


@pytest.fixture
def client() -> oxr.Client:
    app_id = os.getenv("OXR_APP_ID")
    if not app_id:
        pytest.skip("OXR_APP_ID is not set")
    return oxr.Client(app_id)


def test_latest(client: oxr.Client) -> None:
    resp = client.latest()
    assert resp["base"] == "USD"
    assert "EUR" in resp["rates"]
    assert "JPY" in resp["rates"]

    # Narrow the symbols.
    resp = client.latest(symbols=["EUR"])
    assert resp["base"] == "USD"
    assert "EUR" in resp["rates"]
    assert len(resp["rates"]) == 1


def test_historical(client: oxr.Client) -> None:
    resp = client.historical(dt.date(2021, 1, 1))
    assert resp["base"] == "USD"
    assert "EUR" in resp["rates"]
    assert "JPY" in resp["rates"]

    # Narrow the symbols.
    resp = client.historical(dt.date(2021, 1, 1), symbols=["EUR"])
    assert resp["base"] == "USD"
    assert "EUR" in resp["rates"]
    assert len(resp["rates"]) == 1


def test_currencies(client: oxr.Client) -> None:
    resp = client.currencies()
    assert "USD" in resp
    assert "EUR" in resp
    assert "JPY" in resp
    assert "ZAR" in resp


def test_usage(client: oxr.Client) -> None:
    resp = client.usage()
    assert "status" in resp
    assert "plan" in resp["data"]
    assert "usage" in resp["data"]
    assert "daily_average" in resp["data"]["usage"]


def test_no_access(client: oxr.Client) -> None:
    with pytest.raises(oxr.exceptions.NoAccessError):
        client.ohlc(dt.datetime(2021, 1, 1), "1d", symbols=["USD"])
