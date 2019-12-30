import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {"movAvg_window_days_short_term":10,
"movAvg_window_days_long_term":30,
"macd_periods_long_term":26,
"macd_periods_short_term":12,
"expMA_periods":9, 
"rsi_overbought":70,
"rsi_oversold":30}
with open('config.py', 'w') as configfile:
    config.write(configfile)