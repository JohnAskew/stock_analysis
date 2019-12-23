''' Street Cred: John G. Fisher - scraping Google headlines 
    All creativity (bugs), changes and results by J. Askew (bucbowie)
    Take that, Sentiment Analysis, try processing sarcasm.
'''
import os, sys
try:
    from tools_get_company import *
except:
    print("#########################################")
    print("ERROR: unable to find tools_get_company.")
    print("       Web Sentiment Analysis using")
    print("       stock symbol and not company name!")
    print("#########################################")
try:
    from textblob import TextBlob
except:
    os.system('pip install textblob')
    from textblob import TextBlob
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

if len(sys.argv) > 1:
     term = sys.argv[1]
else:
    term = None

class Analysis:
    def __init__(self, term):
        self.term = term
        self.subjectivity = 0
        self.sentiment = 0
        self.plot = []

        try:
            self.term = get_symbol(self.term)
            print("tool_scrape searching with", self.term)
        except Exception as e:
            print(e)
            sys.exit()
             
        self.url = 'https://www.google.com/search?q={0}&num=30&source=lnms&tbm=nws'.format(self.term)

    def run(self):
        response = requests.get(self.url)
        #print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_results = soup.find_all('div', {"class":"BNeawe s3v9rd AP7Wnd"})
        hl_set = set()
        plot_cnt = 0
        for h in headline_results:
            hl_set.add(h)

        for h in hl_set:
            d = dict()
            blob = TextBlob(h.get_text())
            d['sentiment'] = blob.sentiment.polarity / len(hl_set)
            d['subjectivity'] = blob.sentiment.subjectivity / len(hl_set)
            self.plot.append(d)
            self.sentiment += blob.sentiment.polarity / len(hl_set)
            self.subjectivity += blob.sentiment.subjectivity / len(hl_set)

        return self.sentiment, self.subjectivity, self.plot

if __name__ == "__main__":
    a = Analysis('EBAY')
    a.run()
    print(a.term,  '\tsubjectivity', str(a.subjectivity) + '\n', '\t\t\tsentiment' + ' -1 < ', a.sentiment, '< 1')
