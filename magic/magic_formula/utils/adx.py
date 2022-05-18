import pandas as pd 
import numpy as np

import warnings
warnings.filterwarnings('ignore')

def calc_adx(data, window=14): 

  data_ant = data.shift(1)

  data['tr'] = pd.DataFrame([
          data.High - data.Low, 
          np.absolute(data.High - data_ant.Close), 
          np.absolute(data.Low - data_ant.Close)]).transpose().max(axis=1)
  
  data['dmPlus'] = np.where((data.High - data_ant.High) > (data_ant.Low - data.Low), 
                      (data.High - data_ant.High).apply(
                              lambda x: np.max([x, 0])),
                      0)
  
  data['dmMinus'] = np.where((data_ant.Low - data.Low) > (data.High - data_ant.High), 
                      (data_ant.Low - data.Low).apply(
                              lambda x: np.max([x, 0])),
                      0)
    
  data = data[1:]

  data['trAvg'] = np.NaN
  data['dmPlusAvg'] = np.NaN
  data['dmMinusAvg'] = np.NaN

  data.trAvg[window-1] = np.sum(data.iloc[0:window].tr)
  data.dmPlusAvg[window-1] = np.sum(data.iloc[0:window].dmPlus)
  data.dmMinusAvg[window-1] = np.sum(data.iloc[0:window].dmMinus)

  for i in range(window, len(data)):
      data.trAvg[i] = data.trAvg[i-1] - (data.trAvg[i-1] / window) + data.tr[i]
      data.dmPlusAvg[i] = data.dmPlusAvg[i-1] - (data.dmPlusAvg[i-1] / window) + data.dmPlus[i]
      data.dmMinusAvg[i] = data.dmMinusAvg[i-1] - (data.dmMinusAvg[i-1] / window) + data.dmMinus[i]
      
  data = data.dropna()

  data['diPlus'] = (data.dmPlusAvg / data.trAvg) * 100
  data['diMinus'] = (data.dmMinusAvg / data.trAvg) * 100

  data['DX'] = (np.absolute(data.diPlus - data.diMinus) / (data.diPlus + data.diMinus)) * 100
  data['ADX'] = np.NaN
  data['ADX'][window-1] = data.DX[0:window].mean()

  for i in range(window, len(data)):
      data.ADX[i] = (data.ADX[i-1] * (window - 1) + data.DX[i]) / window  

  data = data.dropna()

  return round(data[['ADX']].tail(1).values[0][0],2)