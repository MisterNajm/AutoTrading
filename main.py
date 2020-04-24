import time
import ccxt
import Trade
import Trend
import random
from get_data import pull_next_history, print_total_history, persist_results, init_conn
from Options import Option, get_option

def main(stoploss=0.05, takeprofit=0.1, treshold = 250):
  init_conn()
  print_total_history()
  trend = Trend.Trend()
  gen = pull_next_history()
  debug = get_option(Option.debug)
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
  #treshold = 250
  sell_amount_btc = -1
  buy_amount_usd = -1
  bought_at = 0
  buy_count = 0
  sell_count = 0
  open_price_list = []
  step = 0
  take_profit_counter = 0
  stop_loss_counter = 0
  while True:
      ##Use Delay -> Live Data, 1-2 seconds per pull
      if not disable_delay:
        print("USING LIVE DATA")
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
          print("End. Balance is %s. %s Buys, %s Sells. Takeprofit: %s Stoploss: %s "% (Trade.get_balance(), buy_count, sell_count, take_profit_counter, stop_loss_counter))
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
        if open_price > 1.005 * mean and trend.get_trend() > 1:
          amount = Trade.trade("USD", "BTC", open_price, buy_amount_usd, False, False)
          if amount[0] > 0:
            buy_count += 1
            bought_at = open_price
            if debug:
              print("Bought at %s$. %s" % (open_price, Trade.get_balance()))
        #Takeprofit
        if open_price > 1.1 * bought_at:
          
          amount=Trade.trade("BTC", "USD", open_price, sell_amount_btc, True, False)

          if amount[0] > 0:
            print(Trade.get_balance())
            sell_count +=1
            take_profit_counter += 1
            if debug:
              print("[TAKEPROFIT] Sold at %s$. %s" % (open_price, Trade.get_balance()))
          
        #Stoploss @ 5%
        if open_price < 0.95 * bought_at:
          amount=Trade.trade("BTC", "USD", open_price, sell_amount_btc, True, False)
          if amount[0] > 0:
            sell_count +=1
            stop_loss_counter += 1
            if debug:
              print("[STOPLOSS] Sold at %s$. %s" % (open_price, Trade.get_balance()))
  if(get_option(Option.persist_results)):
    print("Persisted")
    persist_results(Trade.get_balance("*", True)[0][1], stoploss, takeprofit, trend.get_trend(), treshold, buy_count, sell_count, take_profit_counter, stop_loss_counter, "Automated with random")


tresholdlist = [1, 5, 10,20, 40, 50, 100, 150, 200, 250, 500, 750, 1000, 2000, 4000, 8000, 10000]
stoplosslist = [0.01, 0, 0.02, 0.03, 0.04, 0.05, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3]
takeprofitlist = [0.01, 0, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.9, 0.25, 0.07]

run = 0
while True:
  run += 1
  print("Run %d" % run)
  main(random.choice(stoplosslist), random.choice(takeprofitlist), random.choice(tresholdlist))













    
    
    
    

    
    
    