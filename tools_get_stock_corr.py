import os, sys
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
        
            msg = "tools_get_stock_corr needs stock passed to it. Aborting with no action taken."

            print(msg)
        
            sys.exit(0)
    
    def run(self, stock):
    
        mystocks = visualize_data(stock)
    
        return mystocks


def visualize_data(stock):
    #DEBUG print("Entering visualize_data with stock", stock)
    
    os.chdir(myPath)
    
    df  = pd.read_csv('sp500_joined_closes.csv')

    df_corr = df.corr()
    
    df1 = pd.DataFrame(columns = df_corr.columns)
    
    df1  = df_corr[[stock]]
    
    df1.reset_index()
    
    df1.set_index(df1.axes[0])
   
    #DEBUG print("df1.axes[0] =", df1.axes[0])
    #DEBUG print("df1.axes[1] = ", df1.axes[1])
    
    data = df1.values
    
    dict = {}
    
    counter = 0
    
    for datum in data:
    
        if datum > .80 and datum < 1:
    
            #DEBUG print("tools_get_stock_corr -->datum:", datum, "counter:", counter, "column:", (df1.axes[0][counter]))
    
            dict[(df1.axes[0][counter])] = float(datum)
    
        counter += 1
    
    #DEBUG print("tools_get_stock_corr returning -->", dict)
    
    return dict


    

#########################################
# M A I N   L O G I C
#########################################
if __name__ == "__main__":
    
    a = corr('TSLA')
    
    a.run('TSLA')
