import os, sys

try:

    import time

except:

    os.system('pip install time')

    import time

try:

    import math

except:

    os.system('pip install math')

    import math

try:

    import csv

except:

    os.system("pip3 install csv")

    import csv

try:

    import requests

except:

    os.system('pip install requests')

    import requests

try:

    import matplotlib as mpl

except:

    os.system('pip3 install matplotlib')

    import matplotlib as mpl

try:

    import matplotlib.pyplot as plt

except:

    os.system("pip3 install matplotlib")

    import matplotlib.pyplot as plt

from  matplotlib import style

try:

    import pandas as pd

except:

    os.system('pip3 install pandas')

    import pandas as pd

try:

    import numpy as np

except:

    os.system("pip3 install numpy")

    import numpy as np

try:

    from sklearn.svm import SVR

except:

    os.system('pip install sklearn.svm')

    from sklearn.svm import SVR

try:

    from sklearn.model_selection import train_test_split

except:

    os.system('pip install sklearn.model_selection')

    from sklearn.model_selection import train_test_split

try:

    from sklearn.svm import SVR

except:

    os.system('pip install sklearn.svm')

    from sklearn.svm import SVR

try:

    from sklearn.linear_model import LinearRegression

except:

    os.system('pip import sklearn.linear_model')

    from sklearn.linear_model import LinearRegression

try:

    from sklearn.preprocessing import MinMaxScaler

except:

    os.system('pip install sklearn.preprocessing')

    from sklearn.preprocessing import MinMaxScaler

try:

    import scipy

except:

    os.system('pip install scipy')

    import scipy

try:

    import tensorflow

except:

    os.system('pip install tensorflow')

    import tensorflow

try:

    from keras.models  import Sequential 

except:

    os.system('pip install keras')

    from keras.models  import Sequential 

from keras.layers import Dense, LSTM 




style.use('fivethirtyeight')

plt.rcParams['axes.formatter.useoffset'] = False

pd.plotting.register_matplotlib_converters()

FEATURE_VARIABLE = 'Close'


#######################################
# FUNCTIONS
#######################################
#-------------------------------------#
def popupmsg(msg):
#-------------------------------------#
    import tkinter as tk

    from tkinter import ttk

    popup = tk.Tk()
    
    popup.wm_title(" Warning!")
    
    label = ttk.Label(popup, text = msg)
    
    label.grid(row = 3, column = 5)
    
    B1 = ttk.Button(popup, text = "Okay", command = lambda: popup.destroy())
    
    B1.grid(row = 5, column = 5)
    
    popup.mainloop()

######################################
# Classes
######################################
class Prediction_Test:
######################################
    #---------------------------------#
    def __init__(self, stock):
    #---------------------------------#

        self.stock = stock

        self.DAYS_TO_REGRESS = 60

        if __name__ == "__main__":

            self.currPath = os.getcwd()              # Directory you are in NOW

            self.savePath = 'askew'                  # We will be creating this new sub-directory

            self.myPath = (self.currPath + '/' + self.savePath)# The full path of the new sub-dir

            self.dir_path = os.path.dirname(os.path.realpath(__file__))
       
            os.chdir(self.myPath)

            try:

                self.stock= 'JCP'

                self.df = pd.read_csv((self.stock + '.csv'), parse_dates=True, index_col =0)

                # print("tools_predict_generic: df:", self.df.head(10))

            except Exception as e:

                print("tools_prediction_test did not find", self.stock, "information. As it's not in the datawarehouse, is the ticker symbol spelled correctly?")

                print(e)

                popupmsg("Symbol " + self.stock + " is not found! -- Spelling?")

                sys.exit(0)


        if __name__ != '__main__':

            self.df = pd.DataFrame()

            if len(sys.argv) > 1:
                
                if sys.argv[1]:
                
                   self.df = sys.argv[1]


    #-----------------------------#
    def parse_df(self, df):
    #-----------------------------#
        self.df = df

        DAYS_TO_REGRESS = 60


        df_save_last = df.tail(1) 

        #df = df.head(len(df) -1)
        df = df.iloc[-(DAYS_TO_REGRESS):-1]

        df.reset_index(inplace = True)

        df_dates = df.loc[:, 'Date']

        df_FEATURE = df.loc[:, FEATURE_VARIABLE]

        dates = []

        prices = []

        #-------------------------------------#
        # Use cnt instead of day of month, as 
        #     we can read in more than 1 month
        #     or we start on mid-month (from 15nth
        #     thru the next 14nth.)
        #-------------------------------------#

        for x in range(len(df_dates)):

                dates.append([x+1])

        for open_price in df_FEATURE:

            prices.append(float(open_price))

        return dates, prices
                
    #------------------------------------#
    def predict_prices(self,dates, prices, x = 61):
    #------------------------------------#
        print("tools_predict_generic: predict_prices ENTRY")
        svr_lin = SVR(kernel = 'linear', C=1e3)
        svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma =  0.0004)
        svr_poly = SVR(kernel = 'poly', C = 1e3, degree = 2)

        #print("tools_predict_generic: predict_prices starting to svr_lin.fit data")
        #svr_lin.fit(dates, prices)
        
        print("tools_predict_generic: predict_prices starting to svr_poly.fit data")
        svr_poly.fit(dates, prices)
        x = np.reshape(x, (1, -1))
        poly_predict_feature = svr_poly.predict(x)[0]

        print("tools_predict_generic: predict_prices starting to rbf_poly.fit data")
        svr_rbf.fit(dates, prices)
        rbf_predict_feature = svr_rbf.predict(x)[0]

        if __name__ == "__main__":

            plt.scatter(dates, prices, color='black', label = 'Actual Data')
            plt.scatter( dates, svr_poly.predict(dates), color = 'green', label = 'Poly Model', alpha = 0.1)
            plt.scatter( dates, svr_rbf.predict(dates), color = 'red', label = 'RBF Model')
            plt.plot(x, poly_predict_feature, '*', color = 'green', label = 'Poly Predict_' + FEATURE_VARIABLE)
            plt.plot( x, rbf_predict_feature, '*', color = 'blue', label = 'RBF Predict_' + FEATURE_VARIABLE)

            plt.xlabel('Date')
            plt.ylabel('Prices')
            plt.title(" Support Vector Regression")
            plt.legend()


            print("Poly answer for predicting the "  + FEATURE_VARIABLE + " record", str(x), "is:",poly_predict_feature)
            print("RBF answer for predicting the "  + FEATURE_VARIABLE + " record", str(x), "is:", rbf_predict_feature )#svr_rbf.predict(x)[0])

            plt.show()

        return  poly_predict_feature, rbf_predict_feature


if __name__ == "__main__":

    a = Prediction_Test('JCP')


    try:

        stock= 'JCP'

        df = pd.read_csv((stock + '.csv'), parse_dates=True, index_col =0)


    except Exception as e:

        print("tools_prediction_test did not find", stock, "information. As it's not in the datawarehouse, is the ticker symbol spelled correctly?")

        print(e)

        popupmsg("Symbol " + stock + " is not found! -- Spelling?")

        sys.exit(0)

    dates = []
    
    prices = []
    
    dates, prices = a.parse_df(df)
    
    DAYS_TO_REGRESS = [a.DAYS_TO_REGRESS + 1]
    
    poly_predict_feature, rbf_predict_feature = a.predict_prices(dates, prices, DAYS_TO_REGRESS)
    
    print("Poly answer for predicting the "  + FEATURE_VARIABLE + " record", DAYS_TO_REGRESS, "is:",poly_predict_feature)
    print("RBF answer for predicting the "  + FEATURE_VARIABLE + " record", DAYS_TO_REGRESS, "is:", rbf_predict_feature )#svr_rbf.predict(x)[0])

    # plt.show()
