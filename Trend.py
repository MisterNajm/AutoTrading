from statistics import mean 
class Trend:
  
  def __init__(self):
    self.trend = 1
    self.prev = 0
    self.trendlist = []

  def get_trend(self):
    return self.trend
  
  def get_trend_history(self, range):
     return self.trendlist[-range::]

  def get_trend_avg(self, range):
    return mean(self.trendlist[-range::])

  def update_trend_history(self, value):
    if len(self.trendlist) > 500:
      self.trendlist.pop(0)

    if value > 0:
      if self.trendlist[-1] > 0:
        self.trendlist[-1] += 1
      elif self.trendlist[-1] < 0:
        self.trendlist[-1] = 1
    if value < 0:
      if self.trendlist[-1] > 0:
        self.trendlist[-1] = -1
      elif self.trendlist[-1] < 0:
        self.trendlist[-1] -= 1

  def update_trend(self, value):
    if value > self.prev and self.trend > 0:
      self.trend += 1
      self.trendlist.append(self.trend)
    elif value > self.prev and self.trend < 0:
      self.trend = 1
      self.trendlist.append(self.trend)
    elif value < self.prev and self.trend < 0:
      self.trend -= 1
      self.trendlist.append(self.trend)
    elif value < self.prev and self.trend > 0:
      self.trend = -1
      self.trendlist.append(self.trend)
    
    self.update_trend_history(self.trend)
    self.prev = value
    return


