import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from ib_insync import *

description = """
In the script above, we use the ib_insync library to connect to Interactive Brokers TWS API. The script assumes you have a running TWS instance on your local machine. Please make sure to update the connection details (host, port, and clientId) accordingly.

The script retrieves the current stock price using Yahoo Finance (yfinance library) and sets a strike price for the call option based on the desired adjustment. It then creates an Option object with the ticker symbol, expiration date, strike price, and other contract details.

The script requests market data for the option and waits for a couple of seconds to ensure data is received. It extracts the bid and ask prices and calculates the net premium by taking the average of the bid and ask prices.

Next, it places two orders: one to buy the underlying asset (100 shares of the stock) using a market order and another to sell the call option using a limit order with the calculated premium. The script checks the order status to confirm whether the orders were filled successfully.

Finally, the script disconnects from the Interactive Brokers TWS API.
"""

# Connect to Interactive Brokers TWS
ib = IB()
ib.connect('localhost', 7497, clientId=1)  # Update with your TWS connection details

# Define the ticker symbol and expiration date of the option
ticker = 'AAPL'
expiry = dt.datetime(2023, 6, 16)

# Get the current stock price
stock = ib.reqTickers(Ticker(ticker))[0]
stock_price = stock.marketPrice()

# Define the strike price for the call option
strike_price = stock_price + 10  # Add your desired strike price adjustment

# Define the contract details
contract = Option(ticker, expiry, strike=strike_price, right='Call', exchange='SMART')

# Get the option market data
market_data = ib.reqMktData(contract)
ib.sleep(2)  # Add a delay to ensure data is received

# Extract the option bid and ask prices
bid_price = market_data.bid
ask_price = market_data.ask

# Calculate the net premium from selling the option
premium = (bid_price + ask_price) / 2  # Assuming the premium is the average of bid and ask

# Calculate the number of shares required to cover the call option
shares_required = 100  # Assuming one option contract represents 100 shares

# Buy the underlying asset (100 shares of the stock)
order_stock = MarketOrder('BUY', shares_required)
trade_stock = ib.placeOrder(contract, order_stock)

# Sell the call option
order_option = LimitOrder('SELL', shares_required, premium)
trade_option = ib.placeOrder(contract, order_option)

# Wait for the orders to fill
ib.sleep(2)

# Check the order status
if trade_stock.orderStatus.status == 'Filled' and trade_option.orderStatus.status == 'Filled':
    print('Covered Call Strategy Executed Successfully!')
else:
    print('Covered Call Strategy Execution Failed.')

# Disconnect from Interactive Brokers TWS
ib.disconnect()
