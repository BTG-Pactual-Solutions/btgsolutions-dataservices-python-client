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

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

```
## Example - WebSocket Trades Delayed
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', ws_type='trades', target='delayed', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

```
## Example - WebSocket Candles 1S
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', ws_type='candles-1S', target='delayed')
ws.run(on_message=lambda message: print(message))
ws.candle_subscribe(list_instruments=['PETR4','VALE3'], candle_type='partial')

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

## Another examples
# ws.candle_subscribe(list_instruments=['PRIO3'], candle_type='closed')
# ws.candle_subscribe(list_instruments=['WEGE3'], candle_type='all')
# ws.candle_unsubscribe(list_instruments=['PRIO3', 'PETR4'], candle_type='all')
```

## Example - WebSocket High Frequency News
```python
import btgsolutions_dataservices as btg
ws = btg.WebSocketClient(api_key='YOUR_API_KEY', feed='hfn', ws_type='brazil')
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)
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
hist_candles.get_intraday_history_candles(ticker='PETR4',  market_type='stocks', corporate_events_adj=True, date='2023-10-06', candle='1m', rmv_after_market=True, timezone='UTC', raw_data=False).plot(x='candle_time', y='close_price', kind='scatter')
# hist_candles.get_interday_history_candles(ticker='PETR4',  market_type='stocks', corporate_events_adj=True, start_date='2023-10-01', end_date='2023-10-13', rmv_after_market=True, timezone='UTC', raw_data=False).plot(x='date', y='close_price', kind='scatter')
```

## Example - Quotes
```python
import btgsolutions_dataservices as btg
quotes = btg.Quotes(api_key='YOUR_API_KEY')
quotes.get_quote(market_type = 'stocks', tickers = ['PETR4', 'VALE3'])
```

## Example - BulkData
```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_data(ticker='PETR4', date='2023-07-03', data_type='trades')
```

## Example - Intraday Tick Data
```python
import btgsolutions_dataservices as btg
intra_tickdata = btg.IntradayTickData(api_key='YOUR_API_KEY')
intra_tickdata.get_trades(ticker='PETR4')
```

## Example - HighFrequencyNews
```python
import btgsolutions_dataservices as btg
hfn = btg.HighFrequencyNews(api_key='YOUR_API_KEY')
hfn.latest_news()
```

## Documentation
The official documentation is hosted at https://python-client-docs.dataservices.btgpactualsolutions.com/