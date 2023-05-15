from ib_insync import *
explanation = """
In this example, we connect to the IB API using the IB_insync library and define the option contract details for Apple Inc. with a strike price of 150 and an expiration date of January 21, 2022. We then place orders for both the call and put options with a limit price of 1.00.

Next, we monitor the market using the reqMktData function and adjust the orders as needed to maximize profits. If the bid price for the call option is higher than the current limit price, we update the limit price and place a new order. Similarly, if the ask price for the put option is lower than the current limit price, we update the limit price and place a new order.
"""

# Connect to the IB API
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the option contract details
contract = Option('AAPL', '20220121', 150, 'C', 'SMART')
call_order = LimitOrder('BUY', 1, 1.00)
put_order = LimitOrder('BUY', 1, 1.00)

# Place orders for both the call and put options
call_trade = ib.placeOrder(contract, call_order)
put_trade = ib.placeOrder(contract, put_order)

# Monitor the market and adjust the orders as needed
while True:
    # Get the latest market data
    ib.sleep(1)
    ticker = ib.reqMktData(contract, '', False, False)

    # Check if the call option is profitable
    if ticker.bid > call_order.lmtPrice:
        call_order.lmtPrice = ticker.bid
        ib.placeOrder(contract, call_order)

    # Check if the put option is profitable
    if ticker.ask < put_order.lmtPrice:
        put_order.lmtPrice = ticker.ask
        ib.placeOrder(contract, put_order)
        
        

