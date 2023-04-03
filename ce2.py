# Chandelier Exit

import matplotlib.pyplot as plt
import numpy as np
# Import libraries
import ta.volatility as volatility

# Input parameters
length = 22
mult = 3.0
showLabels = True
useClose = True
highlightState = True

# Load data
high = np.array(high)
low = np.array(low)
close = np.array(close)

# Calculate ATR
atr = volatility.average_true_range(high, low, close, window=length) * mult

# Initialize variables
dir = 1
longStop = np.zeros(close.size)
longStopPrev = np.zeros(close.size)
shortStop = np.zeros(close.size)
shortStopPrev = np.zeros(close.size)
longColor = 'g'
shortColor = 'r'

# Calculate Chandelier Exit
for i in range(close.size):
    if i == 0:
        longStop[i] = high[i] - atr[i]
        longStopPrev[i] = longStop[i]
        shortStop[i] = low[i] + atr[i]
        shortStopPrev[i] = shortStop[i]
    else:
        longStop[i] = max(high[i - length:i]) - atr[i]
        longStopPrev[i] = longStop[i - 1] if close[i - 1] > longStop[i - 1] else longStopPrev[i - 1]
        longStop[i] = max(longStop[i], longStopPrev[i])

        shortStop[i] = min(low[i - length:i]) + atr[i]
        shortStopPrev[i] = shortStop[i - 1] if close[i - 1] < shortStop[i - 1] else shortStopPrev[i - 1]
        shortStop[i] = min(shortStop[i], shortStopPrev[i])

        if close[i] > shortStopPrev[i]:
            dir = 1
        elif close[i] < longStopPrev[i]:
            dir = -1

    # Plot the indicator
    plt.plot([i], [longStop[i]] if dir == 1 else [np.nan], color=longColor, marker='.', markersize=1)
    plt.plot([i], [shortStop[i]] if dir == -1 else [np.nan], color=shortColor, marker='.', markersize=1)
    if dir == 1 and dir[i - 1] == -1:
        plt.scatter(i, longStop[i], marker='o', color=longColor, s=20)
        if showLabels:
            plt.text(i, longStop[i], 'Buy', ha='center', va='bottom', color='w', fontsize=8)
    elif dir == -1 and dir[i - 1] == 1:
        plt.scatter(i, shortStop[i], marker='o', color=shortColor, s=20)
        if showLabels:
            plt.text(i, shortStop[i], 'Sell', ha='center', va='top', color='w', fontsize=8)

# Fill between long and short stops
plt.fill_between(np.arange(close.size), longStop, shortStop, where=(dir == 1), color=longColor, alpha=0.2)
plt.fill_between(np.arange(close.size), longStop, shortStop, where=(dir == -1), color=shortColor, alpha=0.2)

# Show plot
plt.show()
