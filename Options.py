import configparser
from enum import Enum
"""
Reads and sets options.json values for persistent options.
"""
config = configparser.ConfigParser()

class Option(Enum):
  simulate = "simulate"
  pulls_per_second = "pulls_per_second"
  use_historical_data ="use_historical_data"
  exchange = "exchange"
  override_limits ="override_limits"

def get_option(option: Option):
    config.read('options.ini')
    if(option == Option.pulls_per_second):
      if(float(config["NORMAL"]["pulls_per_second"]) > 1 and config["NORMAL"]["override_limits"] == "False"):
        return 1
    return config["NORMAL"][option.name]

def set_option(option: Option, value):
    config["NORMAL"][option.name] = value
    with open('options.ini', 'w') as configfile:
        config.write(configfile)
