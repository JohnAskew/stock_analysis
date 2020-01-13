import os, sys
try:
    import configparser
except:
    os.system('pip install configparser')
    import configparser

#######################################
class ParseConfig:
#######################################
#-------------------------------------#
    def __init__(self):
#-------------------------------------#
        pass

#-------------------------------------#
    def run(self):
#-------------------------------------#
        config = configparser.ConfigParser()

        config.read('config.ini')
        
        return config['DEFAULT']['movavg_window_days_short_term'] \
        ,config['DEFAULT']['movavg_window_days_long_term']        \
        ,config['DEFAULT']['macd_periods_long_term']              \
        ,config['DEFAULT']['macd_periods_short_term']             \
        ,config['DEFAULT']['expma_periods']                       \
        ,config['DEFAULT']['rsi_overbought']                      \
        ,config['DEFAULT']['rsi_oversold']                        \
        ,config['DEFAULT']['pct_chg']                             \
        ,config['DEFAULT']['boll']                                \
        ,config['DEFAULT']['boll_window_days']                    \
        ,config['DEFAULT']['boll_weight']                         \
        ,config['DEFAULT']['fib']                                 \
        ,config['DEFAULT']['sel_stocks']


#######################################
# M A I N   L O G I C
#######################################
if __name__ == '__main__':

    a = ParseConfig()
    movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold, pct_chg, boll, boll_window_days, boll_weight, fib, sel_stocks = a.run()

    print(movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold, pct_chg, boll, boll_window_days, boll_weight, fib, sel_stocks)







