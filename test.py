
from trade import DataFetcher
from trade import IndicatorRSI
from trade import IndicatorMACD
from trade import IndicatorSTOCH
from trade import IndicatorSMA
from trade import IndicatorEMA
from trade import GenerateAlert
from trade import PushAlert


# CONFIGURABLE PARAMETERS
SYMBOL = 'Reliance.NS'
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
LONG_TIMEPERIOD = 200
SHORT_TIMEPERIOD = 50


# HISTORICAL DATA COLLECTION
historical_data, closure_values, low_values, high_values = DataFetcher(symbol=SYMBOL, period=PERIOD_FOR_DATA_COLLECTION, interval=INTERVAL).fetchClosureHistoryData()



# -------------TEST CASES----------------

# # >> CASE: RSI
# rsi_suggestions, rsi_values = IndicatorRSI(closure_value=closure_values, period=PERIOD_FOR_CALCULATION).cal_suggestions()

# alert_messages = GenerateAlert(indicator='RSI', indicator_suggestions=rsi_suggestions, indicator_values=rsi_values, historical_data=historical_data).alerts

# PushAlert(alert_messages=alert_messages).pushConsole()


# # >> CASE: MACD
# macd_suggestions, macd_hist_values = IndicatorMACD(closure_value=closure_values, fastperiod=FAST_PERIOD, slowperiod=SLOW_PERIOD, signalperiod=SIGNAL_PERIOD).cal_suggestions()

# alert_messages = GenerateAlert(indicator='MACD', indicator_suggestions=macd_suggestions, indicator_values=macd_hist_values, historical_data=historical_data).alerts

# PushAlert(alert_messages=alert_messages).pushConsole()


# # >> CASE: STOCH
# stoch_suggestions, stoch_values = IndicatorSTOCH(closure_value=closure_values, low_values=low_values, high_values=high_values, kperiod=K_PERIOD, dperiod=D_PERIOD, lookback=LOOKBACK).cal_suggestions()

# alert_messages = GenerateAlert(indicator='STOCH', indicator_suggestions=stoch_suggestions, indicator_values=stoch_values, historical_data=historical_data).alerts

# PushAlert(alert_messages=alert_messages).pushConsole()


# # >> CASE: SMA
# sma_suggestions, sma_values = IndicatorSMA(closure_value=closure_values, short_sma_timeperiod=SHORT_TIMEPERIOD, long_sma_timeperiod=LONG_TIMEPERIOD).cal_suggestions()

# alert_messages = GenerateAlert(indicator='SMA', indicator_suggestions=sma_suggestions, indicator_values=sma_values, historical_data=historical_data).alerts

# PushAlert(alert_messages=alert_messages).pushConsole()


# # >> CASE: EMA
# ema_suggestions, ema_values = IndicatorEMA(closure_value=closure_values, short_ema_timeperiod=SHORT_TIMEPERIOD, long_ema_timeperiod=LONG_TIMEPERIOD).cal_suggestions()

# alert_messages = GenerateAlert(indicator='EMA', indicator_suggestions=ema_suggestions, indicator_values=ema_values, historical_data=historical_data).alerts

# PushAlert(alert_messages=alert_messages).pushConsole()