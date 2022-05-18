import pandas as pd 
import yfinance as yf
import numpy as np
from .rsi import *
from .adx import *
from .hilo import *

import warnings
warnings.filterwarnings('ignore')

w = 30
adx_window = 14
rsi_window = 14
hilo_window = 14

def indicators(companies):
  for company in companies:
    data = yf.Ticker(f'{company["sigla"]}.sa').history(period=f'{w}d')

    company['rsi'] = calc_rsi(data = data.copy(), column='Close', window=rsi_window)
    company['adx'] = calc_adx(data = data.copy(), window=adx_window)
    company['hilo'] = calc_hilo(data = data.copy(), window=hilo_window)
  return companies
