import sqlite3
import Market

connection = sqlite3.connect("crypto_trading.db")
cursor = connection.cursor()

##TODO
##Funktion ist scheiße, man muss die Umrechnungsquoten noch mit einbeziehen
def trade(origin, target, price, amount):
    SQL_STATEMENT = "SELECT amount FROM wallet WHERE id = '%s'" % origin
    cursor.execute(SQL_STATEMENT)
    balanceOrigin = cursor.fetchone()[0]

    #Qnty: Einzukaufende Anzahl Target Währung
    #Amount: Auszugebende Anzahl Origin Währung
    #Price: Momentaner Tauschpreis

    qnty = amount / price
    SQL_STATEMENT = "SELECT amount FROM wallet WHERE id = '%s'" % target
    cursor.execute(SQL_STATEMENT)
    balanceTarget = cursor.fetchone()[0]

    if (amount > balanceOrigin):
        raise NameError("Bruh du hast nicht genug $$$ :<(")
        return
    SQL_STATEMENT = "UPDATE wallet SET amount = %f WHERE id = '%s'" % (
        (balanceOrigin - amount), origin)
    cursor.execute(SQL_STATEMENT)

    SQL_STATEMENT = "UPDATE wallet SET amount = %f WHERE id = '%s'" % (
        (balanceTarget + qnty), target)
    cursor.execute(SQL_STATEMENT)
    SQL_STATEMENT = """INSERT INTO transactions(type, price, qnty, origin, target)
  VALUES(
    'BUY',
    %f,
    %d,
    '%s',
    '%s'
  );
  """ % (price, qnty, origin, target)
    cursor.execute(SQL_STATEMENT)

    #TODO: Verification
    return


def get_balance(id=""):
    if id == "":
        id = '*'
    SQL_STATEMENT = """SELECT %s FROM wallet;
  """ % (id)
    cursor.execute(SQL_STATEMENT)
    return cursor.fetchall()


def initialize():
    currencies = ["USD", "EUR", "BTC", "ETH"]
    for currency in currencies:
        SQL_STATEMENT = "INSERT INTO wallet(id, amount) VALUES ('%s', 100.00);" % currency
        if(currency == "BTC"):
          SQL_STATEMENT = "INSERT INTO wallet(id, amount) VALUES ('%s', 0.00);" % currency
        cursor.execute(SQL_STATEMENT)


## Not required, only if db is deleted.
def create():

    SQL_STATEMENT = """CREATE TABLE transactions (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  type VARCHAR(4),
	  price FLOAT(5),
	  qnty INTEGER,
	  origin VARCHAR(4),
    target VARCHAR(4)
    );"""

    cursor.execute(SQL_STATEMENT)
    SQL_STATEMENT = """CREATE TABLE wallet (
	  id VARCHAR(4) PRIMARY KEY,
	  amount FLOAT(5)
    );"""
    cursor.execute(SQL_STATEMENT)
