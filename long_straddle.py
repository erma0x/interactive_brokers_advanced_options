from ib_insync import *

explanation = """
In this code, we first connect to the IB API using the IB() function. We then define the contract for the underlying asset, which in this case is Apple (AAPL) stock. We also define the strike price and expiration date for the options, which are set to $150 and December 17, 2021, respectively.

Next, we define the call and put options contracts using the Option() function. We then request market data for the underlying asset and options using the reqTickers() function. We calculate the total cost of the long straddle operation by adding the ask prices of the call and put options.

Finally, we place the order for the long straddle operation using the placeOrder() function and disconnect from the IB API using the disconnect() function.

It's important to note that this is just an example code and should not be used as is for actual trading. You should always do your own research and analysis before making any trades. Additionally, you should always test your trading strategies on a demo account before using real money.
"""

# Connect to the IB API
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the contract for the underlying asset
contract = Stock('AAPL', 'SMART', 'USD')

# Define the strike price and expiration date for the options
strikePrice = 150
expirationDate = '20211217'

# Define the call and put options contracts
callOption = Option('AAPL', expirationDate, strikePrice, 'C', 'SMART')
putOption = Option('AAPL', expirationDate, strikePrice, 'P', 'SMART')

# Request market data for the underlying asset and options
ib.qualifyContracts(contract)
ib.qualifyContracts(callOption)
ib.qualifyContracts(putOption)
ticker = ib.reqTickers(contract)[0]
callTicker = ib.reqTickers(callOption)[0]
putTicker = ib.reqTickers(putOption)[0]

# Calculate the total cost of the long straddle operation
totalCost = callTicker.ask + putTicker.ask

# Place the order for the long straddle operation
order = LimitOrder('BUY', 1, totalCost)
trade = ib.placeOrder(contract, order)

# Disconnect from the IB API
ib.disconnect()


