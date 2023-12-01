
from typing import Optional, List
from ..exceptions import WSTypeError, DelayedError, FeedError
from ..rest import Authenticator
from ..config import market_data_socket_urls, MAX_WS_RECONNECT_RETRIES, VALID_STREAM_TYPES, VALID_EXCHANGES, VALID_MARKET_DATA_TYPES, VALID_MARKET_DATA_SUBTYPES, REALTIME, B3, TRADES, INDICES, ALL, STOCKS
from .websocket_default_functions import _on_open, _on_message, _on_error, _on_close
import websocket 
import json
import ssl
import threading

class MarketDataWebSocketClient:
    """
    This class connects with BTG Solutions Data Services WebSocket, receiving trade and index data, in real time or delayed.

    * Main use case:

    >>> from btgsolutions_dataservices import MarketDataWebSocketClient
    >>> ws = MarketDataWebSocketClient(
    >>>     api_key='YOUR_API_KEY',
    >>>     stream_type='realtime',
    >>>     exchange='b3',
    >>>     data_type='trades',
    >>>     data_subtype='stocks',
    >>>     instruments=['PETR4'],
    >>>     ssl=True
    >>> )
    >>> ws.run()
    >>> ws.subscribe(['MGLU3'])
    >>> ws.unsubscribe(['PETR4'])
    >>> ws.close()

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.

    stream_type: str
        Websocket connection feed.
        Options: 'realtime', 'delayed'.
        Field is not required. Default: 'realtime'.

    exchange: str
        Exchange name.
        Options: 'b3' or 'bmv'.
        Field is not required. Default: 'b3'.

    data_type: str
        Market Data type.
        Options: 'trades', 'books', 'indices', 'securities', 'stoploss', 'candles-1S', 'candles-1M'.
        Field is not required. Default: 'trades'.
    
    data_subtype: str
        Market Data subtype (when applicable).
        Options: 'stocks', 'options', 'derivatives'.
        Field is not required. Default: None.

    instruments: list
        List of tickers or indexes to subscribe.
        Field is not required. Default: [].

    ssl: bool
        Enable or disable ssl configuration.
        Field is not required. Default: True (enable).
    """
    def __init__(
        self,
        api_key:str,
        stream_type:Optional[str] = REALTIME,
        exchange:Optional[str] = B3,
        data_type:Optional[str] = TRADES,
        data_subtype:Optional[str] = None,
        instruments:Optional[List[str]] = [],
        ssl:Optional[bool] = True,
        **kwargs,
    ):
        self.api_key = api_key
        self.instruments = instruments
        self.ssl = ssl

        self.__authenticator = Authenticator(self.api_key)
        self.__nro_reconnect_retries = 0

        if data_subtype is None:
            if exchange is B3 and data_type is not INDICES:
                data_subtype = STOCKS
            else:
                data_subtype = ALL

        if stream_type not in VALID_STREAM_TYPES:
            raise FeedError(f"Must provide a valid 'stream_type' parameter. Valid options are: {VALID_STREAM_TYPES}")
        if exchange not in VALID_EXCHANGES:
            raise FeedError(f"Must provide a valid 'exchange' parameter. Valid options are: {VALID_EXCHANGES}")
        if exchange not in VALID_EXCHANGES:
            raise FeedError(f"Must provide a valid 'exchange' parameter. Valid options are: {VALID_EXCHANGES}")
        if data_type not in VALID_MARKET_DATA_TYPES:
            raise FeedError(f"Must provide a valid 'data_type' parameter. Valid options are: {VALID_MARKET_DATA_TYPES}")
        if data_subtype not in VALID_MARKET_DATA_TYPES:
            raise FeedError(f"Must provide a valid 'data_subtype' parameter. Valid options are: {VALID_MARKET_DATA_SUBTYPES}")

        try:
            self.url = market_data_socket_urls[exchange][data_type][stream_type][data_subtype]
        except:
            raise WSTypeError(f"There is no WebSocket type for your specifications (stream_type:{stream_type}, exchange:{exchange}, data_type:{data_type}, data_subtype:{data_subtype})\nPlease check your request parameters and try again")
            
        self.websocket_cfg = kwargs
    
    def run(
        self,
        on_open = None,
        on_message = None,
        on_error = None,
        on_close = None,
        reconnect=True
    ):
        """
        Initializes a connection to websocket and subscribes to the instruments, if it was passed in the class initialization.

        Parameters
        ----------
        on_open: function
            - Called at opening connection to websocket.
            - Field is not required. 
            - Default: prints that the connection was opened in case of success.
        
        on_message: function
            - Called every time it receives a message.
            - Arguments:
                1. Data received from the server.
            - Field is not required. 
            - Default: prints the data.

        on_error: function
            - Called when a error occurs.
            - Arguments: 
                1. Exception object.
            - Field is not required. 
            - Default: prints the error.

        on_close: function
            - Called when connection is closed.
            - Arguments: 
                1. close_status_code.
                2. close_msg.
            - Field is not required. 
            - Default: prints a message that the connection was closed.
        reconnect: bool
            Try reconnect if connection is closed.
            Field is not required.
            Default: True.
        """
        if on_open is None:
            on_open = _on_open
        if on_message is None:
            on_message = _on_message
        if on_error is None:
            on_error = _on_error
        if on_close is None:
            on_close = _on_close

        def intermediary_on_open(ws):
            on_open()
            if self.instruments:
                self.subscribe(self.instruments)
            self.__nro_reconnect_retries = 0

        def intermediary_on_message(ws, data):
            on_message(data)

        def intermediary_on_error(ws, error):
            on_error(error)

        def intermediary_on_close(ws, close_status_code, close_msg):
            on_close(close_status_code, close_msg)
            
            if reconnect:
                if self.__nro_reconnect_retries == MAX_WS_RECONNECT_RETRIES:
                    print(f"### Fail retriyng reconnect")
                    return
                self.__nro_reconnect_retries +=1
                print(f"### Reconnecting.... Attempts: {self.__nro_reconnect_retries}/{MAX_WS_RECONNECT_RETRIES}")
                self.run(on_open, on_message, on_error, on_close, reconnect)

        self.ws = websocket.WebSocketApp(
            url=self.url,
            on_open=intermediary_on_open,
            on_message=intermediary_on_message,
            on_error=intermediary_on_error,
            on_close=intermediary_on_close,
            header={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
                "Sec-WebSocket-Protocol": self.__authenticator.token,
            }
        )

        ssl_conf = {} if self.ssl else {"sslopt": {"cert_reqs": ssl.CERT_NONE}}
        wst = threading.Thread(target=self.ws.run_forever, kwargs=ssl_conf)
        wst.daemon = True
        wst.start()

    def __send(self, data):
        """
        Class method to be used internally. Sends data to websocket.
        """
        if not isinstance(data, str):
            data = json.dumps(data)   
        print(f'Sending data: {data}')
        return self.ws.send(data)
    
    def close(self):
        """
        Closes connection with websocket.
        """
        self.ws.close()

    def subscribe(self, list_instruments):
        """
        Subscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        """
        self.__send({'action':'subscribe', 'params': list_instruments})
        print(f'Socket subscribed the following instrument(s): {list_instruments}')

    def unsubscribe(self, list_instruments):
        """
        Unsubscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        """
        self.__send({'action':'unsubscribe', 'params': list_instruments})
        print(f'Socket subscribed the following instrument(s): {list_instruments}')

    def notify_stoploss(self, instrument_params):
        """
        Create a stoploss notification routine on the provided instrument(s).

        Parameters
        ----------
        instrument_params: dict
            Field is required.
        """
        self.__send({'action':'notify_stoploss', 'params': instrument_params})

    def stoploss_status(self):
        """
        Return client stop loss status.
        """
        self.__send({'action':'stoploss_status'})

    def clear_stoploss(self):
        """
        Clears client stop loss notifications.
        """
        self.__send({'action':'clear_stoploss'})

    def get_last_event(self, ticker:str):
        """
        Get the last event for the provided ticker.

        Parameters
        ----------
        ticker: str
            Field is required.
        """
        self.__send({'action':'get_last_event', 'params': ticker})

    def candle_subscribe(self, list_instruments:list, candle_type:str):
        """
        Subscribes a list of instruments, for partial/closed candle updates.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        candle_type: str
            Field is required.
        """
        self.__send({'action':'subscribe', 'params': list_instruments, 'type':candle_type})
        print(f'Socket subscribed the following instrument(s): {list_instruments}')

    def candle_unsubscribe(self, list_instruments:list, candle_type:str):
        """
        Unsubscribes a list of instruments, for partial/closed candle updates.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        candle_type: str
            Field is required.
        """
        self.__send({'action':'unsubscribe', 'params': list_instruments, 'type':candle_type})
        print(f'Socket unsubscribed the following instrument(s): {list_instruments}')
