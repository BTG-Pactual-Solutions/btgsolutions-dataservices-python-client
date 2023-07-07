# BTG Solutions - Data Service

It's a Python library to get Brazilian Financial Market Data.

## Installation

```bash
pip3 install btgsolutions-dataservices-python-client
```

## Example - WebSocket Books
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', ws_type='books', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))
```
## Example - WebSocket Trades Delayed
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', ws_type='trades', target='delayed', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))
```

## Example - IntradayCandles
```python
import btgsolutions_dataservices as btg
int_candles = btg.IntradayCandles(api_key='YOUR_API_KEY')
int_candles.get_intraday_candles(market_type='stocks', tickers=['PETR4', 'VALE3'], candle_period='1m', mode='relative', raw_data=True)
```
## Example - Plot HistoricalCandles
```python
import btgsolutions_dataservices as btg
hist_candles = btg.HistoricalCandles(api_key='YOUR_API_KEY')
hist_candles.get_historical_candles(ticker='PETR4', lookback='5D', mode='absolute').plot(x='date', y='close_price', kind='scatter')
```
## Documentation
The official documentation is hosted at https://python-client-docs.dataservices.btgpactualsolutions.com/