import time
import ccxt
import Trade
import Market

Trade.create()
Trade.initialize()
print(Trade.get_balance())



exchange = ccxt.binance()
exchange.load_markets()

delay = 2 # seconds
# ACHTUNG - NICHT AUF UNTER 1 SETZEN! Sonst werden wir gebannt.
trend = 1 #0 bedeutet down, 1 bedeutet up. Sollte bei 1 starten.
up = 1 # Muss auf 1 bleiben (ENUM)
down = 0 # Muss auf 0 bleiben (ENUM)
prev = 0
dur = 0
recentTrendTicker = 0
recentUps = 0
recentDowns = 0
##Verständlichere Variablen -> 'Verkaufte Währung',....
while True:
    time.sleep (delay) # rate limit
    orderbook = exchange.fetch_order_book('BTC/USDT')
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    print (exchange.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })
    recentTrendTicker += 1
    if (recentTrendTicker >= (60/delay)):
      recentTrendTicker = 0
      if(recentUps == 0):
        recentUps = 1
      if(recentDowns == 0):
        recentDowns = 1
      totalRecents = recentUps + recentDowns
      print("\033[94mTrend of last 60 seconds is %d%% up and %d%% down.\033[0m" % ((recentUps/totalRecents*100), (recentDowns/totalRecents*100)))
      recentUps = 0
      recentDowns = 0
    if(prev == 0):
      prev = bid
      continue
    if(bid > prev):    
      if(trend == down):
        print("=======\nTrend lasted %s seconds downwards.\n=======" % (dur*delay))
        dur = 0
      else:
        dur += 1
        if dur == 5:
          #Kaufen
          target_amount, origin_amount = Trade.trade("USD", "BTC", Market.get_current_ask("BTC/USDT"), -1)
          print("\033[92mBought %f BTC for 100$\033[0m" % target_amount)
      trend = up
      recentUps += 1
    else:
      if(trend == up): 
        print("=======\nTrend lasted %s seconds upwards.\n=======" % (dur*delay))
        dur = 0
        #Verkaufen
        target_amount, origin_amount = Trade.trade("BTC", "USD", Market.get_current_bid("BTC/USDT"), -1, True)
        if(target_amount > 0):
          print("\033[91mSold %f bitcoin for %f$, new balance is: %s\033[0m" % (origin_amount, target_amount,Trade.get_balance()))
      else:
        dur += 1

      trend = down
      recentDowns += 1
    prev = bid
