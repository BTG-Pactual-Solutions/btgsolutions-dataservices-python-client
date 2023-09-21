from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_api_v1
from .authenticator import Authenticator
import pandas as pd
import json

class IntradayTickData:
    """
    This class provides tick-by-tick market data from the current day, for the provided ticker

    * Main use case:

    >>> from btgsolutions_dataservices import IntradayTickData
    >>> tick_data = IntradayTickData(
    >>>     api_key='YOUR_API_KEY',
    >>> )

    >>> tick_data.get_trades(
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

    def get_trades(self, ticker:str, raw_data:bool=False):

        """
        This method provides tick-by-tick trade data from the current day, for the provided ticker.

        Parameters
        ----------------
        ticker: str
            Ticker symbol.
            Field is required. Example: 'PETR4'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        url = f"{url_api_v1}/marketdata/tick/intraday/trades/{ticker}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            if raw_data:
                return response.json()
            else:
                return pd.DataFrame(response.json())
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("error", "")}')
