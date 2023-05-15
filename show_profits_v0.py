from ib_insync import *
import matplotlib.pyplot as plt

# Connect to the Interactive Brokers API
ib = IB()
ib.connect('localhost', 7497, clientId=1)

# Define the option contract
contract = Option('AAPL', '20220121', 150, 'C', 'SMART')

# Request real-time market data for the option contract
ticker = ib.reqMktData(contract)

# Define the strike prices and calculate the operation profit for each strike price
strike_prices = range(100, 200, 5)
operation_profit = [ticker.marketPrice() - contract.strikePrice for contract.strikePrice in strike_prices]

# Create a 2D plot with the strike prices on the x-axis and the operation profit on the y-axis
plt.plot(strike_prices, operation_profit)
plt.xlabel('Strike Prices')
plt.ylabel('Operation Profit')
plt.title('Option Operation on the Option Market')
plt.show()

# Disconnect from the Interactive Brokers API
ib.disconnect()
