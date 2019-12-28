import requests

#-------------------------------------#
def get_symbol(symbol):
#-------------------------------------#
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        
        if x['symbol'] == symbol:
            
            return x['name']
        
        else:
            
            msg = (sys.argv[0], "tools_get_company.py\nUnable to find Company using ticker:", symbol,  "\nAborting with no action taken.")
            
            print(msg)

if __name__ == "__main__":
    
    company = get_symbol("GOOG")
