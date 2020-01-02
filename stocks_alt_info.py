#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen
try:
    import lxml
except:
    os.system('pip install lxml')
    import lxml
try:
    import html
except:
    os.system('pip install html')
    import html

#######################################
class altAnalysis():
#######################################
#-------------------------------------#
    def __init__(self, sTOCK):
#-------------------------------------#

        self.sTOCK = sTOCK
# For ignoring SSL certificate errors
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        # Input from the user
        self.url = 'https://finance.yahoo.com/quote/' + self.sTOCK + '/'
        # Making the website believe that you are accessing it using a Mozilla browser
        self.req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.webpage = urlopen(self.req).read()
#-------------------------------------#
    # Creating a BeautifulSoup object of the lxml instead of HTML for easy extraction of data.

    def run(self):
#-------------------------------------#

        soup = BeautifulSoup(self.webpage, 'lxml') #'html.parser')
        html = soup.prettify('utf-8')
        company_json = {}
        other_details = {}
        for span in soup.findAll('span',
                                 attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'
                                 }):
            company_json['PRESENT_VALUE'] = span.text.strip()
        for div in soup.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
            for span in div.findAll('span', recursive=False):
                company_json['PRESENT_GROWTH'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'PREV_CLOSE-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['PREV_CLOSE'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'OPEN-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['OPEN'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'BID-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['BID'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'ASK-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['ASK'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'DAYS_RANGE-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['DAYS_RANGE'] = span.text.strip()
        for td in soup.findAll('td',
                               attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['FIFTY_TWO_WK_RANGE'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['TD_VOLUME'] = span.text.strip()
        for td in soup.findAll('td',
                               attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'
                               }):
            for span in td.findAll('span', recursive=False):
                other_details['AVERAGE_VOLUME_3MONTH'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['MARKET_CAP'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'BETA_3Y-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['BETA_3Y'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'PE_RATIO-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['PE_RATIO'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'EPS_RATIO-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['EPS_RATIO'] = span.text.strip()
        for td in soup.findAll('td', attrs={'data-test': 'EARNINGS_DATE-value'}):
            other_details['EARNINGS_DATE'] = []
            for span in td.findAll('span', recursive=False):
                other_details['EARNINGS_DATE'].append(span.text.strip())
        for td in soup.findAll('td',
                               attrs={'data-test': 'DIVIDEND_AND_YIELD-value'}):
            other_details['DIVIDEND_AND_YIELD'] = td.text.strip()
        for td in soup.findAll('td',
                               attrs={'data-test': 'EX_DIVIDEND_DATE-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['EX_DIVIDEND_DATE'] = span.text.strip()
        for td in soup.findAll('td',
                               attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'}):
            for span in td.findAll('span', recursive=False):
                other_details['ONE_YEAR_TARGET_PRICE'] = span.text.strip()
        
        company_json['OTHER_DETAILS'] = other_details

        # x = str(company_json).replace(',','|')
        # print(x)



        with open(self.sTOCK + '.data.json', 'w') as outfile:
            json.dump(company_json, outfile, indent=4)
        sTOCK_json = json.dumps(company_json, indent = 4, sort_keys=True)

        # for sTOCK, values in company_json['OTHER_DETAILS'].items():
        #     print(sTOCK, values)

        with open(self.sTOCK + '.output_file.html', 'wb') as file:
            file.write(html)
        print('---------- ' + os.path.basename(__file__) + '==>Extraction of data is complete. Check json file', self.sTOCK + '.data.json ----------')
        return company_json


if __name__ == "__main__":
    a = altAnalysis('JCP')
    company_json = a.run()
    