import pandas as pd 
import numpy as np
 
def calc_hilo(data, window=14):

  data_hilo = pd.DataFrame(index=data.index)

  data_hilo['high_avg'] = data.High.rolling(window).mean()
  data_hilo['low_avg'] = data.Low.rolling(window).mean()

  data_hilo['high'] = np.where(data.Close > data_hilo['high_avg'], 1, 0)
  data_hilo['low'] = np.where(data.Close < data_hilo['low_avg'], -1, 0)

  if data_hilo[['high']].tail(1).values[0][0] == 0 and data_hilo[['low']].tail(1).values[0][0] == 0:
    return 0
  elif data_hilo[['high']].tail(1).values[0][0] == 1:
    return 1
  elif data_hilo[['low']].tail(1).values[0][0] == -1:
    return -1