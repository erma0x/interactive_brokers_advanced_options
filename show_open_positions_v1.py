from ib_insync import *

# Connect to the IB Gateway or TWS application
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Retrieve the current positions in your account
positions = ib.positions()

# Print the symbol and quantity of each position
for position in positions:
    print(position.contract.symbol, position.position)
