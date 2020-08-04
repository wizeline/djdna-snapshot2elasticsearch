import yfinance as yf

def getTickerStocks(ticker):
    ticker = yf.Ticker(ticker)
    return ticker.history(start="2019-01-01")