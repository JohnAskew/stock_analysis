''' Street Cred: John G. Fisher - scraping Google company_infos 
    
    All creativity (bugs), changes and results by J. Askew (bucbowie)

    This program scrapes stock ticker, company name and info and 

    returns a dictionary containing that information.
'''
import os, sys

try:

    from tools_get_company import *

except:

    print("#########################################")

    print("ERROR: unable to find tools_get_company.")

    print(" using stock symbol and not company name!")

    print("#########################################")

try:

    from bs4 import BeautifulSoup

except:

    os.system('pip install bs4')

    from bs4 import BeautifulSoup

try:

    import requests

except:

    os.system('pip install requests')

    import requests

try:
    if len(sys.argv) > 1:

     term = sys.argv[1]

except:

    print("tools_scrape_profile has issues with sys.argv. Skipping passed arguments and using default ticker.")

else:

    term = None

#######################################
class ScrapProfile:
#######################################
#-------------------------------------#
    def __init__(self, term):
#-------------------------------------#        
        self.term = term
        
        self.subjectivity = 0
        
        self.sentiment = 0
        
        self.plot = []

        try:
        
            self.term = get_symbol(self.term)
        
        except Exception as e:
        
            print(e)

        self.url = 'https://www.marketwatch.com/investing/stock/{}/profile'.format(self.term)
        
    #---------------------------------#
    def run(self):
    #---------------------------------#
        response = requests.get(self.url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ci_dict = {}
        
        co_name = soup.find('title')
        
        co_name = co_name.text.split('profile')
        
        co_name = " ".join(co_name)
        
        co_name = co_name.strip().split('|')
        
        ci_dict['name']   = co_name[1].replace("Profile", "")
        
        ci_dict['ticker'] = co_name[0]
        
        company_info_results = soup.find_all('div', {"class":"full"})
 
        plot_cnt = 0

        for i in company_info_results:

            i = str(i.text).strip('<p>').strip('</p')

            i = i.strip()

            ci_dict["info"] = i

        return ci_dict

#######################################
if __name__ == "__main__":
#######################################
    
    stock = "HEMP"

    a = ScrapProfile(stock.lower())
    
    x = a.run()

    print(x)
