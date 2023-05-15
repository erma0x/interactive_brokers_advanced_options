from ib_insync import *
import matplotlib.pyplot as plt

# Connect to the Interactive Brokers API
util.startLoop()
ib = IB()
ib.connect('localhost', 7497, clientId=1)

# Retrieve the open positions on the option market
open_positions = ib.positions()

# Plot the open positions using Matplotlib
fig, ax = plt.subplots()
ax.bar(open_positions.symbol, open_positions.position)
ax.set_xlabel('Option Symbol')
ax.set_ylabel('Position')
ax.set_title('Open Positions on Option Market')
plt.show()

# Disconnect from the Interactive Brokers API
ib.disconnect()
