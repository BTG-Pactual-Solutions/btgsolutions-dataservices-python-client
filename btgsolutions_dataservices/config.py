### WebSocket 
socket_urls = {
    'derivatives_realtime': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/derivatives",
        'books': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/derivatives",
        'candles-1S': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1S/derivatives",
        'candles-1M': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1M/derivatives",
        'stoploss': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/stoploss/derivatives",
    },
    'derivatives_delayed': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/derivatives/delayed",
    },
    'stocks_realtime': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/stocks",
        'books': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/stocks",
        'candles-1S': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1S/stocks",
        'candles-1M': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1M/stocks",
        'stoploss': "wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/stoploss/stocks",
    },
    'stocks_delayed': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/stocks/delayed",
    },
    'options_realtime': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/options",
        'books': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/options",
    },
    'options_delayed': {
        'trades': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/options/delayed",
    },
    'indices_realtime': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/indices",
    'indices_delayed': "wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/indices/delayed",
    
    'hfn_realtime': {
        'brazil': "wss://dataservices.btgpactualsolutions.com/stream/v2/hfn/brazil",
    },
}

keys_socket = list(socket_urls.keys())

valid_delayed_options = list(set([i.split('_')[1] for i in keys_socket]))
valid_feeds = list(set([i.split('_')[0] for i in keys_socket]))

def valid_ws_options(feed, target):
    return list(set(socket_urls[f'{feed}_{target}']))



MAX_WS_RECONNECT_RETRIES = 5

### Rest
url_apis = "https://dataservices.btgpactualsolutions.com/api/v2"
url_api_v1 = "https://dataservices.btgpactualsolutions.com/api/v1"