from __future__ import annotations

from typing import Literal

from typing_extensions import TypeAlias

# Valid API endpoints.
Endpoint: TypeAlias = Literal[
    "latest",
    "historical",
    "currencies",
    "convert",
    "time-series",
    "ohlc",
    "usage",
]


# Valid periods for the OHLC endpoint.
Period: TypeAlias = Literal["1m", "5m", "15m", "30m", "1h", "12h", "1d", "1w", "1mo"]

# Valid currency codes.
Currency: TypeAlias = str
