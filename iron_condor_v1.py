import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from ib_insync import *

explanation = """
Certainly! Here's an example of a Python trading script for an Iron Condor options strategy. The Iron Condor involves selling both a put credit spread and a call credit spread on the same underlying asset with different strike prices and expiration dates."""

# Connect to Interactive Brokers TWS
ib = IB()
ib.connect('localhost', 7497, clientId=1)  # Update with your TWS connection details

# Define the ticker symbol and expiration dates for the options
ticker = 'AAPL'
expiry_put = dt.datetime(2023, 6, 16)
expiry_call = dt.datetime(2023, 6, 16)

# Get the current stock price
stock = ib.reqTickers(Ticker(ticker))[0]
stock_price = stock.marketPrice()

# Define the strike prices for the put credit spread
put_spread_width = 10  # Define the width of the put spread
put_lower_strike = stock_price - put_spread_width
put_upper_strike = stock_price - put_spread_width - 5  # Adjust the width of the put spread

# Define the strike prices for the call credit spread
call_spread_width = 10  # Define the width of the call spread
call_lower_strike = stock_price + call_spread_width
call_upper_strike = stock_price + call_spread_width + 5  # Adjust the width of the call spread

# Define the contract details for the put credit spread
put_sell_contract = Option(ticker, expiry_put, strike=put_lower_strike, right='Put', exchange='SMART')
put_buy_contract = Option(ticker, expiry_put, strike=put_upper_strike, right='Put', exchange='SMART')

# Define the contract details for the call credit spread
call_sell_contract = Option(ticker, expiry_call, strike=call_lower_strike, right='Call', exchange='SMART')
call_buy_contract = Option(ticker, expiry_call, strike=call_upper_strike, right='Call', exchange='SMART')

# Get the option market data
put_sell_market_data = ib.reqMktData(put_sell_contract)
put_buy_market_data = ib.reqMktData(put_buy_contract)
call_sell_market_data = ib.reqMktData(call_sell_contract)
call_buy_market_data = ib.reqMktData(call_buy_contract)
ib.sleep(2)  # Add a delay to ensure data is received

# Extract the option bid and ask prices
put_sell_bid_price = put_sell_market_data.bid
put_sell_ask_price = put_sell_market_data.ask
put_buy_bid_price = put_buy_market_data.bid
put_buy_ask_price = put_buy_market_data.ask
call_sell_bid_price = call_sell_market_data.bid
call_sell_ask_price = call_sell_market_data.ask
call_buy_bid_price = call_buy_market_data.bid
call_buy_ask_price = call_buy_market_data.ask

# Calculate the net credit from selling the put credit spread
put_credit = (put_sell_bid_price - put_buy_ask_price)  # Assuming selling at bid and buying at ask

# Calculate the net credit from selling the call credit spread
call_credit = (call_sell_bid_price - call_buy_ask_price)  # Assuming selling at bid and buying at ask

# Calculate the maximum profit, maximum loss, and breakeven points
max_profit = put_credit + call_credit
max_loss = put_spread


