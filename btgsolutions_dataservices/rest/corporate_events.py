from typing import List, Optional
from ..exceptions import BadResponse
import requests
from ..config import url_apis
from .authenticator import Authenticator
import pandas as pd
import json

class CorporateEvents:
    """
    This class provides the market data corporate events

    * Main use case:

    >>> from btgsolutions_dataservices import CorporateEvents
    >>> corporate_events = CorporateEvents(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> corporate_events.get(
    >>>     start_date = '2024-05-10',
    >>>     end_date = '2024-05-31',
    >>>     tickers = ['PETR4']
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

    def get(self, start_date:str, end_date:str, tickers:List[str] = [], raw_data:bool=False): 

        """
        This method uses corporate events filtered by a range of dates (ex_date) and a list of tickers

        Parameters
        ----------------
        start_date: string<date>
            Lower bound for corporate events. Filtering by ex_date. Format: "YYYY-MM-DD".
            Field is required. Example: '2023-10-06'.
        end_date: string<date>
            Upper bound for corporate events. Filtering by ex_date. Format: "YYYY-MM-DD".
            Field is required. Example: '2023-10-06'.
        ticker: List[str]
            List of tickers.
            Field is not required. Example: ['PETR4', 'VALE3']. Default: [].
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """

        url = f"{url_apis}/marketdata/corporate-events?start_date={start_date}&end_date={end_date}" + (f"&tickers={','.join(tickers)}" if len(tickers) > 0 else "")

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            if raw_data:
                return response.json()
            else:
                return pd.DataFrame(response.json())
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("error", "")}')