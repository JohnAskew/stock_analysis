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

        config.read('config.py')
        
        return config['DEFAULT']['movavg_window_days_short_term'],config['DEFAULT']['movavg_window_days_long_term'],config['DEFAULT']['macd_periods_long_term'],config['DEFAULT']['macd_periods_short_term'],config['DEFAULT']['expma_periods'],config['DEFAULT']['rsi_overbought'],config['DEFAULT']['rsi_oversold']


#######################################
# M A I N   L O G I C
#######################################
if __name__ == '__main__':

    a = ParseConfig()
    movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold = a.run()

    print(movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold)







