"""Client for Open Exchange Rates API.

Examples:

```python
import openexchangerates as oxr

client = oxr.Client("YOUR_APP_ID")

# Get the latest exchange rates.
latest = client.latest("USD")

# Get historical exchange rates.
historical = client.historical("2021-01-01")

# Get time series exchange rates.
time_series = client.time_series(dt.date(2021, 1, 1), dt.date(2021, 1, 31))

# Get OHLC exchange rates.
ohlc = client.ohlc(dt.date(2021, 1, 1), dt.date(2021, 1, 31))

# Convert currency.
conversion = client.convert("USD", "EUR", 100)
```
"""

from __future__ import annotations

from oxr.client import Client

__all__ = ["Client"]
