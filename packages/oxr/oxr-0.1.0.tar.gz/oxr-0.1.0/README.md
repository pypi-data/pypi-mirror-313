# oxr

`oxr` is a type-safe Python client with synchronous and asynchronous support for the [Open Exchange Rates API](https://openexchangerates.org/). Allowing you to easily fetch exchange rates and convert between currencies.


## Installation

```bash
pip install oxr
```

If you want to use the asynchronous client, you can install the package with the following command:

```bash
pip install oxr[async]
```

## Usage

### Synchronous Client

```python
import oxr

import datetime as dt

# Base default to USD
client = oxr.Client(app_id='your_app_id')

# Fetch the latest exchange rates
rates = client.latest(symbols=['EUR', 'JPY'])

# Convert 100 USD to EUR
converted = client.convert(amount, 'USD', 'EUR')

# Get time series data
timeseries = client.timeseries(start_date=dt.date(2020, 1, 1), end_date=dt.date(2020, 1, 31), symbols=['EUR', 'JPY'])

# Get open, high, low, close data
ohlc = client.ohlc(start_time=dt.datetime(2020, 1, 1), period="1m", symbols=['EUR', 'JPY'])
```

### Asynchronous Client

The asynchronous client is built on top of `aiohttp`, and can be used in an `async` context.

```python
import oxr.asynchronous
import asyncio
import datetime as dt

async def main():
    async with oxr.asynchronous.Client(app_id='your_app_id') as client:        
        # Fetch the latest exchange rates asynchronously
        rates = await client.latest(symbols=['EUR', 'JPY'])

        # Asynchronously convert 100 USD to EUR
        converted = await client.convert(100, 'USD', 'EUR')

        # Get time series data asynchronously
        timeseries = await client.timeseries(start_date=dt.date(2020, 1, 1), end_date=dt.date(2020, 1, 31), symbols=['EUR', 'JPY'])

        # Get OHLC data asynchronously
        ohlc = await client.ohlc(start_time=dt.datetime(2020, 1, 1), period="1m", symbols=['EUR', 'JPY'])

asyncio.run(main())
```

## License

MIT

