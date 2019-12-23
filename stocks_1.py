#! python3
import os
from formulas import *
from tools_scrape import *
try:
    from tools_get_company import *
except:
    print("#########################################")
    print("ERROR: unable to find tools_get_company.")
    print("       Web Sentiment Analysis using")
    print("       stock symbol and not company name!")
    print("#########################################")
#------------------------------------#
# This section will install python 
# modules needed to run this script
#------------------------------------#
try:
    import csv
except:
    os.system("pip3 install csv")
    import csv

import datetime as dt
from datetime import timedelta
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
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
try:
    import mpl_finance
except:
    os.system('pip3 install mpl_finance')
    import mpl_finance
from  mpl_finance import candlestick_ohlc
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
    import pandas_datareader.data as web
except:
    os.system("pip3 install pandas-datareader")
    import pandas_datareader.data as web
try:
    from pylab import *
except:
    os.system('pip install pylab')
    from pylab import *
try:
    import re
except:
    os.system("pip3 install re")
    import re
try:
    import getpass
except:
    os.system('pip install getpass')
    import getpass
import sys
try:
    from datetime import datetime, timedelta
except:
    os.system("pip3 install datetime")
    from datetime import datetime, timedelta
import time

style.use('fivethirtyeight')

plt.rcParams['axes.formatter.useoffset'] = False
########################################################
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
    a = np.convolve(values, weights, mode = 'full')[:len(values)]
    a[:window] = a[window]
    return a
#-------------------------------------------------------#
def calc_macd(x, slow=26, fast = 12):
#-------------------------------------------------------#
    eMaSlow = calc_ema(x, slow)
    eMaFast = calc_ema(x, fast)
    return eMaSlow, eMaFast, eMaFast - eMaSlow
#-------------------------------------------------------#
def rotate_xaxis(owner):
#-------------------------------------------------------#
    for label in owner.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_fontsize(6)
#-------------------------------------------------------#
def set_labels(owner):
#-------------------------------------------------------#
    #owner.set_xlabel('Dates', fontsize=8, fontweight =2, color = 'b')
    owner.set_ylabel('Price', fontsize=8, fontweight =5, color = 'g')
#-------------------------------------------------------#
def hide_frame(owner):
#-------------------------------------------------------#
    owner.grid(False)
    owner.xaxis.set_visible(False)
    owner.yaxis.set_visible(False)
    owner.set_xlabel(False)
#-------------------------------------------------------#
def set_spines(owner):
#-------------------------------------------------------#
    owner.spines['left'].set_color('m')
    owner.spines['left'].set_linewidth(1)
    owner.spines['right'].set_visible(False) #color('m')
    owner.spines['top'].set_color('m')
    owner.spines['top'].set_linewidth(1)
    owner.spines['bottom'].set_visible(False)
#######################################
# M A I N  L O G I C
#######################################

if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        if sys.argv[1]:
            print('len(sys.argv)=', len(sys.argv))
            ax1_subject = sys.argv[1]
        else:
            ax1_subject = 'JCP'
        if len(sys.argv[2]) > 0:
            ax2_sentiment_subject = sys.argv[2]
        else:
            ax2_sentiment_subject = 'EBAY'
    else:
        ax1_subject = 'JCP'
        ax2_sentiment_subject = 'EBAY'

user = getpass.getuser()
movAvg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
movAvg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
macd_periods_long_term = 26
macd_periods_short_term = 12
expMA_periods = 9 
#-----------------------------------#
# Variables
#-----------------------------------#
provider = 'yahoo' 
currPath = os.getcwd()              # Directory you are in NOW
savePath = 'askew'                  # We will be creating this new sub-directory
myPath = (currPath + '/' + savePath)# The full path of the new sub-dir
#-----------------------------------#
# Grab Dates
#-----------------------------------#
start = ( dt.datetime.now() - dt.timedelta(days = 365) )       # Format is year, month, day
end = dt.datetime.today()           # format of today() = [yyyy, mm, dd] - list of integers
#-----------------------------------#
# Set up place to save spreadsheet
#-----------------------------------#
if not os.path.exists(myPath):      # The directory you are in NOW
    os.makedirs(myPath)             # create a new dir below the dir your are in NOW
os.chdir(myPath)                    # move into the newly created sub-dir

for subject in ax1_subject:#:
    saveFile=(subject + '.csv')    # The RESUlTS we are saving on a daily basis
    if os.path.exists(saveFile):
        st = os.stat(saveFile)
        if dt.date.fromtimestamp(st.st_mtime) != dt.date.today():
            df = web.DataReader(subject, provider, start, end)
            df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
            df['MA10'] = df['Adj_Close'].rolling(10).mean()
            df['MA30'] = df['Adj_Close'].rolling(30).mean()
            df.to_csv(saveFile)
    else:
        df = web.DataReader(subject, provider, start, end)
        df.rename(columns={"Adj Close":'Adj_Close'}, inplace=True)
        df['MA10'] = df['Adj_Close'].rolling(10).mean()
        df['MA30'] = df['Adj_Close'].rolling(30).mean()
        df.to_csv(saveFile)#, columns = header)
             #Lose the date index so we can address it as a column

    
                 # Company providing the raw data we are after


########################################################
## Let's define our canvas, before we go after the data
## Odd numbers (ex. ax1_vol) are for stock 1. Even = stock 2.
#########################################################
plot_row = 18 + 122 #98
plot_col = 18
fig, axs = plt.subplots(figsize=(20,8), facecolor='#FFFFFA', sharex = True, sharey = True) #Too Bad, I really liked this color, facecolor = '#FFFFFA')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))

ax1_year = plt.subplot2grid((plot_row,plot_col), (0,0),  rowspan = 10, colspan = 4)
ax1_ohlc = plt.subplot2grid((plot_row,plot_col), (21,0), rowspan = 10, colspan = 4, sharex = ax1_year, sharey = ax1_year)
ax1_ma   = plt.subplot2grid((plot_row,plot_col), (42,0), rowspan = 10, colspan = 4, sharex = ax1_year, sharey = ax1_year)
ax1_rsi  = plt.subplot2grid((plot_row,plot_col), (64,0), rowspan = 10, colspan = 4, sharex = ax1_year)
ax1_macd = plt.subplot2grid((plot_row,plot_col), (86,0), rowspan = 10, colspan = 4, sharex = ax1_year)
ax1_vol  = plt.subplot2grid((plot_row,plot_col), (109,0), rowspan = 10, colspan = 4, sharex = ax1_year)
ax1_tot  = plt.subplot2grid((plot_row,plot_col), (134,0), rowspan = 10, colspan = 2)

ax_a    = plt.subplot2grid((plot_row,plot_col), (0,6),   rowspan = 12, colspan = 5)
ax_b    = plt.subplot2grid((plot_row,plot_col), (12,6),  rowspan = 83, colspan = 5)
ax_c    = plt.subplot2grid((plot_row,plot_col), (95,6),  rowspan = 20, colspan = 5)
ax_d    = plt.subplot2grid((plot_row,plot_col), (115,6), rowspan = 40, colspan = 5)

ax2_sentiment = plt.subplot2grid((plot_row,plot_col), (0,12),  rowspan = 30, colspan = 4)
ax2_sentiment_plots = plt.subplot2grid((plot_row,plot_col), (50,12),  rowspan = 40, colspan = 4)
#ax2_sentiment_score = plt.subplot2grid((plot_row,plot_col), (42,12), rowspan = 10, colspan = 4)
#ax2_subjectivity_score = plt.subplot2grid((plot_row,plot_col), (60,12), rowspan = 10, colspan = 4)
# ax_predict_ohlc = plt.subplot2grid((plot_row,plot_col), (21,12), rowspan = 10, colspan = 4, sharex = ax2_sentiment, sharey = ax2_sentiment)
# ax_predict_ma   = plt.subplot2grid((plot_row,plot_col), (42,12), rowspan = 10, colspan = 4, sharex = ax2_sentiment, sharey = ax2_sentiment)
# ax_predict_rsi  = plt.subplot2grid((plot_row,plot_col), (64,12), rowspan = 10, colspan = 4, sharex = ax2_sentiment)
# ax_predict_macd = plt.subplot2grid((plot_row,plot_col), (86,12), rowspan = 10, colspan = 4, sharex = ax2_sentiment)
# ax_predict_vol  = plt.subplot2grid((plot_row,plot_col), (109,12),rowspan = 10, colspan = 4, sharex = ax2_sentiment)
# ax_predict_tot  = plt.subplot2grid((plot_row,plot_col), (134,12),rowspan = 10, colspan = 2)
########################################################
#      ####  #####    ###     ###  #   #      # 
#     #        #     #   #   #     #  #      ##
#       #      #     #   #   #     # #      # #
#         #    #     #   #   #     #  #       #
#         #    #     #   #   #     #   #      #
#      ###     #      ###     ###  #    #   #####
########################################################
# Populate Data
########################################################
df = pd.read_csv((ax1_subject + '.csv'), parse_dates=True, index_col =0)

df_ohlc = df['Adj_Close'].resample('10D').ohlc()

#FUTURE df_last = (len(df_ohlc) -1)
#FUTURE df_start = int(round((df_last)/2) * 1.5)
#FUTURE df_ohlc= df_ohlc[df_start:df_last]
df.reset_index(inplace = True)      
########################################################
#Define DATA and attributes
########################################################
stock_entry = (df['Adj_Close'][0])               # Set marker of last years close.
movAvg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
movAvg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
macd_periods_long_term = 26
macd_periods_short_term = 12
expMA_periods = 9 
df.reset_index(inplace = True) 
                  #Lose the date index so we can address it as a column
#df_ohlc = df[["Date", "Open", "High", "Low", "Close"]]


ax1_subject_future_date = []
#df['MA10'] = moving_average(df['Adj_Close'], movAvg_window_days_short_term)
#print(random(df))
ma1 = moving_average(df['Adj_Close'], movAvg_window_days_short_term)
ma2 = moving_average(df['Adj_Close'], movAvg_window_days_long_term)
start = len(df['Date'][movAvg_window_days_long_term - 1:])
########################################################
#Start Plotting
########################################################
ax1_year.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'blue', linewidth = 1)
ax1_year.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'k', alpha = 0.9)
ax1_year.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)
ax1_year.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='g', alpha=0.6)
ax1_year.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='r', alpha=0.6)
rotate_xaxis(ax1_year)
ax1_year.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
set_spines(ax1_year)
ax1_year.tick_params(axis = 'x', colors = '#890b86')
ax1_year.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax1_year.set_title(ax1_subject, color = '#353335', size = 10)
set_labels(ax1_year)
ax1_year.set_color = '#890b86'
ax1_year.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')

rotate_xaxis(ax1_ma)
ax1_ma.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] > ma2[-start:]), facecolor='g', alpha=0.6)
ax1_ma.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] < ma2[-start:]), facecolor='red', alpha=0.6)
ax1_ma.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
ax1_ma.plot(df['Date'][- start:], ma1[- start:], color = 'b', linewidth = 1)     #Have to skip date ahead 10days (movAvg_window_days_short_term)
ax1_ma.plot(df['Date'][- start:], ma2[- start:], color = 'k', linewidth = 1 )      #Have to skip date ahead 30 days (movAvg_window_days_long_term)
set_spines(ax1_ma)
ax1_ma.tick_params(axis = 'x', colors = '#890b86')
ax1_ma.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax1_ma.plot([],[], linewidth = 2, label = '10d mov. avg.' , color = 'b', alpha = 0.9)
ax1_ma.plot([],[], linewidth = 2, label = '30d mov. avg.' , color = 'k', alpha = 0.9)
ax1_ma.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')
#set_labels(ax1_ma)
ax1_ma.set_ylabel('Moving Average', fontsize=8, fontweight =5, color = 'r')
##
### ax1_rsi
##
rsi = calc_rsi(df["Close"])
rotate_xaxis(ax1_rsi)
set_spines(ax1_rsi)
ax1_rsi.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax1_rsi.set_ylabel('RSI', fontsize=8, fontweight =5, color = 'darkorange')
rsi_col_over= 'red'
rsi_col_under = 'lightgreen'
ax1_rsi.plot(df['Date'],rsi, linewidth =1, color = 'orange')
ax1_rsi.axhline(30, color=rsi_col_under, linewidth = 1)
ax1_rsi.axhline(70, color=rsi_col_over, linewidth = 1)
ax1_rsi.set_yticks([30,70])
ax1_rsi.fill_between(df['Date'], rsi, 70, where = (rsi > 70), facecolor='r', alpha=0.6)
ax1_rsi.fill_between(df['Date'], rsi, 30, where = (rsi < 30), facecolor='darkgreen', alpha=0.6)
ax1_rsi.tick_params(axis = 'x', colors = '#890b86')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
ax1_rsi.plot([],[], linewidth = 2, label = 'OverVal' , color = 'red', alpha = 0.9)
ax1_rsi.plot([],[], linewidth = 2, label = 'UnderVal' , color = 'darkgreen', alpha = 0.9)
ax1_rsi.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 2, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

eMaSlow, eMaFast, macd = calc_macd(df['Close'])
ema9 = calc_ema(macd, expMA_periods)
macd_col_over = 'red'
macd_col_under = 'lightgreen'
rotate_xaxis(ax1_macd)
set_spines(ax1_macd)
ax1_macd.plot(df['Date'], macd, linewidth =2, color = 'darkred')
ax1_macd.plot(df['Date'], ema9, linewidth =1, color = 'blue')
ax1_macd.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = 'darkgreen', where = (macd - ema9 > 0))
ax1_macd.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = macd_col_over, where = (macd - ema9 < 0))
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax1_macd.tick_params(axis = 'x', colors = '#890b86')
ax1_macd.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax1_macd.set_ylabel('MACD', fontsize=8, fontweight =5, color = 'darkred')

ax1_macd.plot([], label='macd ' + str(macd_periods_short_term)  + ',' + str(macd_periods_long_term) + ',' + str(expMA_periods), linewidth = 2, color = 'darkred')
ax1_macd.plot([], label='ema ' + str(expMA_periods),  linewidth = 2, color = 'blue')
ax1_macd.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize = 6.0)



### ax1_vol
##
ax1_vol.tick_params(axis = 'x', colors = '#890b86')
ax1_vol.plot_date(df['Date'], df['Volume'], '-', label='Volume', color = 'blue', linewidth = 1)
ax1_vol.tick_params(axis = 'y', colors = 'k', labelsize = 6)
rotate_xaxis(ax1_vol)
set_spines(ax1_vol)
ax1_vol.set_ylim(df['Volume'].min(),df['Volume'].max())
ax1_vol.set_ylabel('Volume', fontsize=8, fontweight =5, color = 'b')
ax1_vol.fill_between(df['Date'],df['Volume'], facecolor='#00ffe8', alpha=.5)


last_rec = (len(df) -1)
#ax1_tot.text(0,-2.1,str(df.iloc[last_rec]), fontsize=9, fontweight = 20)\
last_open = df['Open'].iloc[-1]
last_high = df['High'].iloc[-1]
last_low  = df['Low'].iloc[-1]
last_vol  = df['Volume'].iloc[-1]
last_close = df['Close'].iloc[-1]
hide_frame(ax1_tot)
ax1_tot.text(1,1,'Open:' + '{:20,.2f}'.format(last_open) + '     ', verticalalignment='bottom', horizontalalignment='left',
         color='darkblue', fontsize=8)

ax1_tot.text(1,1,'Close:' + '{:20,.2f}'.format(last_close), verticalalignment='top', horizontalalignment='left',
         color='darkblue', fontsize=8)
ax1_tot.text(1,1,'High:' + '{:20,.2f}'.format(last_high) + '     ', verticalalignment='bottom', horizontalalignment='right',
         color='darkblue', fontsize=8)
ax1_tot.text(1,1,'Low:' + '{:20,.2f}'.format(last_low)+ '     ', verticalalignment='top', horizontalalignment='right',
         color='darkblue', fontsize=8)
ax1_tot.text(0.5,0.25, "Diff:" + str('{:5,.2f}'.format(last_high - last_low)), verticalalignment='bottom', horizontalalignment='left',
         color='darkblue', fontsize=8)
ax1_tot.text(0.5,0.25,"                                    Diff:" + str('{:5,.2f}'.format(last_close - last_open)), verticalalignment='bottom', horizontalalignment='left',
         color='darkblue', fontsize=8)




ax1_macd.axvline(x = df['Date'][int(len(df['Date'])/2)], linewidth = 1,  color = 'yellow')


##
### Extract what is needed for candlestick_ohlc AND
###    Every 10 days take and average
###  candlestick_ohlc expects: date, high low, close as inputs
##
### Drop index to set up mdates to replace date 
###  needed by candelstick_ohlc - does not use std. date fmt.
##
#df_ohlc = formulaz.heikenashi(df_ohlc)
df_ohlc.reset_index(inplace=True)                #Date becomes addressable column
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) #Date is now in ohlc format
df_ohlc.set_index(df_ohlc['Date'])
candlestick_ohlc(ax1_ohlc, df_ohlc.values, width = 1, colorup = 'g')
rotate_xaxis(ax1_ohlc)
set_labels(ax1_ohlc)
set_spines(ax1_ohlc)
ax1_ohlc.tick_params(axis = 'x', colors = '#890b86')
ax1_ohlc.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax1_ohlc.set_ylabel('OHLC', fontsize=8, fontweight =5, color = 'darkgreen')
ax1_ohlc.plot([],[], linewidth = 2, label = 'Up' , color = 'green', alpha = 0.9)
ax1_ohlc.plot([],[], linewidth = 2, label = 'Down' , color = 'red', alpha = 0.9)
ax1_ohlc.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')


rsi = calc_rsi(df["Close"])
rotate_xaxis(ax_a)
set_spines(ax_a)
ax_a.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax_a.set_ylabel('RSI', fontsize=8, fontweight =5, color = 'darkorange')
rsi_col_over= 'red'
rsi_col_under = 'lightgreen'
ax_a.plot(df['Date'],rsi, linewidth =1, color = 'orange')
ax_a.axhline(30, color=rsi_col_under, linewidth = 1)
ax_a.axhline(70, color=rsi_col_over, linewidth = 1)
ax_a.set_yticks([30,70])
ax_a.fill_between(df['Date'], rsi, 70, where = (rsi > 70), facecolor='r', alpha=0.6)
ax_a.fill_between(df['Date'], rsi, 30, where = (rsi < 30), facecolor='darkgreen', alpha=0.6)
ax_a.tick_params(axis = 'x', colors = '#890b86')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
ax_a.grid(True, color='lightgray', linestyle = '-', linewidth=2)
ax_a.plot([],[], linewidth = 2, label = 'OverVal' , color = 'red', alpha = 0.9)
ax_a.plot([],[], linewidth = 2, label = 'UnderVal' , color = 'darkgreen', alpha = 0.9)
ax_a.legend(fontsize = 6, fancybox = True, loc = 2, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')



ax_b.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'lightblue', linewidth = 1)
ax_b.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'gray', alpha = 0.9)
ax_b.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)
ax_b.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='lightgreen', alpha=0.6)
ax_b.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='pink', alpha=0.6)
rotate_xaxis(ax_b)
ax_b.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
set_spines(ax_b)
ax_b.tick_params(axis = 'x', colors = '#890b86')
ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 0)
#
#
#ax_b.set_title(ax1_subject, color = '#353335', size = 10)
#
set_labels(ax_b)
ax_b.set_color = '#890b86'
ax_b.legend(fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')

rotate_xaxis(ax_b)
ax_b.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] > ma2[-start:]), facecolor='darkgreen', alpha=0.6)
ax_b.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] < ma2[-start:]), facecolor='darkred', alpha=0.6)
ax_b.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
ax_b.plot(df['Date'][- start:], ma1[- start:], color = 'b', linewidth = 1)     #Have to skip date ahead 10days (movAvg_window_days_short_term)
ax_b.plot(df['Date'][- start:], ma2[- start:], color = 'k', linewidth = 1 )      #Have to skip date ahead 30 days (movAvg_window_days_long_term)
set_spines(ax1_ma)
ax_b.tick_params(axis = 'x', colors = '#890b86')
ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax_b.plot([],[], linewidth = 2, label = '10d mov. avg.' , color = 'darkblue', alpha = 0.9)
ax_b.plot([],[], linewidth = 2, label = '30d mov. avg.' , color = 'k', alpha = 0.9)
ax_b.legend(fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')
#set_labels(ax1_ma)
ax_b.set_ylabel( ax1_subject + ' Price and Composite ', fontsize=8, fontweight =5, color = 'r')

candlestick_ohlc(ax_b, df_ohlc.values, width = 1, colorup = 'g')
rotate_xaxis(ax_b)
set_labels(ax_b)
set_spines(ax_b)
ax_b.tick_params(axis = 'x', colors = '#890b86')
ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax_b.set_ylabel('OHLC', fontsize=8, fontweight =5, color = 'darkgreen')
ax_b.plot([],[], linewidth = 2, label = 'Up' , color = 'green', alpha = 0.9)
ax_b.plot([],[], linewidth = 2, label = 'Down' , color = 'red', alpha = 0.9)
ax_b.legend(fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

rotate_xaxis(ax_c)
set_spines(ax_c)
ax_c.plot(df['Date'], macd, linewidth =2, color = 'darkred')
ax_c.plot(df['Date'], ema9, linewidth =1, color = 'blue')
ax_c.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = 'darkgreen', where = (macd - ema9 > 0))
ax_c.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = macd_col_over, where = (macd - ema9 < 0))
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax_c.tick_params(axis = 'x', colors = '#890b86')
ax_c.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax_c.set_ylabel('MACD', fontsize=8, fontweight =5, color = 'darkred')

ax_c.plot([], label='macd ' + str(macd_periods_short_term)  + ',' + str(macd_periods_long_term) + ',' + str(expMA_periods), linewidth = 2, color = 'darkred')
ax_c.plot([], label='ema ' + str(expMA_periods),  linewidth = 2, color = 'blue')
ax_c.legend(loc=2, borderaxespad=0., fontsize = 6.0)



#ax_d = ax_b.twinx()
ax_d.tick_params(axis = 'x', colors = '#890b86')
ax_d.plot_date(df['Date'], df['Volume'], '-', label='Volume', color = 'blue', linewidth = 1)
ax_d.tick_params(axis = 'y', colors = 'k', labelsize = 6)
rotate_xaxis(ax_d)
set_spines(ax_d)
ax_d.set_ylim(df['Volume'].min(),df['Volume'].max())
ax_d.set_ylabel('Volume', fontsize=8, fontweight =5, color = 'b')
ax_d.fill_between(df['Date'],df['Volume'], facecolor='#00ffe8', alpha=.5)

#######################################
# S T A R T   S E N T I M E N T   A N.#
#                                     #
#######################################
a = Analysis(ax1_subject)
sentiment, subjectivity, plots  = a.run()
print(ax1_subject, '\tsubjectivity', str(a.subjectivity) + '\n', '\t\tsentiment' + ' -1 < ', a.sentiment, '< 1')
##
### Convert list of dictionaries to a DataFrame
##
df_plot = pd.DataFrame()
##
### Map the returned list of dictionary entries
###     to a set we can plot
##
x = 0  
y = 0
x_plot_list = []
y_plot_list = []
for dict_plot in plots: # Per Doctor Rob, PhD, leave in the zeros
    # if ( dict_plot['sentiment'] == 0.0 ) & ( dict_plot['subjectivity'] == 0.0 ):
    #     continue
    x = dict_plot['sentiment'] #* 100
    y = dict_plot['subjectivity'] #* 100
    x_plot_list.append(x)
    y_plot_list.append(y)
df_plot['sentiment'] = x_plot_list
df_plot['subjectivity'] = y_plot_list

ax2_sentiment.plot(sentiment, subjectivity, '*', label='Sentiment Points', color = 'red', linewidth = 1)
set_spines(ax2_sentiment)
rotate_xaxis(ax2_sentiment)
ax2_sentiment.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
ax2_sentiment.set_xlim(-1, 1)
ax2_sentiment.set_ylim(0, 1)
ax2_sentiment.tick_params(axis = 'x', colors = '#890b86', labelsize = 6)
ax2_sentiment.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax2_sentiment.set_title("(neg) <-- " + ax1_subject + " Composite Sentiment Score --> (pos)", color = '#353335', size = 10)
ax2_sentiment.set_ylabel('Subjectivity', fontsize=8, fontweight =5, color = '#890b86')
ax2_sentiment.axhline(0, color = 'k', linewidth = 2, label = '0.0 = Neutral')
ax2_sentiment.plot([],[], linewidth = 2, label = 'Sentiment: ' + str(sentiment) , color = 'red', alpha = 0.9)
ax2_sentiment.plot([],[], linewidth = 2, label = 'Subjectivity: ' + str(subjectivity) , color = 'red', alpha = 0.9)
ax2_sentiment.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')


ax2_sentiment_plots.plot(df_plot['sentiment'], df_plot['subjectivity'], '*', color = 'blue')
ax2_sentiment_plots.plot([],[], linewidth = 2, label = 'Neutral' , color = 'k', alpha = 0.9)
ax2_sentiment_plots.axhline(0, color = 'yellow', linewidth = 1)
rotate_xaxis(ax2_sentiment_plots)
set_spines(ax2_sentiment_plots)
ax2_sentiment_plots.axvline(x = 0, linewidth = 1,  color = 'yellow')
#ax2_sentiment_plots.set_ylim(0, 1)
ax2_sentiment_plots.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
ax2_sentiment_plots.tick_params(axis = 'x', colors = '#890b86', labelsize = 6)
ax2_sentiment_plots.tick_params(axis = 'y', colors = 'g', labelsize = 6)
ax2_sentiment_plots.set_title("(neg) <-- " + ax1_subject + " Individual Sentiment Scores --> (pos)", color = '#353335', size = 10)
ax2_sentiment_plots.set_ylabel('Subjectivity', fontsize=8, fontweight =5, color = '#890b86')




#ax2_sentiment.plot(df_plot['sentiment'], df_plot['subjectivity'], '*', label='Sentiment Points', color = 'blue', linewidth = 1)

#ax2_sentiment.plot(sentiment, subjectivity, '-', label='Sentiment', color = 'red', linewidth = 2)


# ax2_sentiment.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='g', alpha=0.6)
# ax2_sentiment.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='r', alpha=0.6)
# #rotate_xaxis(ax2_sentiment)

# set_labels(ax2_sentiment)
####ax2_sentiment.set_color = '#890b86'
# ax2_sentiment.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')

# candlestick_ohlc(ax_predict_ohlc, df_ohlc.values, width = 1, colorup = 'g')
# rotate_xaxis(ax_predict_ohlc)
# set_labels(ax_predict_ohlc)
# set_spines(ax_predict_ohlc)
# ax_predict_ohlc.tick_params(axis = 'x', colors = '#890b86')
# ax_predict_ohlc.tick_params(axis = 'y', colors = 'g', labelsize = 6)
# ax_predict_ohlc.set_ylabel('OHLC', fontsize=8, fontweight =5, color = 'darkgreen')
# ax_predict_ohlc.plot([],[], linewidth = 2, label = 'Up' , color = 'green', alpha = 0.9)
# ax_predict_ohlc.plot([],[], linewidth = 2, label = 'Down' , color = 'red', alpha = 0.9)
# ax_predict_ohlc.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

# rotate_xaxis(ax_predict_ma)
# ax_predict_ma.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] > ma2[-start:]), facecolor='g', alpha=0.6)
# ax_predict_ma.fill_between(df['Date'][- start:], ma1[-start:], ma2[-start:], where = (ma1[-start:] < ma2[-start:]), facecolor='red', alpha=0.6)
# ax_predict_ma.grid(True, color='lightgreen', linestyle = '-', linewidth=2)
# ax_predict_ma.plot(df['Date'][- start:], ma1[- start:], color = 'b', linewidth = 1)     #Have to skip date ahead 10days (movAvg_window_days_short_term)
# ax_predict_ma.plot(df['Date'][- start:], ma2[- start:], color = 'k', linewidth = 1 )      #Have to skip date ahead 30 days (movAvg_window_days_long_term)
# set_spines(ax_predict_ma)
# ax_predict_ma.tick_params(axis = 'x', colors = '#890b86')
# ax_predict_ma.tick_params(axis = 'y', colors = 'g', labelsize = 6)
# ax_predict_ma.plot([],[], linewidth = 2, label = '10d mov. avg.' , color = 'b', alpha = 0.9)
# ax_predict_ma.plot([],[], linewidth = 2, label = '30d mov. avg.' , color = 'k', alpha = 0.9)
# ax_predict_ma.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')
# #set_labels(ax_predict_ma)
# ax_predict_ma.set_ylabel('Moving Average', fontsize=8, fontweight =5, color = 'r')

# ##
# ### ax_predict_rsi
# ##
# rsi = calc_rsi(df["Close"])
# rotate_xaxis(ax_predict_rsi)
# set_spines(ax_predict_rsi)
# ax_predict_rsi.tick_params(axis = 'y', colors = 'g', labelsize = 6)
# ax_predict_rsi.set_ylabel('RSI', fontsize=8, fontweight =5, color = 'darkorange')
# rsi_col_over= 'red'
# rsi_col_under = 'lightgreen'
# ax_predict_rsi.plot(df['Date'],rsi, linewidth =1, color = 'orange')
# ax_predict_rsi.axhline(30, color=rsi_col_under, linewidth = 1)
# ax_predict_rsi.axhline(70, color=rsi_col_over, linewidth = 1)
# ax_predict_rsi.set_yticks([30,70])
# ax_predict_rsi.fill_between(df['Date'], rsi, 70, where = (rsi > 70), facecolor='r', alpha=0.6)
# ax_predict_rsi.fill_between(df['Date'], rsi, 30, where = (rsi < 30), facecolor='darkgreen', alpha=0.6)
# ax_predict_rsi.plot([],[], linewidth = 2, label = 'OverVal' , color = 'red', alpha = 0.9)
# ax_predict_rsi.plot([],[], linewidth = 2, label = 'UnderVal' , color = 'darkgreen', alpha = 0.9)
# ax_predict_rsi.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 2, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')


# eMaSlow, eMaFast, macd = calc_macd(df['Close'])
# ema9 = calc_ema(macd, expMA_periods)
# macd_col_over = 'red'
# macd_col_under = 'lightgreen'
# rotate_xaxis(ax_predict_macd)
# set_spines(ax_predict_macd)
# ax_predict_macd.plot(df['Date'], macd, linewidth =2, color = 'darkred')
# ax_predict_macd.plot(df['Date'], ema9, linewidth =1, color = 'blue')
# ax_predict_macd.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = 'darkgreen', where = (macd - ema9 > 0))
# ax_predict_macd.fill_between(df['Date'], macd - ema9, 0, alpha = 0.5, facecolor = macd_col_over, where = (macd - ema9 < 0))
# plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
# ax_predict_macd.tick_params(axis = 'x', colors = '#890b86')
# ax_predict_macd.tick_params(axis = 'y', colors = 'g', labelsize = 6)
# ax_predict_macd.set_ylabel('MACD', fontsize=8, fontweight =5, color = 'darkred')

# ax_predict_macd.plot([], label='macd ' + str(macd_periods_short_term)  + ',' + str(macd_periods_long_term) + ',' + str(expMA_periods), linewidth = 2, color = 'darkred')
# ax_predict_macd.plot([], label='ema ' + str(expMA_periods),  linewidth = 2, color = 'blue')
# ax_predict_macd.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize = 6.0)



# ax_predict_vol.tick_params(axis = 'x', colors = '#890b86')

# ax_predict_vol.plot_date(df['Date'], df['Volume'], '-', label='Volume', color = 'blue', linewidth = 1)
# ax_predict_vol.set_ylim( df['Volume'].min(),df['Volume'].max())
# rotate_xaxis(ax_predict_vol)
# set_spines(ax_predict_vol)
# ax_predict_vol.set_ylabel('Volume', fontsize=8, fontweight =5, color = 'b')
# ax_predict_vol.tick_params(axis = 'y', colors = 'k', labelsize = 6)
# ax_predict_vol.fill_between(df['Date'],df['Volume'], facecolor='#00ffe8', alpha=.5)

# last_rec = (len(df) -1)
# #ax1_tot.text(0,-2.1,str(df.iloc[last_rec]), fontsize=9, fontweight = 20)\
# last_open = df['Open'].iloc[-1]
# last_high = df['High'].iloc[-1]
# last_low  = df['Low'].iloc[-1]
# last_vol  = df['Volume'].iloc[-1]
# last_close = df['Close'].iloc[-1]
# hide_frame(ax_predict_tot)
# ax_predict_tot.text(1,1,'Open:' + '{:20,.2f}'.format(last_open) + '     ', verticalalignment='bottom', horizontalalignment='left',
#          color='darkblue', fontsize=8)

# ax_predict_tot.text(1,1,'Close:' + '{:20,.2f}'.format(last_close), verticalalignment='top', horizontalalignment='left',
#          color='darkblue', fontsize=8)
# ax_predict_tot.text(1,1,'High:' + '{:20,.2f}'.format(last_high) + '     ', verticalalignment='bottom', horizontalalignment='right',
#          color='darkblue', fontsize=8)
# ax_predict_tot.text(1,1,'Low:' + '{:20,.2f}'.format(last_low)+ '     ', verticalalignment='top', horizontalalignment='right',
#          color='darkblue', fontsize=8)
# ax_predict_tot.text(0.5,0.25, "Diff:" + str('{:5,.2f}'.format(last_high - last_low)), verticalalignment='bottom', horizontalalignment='left',
#          color='darkblue', fontsize=8)
# ax_predict_tot.text(0.5,0.25,"                                    Diff:" + str('{:5,.2f}'.format(last_close - last_open)), verticalalignment='bottom', horizontalalignment='left',
#          color='darkblue', fontsize=8)


plt.rc('ytick', labelsize=6 )    # fontsize of the tick labels
plt.subplots_adjust(left = 0.10, bottom = 0.16, right = 0.920, top = 0.93, wspace = 0.2, hspace = -.1)
fig = gcf()
my_title = (user, "Stock Page")
fig.suptitle(user + " Stock Page", fontsize=14)
plt.show()
fig.savefig(ax1_subject + '.png')
