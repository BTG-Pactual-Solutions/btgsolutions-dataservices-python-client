from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_api_v1
from .authenticator import Authenticator
import pandas as pd
import json

class TickerLastEvent:
    """
    This class provides the last market data event available, for the provided ticker

    * Main use case:

    >>> from btgsolutions_dataservices import TickerLastEvent
    >>> last_event = TickerLastEvent(
    >>>     api_key='YOUR_API_KEY',
    >>> )

    >>> last_event.get_trades(
    >>>     ticker = 'PETR4',
    >>>     raw_data = False
    >>> )

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.
    """
    def __init__(
        self,
        api_key:Optional[str]
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.headers = {"authorization": f"authorization {self.token}"}

        self.available_data_types = ['equities', 'derivatives']

    def get_trades(self, data_type:str, ticker:str, raw_data:bool=False):

        """
        This method provides the last market data event available, for the provided ticker.

        Parameters
        ----------------
        data_type: str
            Market Data Type.
            Field is required. 
            Example: 'equities', 'derivatives'.
        ticker: str
            Ticker symbol.
            Field is required. Example: 'PETR4'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """
        if data_type not in self.available_data_types:
            raise Exception("Must provide a valid data_type. Valid data types are: {self.available_data_types}")

        url = f"{url_api_v1}/marketdata/last-event/trades/{data_type}?ticker={ticker}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            if raw_data:
                return response.json()
            else:
                return pd.DataFrame([response.json()])
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("error", "")}')

    def get_available_tickers(self, data_type:str):

        """
        This method provides all the available tickers for the specific data type.

        Parameters
        ----------------
        data_type: str
            Market Data Type.
            Field is required. 
            Example: 'equities', 'derivatives'.
        """

        url = f"{url_api_v1}/marketdata/last-event/trades/{data_type}/available-tickers"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("error", "")}')