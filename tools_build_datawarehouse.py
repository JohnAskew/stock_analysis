'''From the Sentdex series on Matplotlib for Finance. This script
scrapes Wiki for stock abbreviations and returns list of abbrv. The
current DataReader documentation states yahoo! no longer works, but 
as of 2019.06.23, it's working for this script and we are pulling 
stock prices from yahoo.


TTTTTTTTTT         D D
    TT             D   D
    TT             D     D
    TT  ooooo  --  D     D  ooooo
    TT  o   o      D   D    o   o
    TT  00000      D D      ooooo

1. Add pop-up box when get_data_from_yahoo fails. 
Tell user able to refresh data and results are 
from last time this ran successfully.

2. Add S&P400 - scrape and add to Menu bar
https://www.barchart.com/stocks/indices/sp/sp400?page=all

3. Calculate earnings per share from PER
P/E Ratio=  Price per Share​(year end closing price)
            ---------------
            Earnings per Share

EARNINGS PER SHARE = 



'''
import os, sys

try:

    from tools_scrape_nasdaq  import get_NASDAQ

except Exception as e:

    print("tools_build_datawarehouse unable to import get_NASDAQ from tools_scrape_nasdaq.py. Skipping NASDAQ stocks")

    print(e)

    sys.exit(0) 

try:

    from tools_scrape_wiki_stocks import get_WIKI

except Exception as e:

    print("tools_build_datawarehouse unable to import get_WIKI from tools_scrape_wiki_stocks. Skipping NYSE stocks on WIKI")    

    print(e)

    sys.exit(0)

try:
    
    from stocks_alt_info import altAnalysis

except Exception as e:

    print("Unable to access python module stocks_alt_info. Skipping financial details and continuing on...")

    print(e)

try:

    import configparser

except:

    os.system('pip install configparser')

    import configparser

from tools_parse_config import ParseConfig

import datetime as dt

try:

    import bs4 as bs

except:

    os.system('pip install BeautifulSoup')

    import bs4 as bs

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

try:

    a = ParseConfig()

except Exception as e:

    print("Unable to find or utilize ParseConfig class in tools_parse_config.py")

    print(e)

    movavg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
    
    movavg_window_days_long_term  = 30                                         #Moving Average 30 days (slow)
    
    macd_periods_long_term        = 26
    
    macd_periods_short_term       = 12
    
    expma_periods                 = 9 

    pct_chg                       = 'new'

    boll                          = 'y'

    boll_window                   = 20

    boll_weight                   = 2

    fib                           = 'y'

try:
    
    movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold, pct_chg, boll, boll_window_days, boll_weight, fib, sel_stocks = a.run()
    ##
    ### Convert numeric config settings to integer. String vars need no conversion.
    ##
    movavg_window_days_short_term = int(movavg_window_days_short_term)

    movavg_window_days_long_term  = int(movavg_window_days_long_term)

    macd_periods_long_term        = int(macd_periods_long_term)

    macd_periods_short_term       = int(macd_periods_short_term)

    expma_periods                 = int(expma_periods)

    rsi_overbought                = int(rsi_overbought)

    rsi_oversold                  = int(rsi_oversold)

    boll_window_days              = int(boll_window_days)

    boll_weight                   = int(boll_weight)

except Exception as e:

    print("tools_build_datawarehouse--> call to a.run() in tool_parse_config.py failed. Using defaults.")

    print(e)

    movavg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
    
    movavg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
    
    macd_periods_long_term = 26
    
    macd_periods_short_term = 12
    
    expma_periods = 9 

    rsi_overbought = 70
    
    rsi_oversold = 30
    
    pct_chg = new
    
    boll = n
    
    boll_window_days = 20
    
    boll_weight = 2
    
    fib = n




#######################################################
# Functions (before Main Logic)
########################################################
#-------------------------------------------------------#
def get_fina_summary(csv, stock = 'JCP'):
#-------------------------------------------------------#

    if not os.path.exists(csv):

        print(sys.argv[0], "tools_build_datawarehouse section: get_fina_summary -->  Did not receive valid CSV file.")
        
        print("\t--> skipping financial summary for", stock)

        return

    try:

        a = altAnalysis(stock)         #Call Fina Summary Scraping Class

        company_json = a.run()         #Run the Class, save the JSON returned

    except Exception as e:

        print("tools_build_datawarehouse section: get_fina_summary --> Unable to extract Accounting details from program stock_alt_info.py. Skipping accounting details.")
        
        print(e)

        return

    col_list   =[]
   
    fin_list  = []
   
    try:

        # col_list.append("BID")

        # col_list.append("ASK")

        col_list.append("TD_VOLUME")

        col_list.append("PE_RATIO")

        col_list.append("EPS_RATIO")

        col_list.append("AVERAGE_VOLUME_3MONTH")

        col_list.append("MARKET_CAP")

        col_list.append("DIVIDEND_AND_YIELD")

        col_list.append("ONE_YEAR_TARGET_PRICE")


        # fin_list.append(company_json["OTHER_DETAILS"]["BID"])

        # fin_list.append(company_json["OTHER_DETAILS"]["ASK"])

        fin_list.append(company_json["OTHER_DETAILS"]["TD_VOLUME"])

        fin_list.append(company_json["OTHER_DETAILS"]["PE_RATIO"])

        fin_list.append(company_json["OTHER_DETAILS"]["EPS_RATIO"])

        fin_list.append(company_json["OTHER_DETAILS"]["AVERAGE_VOLUME_3MONTH"])

        fin_list.append(company_json["OTHER_DETAILS"]["MARKET_CAP"])

        fin_list.append(company_json["OTHER_DETAILS"]["DIVIDEND_AND_YIELD"])

        fin_list.append(company_json["OTHER_DETAILS"]["ONE_YEAR_TARGET_PRICE"])

    except Exception as e:

        print("tools_build_datawarehouse section: get_fina_summary --> Unable to parse JSON received from stocks_alt_info. Skipping accounting details on report.")
        
        print(e)

        return

    try:

        df_fina = pd.read_csv((csv), parse_dates=True)

    except Exception as e:

        print(sys.argv[0], "tools_build_datawarehouse section: get_fina_summary --> Unable to read CSV for", stock, "...skipping Financial Summary data.")

        print(e)

        return
        
    df_fina.set_index('Date', inplace = True)
        
    df_fina_len = len(df_fina)

    for i in col_list:
        
        df_fina[i] = ""

    
    df_fina_tail = df_fina.iloc[df_fina_len - 1 :df_fina_len, :]

    df_fina_tail.reset_index()

    for i in range(0,len(fin_list)):
        
        df_fina_tail[col_list[i]] = fin_list[i]

    df_fina.iloc[df_fina_len - 1 :df_fina_len, :] = df_fina_tail

    df_fina.to_csv(csv, sep = ',', encoding = 'utf-8')

    os.remove(stock + '.data.json')
    
    os.remove(stock + '.output_file.html')
     
    # except Exception as e:
    #     print("stocks_1.py unable to parse JSON received from stocks_alt_info. Skipping accounting details on report.")
    #     print(e)
    #     return
#-------------------------------------------------------#
def calc_rsi(prices, n=14):
#-------------------------------------------------------#
    deltas = np.diff(prices)

    seed = deltas[:n + 1]

    up = seed[seed >= 0].sum()/n

    down = -seed[seed < 0].sum()/n

    rs = up/down

    rsi = np.zeros_like(prices)

    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):

        delta = deltas[i - 1]

        if delta > 0:

            upval = delta

            downval = 0.

        else:

            upval = .0

            downval = -delta

        up   = (up   * (n - 1) + upval)   / n

        down = (down * (n - 1) + downval) / n

        rs = up/down

        rsi[i] = 100. - 100./(1. + rs)

    return rsi

#-------------------------------------------------------#
def moving_average(values, window):
#-------------------------------------------------------#
    weights  = np.repeat(1.0, window) / window   #Numpy repeat - repeats items in array - "window" times

    smas = np.convolve(values, weights, 'valid') #Numpy convolve - returns the discrete, linear convolution of 2 seq.
    #https://stackoverflow.com/questions/20036663/understanding-numpys-convolve
    return smas
#-------------------------------------------------------#
def calc_ema(values,window):
#-------------------------------------------------------#
    weights = np.exp(np.linspace(-1, 0., window))

    weights /= weights.sum()

    a = np.convolve(values, weights,  mode = 'full')[:len(values)]

    a[:window] = a[window]

    return a
#-------------------------------------------------------#
def calc_macd(x, slow=macd_periods_long_term, fast = macd_periods_short_term):
#-------------------------------------------------------#
    eMaSlow = calc_ema(x, slow)

    eMaFast = calc_ema(x, fast)

    return eMaSlow, eMaFast, eMaFast - eMaSlow

#---------------------------------------#
def save_sp500_stocks():
#---------------------------------------#

    a = get_WIKI()

    stocks_wiki = a.run()

    # a = get_NASDAQ()

    # stocks_nasdaq = a.run()

    # stocks = list(set(stocks_wiki + stocks_nasdaq))

    stocks = stocks_wiki # temp code, while we remove the NASDAQ stocks -- 3500 stocks

    print(stocks)

    sel_stockz = sel_stocks.split(',')

    for in_stock in sel_stockz:

        stocks.append(in_stock)

    stocks = list(set(stocks))

    stocks.sort()

    with open("sp500stocks.pickle", "wb") as in_file:    #Pickle saves results as reuable object

        pickle.dump(stocks, in_file)                     #Save results from above to Pickle.
    
    return(stocks)

#---------------------------------------#
def get_data_from_yahoo(reload_sp500 = True):
#---------------------------------------#
    os.chdir(myPath) 

    if reload_sp500:

        stocks = save_sp500_stocks()

    else:

        with open("sp500stocks.pickle", 'rb') as in_file:

            stocks = pickle.load(in_file)

    start = ( dt.datetime.now() - dt.timedelta(days = 365) )       # Format is year, month, day
    
    end = dt.datetime.today()           # format of today() = [yyyy, mm, dd] - list of integers

    ##
    ### If now is before today's market is open, then skip. 
    ##
    
    market_open  = dt.datetime.strptime("09:00", "%H:%M")

    market_open  = dt.datetime.time(market_open)

    for subject in stocks:
    
        saveFile=('{}'.format(subject) + '.csv')    # The RESUlTS we are saving on a daily basis

        if os.path.exists(saveFile):

            st = os.stat(saveFile)     #The csv date (created)



            if (os.path.exists(saveFile)) and (( dt.datetime.now().time() < market_open) or ((dt.date.fromtimestamp(st.st_mtime) == dt.date.today()))):

                print("Skipping", subject, "its' current as of today:" , end)

            else:
                ##
                ### Not current or does not exist
                ##

                try:
            
                    df = web.DataReader(subject, provider, start, end)
            
                    df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
            
                    df['MA10'] = df['Adj_Close'].rolling(movavg_window_days_short_term).mean()

                    df['MA30'] = df['Adj_Close'].rolling(movavg_window_days_long_term).mean()

                    df['RSI']  = calc_rsi(df["Close"])

                    eMaSlow, eMaFast, df['MACD'] = calc_macd(df['Close'])

                    df['EMA9'] = calc_ema(df['MACD'], expma_periods)

                    df.to_csv('{}.csv'.format(subject))

                    get_fina_summary('{}.csv'.format(subject), subject)

                except:

                    print("tools_build_datawarehouse section: get_data_from_yahoo --> Issue with processing ", subject, "skipping data extract")

        else:

            try:
            
                df = web.DataReader(subject, provider, start, end)
        
                df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
        
                df['MA10'] = df['Adj_Close'].rolling(movavg_window_days_short_term).mean()

                df['MA30'] = df['Adj_Close'].rolling(movavg_window_days_long_term).mean()

                df['RSI']  = calc_rsi(df["Close"])

                eMaSlow, eMaFast, df['MACD'] = calc_macd(df['Close'])

                df['EMA9'] = calc_ema(df['MACD'], expma_periods)

                df.to_csv('{}.csv'.format(subject))

                get_fina_summary('{}.csv'.format(subject), subject)

            except:

                print("tools_build_datawarehouse section: get_data_from_yahoo --> Issue with processing ", subject, "skipping data extract")  
    
#-------------------------------------------------------#
def stocks_join_closeprice():
#-------------------------------------------------------#
    os.chdir(myPath)

    with open("sp500stocks.pickle", "rb") as in_file:

        stocks = pickle.load(in_file)

    main_df = pd.DataFrame()

    for count, subject in enumerate(stocks):

        try:

            df = pd.read_csv('{}.csv'.format(subject))

        except:

            print("tools_build_datawarehouse section stocks_join_closeprice --> Unable to read ", subject, "csv for DataFrame processing...skipping..")

            continue

        try:

            df.set_index('Date', inplace = True)

            df.rename(columns = {'Adj_Close': subject}, inplace = True)

            try:

                df.drop(['Open', 'High','Low','Close', 'Volume', 'MA10', 'MA30', 'RSI', 'MACD', 'EMA9', 'TD_VOLUME', 'PE_RATIO', 'EPS_RATIO', 'AVERAGE_VOLUME_3MONTH', 'MARKET_CAP', 'DIVIDEND_AND_YIELD', 'ONE_YEAR_TARGET_PRICE'], axis = 1, inplace = True)
            
            except Exception as e:

                try:

                    df.drop(['Open', 'High','Low','Close', 'Volume', 'MA10', 'MA30', 'RSI', 'MACD', 'EMA9'], axis = 1, inplace = True)
            
                except Exception as e:

                    print("tools_build_datawarehouse section stocks_join_closeprice --> Issues with dropping columns. Skipping")

                    print(e)

                    continue 

        except:

            print("Issue with enumerating stock:", subject, "skipping...")

            continue

        if main_df.empty:

            try:

                main_df = df

            except:

                print("main_df empty and issues with current df, skipping")

        else:

            try:

                main_df = main_df.join(df, how = 'outer')

            except:

                print("main_df join issues, skipping current df.")


    main_df.to_csv('sp500_joined_closes.csv')


#-------------------------------------------------------#
def stocks_join_per():
#-------------------------------------------------------#
    os.chdir(myPath)

    with open("sp500stocks.pickle", "rb") as in_file:

        stocks = pickle.load(in_file)

    main_df = pd.DataFrame()

    for count, subject in enumerate(stocks):

        try:

            df = pd.read_csv('{}.csv'.format(subject))

        except:

            print("tools_build_datawarehouse section stocks_join_per --> Unable to read ", subject, "csv for DataFrame processing...skipping..")

            continue

        try:

            df.set_index('Date', inplace = True)

            df.rename(columns = {'PE_RATIO': subject}, inplace = True)

            try:

                df.drop(['Open', 'High','Low','Close', 'Adj_Close', 'Volume', 'MA10', 'MA30', 'RSI', 'MACD', 'EMA9', 'BID',  'ASK', 'TD_VOLUME',  'EPS_RATIO', 'AVERAGE_VOLUME_3MONTH', 'MARKET_CAP', 'DIVIDEND_AND_YIELD', 'ONE_YEAR_TARGET_PRICE'], axis = 1, inplace = True)
            
                df.replace('', np.nan, inplace = True)

                try:

                    df.dropna(how = 'any', axis =0, inplace = True)

                except Exception as e:

                    print("tools_build_datawarehouse section sp500_join_per: --> Issue for", subject, ": dropna filter encounted issues...skipping", subject)

                    print(e)

                    continue

            except Exception as e:

                print("tools_build_datawarehouse section stocks_join_per --> Issues for", subject, "renaming PE_Ratio while dropping columns. Skipping")

                print(e)

                continue 

        except Exception as e:

            print("Issue with PE_Ratio while enumerating stock:", subject, "skipping...")

            print(e)

            continue



        if main_df.empty:

            try:

                main_df = df

            except Exception as e:

                print("main_df empty and issues with current df on PE_RATIO, skipping")

                print(e)

        else:

            try:

                main_df = main_df.join(df, how = 'outer')

            except Exception as e:

                print("main_df join issues with PE_RATIO, skipping current df.")

                print(e)


    main_df.to_csv('sp500_joined_per.csv')
#########################################
# M A I N   L O G I C
#########################################
#---------------------------------------#
# Variables
#---------------------------------------#
in_file = 'in_file'                            # Read Wiki data into this file

subject = ''                            # Stock Abbreviation

provider = 'yahoo' 

currPath = os.getcwd()                  # Directory you are in NOW

savePath = 'askew'                      # We will be creating this new sub-directory

myPath = (currPath + '/' + savePath)    # The full path of the new sub-dir

if not os.path.exists(myPath):      # The directory you are in NOW

    os.makedirs(myPath)             # create a new dir below the dir your are in NOW

    os.chdir(myPath)   

get_data_from_yahoo(True) #Set to true if first time run of want to refresh

stocks_join_closeprice()

#stocks_join_per()

