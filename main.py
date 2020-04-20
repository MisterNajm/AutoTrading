import time
import ccxt
import Trade
import Trend

from get_data import pull_next_history
from Options import Option, get_option

def main():
  trend = Trend.Trend()
  gen = pull_next_history()
  debug = True
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
  sell_amount_btc = -1
  buy_amount_usd = 10

  buy_count = 0
  sell_count = 0
  open_price_list = []
  step = 0

  while True:
      ##Use Delay -> Live Data, 1-2 seconds per pull
      if not disable_delay:
        print("Test")
        time.sleep(delay) # rate limit
        orderbook = exchange.fetch_order_book('BTC/USDT')
        bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
        spread = (ask - bid) if (bid and ask) else None
      
      ##Simulate a lot faster with historical data -> 100k pulls immediately
      else:
        current = next(gen, "EEND")[1::]
        open_price = current[1]
        step += 1

        if(current == "END"):
          Trade.trade("BTC", "USD", open_price_list[-1], sell_amount_btc, True)
          print("2")
          print("End. Balance is %s. %s Buys, %s Sells." % (Trade.get_balance(), buy_count, sell_count))
          break
  
        while len(open_price_list) < treshold:
          step += 1
          current = next(gen, "EEND")[1::]
          open_price = current[1]
          open_price_list.append(open_price)
  
        open_price_list.pop(0)
        open_price_list.append(open_price)
  
        sum_all = 0
        for historical_price in open_price_list:
          sum_all += historical_price
          mean = sum_all / len(open_price_list)
        trend.update_trend(open_price)
        if open_price < mean and trend.get_trend() > 3:
          amount = Trade.trade("USD", "BTC", open_price, buy_amount_usd, False, True)
          if amount[0] > 0:
            buy_count += 1
            if debug:
              print("Bought at %s$. %s" % (open_price, Trade.get_balance()))
        if open_price > 1 * mean and trend.get_trend() < -5:
          amount=Trade.trade("BTC", "USD", open_price, sell_amount_btc, True)
          if amount[0] > 0:
            sell_count +=1
            if debug:
              print("Sold at %s$. %s" % (open_price, Trade.get_balance()))
      #if(amount > 0):

main()













    
    
    
    

    
    
    