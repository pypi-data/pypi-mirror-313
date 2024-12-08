"""Test endpoints that don't require a paid plan."""

from __future__ import annotations

import datetime as dt
import os

import pytest

import oxr.asynchronous
import oxr.exceptions


@pytest.fixture
def client() -> oxr.asynchronous.Client:
    app_id = os.getenv("OXR_APP_ID")
    if not app_id:
        pytest.skip("OXR_APP_ID is not set")
    return oxr.asynchronous.Client(app_id)


@pytest.mark.asyncio
async def test_latest(client: oxr.asynchronous.Client) -> None:
    resp = await client.latest()
    assert resp.base == "USD"
    assert "EUR" in resp.rates
    assert "JPY" in resp.rates

    # Narrow the symbols.
    resp = await client.latest(symbols=["EUR"])
    assert resp.base == "USD"
    assert "EUR" in resp.rates
    assert len(resp.rates) == 1


@pytest.mark.asyncio
async def test_historical(client: oxr.asynchronous.Client) -> None:
    resp = await client.historical(dt.date(2021, 1, 1))
    assert resp.base == "USD"
    assert "EUR" in resp.rates
    assert "JPY" in resp.rates

    # Narrow the symbols.
    resp = await client.historical(dt.date(2021, 1, 1), symbols=["EUR"])
    assert resp.base == "USD"
    assert "EUR" in resp.rates
    assert len(resp.rates) == 1


@pytest.mark.asyncio
async def test_currencies(client: oxr.asynchronous.Client) -> None:
    resp = await client.currencies()
    assert "USD" in resp
    assert "EUR" in resp
    assert "JPY" in resp
    assert "ZAR" in resp


@pytest.mark.asyncio
async def test_usage(client: oxr.asynchronous.Client) -> None:
    resp = await client.usage()
    assert "status" in resp
    assert "plan" in resp["data"]
    assert "usage" in resp["data"]
    assert "daily_average" in resp["data"]["usage"]


@pytest.mark.asyncio
async def test_session_static(client: oxr.asynchronous.Client) -> None:
    async with client as async_client:
        session = async_client._session  # type: ignore
        assert session is None
        await async_client.usage()
        session = async_client._session  # type: ignore
        await async_client.currencies()
        assert async_client._session is session  # type: ignore


@pytest.mark.asyncio
async def test_no_access(client: oxr.asynchronous.Client):
    """Test that we properly re-raise 403 errors as `NoAccessError`."""
    with pytest.raises(oxr.exceptions.NoAccessError):
        await client.ohlc(dt.datetime(2021, 1, 1), "1d", symbols=["USD"])
