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

        self.config.read('config.py')

        print("tools_config_manager.py --",self.config['DEFAULT'][self.parameter])

        self.config.set('DEFAULT', self.parameter, self.variable)

        print("tools_config_manager.py --", self.config['DEFAULT'][self.parameter])

        with open('config.py', 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    
    if len(sys.argv) > 2:

        parameter = sys.argv[1]
        
        variable  = sys.argv[2]

        a = ConfigUpdater(parameter, variable)
        
        a.run()

    else:
        a = ConfigUpdater('movavg_window_days_short_term', '13')
        
        a.run()









