import os
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
#######################################################
# Functions (before Main Logic)
########################################################
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
def calc_macd(x, slow=26, fast = 12):
#-------------------------------------------------------#
    eMaSlow = calc_ema(x, slow)
    eMaFast = calc_ema(x, fast)
    return eMaSlow, eMaFast, eMaFast - eMaSlow

#---------------------------------------#
def save_sp500_stocks():
#---------------------------------------#

    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'}) #Wiki only has 1 table.
    stocks = []                                    #Allocate list to save results
    stocks.append('TSLA')
    stocks.append('JCP')
    stocks.append('MANH')                          # Add missing stock

    for row in table.findAll('tr')[1:]:            #Wiki data starts w/2nd row
        subject = row.findAll('td')[0].text        #Wiki data starts 1st col
        subject = str(subject).replace('\n', '')
        stocks.append(subject)

    with open("sp500stocks.pickle", "wb") as in_file:    #Pickle saves results as reuable object
        pickle.dump(stocks, in_file)                     #Save results from above to Pickle.
    
    print(stocks)

    return(stocks)

#save_sp500_stocks()

#---------------------------------------#
def get_data_from_yahoo(reload_sp500 = True):
#---------------------------------------#
    os.chdir(myPath) 
    if reload_sp500:
        stocks = save_sp500_stocks()
    else:
        with open("sp500stocks.pickle", 'rb') as in_file:
            stocks = pickle.load(in_file)

    # if not os.path.exists(myPath):      # The directory you are in NOW
    #     os.makedirs(myPath)             # create a new dir below the dir your are in NOW
    # os.chdir(myPath)                    # move into the newly created sub-dir

    # if not os.path.exists(savePath):
    #     os.makedirs(savePath)

    start = ( dt.datetime.now() - dt.timedelta(days = 365) )       # Format is year, month, day
    end = dt.datetime.today()           # format of today() = [yyyy, mm, dd] - list of integers

    for subject in stocks:
        saveFile=('{}'.format(subject) + '.csv')    # The RESUlTS we are saving on a daily basis
        if os.path.exists(saveFile): #If results (stock.csv) exists, chk creation time.
            print('Already have {}'.format(subject), end = ' ') 
            st = os.stat(saveFile)
            if dt.date.fromtimestamp(st.st_mtime) != dt.date.today():
                try:
                    print(" but updating data to bring current to today:" , end)
                    df = web.DataReader(subject, provider, start, end)
                    df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
                    df['MA10'] = df['Adj_Close'].rolling(10).mean()
                    df['MA30'] = df['Adj_Close'].rolling(30).mean()
                    df['RSI']  = calc_rsi(df["Close"])
                    eMaSlow, eMaFast, df['MACD'] = calc_macd(df['Close'])
                    df['EMA9'] = calc_ema(df['MACD'], expMA_periods)
                    df.to_csv('{}.csv'.format(subject))
                except:
                    print("Issue with updating ", subject, "skipping data extract")
            else:
                print(" and is current as of today:" , end)
        else:
            try:
                df = web.DataReader(subject, provider, start, end)
                df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
                df['MA10'] = df['Adj_Close'].rolling(10).mean()
                df['MA30'] = df['Adj_Close'].rolling(30).mean()
                df['RSI']  = calc_rsi(df["Close"])
                eMaSlow, eMaFast, df['MACD'] = calc_macd(df['Close'])
                df['EMA9'] = calc_ema(df['MACD'], expMA_periods)
                df.to_csv('{}.csv'.format(subject))
            except:
                print("Issue with new file:", subject, "skipping data extract")

#-------------------------------------------------------#
def compile_data():
#-------------------------------------------------------#
    os.chdir(myPath)
    with open("sp500stocks.pickle", "rb") as in_file:
        stocks = pickle.load(in_file)
    main_df = pd.DataFrame()

    for count, subject in enumerate(stocks):
        try:
            df = pd.read_csv('{}.csv'.format(subject))
            df.set_index('Date', inplace = True)
            df.rename(columns = {'Adj_Close': subject}, inplace = True)
            df.drop(['Open', 'High','Low','Close', 'Volume', 'MA10', 'MA30', 'RSI', 'MACD', 'EMA9'], axis = 1, inplace = True)
        except:
            print("Issue with enumerating stock:", subject, "skipping...")

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

        if count % 10 == 0:
            print(count)

    print(main_df.sample(n=10))
    main_df.to_csv('sp500_joined_closes.csv')



#########################################
# M A I N   L O G I C
#########################################
#---------------------------------------#
# Variables
#---------------------------------------#
movAvg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
movAvg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
macd_periods_long_term = 26
macd_periods_short_term = 12
expMA_periods = 9 
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
compile_data()

