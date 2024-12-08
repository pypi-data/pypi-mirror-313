from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import Mapping, final

import pydantic
from typing_extensions import TypeAlias

from oxr._types import Currency


class _FrozenModel(pydantic.BaseModel):
    """A frozen Pydantic model."""

    model_config = {"frozen": True}


@final
class Rates(_FrozenModel):
    """The response for the latest and historical endpoints."""

    time: dt.datetime = pydantic.Field(validation_alias="timestamp")
    base: Currency
    rates: Mapping[Currency, Decimal] = pydantic.Field(
        examples=[{"EUR": Decimal("1.0"), "USD": Decimal("1.1")}]
    )


@final
class ConversionMetadata(_FrozenModel):
    """The metadata for the conversion response."""

    time: dt.datetime = pydantic.Field(validation_alias="timestamp")
    rate: Decimal


@final
class Conversion(_FrozenModel):
    """The response for the convert endpoint."""

    meta: ConversionMetadata
    amount: Decimal = pydantic.Field(validation_alias="response")


@final
class TimeSeries(_FrozenModel):
    """The response for the time series endpoint."""

    start_date: dt.date
    end_date: dt.date
    base: Currency
    rates: Mapping[dt.date, Mapping[Currency, Decimal]]


@final
class OHLCRates(_FrozenModel):
    """Response for rates as a part of the olch endpoint."""

    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    average: Decimal


@final
class OHLC(_FrozenModel):
    """The response for the olhc endpoint."""

    start_time: dt.datetime
    end_time: dt.datetime
    base: Currency
    rates: Mapping[Currency, OHLCRates]


Currencies: TypeAlias = Mapping[Currency, str]
