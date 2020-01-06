import os, sys
import bs4 as bs
import requests
import urllib
import string

#######################################
class get_NASDAQ():
#######################################

    #-------------------------------------#
    def __init__(self):
    #-------------------------------------#

        pass

    #-------------------------------------#
    def run(self):
    #-------------------------------------#

        stocks = []                                    #Allocate list to save results

        alphabet  = string.ascii_uppercase

        alphabet  = list(alphabet)

        for char in alphabet:

            resp = requests.get("http://eoddata.com/stocklist/NASDAQ/" + char + ".HTM")

            soup = bs.BeautifulSoup(resp.text, "lxml")

            table = soup.find('table', {'class': 'quotes'}) #Wiki only has 1 table.

            for row in table.findAll('tr')[1:]:            #Wiki data starts w/2nd row

                subject = row.findAll('td')[0].text        #Wiki data starts 1st col

                subject = str(subject).replace('\n', '')

                stocks.append(subject)

        return stocks

if __name__ == "__main__":

    a = get_NASDAQ()

    stocks = a.run()

    print(stocks)