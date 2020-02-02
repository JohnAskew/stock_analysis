import os, sys
import bs4 as bs
import requests
import urllib
import string

#######################################
class get_WIKI():
#######################################

    #-------------------------------------#
    def __init__(self):
    #-------------------------------------#

        pass

    #-------------------------------------#
    def run(self):
    #-------------------------------------#

        stocks = []                                    #Allocate list to save results

        stocks.append('TSLA')
    
        stocks.append('JCP')
    
        stocks.append('MANH') 

        stocks.append('LK')

        stocks.append('BABA') 

        stocks.append('HEMP') 

        stocks.append('ITMC') 


        resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

        soup = bs.BeautifulSoup(resp.text, "lxml")

        table = soup.find('table', {'class': 'wikitable sortable'}) #Wiki only has 1 table.

        for row in table.findAll('tr')[1:]:            #Wiki data starts w/2nd row

            subject = row.findAll('td')[0].text        #Wiki data starts 1st col

            subject = str(subject).replace('\n', '')

            stocks.append(subject)

        return stocks

if __name__ == "__main__":

    a = get_WIKI()

    stocks = a.run()

    print(stocks)