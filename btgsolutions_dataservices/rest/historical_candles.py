from typing import Optional
from ..exceptions import BadResponse, MarketTypeError
import requests
from ..config import url_apis_v3
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

    def get_intraday_history_candles(
        self,
        market_type:str,
        ticker:str,
        date:str,
        candle:str,
        corporate_events_adj:bool,
        rmv_after_market:bool,
        timezone:str,
        raw_data:bool=False
    ):
        """
        This method provides historical candles for a given ticket in determined period.

        Parameters
        ----------------
        market_type: str
            Field is required. Allowed values: 'stocks' or 'derivatives'.
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        date: string<date>
            Date of requested data. Format: "YYYY-MM-DD".
            Field is required. Example: '2023-10-06'.
        candle: str
            Candle period.
            Field is required. Allowed values: '1s', '1m', '5m', '15m', '30m' or '1h'.
        corporate_events_adj: bool
            Corporate events adjustment.
            Field is required. Allowed values: 'true' or 'false'.
        rmv_after_market: bool
            Remove trades after market close.
            Field is required. Allowed values: 'true' or 'false'.
        timezone: str
            Timezone of the datetime.
            Field is required. Allowed values: 'America/Sao_Paulo' or 'UTC'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        
        if market_type not in ['stocks', 'derivatives']:
            raise MarketTypeError(f'Allowed values: "stocks" or "derivatives". Input value: "{market_type}".')
        
        url = f"{url_apis_v3}/marketdata/history/candles/intraday/{market_type}?ticker={ticker}&corporate_events_adj={corporate_events_adj}&rmv_after_market={rmv_after_market}&timezone={timezone}&date={date}&candle={candle}"
        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data if raw_data else pd.DataFrame(response_data)

        response = json.loads(response.text)
        raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')
    
    def get_interday_history_candles(
        self,
        market_type:str,
        ticker:str,
        start_date:str,
        end_date:str,
        corporate_events_adj:bool,
        rmv_after_market:bool,
        timezone:str,
        raw_data:bool=False
    ):
        """
        This method provides historical candles for a given ticket in determined period.

        Parameters
        ----------------
        market_type: str
            Field is required. Allowed values: 'stocks' or 'derivatives'.
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        start_date: string<date>
            Start date of analysis. Format: "YYYY-MM-DD".
            Field is required. Example: '2022-10-06'.
        end_date: string<date>
            End date of analysis. Format: "YYYY-MM-DD".
            Field is required. Example: '2023-01-22'.
        corporate_events_adj: bool
            Corporate events adjustment.
            Field is required. Allowed values: 'true' or 'false'.
        rmv_after_market: bool
            Remove trades after market close.
            Field is required. Allowed values: 'true' or 'false'.
        timezone: str
            Timezone of the datetime.
            Field is required. Allowed values: 'America/Sao_Paulo' or 'UTC'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        
        if market_type not in ['stocks', 'derivatives']:
            raise MarketTypeError(f'Allowed values: "stocks" or "derivatives". Input value: "{market_type}".')
        
        url = f"{url_apis_v3}/marketdata/history/candles/interday/{market_type}?ticker={ticker}&corporate_events_adj={corporate_events_adj}&rmv_after_market={rmv_after_market}&timezone={timezone}&start_date={start_date}&end_date={end_date}"
        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data if raw_data else pd.DataFrame(response_data)

        response = json.loads(response.text)
        raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')