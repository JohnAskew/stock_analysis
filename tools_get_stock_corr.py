import os, sys
import datetime as dt
try:
    import bs4 as bs
except:
    os.system('pip install BeautifulSoup')
    import ba4 as bs
try:
    import matplotlib.pyplot as plt
except:
    os.system('pip install matplotlib')
    import matplotlib.pyplot as plt
try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np
try:
    import pandas as pd
except:
    os.system('pip install pandas')
    import pandas as pd
try:
    import pandas_datareader.data as web
except:
    os.system('pip install pandas-datareader')
    import pandas_datareader.data as web
try:
    import pickle
except:
    os.system('pip install pickle')
    import pickle
try:
    import requests
except:
    os.system('pip install requests')
    import requests
'''From the Sentdex series on Matplotlib for Finance. This script
scrapes Wiki for stock abbreviations and returns list of abbrv. The
current DataReader documentation states yahoo! no longer works, but 
as of 2019.06.23, it's working for this script and we are pulling 
stock prices from yahoo.
'''
#---------------------------------------#
# Variables
#---------------------------------------#
in_file = 'in_file'                            # Read Wiki data into this file
provider = 'yahoo' 
currPath = os.getcwd()                  # Directory you are in NOW
savePath = 'askew'                      # We will be creating this new sub-directory
myPath = (currPath + '/' + savePath)    # The full path of the new sub-dir
stock = ""
stock = ""
#########################################
class corr():
#########################################
    def __init__(self, stock):
        self.stock = stock
        self.dict  = {}
        if len(stock) == 0:
            print("tools_get_stock_corr needs stock passed to it. Aborting with no action taken.")
            sys.exit(0)
    def run(self, stock):
        mystocks = visualize_data(stock)
        return mystocks


def visualize_data(stock):
    print("Entering visualize_data with stock", stock)
    os.chdir(myPath)
    df  = pd.read_csv('sp500_joined_closes.csv')

    df_corr = df.corr()
    df1 = pd.DataFrame(columns = df_corr.columns)
    df1  = df_corr[[stock]]
    df1.reset_index()
    df1.set_index(df1.axes[0])
    #df1.set_index(df['Date'], inplace = True)
   
    #df1.set_index(['Date'])
    print("df1.axes[0] =", df1.axes[0])
    print("df1.axes[1] = ", df1.axes[1])
    # mask = np.zeros_like(df.corr())
    # triangle_indices = np.triu_indices_from(mask)
    # mask[triangle_indices] = True
    # print(mask)

    #data = df_corr.values
    data = df1.values
    dict = {}
    counter = 0
    for datum in data:
        if datum > .80 and datum < 1:
            print("tools_get_stock_corr -->datum:", datum, "counter:", counter, "column:", (df1.axes[0][counter]))
            dict[(df1.axes[0][counter])] = float(datum)
        counter += 1
    print("tools_get_stock_corr returning -->", dict)
    return dict


    

#########################################
# M A I N   L O G I C
#########################################
if __name__ == "__main__":
    a = corr('JCP')
    a.run('JCP')
