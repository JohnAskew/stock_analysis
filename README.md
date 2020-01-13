# stock_analysis
stock_main_tk.py is the driver module. This project should be plug and play.

Presentation includes ohlc candlesticks, dual band moving averages, macd, optional bollinger bands and fibonacci retracement bands, sentiment analysis from Google News and stocks which have an 80% or greater correlation to your stock.

By default, this project is driven by S&P500 stock data. The data is always 365 days worth of data, current as of time of running. The data is extracted and saved in a series of spreadsheets, located in new folder, "askew". 

The UI is stock_main_tk.py and allows user to customize the chart's content, such as displaying the full year or only the last 6 months, whether to include the fibonacci retracement bands, which days to use in plotting the moving averages and the macd charts, etc.

Enter the desired stock symbol and click "Accept Choice". Click "Create Graph" to generate the presentation.
