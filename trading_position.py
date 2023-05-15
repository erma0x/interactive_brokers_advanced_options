# Import necessary libraries
import numpy as np
import pandas as pd

# Define your trading strategy
def trading_strategy(data):
    # Calculate technical indicators
    data['SMA'] = data['Close'].rolling(window=20).mean()  # Simple Moving Average
    data['RSI'] = calculate_rsi(data['Close'], window=14)  # Relative Strength Index

    # Define trading signals based on indicators
    data['Buy_Signal'] = np.where((data['Close'] > data['SMA']) & (data['RSI'] < 30), 1, 0)
    data['Sell_Signal'] = np.where((data['Close'] < data['SMA']) & (data['RSI'] > 70), -1, 0)

    # Calculate positions based on signals
    data['Position'] = data['Buy_Signal'] + data['Sell_Signal']
    data['Position'] = data['Position'].fillna(0)
    data['Position'] = data['Position'].shift()

    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change()
    data['Strategy_Returns'] = data['Position'] * data['Returns']

    return data

# Calculate Relative Strength Index (RSI)
def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Load historical price data
data = pd.read_csv('historical_data.csv')  # Replace with your own data source

# Apply trading strategy to the data
result = trading_strategy(data)

# Print the resulting data with positions and strategy returns
print(result[['Date', 'Close', 'Position', 'Strategy_Returns']])
