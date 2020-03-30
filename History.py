import pandas
import datetime

class History:
  currDay = 0
  companies = {}
  def __init__(self, days):
    for day in days:
      stocks = day.getStocks()
      for stock in stocks:
        if()
        companies[stock.getId()] = stock.getName()
    self.dates = np.asArray(pandas.date_range(days[0].getDate(), periods=len[days]))
    self.days = pandas.DataFrame(index = dates)
  
  def getDayByDate(date)
    