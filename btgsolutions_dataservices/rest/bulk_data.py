from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_api_v1
from .authenticator import Authenticator
import json
import pandas as pd
from io import BytesIO
import pyarrow.parquet as pq

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

    def get_data(
        self,
        ticker:str,
        date:str,
        data_type:str='trades',
        raw_data:bool=False
    ):
        """
        This method provides historical candles for a given ticket in determined period.

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
            Field is required. Example: 'trades', 'trades-rlp', 'books'.
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
