import sqlite3
import ccxt
import pandas as pd
import datetime
from Options import Option, get_option



def init_conn():
  connection = sqlite3.connect("history.db", isolation_level=None)
  connection.execute('pragma journal_mode=wal')
  return connection

connection = init_conn()

def print_total_history():
  connection = sqlite3.connect("history.db")
  if get_option(Option.debug):
    print(Option.debug)
    print(pd.read_sql_query("SELECT * FROM history_minute", connection))
  connection.commit()
  connection.close()

def pull_next_history():
  cursor = connection.cursor()
  SQL_STATEMENT = "SELECT * FROM history_minute";
  cursor.execute(SQL_STATEMENT)
  date = datetime.datetime(2018, 5, 3) 
  time = 0

  for entry in cursor.fetchall():
    time += 1
    if time > 1439:
      time = 0
      date = datetime.datetime.fromtimestamp(entry[1]/1000.0)
      if get_option(Option.debug):
        print("\n\n%s\n" % date)
    yield entry

def persist_results(result_usd, stoploss, takeprofit, trend, treshold, buys, sells, stoplosses, takeprofits, misc="Empty"):
  connection = init_conn()
  cursor = connection.cursor()
  SQL_STATEMENT = """
    CREATE TABLE history_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	  result_usd REAL,
	  stoploss INTEGER,
    takeprofit INTEGER,
    trend INTEGER,
    treshold INTEGER,
    buys INTEGER,
    sells INTEGER,
    stoplosses INTEGER,
    takeprofits INTEGER,
    misc TEXT,
    );"""
  try:
    cursor.execute(SQL_STATEMENT)
  except:
    pass

  SQL_STATEMENT = "INSERT INTO history_results(result_usd, stoploss, takeprofit, trend, treshold,buys, sells, stoplosses, takeprofits, misc) VALUES (%20f, %d, %d, %d, %d, %d, %d, %d, %d, %s);" % (result_usd, stoploss, takeprofit, trend, treshold, buys, sells, stoplosses, takeprofits, misc)
  cursor.execute(SQL_STATEMENT)
  connection.commit()
  print(pd.read_sql_query("SELECT * FROM history_results;", connection))
  
  connection.close()

def check_mean_open(start = 1, end = 500):
  connection = sqlite3.connect("history.db")
  cursor = connection.cursor()
  SQL_STATEMENT = "SELECT AVG(result) FROM (SELECT open AS result FROM history_minute LIMIT %s OFFSET %s);" % ((end-start), start)

  cursor.execute(SQL_STATEMENT)
  return cursor.fetchall()

def generate_history():
  connection = sqlite3.connect("history.db")
  cursor = connection.cursor()
  '''  SQL_STATEMENT = "DROP TABLE history_minute;"

  try:
    cursor.execute(SQL_STATEMENT)
  except:
    pass'''

  SQL_STATEMENT = """
    CREATE TABLE history_minute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	  time INTEGER,
	  open REAL,
    highest REAL,
    lowest REAL,
    closing REAL,
    volume REAL
    );"""
  try:
    cursor.execute(SQL_STATEMENT)
  except:
    pass

  # UTC timestamp in milliseconds, integer
  # (O)pen price, float
  # (H)ighest price, float
  # (L)owest price, float
  # (C)losing price, float
  # (V)olume (in terms of the base currency), float 
  exchange = ccxt.binance({
    'rateLimit': 2000,
    'enableRateLimit': True,
    # 'verbose': True,
  })

  now = exchange.milliseconds()
  since = exchange.parse8601('2020-03-23T07:00:00Z')
  symbol = 'BTC/USDT'
  timeframe = '1m'
  loopvar = 0
  while since < now:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)    
    print('First candle:', exchange.iso8601(ohlcv[0][0]))
    print('Last candle:', exchange.iso8601(ohlcv[-1][0]))
    print('Candles returned:', len(ohlcv))
    since += len(ohlcv) * 60000
    for entry in ohlcv:
      SQL_STATEMENT = """
      INSERT INTO history_minute(time, open, highest, lowest, closing, volume) VALUES(
      %d,%f, %f,%f,%f,%f
      );""" % (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
      cursor.execute(SQL_STATEMENT)
    loopvar += 1
    print(pd.read_sql_query("SELECT COUNT(*) FROM history_minute", connection))
    if(loopvar > 72):
      connection.commit()
      break






  






