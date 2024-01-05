# WebSocket
MAX_WS_RECONNECT_RETRIES = 5

REALTIME = 'realtime'
DELAYED = 'delayed'
THROTTLE = 'throttle'
PROCESSED = 'processed'

BR = 'brazil'
MX = 'mexico'
CL = 'chile'

B3 = 'b3'
BMV = 'bmv'

SECURITIES = 'securities'
TRADES = 'trades'
PROCESSEDTRADES = 'processed-trades'
BOOKS = 'books'
INDICES = 'indices'
CANDLES1S = 'candles-1S'
CANDLES1M = 'candles-1M'
STOPLOSS = 'stoploss'

ALL = 'all'
STOCKS = 'stocks'
OPTIONS = 'options'
DERIVATIVES = 'derivatives'

VALID_STREAM_TYPES = [REALTIME, DELAYED, THROTTLE]
VALID_COUNTRIES = [BR, MX, CL]
VALID_EXCHANGES = [B3, BMV]
VALID_MARKET_DATA_TYPES = [SECURITIES, TRADES, PROCESSEDTRADES,
                           BOOKS, INDICES, CANDLES1S, CANDLES1M, STOPLOSS]
VALID_MARKET_DATA_SUBTYPES = [ALL, STOCKS, OPTIONS, DERIVATIVES]

market_data_socket_urls = {
    B3: {
        TRADES: {
            REALTIME: {
                STOCKS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{STOCKS}',
                OPTIONS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{OPTIONS}',
                DERIVATIVES: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{DERIVATIVES}',
            },
            DELAYED: {
                STOCKS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{STOCKS}/{DELAYED}',
                OPTIONS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{OPTIONS}/{DELAYED}',
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/trade/{DERIVATIVES}/{DELAYED}",
            },
            THROTTLE: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/trade/{STOCKS}",
                OPTIONS: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/trade/{OPTIONS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/trade/{DERIVATIVES}",
            },
        },
        PROCESSEDTRADES: {
            REALTIME: {
                STOCKS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{PROCESSED}/trade/{STOCKS}',
                OPTIONS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{PROCESSED}/trade/{OPTIONS}',
                DERIVATIVES: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{PROCESSED}/trade/{DERIVATIVES}',
            },
        },
        BOOKS: {
            REALTIME: {
                STOCKS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/{STOCKS}',
                OPTIONS: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/{OPTIONS}',
                DERIVATIVES: f'wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/{DERIVATIVES}',
            },
            THROTTLE: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/book/{STOCKS}",
                OPTIONS: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/book/{OPTIONS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{THROTTLE}/book/{DERIVATIVES}",
            },
        },
        SECURITIES: {
            REALTIME: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/sec_list/{STOCKS}",
                OPTIONS: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/sec_list/{OPTIONS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/sec_list/{DERIVATIVES}",
            },
        },
        INDICES: {
            REALTIME: {
                ALL: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{INDICES}",
            },
            DELAYED: {
                ALL: f"wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/{INDICES}/{DELAYED}",
            }
        },
        CANDLES1S: {
            REALTIME: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1S/{STOCKS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1S/{DERIVATIVES}",
            },
        },
        CANDLES1M: {
            REALTIME: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1M/{STOCKS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/candles/1M/{DERIVATIVES}",
            },
        },
        STOPLOSS: {
            REALTIME: {
                STOCKS: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/{STOPLOSS}/{STOCKS}",
                DERIVATIVES: f"wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/{STOPLOSS}/{DERIVATIVES}",
            },
        },
    },
    BMV: {
        TRADES: {
            REALTIME: {
                ALL: f'wss://dataservices.btgpactualsolutions.com/stream/v1/marketdata/bmv/{TRADES}',
            },
        },
    },
}

hfn_socket_urls = {
    BR: {
        REALTIME: f'wss://dataservices.btgpactualsolutions.com/stream/v2/hfn/{BR}',
    },
    CL: {
        REALTIME: f'wss://dataservices.btgpactualsolutions.com/stream/v2/hfn/{CL}',
    },
}

# Rest
url_apis = "https://dataservices.btgpactualsolutions.com/api/v2"
url_api_v1 = "https://dataservices.btgpactualsolutions.com/api/v1"
url_apis_v3 = "https://dataservices.btgpactualsolutions.com/api/v3"
