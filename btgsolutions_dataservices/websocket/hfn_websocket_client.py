
from typing import Optional, List
from ..exceptions import WSTypeError, DelayedError, FeedError
from ..rest import Authenticator
from ..config import hfn_socket_urls, MAX_WS_RECONNECT_RETRIES, VALID_STREAM_TYPES, VALID_COUNTRIES, REALTIME, BR
from .websocket_default_functions import _on_open, _on_message, _on_error, _on_close
import websocket 
import json
import ssl
import threading

class HFNWebSocketClient:
    """
    This class connects with BTG Solutions Data Services HFN WebSocket, receiving high frequency news in realtime or delayed feeds.

    * Main use case:

    >>> from btgsolutions_dataservices import HFNWebSocketClient
    >>> ws = HFNWebSocketClient(
    >>>     api_key='YOUR_API_KEY',
    >>>     stream_type='realtime',
    >>>     country='brazil',
    >>>     ssl=True
    >>> )
    >>> ws.run()
    >>> ws.get_latest_news()
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

    country: str
        Country name.
        Options: 'brazil' or 'chile'.
        Field is not required. Default: 'brazil'.

    ssl: bool
        Enable or disable ssl configuration.
        Field is not required. Default: True (enable).
    """
    def __init__(
        self,
        api_key:str,
        stream_type:Optional[str] = REALTIME,
        country:Optional[str] = BR,
        ssl:Optional[bool] = True,
        **kwargs,
    ):
        self.api_key = api_key
        self.ssl = ssl

        self.__authenticator = Authenticator(self.api_key)
        self.__nro_reconnect_retries = 0

        if stream_type not in VALID_STREAM_TYPES:
            raise FeedError(f"Must provide a valid 'stream_type' parameter. Valid options are: {VALID_STREAM_TYPES}")
        if country not in VALID_COUNTRIES:
            raise FeedError(f"Must provide a valid 'country' parameter. Valid options are: {VALID_COUNTRIES}")

        try:
            self.url = hfn_socket_urls[country][stream_type]
        except:
            raise WSTypeError(f"There is no WebSocket type for your specifications (stream_type:{stream_type}, country:{country})\nPlease check your request parameters and try again")
            
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
        Initializes a connection to websocket and starts to receive high frequency news.

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

        while True:
            if self.ws.sock is not None and self.ws.sock.connected:
                break
            pass

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
        
    def get_latest_news(self):
        """
        Get the latest news from our High Frequency News service.

        """
        self.__send({'action':'latest_news'})