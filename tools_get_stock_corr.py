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
    #-----------------------------------#    
    def __init__(self, stock):
    #-----------------------------------#    
        
        self.stock = stock
        
        self.dict  = {}
        
        if len(stock) == 0:
        
            msg = "tools_get_stock_corr needs stock passed to it. Aborting with no action taken."

            print(msg)
        
            sys.exit(0)
    
    #-----------------------------------#    
    def run(self, stock):
    #-----------------------------------#    
    
        mystocks = visualize_data(stock)
    
        return mystocks

#-------------------------------------#    
def visualize_data(stock):
#-------------------------------------#    
    os.chdir(myPath)

    try:
    
        df  = pd.read_csv('sp500_joined_closes.csv')
    except Exception as e:

        print("tools_get_stock_corr ==> Unable to read sp500_joined_closes.csv - is it there? Aborting correlation calculations.")

        print(e)

        return 0

    df_corr = df.corr()
    
    df1 = pd.DataFrame(columns = df_corr.columns)

    try:
    
        df1  = df_corr[[stock]]

    except Exception as e:

        print("tools_get_stock_corr ==> Unable to calculate correlations on stock:", stock, "Is it defined in your search list?")

        print(e)

        return 0
    
    df1.reset_index()
    
    df1.set_index(df1.axes[0])
   
    data = df1.values
    
    dict = {}
    
    counter = 0
    
    for datum in data:
    
        if datum > .80 and datum < 1:
    
            dict[(df1.axes[0][counter])] = float(datum)
    
        counter += 1
    
    return dict


    

#########################################
# M A I N   L O G I C
#########################################
if __name__ == "__main__":
    
    a = corr('TSLA')
    
    a.run('TSLA')
