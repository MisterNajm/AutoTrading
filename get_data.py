import sqlite3
import ccxt
import time
import pandas as pd

exchange = ccxt.binance()
exchange.load_markets()

def get_current():
  pass

def get_total_history():
  pass

def pull_next_history():
  connection = sqlite3.connect("history.db")
  cursor = connection.cursor()
  SQL_STATEMENT = "SELECT * FROM history_minute;";
  cursor.execute(SQL_STATEMENT)
  
  for entry in cursor.fetchall():
    yield entry

def generate_history():
  connection = sqlite3.connect("history.db")
  cursor = connection.cursor()
    
  SQL_STATEMENT = """
    CREATE TABLE history_minute (
	  id INTEGER PRIMARY KEY,
	  open REAL,
    highest REAL,
    lowest REAL,
    closing REAL,
    volume REAL
    );"""

  cursor.execute(SQL_STATEMENT)

  # UTC timestamp in milliseconds, integer
  # (O)pen price, float
  # (H)ighest price, float
  # (L)owest price, float
  # (C)losing price, float
  # (V)olume (in terms of the base currency), float 
  recent = ""
  while True:
    time.sleep(len(recent + 1))
    recent = exchange.fetch_ohlcv("BTC/USDT", '1m')
    for entry in recent:
      SQL_STATEMENT = """
      INSERT INTO history_minute VALUES(
      %d,%f, %f,%f,%f,%f
      );""" % (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
      cursor.execute(SQL_STATEMENT)

    print(pd.read_sql_query("SELECT * FROM history_minute", connection))
    connection.commit()





  






