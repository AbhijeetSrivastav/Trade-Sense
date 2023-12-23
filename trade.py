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
                
        return data, data["Close"], data["Low"], data["High"]


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
        self.suggestions = []

        self.BUY_THRESHOLD = 30
        self.SELL_THRESHOLD = 70

    def cal_suggestions(self)->tuple:
        "Calculate suggestions"
        self.rsi = ta.RSI(real=self.closure_value, timeperiod=self.period)

        for i in range(len(self.closure_value)):
            current_value = self.closure_value.iloc[i]

            if current_value < self.BUY_THRESHOLD:
                self.suggestions.append('BUY')
            elif current_value > self.SELL_THRESHOLD:
                self.suggestions.append('SELL')
            else:
                self.suggestions.append('HOLD')
        
        return self.suggestions, self.rsi


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
        self.suggestions = []

        # ta.macd returns three series macd, signal, macd_hist
        self.macd_values, self.signal_values, self.macd_hist_values = ta.MACD(real=closure_value, fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)

    def cal_suggestions(self)->tuple:
        "Calculate suggestions"
        # SIGNAL LOGIC: A
        '''
        If MACD_HIST CROSSES 0 then Buy else Sell
        '''
        for macd_hist in self.macd_hist_values:
            if macd_hist > 0:
                self.suggestions.append('BUY')
            else:
                self.suggestions.append('Sell')

        # # SIGNAL LOGIC: B
        # '''
        # If MACD > SIGNAL then Buy else Sell
        # # '''
        # for macd, signal in zip(self.macd_values, self.signal_values):
        #     if macd > signal:
        #         self.suggestions.append('BUY')
        #     else:
        #         self.suggestions.append('SELL')
        
        return self.suggestions, self.macd_hist_values
          
    
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
    def __init__(self, closure_value: pd.DataFrame, low_values: pd.DataFrame, high_values: pd.DataFrame, kperiod: int, dperiod: int, lookback: int) -> None:
        self.closure_value = closure_value
        self.low_values = low_values
        self.high_values = high_values
        self.kperiod = kperiod
        self.dperiod = dperiod
        self.lookback = lookback
        self.BUY_THRESHOLD = 20
        self.SELL_THRESHOLD = 80
        self.suggestions = []

    def cal_suggestions(self)->tuple:
        "Calculate suggestions"
        self.k_values, self.d_values,  = ta.STOCH(self.closure_value, self.low_values, self.high_values, self.kperiod, self.dperiod, self.lookback)

        for k, d in zip(self.k_values, self.d_values):
            if k > self.SELL_THRESHOLD and d > self.SELL_THRESHOLD:
                self.suggestions.append('SELL')
            elif k < self.BUY_THRESHOLD and d < self.BUY_THRESHOLD:
                self.suggestions.append('BUY')
            else:
                self.suggestions.append('HOLD')
        
        return self.suggestions, self.k_values


class IndicatorSMA:
    """
    Simple Moving Average Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `short_sma_timeperiod`: period over which to calculate the sma shorter
    - `long_sma_timeperiod`: period over which to calculate the sma longer
    -----------------------------------------------------------------
    return: None
    """

    def __init__(self, closure_value: pd.DataFrame, short_sma_timeperiod: int, long_sma_timeperiod: int) ->None:
        self.closure_value = closure_value
        self.short_sma_timeperiod = short_sma_timeperiod
        self.long_sma_timeperiod = long_sma_timeperiod
        self.suggestions = []


    def cal_suggestions(self)->tuple:
        "Calculate suggestions"
        self.short_sma_values = ta.SMA(real=self.closure_value, timeperiod=self.short_sma_timeperiod)

        self.long_sma_values = ta.SMA(real=self.closure_value, timeperiod=self.long_sma_timeperiod)

        self.short_sma_shift_values = self.short_sma_values.shift(1)
        self.long_sma_shift_values = self.long_sma_values.shift(1)

    
        for short_sma, long_sma, short_sma_shift, long_sma_shift in zip(self.short_sma_values, self.long_sma_values, self.short_sma_shift_values, self.long_sma_shift_values):
            if (short_sma > long_sma) and (short_sma_shift <= long_sma_shift):
                self.suggestions.append('BUY')
            elif (short_sma < long_sma) and (short_sma_shift >= long_sma_shift):
                self.suggestions.append('SELL')
            else:
                self.suggestions.append('HOLD')
        
        return self.suggestions, ["SMA Short:" + str(round(short_sma, 2)) + " | " + "LONG SMA:" + str(round(long_sma, 2)) for sma_short, long_sma in zip(self.short_sma_values, self.long_sma_values)]


class IndicatorEMA:
    """
    Exponential Moving Average Indicator
    -----------------------------------------------------------------
    input:
    - `closure_value`: array or pandas series containing closing prices
    - `short_ema_timeperiod`: period over which to calculate the ema shorter
    - `long_ema_timeperiod`: period over which to calculate the ema longer
    -----------------------------------------------------------------
    return: None
    """

    def __init__(self, closure_value: pd.DataFrame, short_ema_timeperiod: int, long_ema_timeperiod: int) ->None:
        self.closure_value = closure_value
        self.short_ema_timeperiod = short_ema_timeperiod
        self.long_ema_timeperiod = long_ema_timeperiod
        self.suggestions = []

        self.short_ema_values = ta.EMA(real=self.closure_value, timeperiod=self.short_ema_timeperiod)

        self.long_ema_values = ta.EMA(real=self.closure_value, timeperiod=self.long_ema_timeperiod)

        self.short_ema_shift_values = self.short_ema_values.shift(1)
        self.long_ema_shift_values = self.long_ema_values.shift(1)
        self.closure_shift_values = self.closure_value.shift(1)
    
        for short_ema, long_ema, short_ema_shift, long_ema_shift, close, close_shift in zip(self.short_ema_values, self.long_ema_values, self.short_ema_shift_values, self.long_ema_shift_values, self.closure_value, self.closure_shift_values):
            if (short_ema > long_ema) and (short_ema_shift <= long_ema_shift):
                self.suggestions.append('BUY')
            elif (close < short_ema) and (close_shift >= short_ema_shift):
                self.suggestions.append('SELL')
            else:
                self.suggestions.append('HOLD')


class GenerateAlert:
    """
    Generate Alert is responsible to generate alert based on Indicator 
    -----------------------------------------------------------------
    input:
    - `indicator`: indicator for which to generate alert
    - `indicator_suggestions`: indicator suggestions
    - `historical_data`: historical data frame 
    - `symbol`: symbol of stock company
    -----------------------------------------------------------------
    return: alerts
    """

    def __init__(self, indicator: str, indicator_suggestions: list, indicator_values: list, historical_data: pd.DataFrame) -> str:
        self.indicator = indicator
        self.indicator_suggestions = indicator_suggestions
        self.indicator_values = indicator_values
        self.historical_data = historical_data
        self.alerts = []

        for suggestion, date, indicator_value in zip(self.indicator_suggestions,[self.historical_data["Close"].index[i].strftime("%Y-%m-%d") for i in range(len(self.indicator_values))], self.indicator_values):
            message = "Signal: {0} | Indicator: {1} | Indicator Value: {2} On Date: {3}".format(suggestion, self.indicator, indicator_value, date)
            
            self.alerts.append(message)
        

class PushAlert:
    """
        Push alert message via required mode
        ---------------------------------------------------------------
        input:
        - `alert_messages`: alert messages to push
        ----------------------------------------------------------------
        return: None
        """
    
    def __init__(self, alert_messages: list) -> None:
        self.alert_messages = alert_messages
    
    def pushConsole(self):
        """
        Push alert to console
        ----------------------------------------------------------------
        return: None
        """
        for i in range(len(self.alert_messages)):
            print('>>  '+ self.alert_messages[i])