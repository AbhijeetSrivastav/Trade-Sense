
from trade import DataFetcher
from trade import IndicatorRSI
from trade import IndicatorMACD
from trade import IndicatorSMA
from trade import IndicatorEMA

# CONFIGURABLE PARAMETERS
SYMBOL = 'TATAMOTORS.NS'
PERIOD_FOR_DATA_COLLECTION = '2y'
INTERVAL = '1d'
INDICATOR = 'RSI'
PERIOD_FOR_CALCULATION = 14
FAST_PERIOD = 12 
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9
K_PERIOD = 14
D_PERIOD = 4
LOOKBACK = 5
TIMEPERIOD = 50


# HISTORICAL DATA COLLECTION
historical_data, closure_values = DataFetcher(symbol=SYMBOL, period=PERIOD_FOR_DATA_COLLECTION, interval=INTERVAL).fetchClosureHistoryData()


# INDICATOR CALCULATION
# >> RSI
rsi_values = IndicatorRSI(closure_value=closure_values, period=PERIOD_FOR_CALCULATION).rsi

#>> MACD
macd_values = IndicatorMACD(closure_value=closure_values, fastperiod=FAST_PERIOD, slowperiod=SLOW_PERIOD, signalperiod=SIGNAL_PERIOD).macd

#>> SMA
sma_values = IndicatorSMA(closure_value=closure_values, timeperiod=TIMEPERIOD).sma

#>> EMA
ema_values = IndicatorEMA(closure_value=closure_values, timeperiod=TIMEPERIOD).ema
