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
                
        return data, data["Close"]


class IndicatorRSI:
    """
    Relative Strength Index Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `timeperiod`: period over which to calculate the ema
    -----------------------------------------------------------------
    return: None
    """

    def __init__(self, closure_value: pd.DataFrame, period: int) -> None:
        self.closure_value = closure_value
        self.period = period
    
        self.rsi = ta.RSI(real=self.closure_value, timeperiod=self.period)
  

class IndicatorMACD:
    """
    Moving Average Convergence/Divergence Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `fastperiod`: period for faster moving EMA
    - `slowperiod`: period for slow moving EMA
    - `signalperiod`: signal period for moving EMA
    -----------------------------------------------------------------
    return: return None
    """

    def __init__(self, closure_value: pd.DataFrame, fastperiod: int, slowperiod: int, signalperiod: int) -> None:
        self.closure_value = closure_value
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

        self.macd = ta.MACD(real=self.closure_value, fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod) 
    

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
    return: None
    """
    def __init__(self, closure_value: pd.DataFrame, kperiod: int, dperiod: int, lookback: int) -> None:
        self.closure_value = closure_value
        self.kperiod = kperiod
        self.dperiod = dperiod
        self.lookback = lookback

        self.stoch = ta.STOCH(close=self.closure_value, kperiod=self.kperiod, dperiod=self.dperiod, lookback=self.lookback)
    

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


class GenerateAlert:
    """
    Generate Alert is responsible to generate alert based on Indicator 
    -----------------------------------------------------------------
    input:
    - `indicator`: indicator for which to generate alert
    - `indicator_values`: calculate indicator value panda series for respective indicator
    - `historical_data`: historical data frame 
    - `symbol`: symbol of stock company
    - `debug`: flag to deactivate debugging, default FALSE
    -----------------------------------------------------------------
    return: alert message
    """

    def __init__(self, indicator: str, indicator_values: pd.Series, historical_data: pd.DataFrame, symbol: str, debug: bool = False) -> str:
        self.indicator = indicator
        self.indicator_values = indicator_values
        self.historical_data = historical_data
        self.symbol = symbol
        self.debug = debug

        # >>>>CONFIGURING THRESHOLD
        if indicator == "SMA" or indicator == "EMA":
            self.BUY_THRESHOLD = self.historical_data["Close"].iloc[-1] > self.indicator_values.iloc[-1] 

            self.SELL_THRESHOLD = self.historical_data["Close"].iloc[-1] < self.indicator_values.iloc[-1] 
        else:
            self.BUY_THRESHOLD = 30
            self.SELL_THRESHOLD = 70
        
        # >>>>Calling Alert Generators
        if debug is True:
            return self.genAlertBackTesting()
        else:
            return self.genAlertDeploy()

    def genAlertBackTesting(self):
        """
        Generate alert message for back testing purpose 
        ------------
        - Gives alert for each day in historical data
        ----------------------------------------------------------------
        return: alert message
        """

        for i in range(len(self.indicator_values)):
            current_value = self.indicator_values.iloc[i]
            current_date = self.historical_data["Close"].index[i].strftime("%Y=-%m-%d")

            if current_value <= self.BUY_THRESHOLD:
                message = "Signal: BUY | Indicator: {0} | Indicator Value: {1} On Date: {2}".format(self.indicator, current_value, current_date)
            
            elif current_value >= self.SELL_THRESHOLD:
                message = "Signal: SELL | Indicator: {0} | Indicator Value: {1} On Date: {2}".format(self.indicator, current_value, current_date)

        return message

    def genAlertDeploy(self):
        """
        Generate alert message for deployment purpose 
        ------------
        - Gives alert with reduced frequency via an applied filter
        - Other options: (cooling period, combining indicators: not implemented)
        ----------------------------------------------------------------
        return: alert message
        """

        for i in range(1, len(self.indicator_values)):
            previous_value = self.indicator_values.iloc[i-1]
            current_value = self.indicator_values.iloc[i]
            current_date = self.historical_data.index[i].strftime("%Y-%m-%d")
            
            if current_value <= self.BUY_THRESHOLD and previous_value > self.BUY_THRESHOLD:
                message = "Signal: BUY | Indicator: {0} | Indicator Value: {1} On Date: {2}".format(self.indicator, current_value, current_date)
            
            elif current_value >= self.SELL_THRESHOLD and previous_value < self.SELL_THRESHOLD:
                message = "Signal: SELL | Indicator: {0} | Indicator Value: {1} On Date: {2}".format(self.indicator, current_value, current_date)
        
        return message
    

class PushAlert:
    """
        Push alert message via required mode
        ---------------------------------------------------------------
        input:
        - `alert_message`: alert message to push
        - `push_mode`: alert mode, default Console
        ----------------------------------------------------------------
        return: None
        """
    
    def __init__(self, alert_message: str, push_mode: str = "Console") -> None:
        self.alert_message = alert_message
        self.push_mode = push_mode

        if push_mode == "Console":
            self.pushConsole:()
        else: 
            pass
    
    def pushConsole(self):
        """
        Push alert to console
        ----------------------------------------------------------------
        return: None
        """
        print(self.alert_message)