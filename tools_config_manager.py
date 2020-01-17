import os, sys
try:
    import configparser
except:
    os.system('pip install configparser')
    import configparser

class ConfigUpdater:
    def __init__(self, parameter ="", variable = ''):
       self.parameter = parameter
       self.variable  = variable

    def run(self):
        self.config = configparser.ConfigParser()

        self.config.read('config.ini')

        self.config.set('DEFAULT', self.parameter, self.variable)

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    
    if len(sys.argv) > 2:

        parameter = sys.argv[1]
        
        variable  = sys.argv[2]

        a = ConfigUpdater(parameter, variable)
        
        a.run()

    else:
        
        a = ConfigUpdater('movavg_window_days_short_term', '10')

        a.run()

        a = ConfigUpdater('movavg_window_days_long_term',  '30')

        a.run()

        a = ConfigUpdater('macd_periods_long_term',        '26')

        a.run()

        a = ConfigUpdater('macd_periods_short_term',       '12')

        a.run()

        a = ConfigUpdater('expma_periods',                  '9')

        a.run()

        a = ConfigUpdater('rsi_overbought',                '70')

        a.run()

        a = ConfigUpdater('rsi_oversold',                  '30')

        a.run()

        a = ConfigUpdater('pct_chg',                      'new')

        a.run()

        a = ConfigUpdater('boll',                           'y')

        a.run()

        a = ConfigUpdater('boll_window_days',              '20')

        a.run()

        a = ConfigUpdater('boll_weight',                    '2')

        a.run()
        
        a = ConfigUpdater('fib',                            'y')

        a.run()

        a = ConfigUpdater('atradx',                        '14')

        a.run()

        a = ConfigUpdater('chomf',                          '14')

        a.run()







