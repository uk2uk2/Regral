##Will implement later, just need the central sources for now, filtering will be added, switching logic and other things in order to speed up data aggregation, will work on centralized and decentralized data sources..

import requests
import json

class DataOrchestrator:
    def __init__(self):
        self.api_sources = {
            "trading_economics": "https://api.tradingeconomics.com/indicators",
            "world_bank": "http://api.worldbank.org/v2/country/all/indicator/",
            "bea": "https://apps.bea.gov/api/data/",
            "financial_modeling_prep": "https://financialmodelingprep.com/api/v3/",
            "eod_historical_data": "https://eodhistoricaldata.com/api/macro-indicator/",
            "census_economic": "https://api.census.gov/data/",
            "alpha_vantage": "https://www.alphavantage.co/query",
            "oecd": "https://stats.oecd.org/SDMX-JSON/data/",
            "un_comtrade": "https://comtrade.un.org/api/get",
            "eurostat": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        }

        self.api_keys = {
            "trading_economics": "YOUR_API_KEY",
            "bea": "YOUR_API_KEY",
            "financial_modeling_prep": "YOUR_API_KEY",
            "eod_historical_data": "YOUR_API_KEY",
            "alpha_vantage": "YOUR_API_KEY",
            "un_comtrade": "YOUR_API_KEY"
        }

    def fetch_trading_economics(self, indicator="GDP"):
        """ Fetch macroeconomic indicators from Trading Economics API """
        url = f"{self.api_sources['trading_economics']}/{indicator}?c={self.api_keys['trading_economics']}&f=json"
        return self.get_data(url)

    def fetch_world_bank(self, indicator="NY.GDP.MKTP.CD"):
        """ Fetch data from the World Bank API """
        url = f"{self.api_sources['world_bank']}{indicator}?format=json"
        return self.get_data(url)

    def fetch_bea_data(self, dataset="NIPA", table_name="T10101"):
        """ Fetch US GDP and National Income data from BEA """
        url = f"{self.api_sources['bea']}?&UserID={self.api_keys['bea']}&method=GetData&datasetname={dataset}&TableName={table_name}&ResultFormat=JSON"
        return self.get_data(url)

    def fetch_financial_modeling_prep(self, indicator="gdp"):
        """ Fetch economic indicators from Financial Modeling Prep API """
        url = f"{self.api_sources['financial_modeling_prep']}economic-indicator/{indicator}?apikey={self.api_keys['financial_modeling_prep']}"
        return self.get_data(url)

    def fetch_eod_historical_data(self, country="US"):
        """ Fetch macroeconomic indicators from EOD Historical Data API """
        url = f"{self.api_sources['eod_historical_data']}{country}?api_token={self.api_keys['eod_historical_data']}&fmt=json"
        return self.get_data(url)

    def fetch_census_economic(self, dataset="timeseries/eits"):
        """ Fetch economic time-series data from US Census API """
        url = f"{self.api_sources['census_economic']}{dataset}"
        return self.get_data(url)

    def fetch_alpha_vantage(self, function="TIME_SERIES_DAILY", symbol="SPY"):
        """ Fetch stock market data from Alpha Vantage API """
        url = f"{self.api_sources['alpha_vantage']}?function={function}&symbol={symbol}&apikey={self.api_keys['alpha_vantage']}"
        return self.get_data(url)

    def fetch_oecd_data(self, dataset="QNA", location="USA"):
        """ Fetch OECD macroeconomic data """
        url = f"{self.api_sources['oecd']}{dataset}/{location}"
        return self.get_data(url)

    def fetch_un_comtrade(self, reporter="all", partner="world", trade_flow="import"):
        """ Fetch international trade data from UN Comtrade API """
        url = f"{self.api_sources['un_comtrade']}?max=5&type=C&freq=A&px=HS&ps=latest&r={reporter}&p={partner}&rg={trade_flow}&cc=AG2&fmt=json"
        return self.get_data(url)

    def fetch_eurostat(self, dataset="nama_10_gdp"):
        """ Fetch GDP data from Eurostat API """
        url = f"{self.api_sources['eurostat']}{dataset}"
        return self.get_data(url)

    def get_data(self, url):
        """ Generalized function to fetch data from APIs """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch data from {url}, Status Code: {response.status_code}"}
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_all_data(self):
        """ Fetch data from all available APIs """
        return {
            "trading_economics": self.fetch_trading_economics(),
            "world_bank": self.fetch_world_bank(),
            "bea": self.fetch_bea_data(),
            "financial_modeling_prep": self.fetch_financial_modeling_prep(),
            "eod_historical_data": self.fetch_eod_historical_data(),
            "census_economic": self.fetch_census_economic(),
            "alpha_vantage": self.fetch_alpha_vantage(),
            "oecd": self.fetch_oecd_data(),
            "un_comtrade": self.fetch_un_comtrade(),
            "eurostat": self.fetch_eurostat()
        }

# Usage
if __name__ == "__main__":
    orchestrator = DataOrchestrator()
    all_data = orchestrator.get_all_data()
    
    # Print consolidated data
    print(json.dumps(all_data, indent=4))
