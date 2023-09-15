
from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_apis
import json
import pandas as pd
from .authenticator import Authenticator

class HighFrequencyNews:
    """
    This class provides realtime and historical news of several news .

    * Main use case:

    >>> from btgsolutions_dataservices import HighFrequencyNews

    >>> hfn = HighFrequencyNews(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> latest_news = hfn.latest_news(
    >>>     n = 15,
    >>> )

    >>> petro_news = hfn.filter_news(
    >>>     ticker = 'PETR4',
    >>> )

    >>> ibov_news = hfn.filter_news(
    >>>     tag = 'IBOV',
    >>> )

    >>> news_21_08 = hfn.historical_news(
    >>>     start_date = '2023-08-21',
    >>>     end_date = '2023-08-22',
    >>> )

    >>> available_feeds = hfn.get_available_feeds()
    >>> available_sources = hfn.get_available_sources()
    >>> available_tickers = hfn.get_available_tickers()
    >>> available_tags = hfn.get_available_tags()

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

        self.available_countries = ['brazil', 'chile']
        self.available_feeds = ['raw', 'economy', 'politics', 'crypto', 'cvm', 'ptax']

        self.available_ref_types = ['tickers','tags', 'feeds', 'sources']

        self.min_news = 1
        self.max_news = 200

    def latest_news(
        self,
        feed:str='raw',
        country:str='brazil',
        n:int=10,
        raw_data:bool=False
    ):     
        """
        Latest news by feed.

        Parameters
        ----------------
        feed: str
            News feed.
            Example: 'raw', 'economy', 'politics', 'crypto', 'cvm'.
            Default: 'raw'.
            Field is not required.
        country: str
            Country name.
            Example: 'brazil', 'chile'.
            Default: 'brazil'.
            Field is not required.
        n: int
            Number of news to be returned.
            Default: 10.
            Field is not required.
        raw_data: bool
            If True, returns raw data from API, if False, returns a Pandas DataFrame.
            Default: False.
            Field is not required.
        """
        
        if country not in self.available_countries:
            raise Exception(f"Must provide a valid 'country' parameter. Input: '{country}'. Accepted values: {self.available_countries}")

        if feed not in self.available_feeds:
            raise Exception(f"Must provide a valid 'feed' parameter. Input: '{feed}'. Accepted values: {self.available_feeds}")
        
        if not self.min_news < n < self.max_news: 
            raise Exception(f"Invalid 'n' parameter. Input: '{n}'. 'n' Must be >= {self.min_news} and <= {self.max_news}")

        url = f"{url_apis}/hfn/{country}/latest_news/{feed}?n={n}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if raw_data:
                return response_data
            else: 
                return pd.DataFrame(response_data)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')

    def filter_news(
        self,
        ticker:str=None,
        tag:str=None,
        force:bool=True,
        country:str='brazil',
        raw_data:bool=False
    ):
        """
        Filter news by ticker or tag. If both ticker and tag are provided, the filter will be by ticker only 

        Parameters
        ----------------
        ticker: str
            Ticker symbol. Will be used to filter news.
            Example: 'VALE3', 'PETR4'.
            Field is not required.
        tag: str
            Tag name. Will be used to filter news.
            Example: 'IBOV', 'TESOURO', 'RENDA_FIXA'.
            Field is not required.
        force: bool
            Force to return news even if it does not match the requested parameters.
            Default: True
            Example: True, False.
            Field is required.
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        raw_data: bool
            If True, returns raw data from API, if False, returns a Pandas DataFrame.
            Default: False.
            Field is not required.
        """
        if force is True: force_str = 'true'
        else: force_str = 'false'

        if country not in self.available_countries:
            raise Exception(f"Must provide a valid 'country' parameter. Input: '{country}'. Accepted values: {self.available_countries}")

        if not isinstance(ticker, str) and not isinstance(tag, str):
            raise Exception(f"Must provide a ticker or a tag in order to filter news")
        elif isinstance(ticker, str):
            url = f"{url_apis}/hfn/{country}/filter_news/tickers/{ticker}?force={force_str}"
        else:
            url = f"{url_apis}/hfn/{country}/filter_news/tags/{tag}?force={force_str}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if raw_data:
                return response_data
            else: 
                return pd.DataFrame(response_data)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')

    def historical_news(
        self,
        start_date:str,
        end_date:str,
        feed:str='raw',
        country:str='brazil',
        raw_data:bool=False
    ):
        """
        Provide a datetime interval and get all the news registered on that interval. The interval between start_date and end_date must be 24 hours maximum.

        Parameters
        ----------------
        start_date: str
            Upper bound for news publishing time. Supported formats: ISO Date (YYYY-MM-DD), Long Date (MMM DD YYYY), Short Date (MM/DD/YYYY).
            Example: '2023-08-21'.
            Field is required.
        end_date: str
            Lower bound for news publishing time. Supported formats: ISO Date (YYYY-MM-DD), Long Date (MMM DD YYYY), Short Date (MM/DD/YYYY).
            Example: '2023-08-22'.
            Field is required.
        feed: str
            Feed name.
            Default: 'raw'
            Example: 'raw', 'economy', 'politics', 'crypto', 'cvm'.
            Field is required.
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        raw_data: bool
            If True, returns raw data from API, if False, returns a Pandas DataFrame.
            Default: False.
            Field is not required.
        """
        if country not in self.available_countries:
            raise Exception(f"Must provide a valid 'country' parameter. Input: '{country}'. Accepted values: {self.available_countries}")

        if feed not in self.available_feeds:
            raise Exception(f"Must provide a valid 'feed' parameter. Input: '{feed}'. Accepted values: {self.available_feeds}")
        
        url = f"{url_apis}/hfn/{country}/news_history?start_date={start_date}&end_date={end_date}&feed={feed}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if raw_data:
                return response_data
            else: 
                return pd.DataFrame(response_data)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')

    def get_available_feeds(self, country:str='brazil'):
        """
        This method provides all feeds available for query.   

        Parameters
        ----------------
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        """
        return self.__get_available_reference(ref_type='feeds', country=country)
    
    def get_available_sources(self, country:str='brazil'):
        """
        This method provides all sources available for query.   

        Parameters
        ----------------
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        """
        return self.__get_available_reference(ref_type='sources', country=country)
    
    def get_available_tickers(self, country:str='brazil'):
        """
        This method provides all tickers available for query.   

        Parameters
        ----------------
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        """
        return self.__get_available_reference(ref_type='tickers', country=country)

    def get_available_tags(self, country:str='brazil'):
        """
        This method provides all tags available for query.   

        Parameters
        ----------------
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        """
        return self.__get_available_reference(ref_type='tags', country=country)

    def __get_available_reference(
        self,
        ref_type:str,
        country:str='brazil',
    ):
        """
        Inner function to query reference data by type.   

        Parameters
        ----------------
        ref_type: str
            Reference type.
            Example: 'brazil', 'chile'.
            Field is required.
        country: str
            Country name.
            Default: 'brazil'
            Example: 'brazil', 'chile'.
            Field is required.
        """
        if ref_type not in self.available_ref_types:
            raise Exception(f"Must provide a valid 'ref_type' parameter. Input: '{ref_type}'. Accepted values: {self.available_ref_types}")

        if country not in self.available_countries:
            raise Exception(f"Must provide a valid 'country' parameter. Input: '{country}'. Accepted values: {self.available_countries}")

        url = f"{url_apis}/hfn/{country}/available_{ref_type}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction", "")}')
