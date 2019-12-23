import requests

#-------------------------------------#
def get_symbol(symbol):
#-------------------------------------#
    print("tools_get_company: received:", symbol)
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            print("tools_get_company: returning:", x['name'])
            return x['name']

if __name__ == "__main__":
    company = get_symbol("JCP")
    print(company)