import os
from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_api_v1
from .authenticator import Authenticator
import json
import pandas as pd
from io import BytesIO
import pyarrow.parquet as pq

def download_compressed_file(url, headers):
    
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()

        try:
            file_name = response.headers.get('content-disposition').split('filename=')[1]
        except:
            file_name = "compressed_file.tar.gz"
        
        total_length = response.headers.get('content-length')
        if total_length is not None:
            total_length = int(total_length)
            bytes_downloaded = 0

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    if total_length is not None:
                        bytes_downloaded += len(chunk)
                        print(f"Downloaded: {bytes_downloaded / total_length * 100:.2f}%", end='\r')

    current_dir_name = os.getcwd()
    print(f"\nDownload completed. File path: '{current_dir_name}/{file_name}'")

class BulkData:
    """
    This class provides market data by ticker and date, in .csv format

    * Main use case:

    >>> from btgsolutions_dataservices import BulkData
    >>> bulk_data = BulkData(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> bulk_data.get_data(
    >>>     ticker = 'PETR4',
    >>>     date = '2023-07-03',
    >>>     data_type = 'trades',
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

    def get_available_tickers(
        self,
        date:str,
        data_type:str,
        prefix:str=''
    ):  
        """
        This method provides all tickers available for query, for the provided market data type.

        Parameters
        ----------------
        date: str
            Date period.
            Field is required.
            Format: 'YYYY-MM-DD'.
            Example: '2023-07-03'.
        data_type: str
            Market data type.
            Field is required.
            Example: 'trades', 'trades-rlp' or 'books'.
        prefix: str
            Filters tickers starting with the prefix.
            Field is optional.
            Example: 'DOL'.
        """
        url = f"{url_api_v1}/marketdata/bulkdata/available-tickers?date={date}&data_type={data_type}&prefix={prefix}"
        response = requests.request("GET", url,  headers=self.headers)

        response_json = response.json()
        if response.status_code == 200: return response_json['tickers']
        raise BadResponse(f'Error: {response_json.get("ApiClientError", "")}.\n{response_json.get("SuggestedAction", "")}')

    def get_market_data_channels(
        self,
        date:str,
    ):
        """
        This method provides all the available market data channels for a given date. For more detailed information about market data channels, please consult our documentation, at https://dataservicesdocs.btgpactualsolutions.com/home > Data Specs > Market Data channel definition.

        Parameters
        ----------------
        date: str
            Date period.
            Field is required.
            Format: 'YYYY-MM-DD'. Example: '2023-07-03', '2023-07-28'.
        """
        url = f"{url_api_v1}/marketdata/bulkdata/channels?date={date}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')

    def get_compressed_data(
        self,
        channel:str,
        date:str,
        data_type:str='instruments',
        binary:bool=False
    ):
        """
        This method provides market data via compressed files (instruments, snapshot, incremental) for a given market data channel and date. Function get_market_data_channels provides all the available channels for a given date.

        Parameters
        ----------------
        channel: str
            Market Data channel.
            Field is required. Example: '001'.
        date: str
            Date period.
            Field is required.
            Format: 'YYYY-MM-DD'. Example: '2023-07-03', '2023-07-28'.
        data_type: str
            Market data type.
            Field is required. Example: 'instruments', 'snapshot', 'incremental'.
        binary: bool
            If true, returns binary data. If false, returns FIX/FAST data.
            Field is not required. Default: false.
        """
        url = f"{url_api_v1}/marketdata/bulkdata/compressed/{data_type}?channel={channel}&date={date}&binary={binary}"
        download_compressed_file(url, headers=self.headers)

    def get_data(
        self,
        ticker:str,
        date:str,
        data_type:str='trades',
        n:int=10,
        raw_data:bool=False
    ):
        """
        This method provides tick-by-tick market data (trades, RLP-trades, books) for a given ticker and date.

        Parameters
        ----------------
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        date: str
            Date period.
            Field is required.
            Format: 'YYYY-MM-DD'. Example: '2023-07-03', '2023-07-28'.
        data_type: str
            Market data type.
            Field is required. Example: 'trades', 'trades-rlp', 'books', 'book-events' or 'auction-times'.
        n: int
            Book depth.
            Field is not required. Default: 10. N must be an integer between 1 and 50, boundaries included.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        url = f"{url_api_v1}/marketdata/bulkdata/{data_type}?ticker={ticker}&date={date}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:

            try:

                if raw_data == False:
                    parquet_buffer = BytesIO(response.content)
                    parquet_file = pq.ParquetFile(parquet_buffer)

                    if data_type == 'books':
                        if not 1 <= n <= 50:
                            raise Exception("'n' must be an integer between 1 and 50, boundaries included.")

                        columns_to_filter = self.__get_cols(n)
                        df = parquet_file.read(columns=columns_to_filter).to_pandas()
                    else:
                        df = parquet_file.read().to_pandas()

                    return df

                else:
                    content_disposition = response.headers.get('Content-Disposition', '')
                    filename = content_disposition.split('filename=')[1]

                    # Write the content to a file
                    with open(filename, 'wb') as file:
                        file.write(response.content)
                    return None
                
            except Exception as e:
                print(f'error while trying to retrieve file:\n{e}')
                return None

        response = json.loads(response.text)
        raise BadResponse(f'Error: {response.get("ApiClientError", "")}.\n{response.get("SuggestedAction", "")}')

    def __get_cols(self, n:int=10):

        book_depth_col_types = ['bp','bq','op','oq']
        book_depth_cols = [type+str(i) for type in book_depth_col_types for i in range(1,n+1)]
        timestamp_col = ['timestamp']
        columns_to_filter = timestamp_col + book_depth_cols

        return columns_to_filter