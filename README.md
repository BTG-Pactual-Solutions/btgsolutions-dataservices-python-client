# BTG Solutions - Data Service

Python library to get Brazilian Financial Market Data.

## Installation

```bash
pip3 install btgsolutions-dataservices-python-client
```

## Examples

### WebSocket Books

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='books', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

## Another examples
# ws.available_to_subscribe()
```

### WebSocket Trades Delayed

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='trades', stream_type='delayed', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

## Another examples
# ws.available_to_subscribe()
```

### WebSocket Trades with 1 second throttle

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='trades', stream_type='throttle', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

## Another examples
# ws.available_to_subscribe()
```

### WebSocket Securities (Derivatives)

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='securities', data_subtype='derivatives')
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)
```

### WebSocket Candles 1S

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='candles-1S', stream_type='realtime')
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

### WebSocket BMV Trades

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', exchange='bmv', data_type='trades')
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)
```

### WebSocket Books (without spawning a new thread for incoming server messages)

```python
import btgsolutions_dataservices as btg
ws = btg.MarketDataWebSocketClient(api_key='YOUR_API_KEY', data_type='books', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message), spawn_thread=False)

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)

## Another examples
# ws.available_to_subscribe()
```

### WebSocket High Frequency News

```python
import btgsolutions_dataservices as btg
ws = btg.HFNWebSocketClient(api_key='YOUR_API_KEY', country='brazil')
ws.run(on_message=lambda message: print(message))

## The following is optional to keep the program running in a .py file:
# from time import sleep
# while True:
#   sleep(1)
```

### IntradayCandles

```python
import btgsolutions_dataservices as btg
int_candles = btg.IntradayCandles(api_key='YOUR_API_KEY')
int_candles.get_intraday_candles(market_type='stocks', tickers=['PETR4', 'VALE3'], candle_period='1m', mode='relative', raw_data=True)
```

### Get Interday History Candles

```python
import btgsolutions_dataservices as btg
hist_candles = btg.HistoricalCandles(api_key='YOUR_API_KEY')
hist_candles.get_interday_history_candles(ticker='PETR4',  market_type='stocks', corporate_events_adj=True, start_date='2023-10-01', end_date='2023-10-13', rmv_after_market=True, timezone='UTC', raw_data=False)
```

### Get Intraday History Candles

```python
import btgsolutions_dataservices as btg
hist_candles = btg.HistoricalCandles(api_key='YOUR_API_KEY')
hist_candles.get_intraday_history_candles(ticker='PETR4',  market_type='stocks', corporate_events_adj=True, date='2023-10-06', candle='1m', rmv_after_market=True, timezone='UTC', raw_data=False)
```

### Plot History Candles

```python
import btgsolutions_dataservices as btg
hist_candles = btg.HistoricalCandles(api_key='YOUR_API_KEY')
hist_candles.get_intraday_history_candles(ticker='PETR4',  market_type='stocks', corporate_events_adj=True, date='2023-10-06', candle='1m', rmv_after_market=True, timezone='UTC', raw_data=False).plot(x='candle_time', y='close_price', kind='scatter')
```

### Quotes

```python
import btgsolutions_dataservices as btg
quotes = btg.Quotes(api_key='YOUR_API_KEY')
quotes.get_quote(market_type = 'stocks', tickers = ['PETR4', 'VALE3'])
```

### Ticker Last Event

```python
import btgsolutions_dataservices as btg
last_event = btg.TickerLastEvent(api_key='YOUR_API_KEY')
last_event.get_trades(data_type='equities', ticker='VALE3')
```

### BulkData - Available Tickers

```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_available_tickers(date='2023-07-03', data_type='trades', prefix='PETR')
```

### BulkData - Get Data

```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_data(ticker='DI1F18', date='2017-01-02', data_type='trades')
# bulk_data.get_data(ticker='PETR4', date='2024-01-22', data_type='books')
# bulk_data.get_data(ticker='VALE3', date='2024-04-01', data_type='trades-and-book-events')
```

### BulkData - Get Market Data Channels

```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_market_data_channels(date='2024-01-03')
```

### BulkData - Get Compressed Data (PCAP files)

```python
import btgsolutions_dataservices as btg
bulk_data = btg.BulkData(api_key='YOUR_API_KEY')
bulk_data.get_compressed_data(channel='001', date='2024-01-03', data_type='instruments')
# bulk_data.get_compressed_data(channel='053', date='2024-01-03', data_type='incremental')
# bulk_data.get_compressed_data(channel='051', date='2024-01-03', data_type='snapshot')
```

### Intraday Tick Data

```python
import btgsolutions_dataservices as btg
intra_tickdata = btg.IntradayTickData(api_key='YOUR_API_KEY')
intra_tickdata.get_trades(ticker='PETR4')
```

### High Frequency News

```python
import btgsolutions_dataservices as btg
hfn = btg.HighFrequencyNews(api_key='YOUR_API_KEY')
hfn.latest_news()
```

### Corporate Events

```python
import btgsolutions_dataservices as btg
corporate_events = btg.CorporateEvents(api_key='YOUR_API_KEY')
corporate_events.get(start_date='2024-05-01', end_date='2024-05-31')
# corporate_events.get(start_date='2024-05-01', end_date='2024-05-31', tickers=['VALE3'])
```

### Company Data
#### Company General Information

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.general_info(ticker='PETR4')
```

#### Income Statement

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.income_statement(ticker='PETR4')
```

#### Balance Sheet

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.balance_sheet(ticker='PETR4')
```

#### Cash Flow

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.cash_flow(ticker='PETR4')
```

#### Valuation

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.valuation(ticker='PETR4')
```

#### Ratios

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.ratios(ticker='PETR4')
```

#### Growth

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.growth(ticker='PETR4')
```

#### Interims

```python
import btgsolutions_dataservices as btg
company_data = btg.CompanyData(api_key='YOUR_API_KEY')
company_data.interims(ticker='PETR4')
```

## Documentation

The official documentation is hosted at https://python-client-docs.dataservices.btgpactualsolutions.com/
