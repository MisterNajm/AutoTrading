class Trend:

  def __init__(self):
    self.trend = 1
    self.prev = 0

  def get_trend(self):
    return self.trend
  
  def update_trend(self, value):
    if value > self.prev and self.trend > 0:
      self.trend += 1

    elif value > self.prev and self.trend < 0:
      self.trend = 1

    elif value < self.prev and self.trend < 0:
      self.trend -= 1

    elif value < self.prev and self.trend > 0:
      self.trend = -1

    self.prev = value
    return


