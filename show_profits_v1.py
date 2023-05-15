from ib_insync import *
import matplotlib.pyplot as plt

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

sell_contract = Option('AAPL', '20220121', 120, 'C', 'SMART')
buy_contract = Option('AAPL', '20220121', 130, 'C', 'SMART')

tickers = ib.reqTickers(sell_contract, buy_contract)
sell_price = tickers[0].marketPrice()
buy_price = tickers[1].marketPrice()

strike_prices = range(100, 150)
operation_profit = []

for strike_price in strike_prices:
    if strike_price <= sell_contract.strike:
        profit = sell_price
    elif sell_contract.strike < strike_price <= buy_contract.strike:
        profit = sell_price - buy_price
    else:
        profit = sell_price - buy_price + (strike_price - buy_contract.strike)
    operation_profit.append(profit)
    
plt.plot(strike_prices, operation_profit)
plt.xlabel('Strike Prices')
plt.ylabel('Operation Profit')
plt.title('Call Credit Spread')
plt.show()

