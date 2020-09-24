import yfinance as yf

def get_ticker_stocks(ticker, start_date):
    ticker = yf.Ticker(ticker)
    return ticker.history(start=start_date)
