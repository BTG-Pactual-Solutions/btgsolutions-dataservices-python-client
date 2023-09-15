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
## Example - WebSocket Candles 1S
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', ws_type='candles-1S', target='delayed')
ws.run(on_message=lambda message: print(message))
ws.candle_subscribe(list_instruments=['PETR4','VALE3'], candle_type='partial')
ws.candle_subscribe(list_instruments=['PRIO3'], candle_type='closed')
ws.candle_subscribe(list_instruments=['WEGE3'], candle_type='all')
ws.candle_unsubscribe(list_instruments=['PRIO3', 'PETR4'], candle_type='all')
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

## Example - BulkData
```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_data(ticker='PETR4', date='2023-07-03', data_type='trades')
```

## Example - HighFrequencyNews
```python
import btgsolutions_dataservices as btg
hfn = btg.HighFrequencyNews(api_key='YOUR_API_KEY')
hfn.latest_news()
```

## Documentation
The official documentation is hosted at https://python-client-docs.dataservices.btgpactualsolutions.com/