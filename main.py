import time
import ccxt
from Trade import Trade
import Trend
import random
import numpy as np

from DataProvider import DataProvider
from Options import Option, get_option

def main(stoploss=0.05, takeprofit=0.1, treshold = 250):
  trade_instance = Trade()
  provider_instance = DataProvider()
  provider_instance.print_total_history()
  trend = Trend.Trend()
  gen = provider_instance.history_generator_provider()
  debug = get_option(Option.debug)


  # ACHTUNG - Formel nicht verändern -> Evtl Ban wegen DDoS
  delay = 1 / float(get_option(Option.pulls_per_second))
  disable_delay = get_option(Option.simulate and Option.use_historical_data)

  ###
  ## START TRADING STRATEGIE ##
  ###

  sell_amount_btc = -1
  buy_amount_usd = -1
  bought_at = 0
  buy_count = 0
  sell_count = 0
  open_price_list = np.array(1)
  step = 0
  take_profit_counter = 0
  stop_loss_counter = 0

  for n in range(0, treshold):
    current = next(gen, "EEND")[1::]
    open_price = current[1]
    np.append(open_price_list, open_price)

  print("Finished setup")
  step += treshold
  begin = time.time()
  for entry in gen:
        t0 = time.time()
        step += 1
        current = entry[1::]
        open_price = current[1]
        t1 = time.time()
        if(current == "END"):
          trade_instance.trade("BTC", "USD", open_price_list[-1], sell_amount_btc, True)
          print("End. Balance is %s. %s Buys, %s Sells. Takeprofit: %s Stoploss: %s "% (trade_instance.get_balance(), buy_count, sell_count, take_profit_counter, stop_loss_counter))
          break
        t2 = time.time()
        np.delete(open_price_list, [0])
        np.append(open_price_list, open_price)
        t3 = time.time()
        mean = np.mean(open_price_list, dtype='float32')
        t4 = time.time()
        trend.update_trend(open_price)
        
        if open_price > 1.005 * mean and trend.get_trend() > 1:
          amount = trade_instance.trade("USD", "BTC", open_price, buy_amount_usd, False, False)
          if amount[0] > 0:
            buy_count += 1
            bought_at = open_price
            if debug:
              print("Bought at %s$. %s" % (open_price, trade_instance.get_balance()))
        t5 = time.time()
        #Takeprofit
        if open_price > (1+takeprofit)* bought_at:
          
          amount=trade_instance.trade("BTC", "USD", open_price, sell_amount_btc, True, False)

          if amount[0] > 0:
            sell_count +=1
            take_profit_counter += 1
            if debug:
              print(trade_instance.get_balance())
              print("[TAKEPROFIT] Sold at %s$. %s" % (open_price, trade_instance.get_balance()))
        t6 = time.time()  
        #Stoploss @ 5%
        if open_price < (1 - stoploss) * bought_at:
          amount=trade_instance.trade("BTC", "USD", open_price, sell_amount_btc, True, False)
          if amount[0] > 0:
            sell_count +=1
            stop_loss_counter += 1
            if debug:
              print("[STOPLOSS] Sold at %s$. %s" % (open_price, trade_instance.get_balance()))
  t7 = time.time()
  if(get_option(Option.persist_results)):
    provider_instance.persist_results(trade_instance.get_balance("*", True)[0][1], stoploss, takeprofit, trend.get_trend(), treshold, buy_count, sell_count, take_profit_counter, stop_loss_counter, "Automated with random")
  t8 = time.time()
  trade_instance.get_balance()
  trade_instance.close_conn()

  provider_instance.close_conn()
  trade_instance = None
  provider_instance = None
  t9 = time.time()
"""  print(t0)
  print(t1 - t0)
  print(t2 - t1)
  print(t3 - t2)
  print(t4 - t3)
  print(t5 - t4)
  print(t6 - t5)
  print(t7 - t6)
  print(t8 - t7)
  print(t9 - t8)
  print("TOTAL %s" % (t9 - begin))"""


tresholdlist = [1, 5, 10,20, 40, 50, 100, 150, 200, 250, 500, 750, 1000, 2000, 4000, 8000, 10000]
stoplosslist = [0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.5]
takeprofitlist = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
run = 0
for stopentry in stoplosslist:
  for takeentry in takeprofitlist:
    run += 1
    print("Let's try... %f + %f" % (stopentry, takeentry))
    print("Run %d of %d" % (run, (len(stoplosslist) * len(takeprofitlist))))
    main(stopentry, takeentry, 4000)






    
    
    
    

    
    
    