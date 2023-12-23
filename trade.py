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


class IndicatorRSI:
    """
    Relative Strength Index Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `timeperiod`: period over which to calculate the ema
    -----------------------------------------------------------------
    return: Pandas Series containing RSA values
    """

    def __init__(self, closure_value: pd.DataFrame, period: str) -> pd.Series:
        self.closure_value = closure_value
        self.period = period
    
        return ta.RSI(real=self.closure_value, timeperiod=self.period)
  

class IndicatorMACD:
    """
    Moving Average Convergence/Divergence Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `fastperiod`: period for faster moving EMA
    - `slowperiod`: period for slow moving EMA
    -----------------------------------------------------------------
    return: Pandas Series containing MACD values
    """

    def __init__(self, closure_value: pd.DataFrame, fastperiod: int, slowperiod: int) -> pd.Series:
        self.closure_value = closure_value
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod

        return ta.MACD(real=self.closure_value, fastperiod=self.fastperiod, slowperiod=self.slowperiod) 
    

class IndicatorSTOCH:
    """
    Stochastic Oscillator Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `kperiod`: period used to calculate the %K line, representing the current price relative to the highest high and lowest low within the period
    - `dperiod`: period used to calculate the %D line, which is a moving average of the %K line
    - `lookback`: starting point for calculating the highest high and lowest low used in the %K calculation
    -----------------------------------------------------------------
    return: Pandas Series containing STOCH values
    """
    def __init__(self, closure_value: pd.DataFrame, kperiod: int, dperiod: int, lookback: int) -> pd.Series:
        self.closure_value = closure_value
        self.kperiod = kperiod
        self.dperiod = dperiod
        self.lookback = lookback

        return ta.STOCH(close=self.closure_value, kperiod=self.kperiod, dperiod=self.dperiod, lookback=self.lookback)
    

class IndicatorSMA:
    """
    Simple Moving Average Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `timeperiod`: period over which to calculate the sma
    -----------------------------------------------------------------
    return: Pandas Series containing SMA values
    """

    def __init__(self, closure_value: pd.DataFrame, timeperiod: int) -> pd.Series:
        self.closure_value = closure_value
        self.timeperiod = timeperiod

        return ta.SMA(real=self.closure_value, timeperiod=self.timeperiod)
    

class IndicatorEMA:
    """
    Exponential Moving Average Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `timeperiod`: period over which to calculate the ema
    -----------------------------------------------------------------
    return: Pandas Series containing EMA values
    """

    def __init__(self, closure_value: pd.DataFrame, timeperiod: int) -> pd.Series:
        self.closure_value = closure_value
        self.timeperiod = timeperiod

        return ta.EMA(real=self.closure_value, timeperiod=self.timeperiod)
