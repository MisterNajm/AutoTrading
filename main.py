import time
import ccxt
import Trade
import Market

Trade.initialize()
print(Trade.get_balance())

Trade.trade("USD", "BTC", Market.get_current_ask("BTC/USDT"), 1)
print(Trade.get_balance())
Trade.trade("BTC", Market.get_current_ask("BTC/USDT"), 1)
print(Trade.get_balance())

exchange = ccxt.binance()
exchange.load_markets()

delay = 2 # seconds
# ACHTUNG - NICHT AUF UNTER 2 SETZEN! Sonst werden wir gebannt.
trend = 0
up = 1
down = 0
prev = 0
dur = 0
recentTrendTicker = 0
recentUps = 0
recentDowns = 0
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
      print("Trend of last 60 seconds is %d%% up and %d%% down." % ((recentUps/totalRecents*100), (recentDowns/totalRecents*100)))
      recentUps = 0
      recentDowns = 0
    if(prev == 0):
      prev = bid
      continue
    if(bid > prev):
      if(trend == down):
        print("Trend lasted %s seconds downwards." % (dur*delay))
        dur = 0
      else:
        dur += 1
      trend = up
      recentUps += 1
    else: 
      if(trend == up):
        print("Trend lasted %s seconds upwards." % (dur*delay))
        dur = 0
      else:
        dur += 1
      trend = down
      recentDowns += 1
    prev = bid
