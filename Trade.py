import sqlite3
import Market

connection = sqlite3.connect("crypto_trading.db")
cursor = connection.cursor()

##TODO
##Funktion ist scheiße, man muss die Umrechnungsquoten noch mit einbeziehen
###
# origin_amount auf unter 0, falls alles verkauft werden soll.
#
###
def trade(origin, target, price, origin_amount=-1, reverse=False):
    
    SQL_STATEMENT = "SELECT origin_amount FROM wallet WHERE id = '%s'" % origin
    cursor.execute(SQL_STATEMENT)
    balanceOrigin = cursor.fetchone()[0]
    if origin_amount < 0:
      origin_amount = balanceOrigin 
    #target_amount: Einzukaufende Anzahl Target Währung
    #origin_amount: Auszugebende Anzahl Origin Währung
    #Price: Momentaner Tauschpreis

    target_amount = origin_amount / price
    if reverse:
      target_amount = origin_amount * price
    SQL_STATEMENT = "SELECT origin_amount FROM wallet WHERE id = '%s'" % target
    cursor.execute(SQL_STATEMENT)
    balanceTarget = cursor.fetchone()[0]

    if (origin_amount > balanceOrigin):
        raise NameError("Bruh du hast nicht genug $$$ :<( Dir fehlen %0.20f %s" % ((balanceOrigin - origin_amount), origin))
        return
    SQL_STATEMENT = "UPDATE wallet SET origin_amount = %0.20f WHERE id = '%s'" % (
        (balanceOrigin - origin_amount), origin)
    cursor.execute(SQL_STATEMENT)

    SQL_STATEMENT = "UPDATE wallet SET origin_amount = %0.20f WHERE id = '%s'" % (
        (balanceTarget + target_amount), target)
    cursor.execute(SQL_STATEMENT)
    SQL_STATEMENT = """INSERT INTO transactions(type, price, target_amount, origin, target)
  VALUES(
    'BUY',
    %0.20f,
    %0.20f,
    '%s',
    '%s'
  );
  """ % (price, target_amount, origin, target)
    cursor.execute(SQL_STATEMENT)

    #TODO: Verification

    if(origin_amount < 0):
      return target_amount, balanceOrigin
    else:
      return target_amount, origin_amount


def get_balance(id=""):
    connection = sqlite3.connect("crypto_trading.db")
    cursor = connection.cursor()

    if id == "":
        id = '*'
    SQL_STATEMENT = "SELECT %s FROM wallet;" % (id)
    cursor.execute(SQL_STATEMENT)
    return cursor.fetchall()


def initialize():
    currencies = ["USD", "BTC"]
    for currency in currencies:
        SQL_STATEMENT = "INSERT INTO wallet(id, origin_amount) VALUES ('%s', 100.00);" % currency
        if(currency == "BTC"):
          SQL_STATEMENT = "INSERT INTO wallet(id, origin_amount) VALUES ('%s', 0.00);" % currency
        cursor.execute(SQL_STATEMENT)


## Not required, only if db is deleted.
def create():
    SQL_STATEMENT = "DROP TABLE transactions;"
    cursor.execute(SQL_STATEMENT)
    SQL_STATEMENT = "DROP TABLE wallet;"
    cursor.execute(SQL_STATEMENT)    
    SQL_STATEMENT = """CREATE TABLE transactions (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  type VARCHAR(4),
	  price REAL,
	  target_amount INTEGER,
	  origin VARCHAR(4),
    target VARCHAR(4)
    );"""

    cursor.execute(SQL_STATEMENT)
    SQL_STATEMENT = """CREATE TABLE wallet (
	  id VARCHAR(4) PRIMARY KEY,
	  origin_amount REAL
    );"""
    cursor.execute(SQL_STATEMENT)
