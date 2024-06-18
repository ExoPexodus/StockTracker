import yfinance as yf
import logging

def fetch_stock_data(ticker):
    logging.info(f"Fetching entire data history for {ticker}")
    stock_data = yf.download(ticker)
    logging.debug(f"Raw data fetched:\n{stock_data}")
    return stock_data
