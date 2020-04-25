import sqlite3
import ccxt
import pandas as pd
import datetime
from Options import Option, get_option


class DataProvider:
  def __init__(self):
    self.init_conn()
    self.time = 0
    self.date = datetime.datetime(2018, 5, 3) 
    self.init_generator()
    self.debug = get_option(Option.debug)

  def init_conn(self):
    self.connection = sqlite3.connect("history.db", isolation_level=None)
    self.connection.execute('pragma journal_mode=wal')
    self.cursor = self.connection.cursor()
    self.connection.execute("BEGIN")

  def close_conn(self):
    self.connection.commit()
    self.connection.close()

  def print_total_history(self):
    if get_option(Option.debug):
      print(pd.read_sql_query("SELECT * FROM history_minute", self.connection))

  def init_generator(self):
    SQL_STATEMENT = "SELECT * FROM history_minute";
    self.cursor.execute(SQL_STATEMENT)
    self.data = self.cursor.fetchall()

  def history_generator_provider(self):
    for entry in self.data:
      self.time += 1
      if self.time > 1439:
        if self.debug:
          print("\n\n%s\n" % self.date)
      yield entry




  def persist_results(self, result_usd, stoploss, takeprofit, trend, treshold, buys, sells, stoplosses, takeprofits, misc="Empty"):
    SQL_STATEMENT = """
      CREATE TABLE history_results (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      result_usd REAL,
      stoploss REAL,
      takeprofit REAL,
      trend INTEGER,
      treshold INTEGER,
      buys INTEGER,
      sells INTEGER,
      stoplosses INTEGER,
      takeprofits INTEGER,
      misc TEXT
      );"""
    try:
      self.cursor.execute(SQL_STATEMENT)
    except Exception as e:
      print("Probably save to ignore: %s" % e)

    SQL_STATEMENT = """INSERT INTO history_results (result_usd, stoploss, takeprofit, trend, treshold, buys, sells, stoplosses, takeprofits, misc) VALUES (%f, %f, %f, %d, %d, %d, %d, %d, %d, '%s');""" % (result_usd, stoploss, takeprofit, trend, treshold, buys, sells, stoplosses, takeprofits, misc)
    try:
      self.cursor.execute(SQL_STATEMENT)
    except Exception as e:
      print("COULD NOT PERSIST RESULT: %s" % e) 

  def check_mean_open(self, start = 1, end = 500):
    SQL_STATEMENT = """SELECT AVG(result) FROM (SELECT open AS result FROM history_minute LIMIT %s OFFSET %s);""" % ((end-start), start)
    self.cursor.execute(SQL_STATEMENT)
    return self.cursor.fetchall()

  def generate_history(self):
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
     self.cursor.execute(SQL_STATEMENT)
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
        self.cursor.execute(SQL_STATEMENT)
      loopvar += 1
      print(pd.read_sql_query("SELECT COUNT(*) FROM history_minute", self.connection))
      if(loopvar > 72):
        self.connection.commit()
        break






  






