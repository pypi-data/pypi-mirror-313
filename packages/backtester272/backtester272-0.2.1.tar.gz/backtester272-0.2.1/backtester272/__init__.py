from backtester272.Backtester import Backtester
from backtester272.Universe import Universe
from backtester272.StrategyBank import *


with open("pyproject.toml") as f:
    for line in f:
        if "version" in line:
            __version__ = line.split("=")[1].strip().replace('"', '')
            break
    else:
        __version__ = "0.0.0"