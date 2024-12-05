import numpy as np
import pandas as pd

def RMSE(Y,Yhat):
    return (((Y-Yhat)**2).mean())**0.5

# Normlized RMSE
def NRMSE(Y,Yhat):
    return RMSE(Y,Yhat)/(Y.max()-Y.min())



def PerformanceMeasure(x):
  """
  input: daily profit
  output:sharpe ratio and maximum drawdown
  """
  x=pd.Series(x)
  wealth=x.cumsum()
  cmax=wealth.cummax()
  dd=(cmax-wealth)/cmax
  sr=x.mean()/x.std()
  return sr, dd.max()