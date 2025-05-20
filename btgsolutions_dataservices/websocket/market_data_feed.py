from typing import Optional, Callable, List
import websocket
import time
from datetime import date
import multiprocessing
import logging
import json
import ssl
import threading
from ..rest import Authenticator
from ..config import market_data_socket_urls, market_data_feedb_socket_urls, REALTIME, B3, TRADES, BOOKS, FEED_A, FEED_B, MAX_WS_RECONNECT_RETRIES
from .websocket_default_functions import _on_open, _on_message_already_serialized, _on_error, _on_close

multiprocessing.set_start_method("spawn", force=True)

class MarketDataFeed:
    """
    WebSocket client that connects with BTG Solutions Data Services WebSocket servers. The servers streams realtime and delayed market data, such as trades and book events.
    This is a multiprocessing-based WebSocket client designed for high-performance, scalable message handling applications. It leverages a system of inter-process communication to efficiently separate concerns and prevent the main application thread from blocking during WebSocket operations or message processing.

    * Main use case:

    >>> from btgsolutions_dataservices import MarketDataFeed
    >>> ws = MarketDataFeed(
    >>>     api_key='YOUR_API_KEY',
    >>>     stream_type='realtime',
    >>>     exchange='b3',
    >>>     data_type='trades',
    >>>     data_subtype='stocks',
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
        Options: 'trades', 'processed-trades', 'books', 'indices', 'securities', 'stoploss', 'candles-1S', 'candles-1M', 'instrument_status'.
        Field is not required. Default: 'trades'.
    data_subtype: str
        Market Data subtype (when applicable).
        Options: 'stocks', 'options', 'derivatives'.
        Field is not required. Default: None.
    feed: str
        Market Data Feed.
        Options: 'A', 'B'.
        Field is not required. Default: 'A' (enable).
    ssl: bool
        Enable or disable ssl configuration.
        Field is not required. Default: True (enable).
    reconnect: bool
        Try reconnect if connection is closed.
        Field is not required.
        Default: True.
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
    """

    def __init__(
        self, 
        api_key: str,
        stream_type: Optional[str]=REALTIME,
        exchange: Optional[str]=B3,
        data_type: Optional[str]=TRADES,
        data_subtype: Optional[str]=None,
        feed: Optional[str]=FEED_A,
        ssl: Optional[bool]=True,
        reconnect: bool=True,
        on_open: Optional[Callable]=None,
        on_message: Optional[Callable]=None,
        on_error: Optional[Callable]=None,
        on_close: Optional[Callable]=None,
    ):

        if feed == FEED_B:
            url_feed_map = market_data_feedb_socket_urls
        else:
            url_feed_map = market_data_socket_urls

        try:
            self.url = url_feed_map[exchange][data_type][stream_type][data_subtype]
        except:
            raise Exception(f"There is no WebSocket type for your specifications (stream_type:{stream_type}, exchange:{exchange}, data_type:{data_type}, data_subtype:{data_subtype})\nPlease check your request parameters and try again")
        
        self.__authenticator = Authenticator(api_key)

        self.data_type = data_type
        self.on_open = _on_open if on_open is None else on_open
        self.on_message = _on_message_already_serialized if on_message is None else on_message
        self.on_error = _on_error if on_error is None else on_error
        self.on_close = _on_close if on_close is None else on_close
        
        self.ssl = ssl
        self.reconnect = reconnect
        self.__nro_reconnect_retries = 0

        self.server_message_queue = multiprocessing.Queue()
        self.client_message_queue = multiprocessing.Queue()
        self.process = None
        self.running = False

        self.logger = logging.getLogger("MarketDataFeed")
        self.logger.setLevel(logging.INFO)
        log_file = f"MarketDataFeed_{date.today().isoformat()}.log"
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _ws_client_process(self, server_message_queue: multiprocessing.Queue, client_message_queue: multiprocessing.Queue, logger: logging.Logger):

        def on_message(ws, message):
            server_message_queue.put(json.loads(message))

        def on_error(ws, error):
            logger.info(f"On Error | {error}")
            self.on_error(error)

        def on_close(ws, close_status_code, close_msg):
            logger.info(f"On Close | Connection closed")
            self.on_close(close_status_code, close_msg)
            if self.reconnect:
                if self.__nro_reconnect_retries == MAX_WS_RECONNECT_RETRIES:
                    logger.info(f"On Close | Maximum number of reconnect attempts reached")
                    return
                self.__nro_reconnect_retries += 1
                logger.info(f"On Close | Reconnecting... attempt: {self.__nro_reconnect_retries}/{MAX_WS_RECONNECT_RETRIES}")
                run_forever_new_thread()

        def on_open(ws):
            logger.info(f"On Open | Connection open")
            self.on_open()
            self.__nro_reconnect_retries = 0

        ws = websocket.WebSocketApp(
            url=self.url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            header={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
                "Sec-WebSocket-Protocol": self.__authenticator.token,
            }
        )

        def run_forever_new_thread():
            ws_thread = websocket.WebSocketApp.run_forever

            t = threading.Thread(target=lambda: ws_thread(ws))
            t.daemon = True
            t.start()

            while True:
                try:
                    if not client_message_queue.empty():
                        msg = client_message_queue.get()
                        ws.send(json.dumps(msg))
                    else:
                        time.sleep(0.05)
                except Exception as e:
                    time.sleep(0.1)

        run_forever_new_thread()

    def run(self):
        """
        Opens a new connection with the websocket server.
        """
        self.process = multiprocessing.Process(target=self._ws_client_process, args=(self.server_message_queue, self.client_message_queue, self.logger))
        self.process.start()
        self.running = True

        def run_on_new_thread(*args):
            log_timer = time.time()
            while self.running:
                if not self.server_message_queue.empty():
                    msg = self.server_message_queue.get()
                    self.on_message(msg)
                else:
                    time.sleep(0.1)

                if time.time() - log_timer >= 5.0:
                    server_queue_size = self.server_message_queue.qsize()
                    client_queue_size = self.client_message_queue.qsize()
                    self.logger.info(f"Server queue: {server_queue_size} | Client queue: {client_queue_size}")
                    log_timer = time.time()
        
        threading.Thread(target=run_on_new_thread).start()

    def close(self):
        """
        Closes the connection with the websocket server.
        """
        self.running = False
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join()

    def _send(self, message):
        """
        Sends a message to the websocket server.
        """
        if not isinstance(message, str):
            message = json.dumps(message)
        self.client_message_queue.put(json.loads(message))

    def subscribe(self, list_instruments: List[str], n=None):
        """
        Subscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        n: int
            Field is not required.
            **For books data_type only.**
            Maximum book level. It must be between 1 and 10.    
        """
        if self.data_type == BOOKS and n is not None:
            self._send({'action': 'subscribe', 'params': {"tickers": list_instruments, "n": n}})
        else:
            self._send({'action': 'subscribe', 'params': list_instruments})

    def unsubscribe(self, list_instruments: List[str]):
        """
        Unsubscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        """
        self._send({'action': 'unsubscribe', 'params': list_instruments})
    
    def subscribed_to(self):
        """
        Return client subscribed tickers.
        """
        self._send({'action': 'subscribed_to'})

    def available_to_subscribe(self):
        """
        Return avaiable tickers to subscribe.
        """
        self._send({'action': 'available_to_subscribe'})

    def get_last_event(self, ticker: str):
        """
        Get the last event for the provided ticker.

        Parameters
        ----------
        ticker: str
            Field is required.
        """
        self._send({'action': 'get_last_event', 'params': ticker})