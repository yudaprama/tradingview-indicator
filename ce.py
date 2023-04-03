import talib
import numpy as np
import matplotlib.pyplot as plt

length = 22
mult = 3.0
showLabels = True
useClose = True
highlightState = True

close = np.random.rand(100)
high = np.random.rand(100)
low = np.random.rand(100)

atr = mult * talib.ATR(high, low, close, timeperiod=length)

longStop = (np.maximum(close, talib.MAX(high, timeperiod=length)) - atr).shift(1).fillna(0)
longStopPrev = longStop.copy()
longStop = np.where(close.shift(1) > longStopPrev, np.maximum(longStop, longStopPrev), longStop)

shortStop = (np.minimum(close, talib.MIN(low, timeperiod=length)) + atr).shift(1).fillna(0)
shortStopPrev = shortStop.copy()
shortStop = np.where(close.shift(1) < shortStopPrev, np.minimum(shortStop, shortStopPrev), shortStop)

dir = np.where(close > shortStopPrev, 1, np.where(close < longStopPrev, -1, 1))

longColor = 'green'
shortColor = 'red'

longStopPlot = np.where(dir == 1, longStop, np.nan)
plt.plot(longStopPlot, label="Long Stop", linewidth=2, color=longColor)
buySignal = np.logical_and(dir == 1, dir.shift(1) == -1)
plt.scatter(buySignal.index[buySignal], longStop[buySignal], label="Long Stop Start", s=10, color=longColor)
if showLabels:
    plt.scatter(longStop[buySignal].index, longStop[buySignal], label="Buy", s=10, color=longColor, marker="^")

shortStopPlot = np.where(dir == 1, np.nan, shortStop)
plt.plot(shortStopPlot, label="Short Stop", linewidth=2, color=shortColor)
sellSignal = np.logical_and(dir == -1, dir.shift(1) == 1)
plt.scatter(sellSignal.index[sellSignal], shortStop[sellSignal], label="Short Stop Start", s=10, color=shortColor)
if showLabels:
    plt.scatter(shortStop[sellSignal].index, shortStop[sellSignal], label="Sell", s=10, color=shortColor, marker="v")

midPricePlot = (high + low + close + close) / 4.0

longFillColor = np.where(dir == 1, longColor, np.nan)
shortFillColor = np.where(dir == -1, shortColor, np.nan)
plt.fill_between(midPricePlot.index, midPricePlot, longStopPlot, where=longFillColor == longColor, interpolate=True)
plt.fill_between(midPricePlot.index, midPricePlot, shortStopPlot, where=shortFillColor == shortColor, interpolate=True)

changeCond = dir != dir.shift(1)
buyCond = buySignal
sellCond = sellSignal
alerts = changeCond | buyCond | sellCond
alerts = alerts[alerts].index

print(alerts)
