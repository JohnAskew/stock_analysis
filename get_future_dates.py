import os

try:

    import datetime as dt

except:

    os.system('pip install datetime')

    import datetime as dt

from datetime import timedelta


def calc_future_date(days = 7):

    dates = []

    for i in range(1,days +1):

        date = dt.datetime.now()

        td   = timedelta(days=i)

        date = date + td

        date = date.strftime("%Y-%m-%d")

        dates.append(date)

    print(dates)

    return dates

if __name__ == "__main__":

    calc_future_date(7)