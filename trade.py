# Import Libraries
import yfinance as yf
import talib as ta
import pandas as pd


class DataFetcher:
    """
    DataFetcher class is responsible to fetch data from yahoo finance 
    -----------------------------------------------------------------
    input:
    - `symbol`: symbol of the stock company
    - `period`: period for which to fetch data
    - `interval`: interval between each data points
    -----------------------------------------------------------------
    return: Pandas Series containing RSA values
    """

    def __init__(self, symbol: str, period: str, interval: str) -> pd.DataFrame:
        self.symbol = symbol
        self.period = period
        self.interval = interval
    
    def fetchClosureHistoryData(self):
        """
        Fetches closure value from historical data from yahoo finance 
        ----------------------------------------------------------------
        return: Pandas Series containing closure values
        """

        try:
            data = yf.Ticker(self.symbol).history(period=self.period, interval=self.interval)
        except Exception as e:
            raise Exception(e)
                
        return data["Close"]



  