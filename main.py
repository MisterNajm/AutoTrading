import time
import ccxt
import Trade
import Market
from get_data import pull_next_history
from Options import Option, get_option

gen = pull_next_history()

Trade.create()
Trade.initialize()

exchange = ccxt.binance()
exchange.load_markets()
exchange.fetch_ohlcv
# ACHTUNG - Formel nicht verändern -> Evtl Ban wegen DDoS
delay = 1 / float(get_option(Option.pulls_per_second))
disable_delay = get_option(Option.simulate and Option.use_historical_data)

###
## START TRADING STRATEGIE ##
###
treshold = 50
stock = 0
open_price_list = []

while True:
    ##Use Delay -> Live Data, 1-2 seconds per pull
    if not disable_delay:
      time.sleep(delay) # rate limit
      orderbook = exchange.fetch_order_book('BTC/USDT')
      bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
      ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
      spread = (ask - bid) if (bid and ask) else None
    
    ##Simulate a lot faster with historical data -> 500 pulls immediately
    else:
      open_price = next(gen, "END")
      if(open_price == "END"):
        print(open_price_list[-1])
        Trade.trade("USD", "BTC", open_price_list[-1], -1, True)
        print("End. Balance is %s USD" % Trade.get_balance()) 
        break
      open_price = open_price[1]
      while len(open_price_list) < treshold:
        open_price = next(gen, "END")[1]
        open_price_list.append(open_price)

      open_price_list.pop(0)
      open_price_list.append(open_price)

    sum_all = 0
    for historical_price in open_price_list:
      sum_all += historical_price
    mean = sum_all / len(open_price_list)
    if open_price > mean:
      Trade.trade("USD", "BTC", open_price)
    if open_price < mean:
      amount=Trade.trade("USD", "BTC", open_price, -1, True)
      print("Sold. %s" % Trade.get_balance())
      #if(amount > 0):






    
    
    
    

    
    
    