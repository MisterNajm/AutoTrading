import ccxt

exchange = ccxt.binance()
exchange.load_markets()

def get_current_ask(id):
    orderbook = exchange.fetch_order_book(id)
    return orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None

def get_current_bid(id):
    orderbook = exchange.fetch_order_book(id)
    return orderbook['bids'][0][0] if len (orderbook['asks']) > 0 else None