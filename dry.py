# Import Libraries
import yfinance as yf
import talib as ta
import pandas as pd


# CONFIGURABLE PARA
INDICATOR = 'RSI'
SYMBOL = 'TATAMOTORS.NS'
PERIOD_DATA = '2y'
INTERVAL = '1d'
PERIOD_CAL = 14

# SIGNAL LOGIC
BUY_THRESHOLD = 30
SELL_THRESHOLD = 70


# Load historical data
data = yf.Ticker(SYMBOL).history(period=PERIOD_DATA, interval=INTERVAL)
close = data["Close"]

# Indicator Definition
def calculateIndicator(close, indicator, period):
    if indicator == "RSI":
        return ta.RSI(close, timeperiod=period)
    elif indicator == "MACD":
        return ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    elif indicator == 'STOCH':
        return ta.STOCH(close, kperiod=14, dperiod=4, lookback=5)
    elif indicator == "SMA":
        return ta.SMA(close, timeperiod=period)
    elif indicator == "EMA":
        return ta.EMA(close, timeperiod=period)
    else:
        raise ValueError(f"No Such Indicator")


# ADJUSTED LOGIC FOR SMA, EMA
# buy_threshold = close.iloc[-1] > sma_values.iloc[-1]  
# sell_threshold = close.iloc[-1] < sma_values.iloc[-1]  


# Indicator Calculation
indicator_values = calculateIndicator(close=close, indicator=INDICATOR,period=PERIOD_CAL)

# ALERT LOGIC
def alert(message):
    print(message)


# Generate alerts - for back testing as it gives alert for each day in historical data

# for i in range(len(indicator_values)):
#     current_value = indicator_values.iloc[i]
#     current_date = data.index[i].strftime("%Y=-%m-%d")

#     if current_value <= BUY_THRESHOLD:
#         message = f"Buy Signal for {SYMBOL} on {current_date}"
#         alert(message)
#     elif current_value >= SELL_THRESHOLD:
#         message = f"Sell Signal for {SYMBOL} on {current_date}"
#         alert(message)
    


# Generate alerts - for deployment with a (other options: cooling period or combining indicators) here used trading frequency to reduce noise
for i in range(1, len(indicator_values)):
    previous_value = indicator_values.iloc[i-1]
    current_value = indicator_values.iloc[i]
    current_date = data.index[i].strftime("%Y-%m-%d")
    if current_value <= BUY_THRESHOLD and previous_value > BUY_THRESHOLD:
        message = f"Buy Signal for {SYMBOL} on {current_date}"
        alert(message)
    elif current_value >= SELL_THRESHOLD and previous_value < SELL_THRESHOLD:
        message = f"Sell Signal for {SYMBOL} on {current_date}"
        alert(message)
