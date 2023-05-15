from ib_insync import *

explanation = """
In this code, we first connect to the IB API using the IB_insync library. Then, we define the option contracts for the iron condor operation by specifying the underlying asset, expiry date, and strike prices. We place the orders for the option contracts using limit orders with the desired prices. Finally, we monitor the trades and adjust them if necessary by canceling the existing orders and placing new ones with different prices.

It's important to note that this is just an example code, and you should modify it according to your specific needs and trading strategy. Also, trading involves risks, and you should always consult with a professional financial advisor before making any investment decisions.
"""


# Connect to the IB API
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the option contracts for the iron condor operation
underlying = Stock('AAPL', 'SMART', 'USD')
expiry = '20220121'
strike1 = 150
strike2 = 160
strike3 = 170
strike4 = 180

call1 = Option(underlying, expiry, strike1, 'C', 'SMART')
call2 = Option(underlying, expiry, strike2, 'C', 'SMART')
put1 = Option(underlying, expiry, strike3, 'P', 'SMART')
put2 = Option(underlying, expiry, strike4, 'P', 'SMART')

# Place the orders for the option contracts
order1 = LimitOrder('SELL', 1, call1, 1.0)
order2 = LimitOrder('BUY', 1, call2, 0.5)
order3 = LimitOrder('SELL', 1, put1, 1.0)
order4 = LimitOrder('BUY', 1, put2, 0.5)

trade1 = ib.placeOrder(call1, order1)
trade2 = ib.placeOrder(call2, order2)
trade3 = ib.placeOrder(put1, order3)
trade4 = ib.placeOrder(put2, order4)

# Monitor the trades and adjust them if necessary
while True:
    ib.sleep(10)
    if trade1.orderStatus.status == 'Filled' and trade2.orderStatus.status == 'Filled' and trade3.orderStatus.status == 'Filled' and trade4.orderStatus.status == 'Filled':
        break

    if trade1.orderStatus.status == 'Filled' and trade2.orderStatus.status == 'Filled':
        ib.cancelOrder(order3)
        ib.cancelOrder(order4)
        order3 = LimitOrder('SELL', 1, put1, 0.5)
        order4 = LimitOrder('BUY', 1, put2, 0.25)
        trade3 = ib.placeOrder(put1, order3)
        trade4 = ib.placeOrder(put2, order4)

    if trade3.orderStatus.status == 'Filled' and trade4.orderStatus.status == 'Filled':
        ib.cancelOrder(order1)
        ib.cancelOrder(order2)
        order1 = LimitOrder('SELL', 1, call1, 0.5)
        order2 = LimitOrder('BUY', 1, call2, 0.25)
        trade1 = ib.placeOrder(call1, order1)
        trade2 = ib.placeOrder(call2, order2)

# Disconnect from the IB API
ib.disconnect()

