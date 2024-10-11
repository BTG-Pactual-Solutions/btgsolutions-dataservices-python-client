import requests
import json
import pandas as pd
from typing import List, Optional
from .authenticator import Authenticator
from ..exceptions import BadResponse
from ..config import url_apis

def process_financial_table(financial_table_content: list):
    fin_table = [k["fields"] for k in financial_table_content]
    
    fin_table_headers = [k for k in fin_table if k["tP_ROW"] == "H"][0]
    fin_table_headers = [v for k,v in fin_table_headers.items() if "tP_" not in k]

    df = pd.DataFrame(fin_table)

    # first row as column
    df = df.loc[:, ~df.columns.str.startswith("tP_")]
    df.columns = fin_table_headers
    df.drop(index=0, inplace=True)

    # first col as index
    first_col = df.columns[0]
    df = df.drop(df[df[first_col] == '&nbsp;'].index)
    df.set_index(first_col, inplace=True)
    df.index.name = "Period"

    df = df.T
    return df

class CompanyData:
    """
    This class provides company general information and fundamentalist data. 

    * Main use case:

    >>> from btgsolutions_dataservices import CompanyData
    >>> company_data = CompanyData(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> company_data.general_info(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.income_statement(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.balance_sheet(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.cash_flow(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.valuation(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.ratios(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.growth(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.interims(
    >>>     ticker = 'PETR4'
    >>> )
    >>> company_data.all_financial_tables(
    >>>     ticker = 'PETR4'
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
    
    def general_info(self, ticker: str, raw_data: bool=False):
        """
        This method returns company general information such as name, ticker, sector, description.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: 'PETR4'.
        raw_data: bool
            If false, returns financial tables in dataframes. If true, returns raw data.
            Field is not required. Default: False.
        """

        url = f"{url_apis}/company_indicators/company_info/{ticker}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if raw_data:
                return data
            else:
                return pd.DataFrame([data])
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError", "")}')
    
    def income_statement(self, ticker: str):
        """
        This method returns the company Income Statement.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Income Statement")
    
    def balance_sheet(self, ticker: str):
        """
        This method returns the company Balance Sheet.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Balance Sheet")

    def cash_flow(self, ticker: str):
        """
        This method returns the company Cash Flow.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Cash Flow")

    def valuation(self, ticker: str):
        """
        This method returns the company Valuation.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Valuation")

    def ratios(self, ticker: str):
        """
        This method returns the company Ratios.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Ratios")

    def growth(self, ticker: str):
        """
        This method returns the company Growth.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Growth")

    def interims(self, ticker: str):
        """
        This method returns the company Interims.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        """
        all_tables = self.all_financial_tables(ticker)
        return all_tables.get("Interims")

    def all_financial_tables(self, ticker: str, raw_data: bool=False):
        """
        This method returns all available financial tables (such as Valuation, Income Statement, Cash Flow) for the requested company ticker.

        Parameters
        ----------------
        ticker: str
            Company ticker symbol.
            Field is required. Example: "PETR4". The ticker radical is also allowed. Example: "PETR".
        raw_data: bool
            If false, returns financial tables in dataframes. If true, returns raw data.
            Field is not required. Default: False.
        """

        url = f"{url_apis}/fundamentalist_data/financial_tables/{ticker}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if raw_data:
                return data
            else:
                tables = {}
                for rawFinancialTable in data["financialTables"]:
                    tables[rawFinancialTable["tableName"]] = process_financial_table(rawFinancialTable["tableContent"])
                return tables
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError", "")}')