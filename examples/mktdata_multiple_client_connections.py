API_KEY = 'PUT_YOUR_API_KEY_HERE'
DATA_TYPE = "books"
DATA_SUBTYPE = "stocks"
TICKER_LIST = None # ['PETR4','VALE3'] # If None, subscribes to all available tickers.
NUM_CONNECTIONS = 1 # Number of client connections to be made. The ticker list will be evenly distributed across clients to maximize performance.


from typing import Optional, Callable
import btgsolutions_dataservices as btg
from time import sleep
import asyncio

def split_tickers(tickers, chunk_size):
    for i in range(0, len(tickers), chunk_size):
        yield tickers[i:i + chunk_size]

class AvailableTickersRetriever:

    def __init__(
        self, 
        api_key: str,
        stream_type: Optional[str]='realtime',
        exchange: Optional[str]='b3',
        data_type: Optional[str]='books',
        data_subtype: Optional[str]='stocks',
    ):

        self.tickers = None
        
        self.client = btg.MarketDataFeed(
            api_key=api_key,
            stream_type=stream_type,
            exchange=exchange,
            data_type=data_type,
            data_subtype=data_subtype,
            on_open=self.on_open,
            on_message=self.on_message,
        )

        self.client.run()
    
    def on_open(self):
        self.client.available_to_subscribe()
    
    def on_message(self, msg):
        if msg["ev"] == "available_to_subscribe":
            self.tickers = msg.get("message", [])
            print(f'available tickers: {len(self.tickers)}')
            self.client.close()
    
    async def get_tickers(self):
        cont = 0
        while True:
            cont += 1
            if not self.tickers is None:
                return self.tickers
            if cont == 20:
                raise Exception('could not retrieve ticker list')
            sleep(1)

class MarketDataFeedMultipleClients:
    def __init__(
        self,
        api_key: str,
        ticker_list=None,
        num_connections=None,
        stream_type: Optional[str]='realtime',
        exchange: Optional[str]='b3',
        data_type: Optional[str]='books',
        data_subtype: Optional[str]='stocks',
        feed: Optional[str]='A',
        ssl: Optional[bool]=True,
        reconnect: bool=True,
        on_open: Optional[Callable]=None,
        on_message: Optional[Callable]=None,
        on_error: Optional[Callable]=None,
        on_close: Optional[Callable]=None,
        log_level: str="DEBUG",
    ):

        self.ticker_list = ticker_list
        self.num_connections = num_connections

        self.api_key=api_key
        self.stream_type=stream_type
        self.exchange=exchange
        self.data_type=data_type
        self.data_subtype=data_subtype
        self.reconnect=reconnect
        self.log_level=log_level
        self.on_open=on_open
        self.on_message=on_message

        self.clients = {}

    async def get_ticker_list(self):
        if self.ticker_list is None:
            print(f'retrieving available tickers...')
            
            ticker_retriever = AvailableTickersRetriever(
                api_key=self.api_key,
                stream_type=self.stream_type,
                exchange=self.exchange,
                data_type=self.data_type,
                data_subtype=self.data_subtype,
            )
            self.ticker_list = await ticker_retriever.get_tickers()

        else:
            print(f'using ticker list provided by the user')
    
    async def run(self):

        await self.get_ticker_list()

        num_tickers = len(self.ticker_list)
        if self.num_connections is None:
            chunk_size = 10000
        else:
            chunk_size = num_tickers // self.num_connections
            if self.num_connections > num_tickers:
                raise Exception(f'num_connections cannot be greater than the ticker list length')

        ticker_chunks = list(split_tickers(self.ticker_list, chunk_size))
        print(f'{len(ticker_chunks)} chunks with max size {chunk_size}')

        for index, ticker_chunk in enumerate(ticker_chunks):
            print(f'instantiating client {index} with ticker chunk starting at ticker {ticker_chunk[0]}')
            
            client = btg.MarketDataFeed(
                api_key=self.api_key,
                stream_type=self.stream_type,
                exchange=self.exchange,
                data_type=self.data_type,
                data_subtype=self.data_subtype,
                reconnect=self.reconnect,
                log_level=self.log_level,
                on_open=self.on_open,
                on_message=self.on_message,
            )

            client.set_instruments(ticker_chunk)
            client.run()
            
            self.clients[index] = client

if __name__ == '__main__':

    mktdata = MarketDataFeedMultipleClients(
        api_key=API_KEY,
        ticker_list=TICKER_LIST,
        data_type=DATA_TYPE,
        data_subtype=DATA_SUBTYPE,
        num_connections=NUM_CONNECTIONS,
    )

    asyncio.run(mktdata.run())

    while True:
        sleep(30)
