#! python3
''' Modified the SentDex stock graphing solution found on YouTube. Context
included the series on graphing a Stock, buidling an S&P 500 heatmap, 
Tkinter UI series for Bitcoin:

https://www.pythonprogramming.net/
http://www.sentdex.com/

Added GUI, Configuration (ini), Sentiment Analysis and Similar stocks.
Additional software written by John "Bucbowie" Askew. I take full 
responsibility for any bugs or design flaws and by no means is 
meant to represent the brand "SentDex", nor https://www.pythonprogramming.net/.

TTTTTTTTTT         D D
    TT             D   D
    TT             D     D
    TT  ooooo  --  D     D  ooooo
    TT  o   o      D   D    o   o
    TT  00000      D D      ooooo

1. Add compamy name and information at top of presentation

2. Add Percent Change chart - if there is value (let user determine denomintor
)
3. Yellow buy bands for RSI score < 30%.

4. Convert OHLC to Heiken Ashi OHLC (See Formulaz)


'''
import os

try:
    from tools_parse_config import ParseConfig
except:
    msg = "Unable to find config file. Using defaults"
    
    print(msg)
    
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

from formulas import *

from tools_scrape import *

from tools_get_stock_corr import corr

try:
    from tools_get_company import *

except:
    print("#########################################")
    
    print("ERROR: unable to find tools_get_company.")
    
    print("       Web Sentiment Analysis using")
    
    print("       stock symbol and not company name!")
    
    print("#########################################")

try:
    
    from tools_scrape_profile import *

except:
    
    print("#########################################")
    
    print("ERROR: unable to find tools_scrape_profile.")
    
    print("    using stock symbol and no company info!")
    
    print("#########################################")

try:
    
    from stocks_alt_info import altAnalysis

except Exception as e:

    print("Unable to access python module stocks_alt_info. Skipping financial details and continuing on...")

    print(e)

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

from mpl_toolkits.mplot3d import Axes3D

from matplotlib.widgets import Button

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

try:

    import subprocess

except:

    os.system("pip install subprocess")

    import subprocess

import sys

try:

    from datetime import datetime, timedelta

except:

    os.system("pip3 install datetime")

    from datetime import datetime, timedelta

import time

from pandas.plotting import register_matplotlib_converters

import json

import pprint

style.use('fivethirtyeight')

plt.rcParams['axes.formatter.useoffset'] = False

pd.plotting.register_matplotlib_converters()

stock_date_adj = int(0)

a = ParseConfig()

movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold, pct_chg, boll, boll_window_days, boll_weight, fib = a.run()
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

########################################################
# Functions (before Main Logic)
########################################################

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

#-------------------------------------------------------#
def rotate_xaxis(owner):
#-------------------------------------------------------#
    for label in owner.xaxis.get_ticklabels():
    
        label.set_rotation(45)
    
        label.set_fontsize(5.5)

#-------------------------------------------------------#
def set_labels(owner):
#-------------------------------------------------------#
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
# H O U S K E E P I N G
#######################################

if __name__ == '__main__':

    if len(sys.argv) > 2:

        stock_date_adj = sys.argv[2]

    else:
    
        stock_date_adj = int(365)
    

    if len(sys.argv) > 1:
        
        if sys.argv[1]:
        
            ax1_subject = sys.argv[1]
        
            ax2_sent_subject = ax1_subject
        
        else:
        
            ax1_subject = 'JCP'
        
            ax2_sent_subject = ax1_subject
    else:
        
        ax1_subject = 'JCP'
        
        ax2_sent_subject = ax1_subject


#######################################
# M A I N  L O G I C 
#######################################
#-----------------------------------#
# Variables
#-----------------------------------#

user = getpass.getuser()

provider = 'yahoo' 

currPath = os.getcwd()              # Directory you are in NOW

savePath = 'askew'                  # We will be creating this new sub-directory

myPath = (currPath + '/' + savePath)# The full path of the new sub-dir

dir_path = os.path.dirname(os.path.realpath(__file__))

##
### Fibbonacci Retracements - which column to use.
###                           compare Close to Adj_Close.
## 
fibbonacci_column = 'Close'
bollinger_column = 'Close'


#-----------------------------------#
# Grab Dates
#-----------------------------------#

start = ( dt.datetime.now() - dt.timedelta(days = int(stock_date_adj)) )       # Format is year, month, day

end = dt.datetime.today()           # format of today() = [yyyy, mm, dd] - list of integers

#-----------------------------------#
# Call to get data - if exists and current, fine. 
#     if not, it will be scraped using
#     the stock symbols loaded at 
#     beginning of tools_build_datawarehouse.py
#-----------------------------------#

try:

    saveFile=(myPath + '/{}'.format(ax1_subject) + '.csv')    # The RESUlTS we are saving on a daily basis
    
    st = os.stat(saveFile)

   
    if os.path.exists(saveFile) and dt.date.fromtimestamp(st.st_mtime) != dt.date.today():
        
        try:
            
            subprocess.call(["python", dir_path + "/" + "tools_build_datawarehouse.py"])
            
        except:

            msg = ("Unable to rebuild:", ax1_subject, "Aborting. Either BAD ticker or python pgm tools_build_datawarehouse.py is NOT in same directory?")

            print(msg)

            sys.exit(0)

except:
    
    subprocess.call(["python", dir_path + "/" + "tools_build_datawarehouse.py"])

########################################################
## Let's define our canvas, before we go after the data
#########################################################
plot_row = 18 + 122 + 35 # On-going expansion. Sloppy...

plot_col = 20



fig , ax  = plt.subplots(figsize=(19,8), dpi=110,frameon=False, sharex = True, sharey = True) #Too Bad, I really liked this color, facecolor = '#FFFFFA')

plt.box(on = None)

plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))



ax1_year = plt.subplot2grid((plot_row,plot_col), (0,  0), rowspan = 10, colspan = 4)

ax1_ohlc = plt.subplot2grid((plot_row,plot_col), (23, 0), rowspan = 10, colspan = 4, sharex = ax1_year, sharey = ax1_year)

ax1_ma   = plt.subplot2grid((plot_row,plot_col), (47, 0), rowspan = 10, colspan = 4, sharex = ax1_year, sharey = ax1_year)

ax1_rsi  = plt.subplot2grid((plot_row,plot_col), (70, 0), rowspan = 10, colspan = 4, sharex = ax1_year)

ax1_macd = plt.subplot2grid((plot_row,plot_col), (94, 0), rowspan = 10, colspan = 4, sharex = ax1_year)

ax1_vol  = plt.subplot2grid((plot_row,plot_col), (121,0), rowspan = 10, colspan = 4, sharex = ax1_year)

ax1_vol.yaxis.set_major_formatter(FormatStrFormatter('%10d'))

ax1_tot  = plt.subplot2grid((plot_row,plot_col), (155,0), rowspan = 300, colspan = 3)

ax1_tot2 = plt.subplot2grid((plot_row,plot_col), (155,3), rowspan = 300, colspan = 3)

##
### ax_b comes first so other graphs can sharex with ax_b
##

ax_b    = plt.subplot2grid((plot_row,plot_col), (12, 6), rowspan = 83, colspan = 6)

ax_c    = plt.subplot2grid((plot_row,plot_col), (95, 6), rowspan = 20, colspan = 6, sharex = ax_b)

ax_d    = plt.subplot2grid((plot_row,plot_col), (136,6), rowspan = 40, colspan = 6, sharex = ax_b)

ax_e    = plt.subplot2grid((plot_row, plot_col), (115, 6), rowspan = 20, colspan = 6, sharex = ax_b)

ax_a    = plt.subplot2grid((plot_row,plot_col), (0,  6), rowspan = 12, colspan = 6, sharex = ax_b)


ax2_sent         = plt.subplot2grid((plot_row,plot_col), (0,  13), rowspan = 30, colspan = 3)

ax2_sent_plots   = plt.subplot2grid((plot_row,plot_col), (50, 13), rowspan = 40, colspan = 3)

ax_sent_chart = plt.subplot2grid((plot_row,plot_col), (110,13), rowspan = 60, colspan = 3)


ax3_sim_stock1 = plt.subplot2grid((plot_row, plot_col), (0,  17), rowspan = 30, colspan = 20)

ax3_sim_stock2 = plt.subplot2grid((plot_row, plot_col), (50 ,17), rowspan = 30, colspan = 20)

ax3_sim_stock3 = plt.subplot2grid((plot_row, plot_col), (110,17), rowspan = 30, colspan = 20)


ax3_sim_stock1.set_visible(False)

ax3_sim_stock2.set_visible(False)

ax3_sim_stock3.set_visible(False)

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
os.chdir(myPath)

try:

    df = pd.read_csv((ax1_subject + '.csv'), parse_dates=True, index_col =0)

except Exception as e:

    print("stocks_1.py did not find", ax1_subject, "information. As it's not in the datawarehouse, is the ticker symbol spelled correctly?")

    print(e)

    popupmsg("Symbol " + ax1_subject + " is not found! -- Spelling?")

    sys.exit(0)

try:

    a = altAnalysis(ax1_subject)

    company_json = a.run()

except Exception as e:

    print("Unable to extract Accounting details from program stock_alt_info.py. Skipping accounting details.")
    print(e)


'''Capture OHLC before resetting index'''

if int(stock_date_adj) >= 270:
    
    df_ohlc = df['Adj_Close'].resample('10D').ohlc()

elif int(stock_date_adj) >= 180 and int(stock_date_adj) < 270:
    
    df_ohlc = df['Adj_Close'].resample('7D').ohlc()

else:

    df_ohlc = df['Adj_Close'].resample('5D').ohlc()





df_ohlc.reset_index(inplace = True)

df_ohlc = df_ohlc[df_ohlc.Date > (dt.datetime.now() - dt.timedelta(days = int(stock_date_adj)))]  

df_ohlc.set_index('Date', inplace = True)


df.reset_index(inplace = True)    

df = df[df.Date > (dt.datetime.now() - dt.timedelta(days = int(stock_date_adj)))]  

df.set_index('Date', inplace = True)

  
########################################################
#Define DATA and attributes
########################################################
stock_entry = (df['Adj_Close'][0])               # Set marker of last years close.

df.reset_index(inplace = True) 

mA_Short = moving_average(df['Adj_Close'], movavg_window_days_short_term)

mA_Long = moving_average(df['Adj_Close'], movavg_window_days_long_term)

start = len(df['Date'][movavg_window_days_long_term - 1:])

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

ax1_ma.fill_between(df['Date'][- start:], mA_Short[-start:], mA_Long[-start:], where = (mA_Short[-start:] > mA_Long[-start:]), facecolor='g', alpha=0.6)

ax1_ma.fill_between(df['Date'][- start:], mA_Short[-start:], mA_Long[-start:], where = (mA_Short[-start:] < mA_Long[-start:]), facecolor='red', alpha=0.6)

ax1_ma.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

ax1_ma.plot(df['Date'][- start:], mA_Short[- start:], color = 'b', linewidth = 1)     #Have to skip date ahead 10days (movavg_window_days_short_term)

ax1_ma.plot(df['Date'][- start:], mA_Long[- start:], color = 'k', linewidth = 1 )      #Have to skip date ahead 30 days (movavg_window_days_long_term)

set_spines(ax1_ma)

ax1_ma.tick_params(axis = 'x', colors = '#890b86')

ax1_ma.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax1_ma.plot([],[], linewidth = 2, label = str(movavg_window_days_short_term)+'d mov. avg.' , color = 'b', alpha = 0.9)

ax1_ma.plot([],[], linewidth = 2, label = str(movavg_window_days_long_term) +'d mov. avg.' , color = 'k', alpha = 0.9)

ax1_ma.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

ax1_ma.set_ylabel('Mov.Avg.', fontsize=8, fontweight =5, color = 'r')

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

ax1_rsi.axhline(rsi_oversold, color=rsi_col_under, linewidth = 1)

ax1_rsi.axhline(rsi_overbought, color=rsi_col_over, linewidth = 1)

ax1_rsi.set_yticks([rsi_oversold,rsi_overbought])

ax1_rsi.fill_between(df['Date'], rsi, rsi_overbought, where = (rsi > rsi_overbought), facecolor='r', alpha=0.6)

ax1_rsi.fill_between(df['Date'], rsi, rsi_oversold, where = (rsi < rsi_oversold), facecolor='darkgreen', alpha=0.6)

ax1_rsi.tick_params(axis = 'x', colors = '#890b86')

plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))

ax1_rsi.plot([],[], linewidth = 2, label = 'OverVal' , color = 'red', alpha = 0.9)

ax1_rsi.plot([],[], linewidth = 2, label = 'UnderVal' , color = 'darkgreen', alpha = 0.9)

ax1_rsi.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 2, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')


eMaSlow, eMaFast, macd = calc_macd(df['Close'])

ema9 = calc_ema(macd, expma_periods)

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

ax1_macd.plot([], label='macd ' + str(macd_periods_short_term)  + ',' + str(macd_periods_long_term) + ',' + str(expma_periods), linewidth = 2, color = 'darkred')

ax1_macd.plot([], label='ema ' + str(expma_periods),  linewidth = 2, color = 'blue')

ax1_macd.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize = 6.0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')


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

autoAxis = plt.axis()

last_rec = (len(df) -1)

last_open = df['Open'].iloc[-1]

last_high = df['High'].iloc[-1]

last_low  = df['Low'].iloc[-1]

last_vol  = df['Volume'].iloc[-1]

last_close = df['Close'].iloc[-1]



#--------------------------------------#
# F I N A N C I A L   D E T A I L S
#   scrunched up to fit the frame
#--------------------------------------#
# a = altAnalysis(ax1_subject)

# company_json = a.run()

hide_frame(ax1_tot)

hide_frame(ax1_tot2)

#Askew rec = Rectangle((autoAxis[0]-0.1,autoAxis[2]-0.2),(autoAxis[1]-autoAxis[0])+1,(autoAxis[3]-autoAxis[2])+0.3,fill=False,lw=5, color = 'blue')
rec = Rectangle((autoAxis[0]-0.5,autoAxis[2]-0.2),(autoAxis[1]-autoAxis[0])+1,(autoAxis[3]-autoAxis[2])+0.3,fill=False,lw=5, color = 'blue')

rec = ax1_tot.add_patch(rec)

rec.set_clip_on(False)

other_DETAILS_List = []

col_cnt = 0

for sTOCK, value in company_json['OTHER_DETAILS'].items():

    other_DETAILS_List.append(sTOCK + " : " + str(value))

cnt_DETAILS = float(0.0)

cnt_DETAILS = 1.0

for i in sorted(other_DETAILS_List, reverse = True,):

    i = str(i)
    
    if col_cnt == 0:

        ax1_tot.text(-.25,cnt_DETAILS, i, verticalalignment='top', horizontalalignment='left', color='darkblue', fontsize=6)

        col_cnt = 1
    
    else:
    
        ax1_tot2.text(-.5,cnt_DETAILS, i, verticalalignment='top', horizontalalignment='left', color='darkblue', fontsize=6)
    
        col_cnt = 0
        
        cnt_DETAILS -= 0.150

ax1_tot.grid(color = 'white')

ax1_tot2.grid(color = 'lightgray')

os.remove(ax1_subject + '.data.json')

os.remove(ax1_subject + '.output_file.html')

'''
Extract what is needed for candlestick_ohlc AND
 Every 10 days take and average
  candlestick_ohlc expects: date, high low, close as inputs

Drop index to set up mdates to replace date 
  needed by candelstick_ohlc - does not use std. date fmt.
'''

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

##
### RSI
##

rsi = calc_rsi(df["Close"])

rotate_xaxis(ax_a)

set_spines(ax_a)

ax_a.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax_a.set_ylabel('RSI', fontsize=8, fontweight =5, color = 'darkorange')

rsi_col_over= 'red'

rsi_col_under = 'lightgreen'

ax_a.plot(df['Date'],rsi, linewidth =1, color = 'orange')

ax_a.axhline(rsi_oversold, color=rsi_col_under, linewidth = 1)

ax_a.axhline(rsi_overbought, color=rsi_col_over, linewidth = 1)

ax_a.set_yticks([rsi_oversold,rsi_overbought])

ax_a.fill_between(df['Date'], rsi, rsi_overbought, where = (rsi > rsi_overbought), facecolor='r', alpha=0.6)

ax_a.fill_between(df['Date'], rsi, rsi_oversold, where = (rsi < rsi_oversold), facecolor='darkgreen', alpha=0.6)

ax_a.tick_params(axis = 'x', colors = '#890b86')

plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))

ax_a.grid(True, color='lightgray', linestyle = '-', linewidth=2)

ax_a.plot([],[], linewidth = 2, label = 'OverVal' , color = 'red', alpha = 0.9)

ax_a.plot([],[], linewidth = 2, label = 'UnderVal' , color = 'darkgreen', alpha = 0.9)

ax_a.legend(fontsize = 6, fancybox = True, loc = 2, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

ax_a.get_xaxis().set_visible(False)

##------------------------------------#
### Main Chart - closing price, mov avg and fibbonnaci retracement bands
##------------------------------------#
fibb_ratio_lvl1 = .236

fibb_ratio_lvl2 = .382

fibb_ratio_lvl3 = .618

fibb_min  = float(df[fibbonacci_column].min())

fibb_max  = float(df[fibbonacci_column].max())

fibb_diff   = float(fibb_max - fibb_min)

fibb_lvl1   = float(df[fibbonacci_column].max() - ((fibb_ratio_lvl1) * fibb_diff))

fibb_lvl2   = float(df[fibbonacci_column].max() - ((fibb_ratio_lvl2) * fibb_diff))

fibb_lvl3   = float(df[fibbonacci_column].max() - ((fibb_ratio_lvl3) * fibb_diff))

start_boll = len(df['Date'][boll_window_days - 1:])

df['Close_STD']  = df[bollinger_column][- start_boll:].rolling(window = boll_window_days).std()

df['Close_SMA']  = df[bollinger_column][- start_boll:].rolling(window = boll_window_days).mean()

df['Boll_Upper'] = df['Close_SMA'] + (boll_weight * df['Close_STD'])

df['Boll_Lower'] = df['Close_SMA'] - (boll_weight * df['Close_STD'])

df['Boll_Mid']   = df['Close_SMA'] 

ax_b.set_facecolor('#FFFFFA')

ax_b.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'blue', alpha = 0.3, linewidth = 1)

ax_b.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'gray', alpha = 0.9)

ax_b.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)

ax_b.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='lightgreen', alpha=0.7)

ax_b.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='pink', alpha=0.7)

rotate_xaxis(ax_b)

ax_b.grid(True, linestyle = '-', linewidth=1, color='lightgray')

set_spines(ax_b)

ax_b.tick_params(axis = 'x', colors = '#890b86')

ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 0)

set_labels(ax_b)

ax_b.set_color = '#890b86'

ax_b.legend(fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')

rotate_xaxis(ax_b)

ax_b.fill_between(df['Date'][- start:], mA_Short[-start:], mA_Long[-start:], where = (mA_Short[-start:] > mA_Long[-start:]), facecolor='darkgreen', alpha=0.6)

ax_b.fill_between(df['Date'][- start:], mA_Short[-start:], mA_Long[-start:], where = (mA_Short[-start:] < mA_Long[-start:]), facecolor='darkred', alpha=0.6)

ax_b.plot(df['Date'][- start:], mA_Short[- start:], color = 'b', linewidth = 1)     #Have to skip date ahead 10days (movavg_window_days_short_term)

ax_b.plot(df['Date'][- start:], mA_Long[- start:], color = 'k', linewidth = 1 )      #Have to skip date ahead 30 days (movavg_window_days_long_term)

set_spines(ax_b)

ax_b.tick_params(axis = 'x', colors = '#890b86')

ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax_b.plot([],[], linewidth = 2, label = str(movavg_window_days_short_term)+'d mov. avg.' , color = 'darkblue', alpha = 0.9)

ax_b.plot([],[], linewidth = 2, label = str(movavg_window_days_long_term)+'d mov. avg.' , color = 'k', alpha = 0.9)

ax_b.plot([],[], linewidth = 2, label = 'original mov. avg. golden cross(buy)' , color = 'yellow', alpha = 0.9)

ax_b.legend(fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')

ax_b.set_ylabel( ax1_subject + ' Price and Composite ', fontsize=8, fontweight =5, color = 'r')

filter2 = df['MA10'] >  df['MA30']

filter3 = df['MA10'].shift(1) <= df['MA30'].shift(1)

start_xz = ( dt.datetime.now() - dt.timedelta(days = 365))

xz = df.where(filter2 & filter3).fillna(start_xz)

xz = xz['Date'].where(xz['Date'] > start_xz)

for i in xz.dropna():

    ax1_ma.axvline(i, linewidth = 1,  color = 'yellow')

    ax_b.axvline(i, linewidth = 1,  color = 'yellow')


candlestick_ohlc(ax_b, df_ohlc.values, width = 1, colorup = 'g')



rotate_xaxis(ax_b)

set_labels(ax_b)

set_spines(ax_b)

ax_b.tick_params(axis = 'x', colors = '#890b86')

ax_b.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax_b.set_ylabel('Composite: Adj Close, Mov Avg, OHLC and more ', fontsize=8, fontweight =5, color = 'darkgreen')

ax_b.plot([],[], linewidth = 2, label = 'Up' , color = 'green', alpha = 0.9)

ax_b.plot([],[], linewidth = 2, label = 'Down' , color = 'red', alpha = 0.9)



ax_b.get_xaxis().set_visible(False)

if boll.upper() == 'Y':

    ax_b.plot(df['Date'][- start_boll:], df['Boll_Upper'][- start_boll:], '-', label='Upper Bollinger ', color = 'maroon', alpha = 0.3, linewidth = 1)

    ax_b.plot(df['Date'][- start_boll:], df['Boll_Lower'][- start_boll:], '-', label='Lower Bollinger ', color = 'turquoise', alpha = 0.8, linewidth = 1)


if fib.upper() == 'Y':

    ax_b.axhspan(fibb_lvl3, fibb_min,  alpha = 0.2, color = 'pink') #'lightsalmon')

    ax_b.axhspan(fibb_lvl2, fibb_lvl3, alpha = 0.2, color = 'orange') #palegoldenrod')

    ax_b.axhspan(fibb_lvl1, fibb_lvl2, alpha = 0.2, color = 'yellow') # 'plum')

    ax_b.axhspan(fibb_max, fibb_lvl1,  alpha = 0.2, color = 'lightblue')

    ax_b.plot([],[], linewidth = 2, label = 'Fibbonacci colors on' , color = 'pink', alpha = 0.3)

ax_b.legend(fontsize = 5, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')



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

ax_c.plot([], label='macd ' + str(macd_periods_short_term)  + ',' + str(macd_periods_long_term) + ',' + str(expma_periods), linewidth = 2, color = 'darkred')

ax_c.plot([], label='ema ' + str(expma_periods),  linewidth = 2, color = 'blue')

ax_c.legend(loc=2, borderaxespad=0., fontsize = 6.0)
ax_c.get_xaxis().set_visible(False)


ax_d.tick_params(axis = 'x', colors = '#890b86')

ax_d.plot_date(df['Date'], df['Volume'], '-', label='Volume', color = 'blue', linewidth = 1)

ax_d.tick_params(axis = 'y', colors = 'k', labelsize = 6)

rotate_xaxis(ax_d)

set_spines(ax_d)

ax_d.set_ylim(df['Volume'].min(),df['Volume'].max())

ax_d.set_ylabel('Volume', fontsize=8, fontweight =5, color = 'b')

ax_d.fill_between(df['Date'],df['Volume'], facecolor='#00ffe8', alpha=.5)



#-------------------------------------#
# Added Signal detrend
#-------------------------------------#
if pct_chg == 'old':

    ax_e.plot(df['Date'], ((df['Adj_Close'] - df['Adj_Close'].shift(1)) / df['Adj_Close']) * 100, linewidth =1, color = 'blue')

else:
    ax_e.plot(df['Date'], ((df['Adj_Close'] - df['Adj_Close'].shift(1)) / df['Adj_Close'].shift(1)) * 100, linewidth =1, color = 'blue')


rotate_xaxis(ax_e)

set_spines(ax_e)

set_labels(ax_e)

ax_e.tick_params(axis = 'x', colors = '#890b86')

ax_e.tick_params(axis = 'y', colors = 'g', labelsize = 0)

ax_e.get_xaxis().set_visible(False)

ax_e.set_ylabel('% Chg',fontsize=8, fontweight =5, color = 'darkred')

#######################################
# S T A R T   S E N T I M E N T   A N.#
#                                     #
#######################################
a = Analysis(ax1_subject)

sentiment, subjectivity, plots  = a.run()
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

''' Calculate the sentiment standard deviation.'''

sentiment_np_array = np.array((x_plot_list))

sentiment_std_dev  = np.std(sentiment_np_array)


ax2_sent.plot(sentiment, subjectivity, '*', label='Sentiment Color Key', color = 'red', linewidth = 1)

set_spines(ax2_sent)

rotate_xaxis(ax2_sent)

ax2_sent.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

ax2_sent.set_xlim(-1, 1)

ax2_sent.set_ylim(0, 1)

ax2_sent.tick_params(axis = 'x', colors = '#890b86', labelsize = 6)

ax2_sent.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax2_sent.set_title("(neg) <-- " + ax1_subject + " Sentiment Score --> (pos)", color = '#353335', size = 10)

ax2_sent.set_ylabel('Subjectivity', fontsize=8, fontweight =5, color = '#890b86')


ax2_sent.plot([],[], linewidth = 2, label = 'Sentiment:' +  "{0:.4f}".format(round(sentiment,4) ) , color = 'red', alpha = 0.9)

ax2_sent.plot([],[], linewidth = 2, label = 'Subjectivity:' + "{0:.4f}".format(round(subjectivity,4) ), color = 'red', alpha = 0.9)

ax2_sent.plot([],[], linewidth = 2, label = 'Std. Dev:' + "{0:.4f}".format(round(sentiment_std_dev,4) ), color = 'darkblue', alpha = 0.9, marker = '+')

ax2_sent.axhline(y=0, color = 'yellow', linewidth = 2, label = '0=Neutral')

ax2_sent.legend(fontsize = 5, fancybox = True, loc = 1, markerscale = -0.5, framealpha  = 0.5, facecolor = '#dde29a')



ax2_sent_plots.plot( df_plot['sentiment'], df_plot['subjectivity'], '*', color = 'red')

ax2_sent_plots.plot([],[], linewidth = 2, label = 'Neutral' , color = 'k', alpha = 0.9)

ax2_sent_plots.axhline(0, color = 'yellow', linewidth = 1)

ax2_sent_plots.axhline(sentiment_std_dev, color = 'darkblue', linewidth = 1)

rotate_xaxis(ax2_sent_plots)

set_spines(ax2_sent_plots)

ax2_sent_plots.axvline(x = 0, linewidth = 1,  color = 'yellow')

#ax2_sent_plots.set_ylim(0, 1)
ax2_sent_plots.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

ax2_sent_plots.tick_params(axis = 'x', colors = '#890b86', labelsize = 6)

ax2_sent_plots.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax2_sent_plots.set_title("(neg) <-- " + ax1_subject + " Sentiment Plots --> (pos)", color = '#353335', size = 10)

ax2_sent_plots.set_ylabel('Subjectivity', fontsize=8, fontweight =5, color = '#890b86')




ax_sent_chart.hist(df_plot['sentiment'], bins = 20, histtype = 'barstacked', rwidth = 2)# ,df_plot['subjectivity'])

ax_sent_chart.plot([],[], linewidth = 2, label = 'Neutral' , color = 'k', alpha = 0.9)

ax_sent_chart.axhline(0, color = 'yellow', linewidth = 1)

rotate_xaxis(ax_sent_chart)

set_spines(ax_sent_chart)

ax_sent_chart.axvline(x = 0, linewidth = 2,  color = 'yellow')

#ax2_sent_plots.set_ylim(0, 1)
ax_sent_chart.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

ax_sent_chart.tick_params(axis = 'x', colors = '#890b86', labelsize = 6)

ax_sent_chart.tick_params(axis = 'y', colors = 'g', labelsize = 6)

ax_sent_chart.set_title("(neg) <-- " + ax1_subject + " Sentiment Chart --> (pos)", color = '#353335', size = 10)

ax_sent_chart.set_ylabel('Counts', fontsize=8, fontweight =5, color = '#890b86')

ax_sent_chart.set_xlabel('Sentiment', fontsize=8, fontweight =5, color = '#890b86')


#######################################
# Generate Similar Stocks
#######################################
a  = corr(ax1_subject)

row_cnt = 0

col_cnt = 0

mydict = a.run(ax1_subject)

stock_items = mydict.items()

for stock_item in stock_items:

    row_cnt += 1

    if row_cnt  ==  1:

        ax3_sim_stock1.set_visible(True)

        ax3_subject = (stock_item[0]) 

        df = pd.read_csv((ax3_subject + '.csv'), parse_dates=True, index_col =0)

        df.reset_index(inplace = True)

        stock_entry = (df['Adj_Close'][0])               # Set marker of last years close.

        ax3_sim_stock1.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'blue', linewidth = 1)

        ax3_sim_stock1.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'k', alpha = 0.9)

        ax3_sim_stock1.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)

        ax3_sim_stock1.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='g', alpha=0.6)

        ax3_sim_stock1.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='r', alpha=0.6)

        rotate_xaxis(ax3_sim_stock1)

        ax3_sim_stock1.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

        set_spines(ax3_sim_stock1)

        ax3_sim_stock1.tick_params(axis = 'x', colors = '#890b86')

        ax3_sim_stock1.tick_params(axis = 'y', colors = 'g', labelsize = 6)

        ax3_sim_stock1.set_title("Similar Stock: " + ax3_subject + " correlates: " + "{0:.2f}".format(round(stock_item[1],2) ) + "%", color = '#353335', size = 9)

        set_labels(ax3_sim_stock1)

        ax3_sim_stock1.set_color = '#890b86'

        ax3_sim_stock1.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')


    if row_cnt  ==  2:

        ax4_subject = (stock_item[0]) 

        df = pd.read_csv((ax4_subject + '.csv'), parse_dates=True, index_col =0)

        ax3_sim_stock2.set_visible(True)

        df.reset_index(inplace = True)

        stock_entry = (df['Adj_Close'][0])               # Set marker of last years close.

        ax3_sim_stock2.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'blue', linewidth = 1)

        ax3_sim_stock2.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'k', alpha = 0.9)

        ax3_sim_stock2.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)

        ax3_sim_stock2.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='g', alpha=0.6)

        ax3_sim_stock2.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='r', alpha=0.6)

        rotate_xaxis(ax3_sim_stock2)

        ax3_sim_stock2.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

        set_spines(ax3_sim_stock2)

        ax3_sim_stock2.tick_params(axis = 'x', colors = '#890b86')

        ax3_sim_stock2.tick_params(axis = 'y', colors = 'g', labelsize = 6)

        ax3_sim_stock2.set_title("Similar Stock: " + ax4_subject + " correlates: " + "{0:.2f}".format(round(stock_item[1],2) ) + "%", color = '#353335', size = 9)

        set_labels(ax3_sim_stock2)

        ax3_sim_stock2.set_color = '#890b86'

        ax3_sim_stock2.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')



    if row_cnt  ==  3:

        ax5_subject = (stock_item[0]) 

        df = pd.read_csv((ax5_subject + '.csv'), parse_dates=True, index_col =0)

        ax3_sim_stock3.set_visible(True)

        df.reset_index(inplace = True)

        stock_entry = (df['Adj_Close'][0])               # Set marker of last years close.

        ax3_sim_stock3.plot_date(df['Date'], df['Adj_Close'], '-', label='ADJ Closing Price', color = 'blue', linewidth = 1)

        ax3_sim_stock3.plot([],[], linewidth = 2, label = 'Adj_Close yr ago' , color = 'k', alpha = 0.9)

        ax3_sim_stock3.axhline(df['Adj_Close'][0], color = 'k', linewidth = 2)

        ax3_sim_stock3.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] > stock_entry), facecolor='g', alpha=0.6)

        ax3_sim_stock3.fill_between(df['Date'], df['Adj_Close'], stock_entry, where = (df['Adj_Close'] < stock_entry), facecolor='r', alpha=0.6)

        rotate_xaxis(ax3_sim_stock3)

        ax3_sim_stock3.grid(True, color='lightgreen', linestyle = '-', linewidth=2)

        set_spines(ax3_sim_stock3)

        ax3_sim_stock3.tick_params(axis = 'x', colors = '#890b86')

        ax3_sim_stock3.tick_params(axis = 'y', colors = 'g', labelsize = 6)

        ax3_sim_stock3.set_title("Similar Stock: " + ax5_subject + " correlates: " + "{0:.2f}".format(round(stock_item[1],2) ) + "%", color = '#353335', size = 9)

        set_labels(ax3_sim_stock3)

        ax3_sim_stock3.set_color = '#890b86'

        ax3_sim_stock3.legend(bbox_to_anchor=(1.01, 1),fontsize = 6, fancybox = True, loc = 0, markerscale = -0.5, framealpha  = 0.5, facecolor = '#f9ffb7')







plt.rc('ytick', labelsize=6 )    # fontsize of the tick labels

plt.subplots_adjust(left = 0.10, bottom = 0.16, right = 0.920, top = 0.93, wspace = 0.2, hspace = -.1)

fig = gcf()

my_title = (user, "Stock Page")

fig.suptitle(user + "'s Stock Tracker Page for " + ax1_subject + " as of " + str(dt.date.today()), fontsize=14)


plt.show()

fig.savefig(ax1_subject + '.png')
