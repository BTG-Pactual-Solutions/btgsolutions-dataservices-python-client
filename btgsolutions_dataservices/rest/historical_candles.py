from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_apis
from .authenticator import Authenticator
import json
import pandas as pd

class HistoricalCandles:
    """
    This class provides historical candles for a given ticker or all tickers available for query.

    * Main use case:

    >>> from btgsolutions_dataservices import HistoricalCandles
    >>> hist_candles = HistoricalCandles(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> hist_candles.get_historical_candles(
    >>>     ticker = 'PETR4',
    >>>     lookback = '1M',
    >>>     mode = 'relative',
    >>>     raw_data = False
    >>> )
    >>> hist_candles.get_available_tickers()

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

    def get_historical_candles(
        self,
        ticker:str,
        lookback:str,
        mode:str='absolute',
        raw_data:bool=False
    ):
        """
        This method provides historical candles for a given ticket in determined period.

        Parameters
        ----------------
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        lookback: str
            Date period.
            Field is required. Example: '5D', '1M', '6M', 'YTD', '1Y', '2Y' or '3Y'.
        mode: str
            Candle mode.
            Field is not required. Example: 'absolute' or 'relative'.
            Default: 'absolute'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        url = f"{url_apis}/marketdata/candles/historical?ticker={ticker}&lookback={lookback}&mode={mode}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data if raw_data else pd.DataFrame(response_data)

        response = json.loads(response.text)
        raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')

    def get_available_tickers(self):  
        """
        This method provides all tickers available for query.   
        """
        url = f"{url_apis}/marketdata/candles/historical/available_tickers"
        response = requests.request("GET", url,  headers=self.headers)

        if response.status_code == 200:
            return json.loads(response.text).get('available_tickers', [])
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')