
from typing import Optional
from ..exceptions import BadResponse, MarketTypeError, DelayError
import requests
from ..config import url_apis
import json
import pandas as pd
from .authenticator import Authenticator

class IntradayCandles:
    """
    This class provides realtime intraday candles for a given ticker or all tickers available for query.

    * Main use case:

    >>> from btgsolutions_dataservices import IntradayCandles
    >>> intraday_candles = IntradayCandles(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> candles = intraday_candles.get_intraday_candles(
    >>>     market_type = 'stocks',
    >>>     tickers = ['PETR4', 'ABEV3'],
    >>>     candle_period = '1m',
    >>>     delay='delayed',
    >>>     mode='absolute',
    >>>     raw_data=False
    >>> )    
    >>> PETR4 = candles.get('PETR4')
    >>> ABEV3 = candles.get('ABEV3')

    >>> intraday_candles.get_available_tickers(
    >>>     market_type='stocks'
    >>> )

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.
    """
    def __init__(
        self,
        api_key: Optional[str]
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.headers = {"authorization": f"authorization {self.token}"}

    def get_intraday_candles(
        self,
        market_type:str,
        tickers:list,
        candle_period:str,
        n:int=0,
        start:int=0,
        end:int=0,
        delay:str='delayed',
        mode:str='absolute',
        raw_data:bool=False
    ):     
        """
        This method provides realtime intraday candles for a given ticker.

        Parameters
        ----------------
        market_type: str
            Market type.
            Example: 'stocks', 'derivatives' or 'options'.
            Field is required.
        tickers: list of str
            Tickers that needs to be returned.
            Example: ['PETR4', 'ABEV3']
        candle_period: str
            Grouping interval.
            Example: '1m', '5m', '30m', '1h' or '1d'.
        n: int
            Number of candles to be returned.
            Default: all.
        start: int
            Start date (in Unix timestamp format).
        end: int
            End date (in Unix timestamp format)
        delay: str
            Data delay.
            Example: 'delayed' or 'realtime'.
            Default: 'delayed'.
        mode: str
            Candle mode.
            Example: 'absolute', 'relative' or 'spark'.
            Default: absolute.
        raw_data: bool
            If false, returns data in a dict of dataframes. If true, returns raw data.
            Default: False.
        """
        if market_type not in ['stocks', 'derivatives', 'options']:
            raise MarketTypeError(f"Must provide a valid 'market_type' parameter. Input: '{market_type}'. Accepted values: 'stocks', 'derivatives' or 'options'")

        if delay not in ['delayed', 'realtime']:
            raise DelayError(f"Must provide a valid 'delay' parameter. Input: '{delay}'. Accepted values: 'delayed' or 'realtime'")
        
        tickers = ','.join(tickers) if type(tickers) is list else tickers 

        if delay == 'realtime':
            url = f"{url_apis}/marketdata/candles/intraday/{market_type}?tickers={tickers}&candle_period={candle_period}&mode={mode}"
        else:
            url = f"{url_apis}/marketdata/candles/intraday/delayed/{market_type}?tickers={tickers}&candle_period={candle_period}&mode={mode}"

        if n:
            url += f'&n={n}'
        if start:
            url += f'&start={start}'
        if end:
            url += f'&end={end}'

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if raw_data:
                return response_data
            else:
                ret = {}
                for key, value in response_data.items():
                    ret[key] = pd.DataFrame(value) 
                return ret
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')

    def get_available_tickers(
        self,
        market_type:str,
        delay:str='delayed',
    ):
        """
        This method provides all tickers available for query.   

        Parameters
        ----------------
        market_type: str
            Market type.
            Example: 'stocks', 'derivatives' or 'options'.
            Field is required.
        delay: str
            Data delay.
            Example: 'delayed' or 'realtime'.
            Default: 'delayed'.
        """
        if market_type not in ['stocks', 'derivatives', 'options']:
            raise MarketTypeError(f"Must provide a valid 'market_type' parameter. Input: '{market_type}'. Accepted values: 'stocks', 'derivatives' or 'options'")

        if delay not in ['delayed', 'realtime']:
            raise DelayError(f"Must provide a valid 'delay' parameter. Input: '{delay}'. Accepted values: 'delayed' or 'realtime'")
        
        if delay == 'realtime':
            url = f"{url_apis}/marketdata/candles/intraday/{market_type}/available_tickers"
        else:
            url = f"{url_apis}/marketdata/candles/intraday/delayed/{market_type}/available_tickers"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')