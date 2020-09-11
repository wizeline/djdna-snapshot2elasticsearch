import yfinance as yf

def get_ticker_stocks(ticker):
    ticker = yf.Ticker(ticker)
    return ticker.history(start="2019-01-01")
