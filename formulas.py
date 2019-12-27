import os
try:
    import pandas as pd
except:
    os.system('pip install pandas')
    import pandas as pd
try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np
try:
    from scipy import stats, optimize
except:
    os.system('pip install scipy')
    from scipy import stats, optimize
from scipy.optimize import OptimizeWarning
try:
    import warnings
except:
    os.system('pip install warnings')
    import warnings
try:
    import math
except:
    os.system('pip install math')
    import math
try:
    import matplotlib.pyplot as plt
except:
    os.system('pip install matplotlib')
    import matplotlib.pyplot as plt
from mpl_finance import _candlestick
from matplotlib.dates import date2num
try:
    from sklearn.linear_model import LinearRegression
except:
    os.system('pip install sklearn')
    from sklearn.linear_model import LinearRegression
try:
    import datetime
except:
    os.system('pip install datetime')
    import datetime

#######################################
class formulaz:
#######################################

    def __init__(self):
        pass
    #---------------------------------#
    def heikenashi(prices):
    #---------------------------------#
        """
        param prices: The Open High Low Close prices in a dataframe
        param return: Heiken Ashi OHLC candles
        """
        results = formulaz()

        dict = {}

        HAclose = prices [['open', 'high','close', 'low']].sum(axis=1)/4

        HAopen = HAclose.copy()

        HAopen.iloc[0] = HAclose.iloc[0]
        HAhigh = HAclose.copy()

        HAlow = HAclose.copy()

        for i in range(1, len(prices)):

            HAopen.iloc[i] = (HAopen.iloc[i-1] + HAclose.iloc[i-1])/2

            HAhigh.iloc[i] = np.array([prices.high.iloc[i], HAopen.iloc[i], HAclose.iloc[i]]).max()

            HAlow.iloc[i] = np.array([prices.low.iloc[i], HAopen.iloc[i], HAclose.iloc[i]]).min()

        df = pd.concat((HAopen, HAhigh, HAlow, HAclose), axis=1)
        df.columns = ['open', 'high','close','low']

        dict[0] = df

        results.candles = dict

        print(dict)
        return results

    #---------------------------------#
    def straighten_trend(prices, method = 'difference'):
    #---------------------------------#
        """
        ;usage: Prepare for Fourier by removing trend from data
        ;parame prices: Open High Low Close dataframe
        ;param method: Method to remove trend, either 'linear' or 'difference'
        ;return: The straighten_trend price series
        """
        if method == 'difference':

            straighten_trend = prices.close[1:] - prices.close[:-1].values

        elif method == 'linear':

            x = np.arange(0, int(len(prices)))
            y = prices.close.values

            model = LinearRegression()

            model.fit(x.reshape(-1,1), y.reshape(-1, 1))

            trend = model.predict(x.reshape(-1,1))

            trend = trend.reshape((len(prices),))

            straighten_trend = prices.close - trend

        else:
            print("Invalid input for removing trend. Options are 'linear' or 'difference'.")

        return straighten_trend












    

