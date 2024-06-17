import yfinance as yf
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker):
    logging.info(f"Fetching entire data history for {ticker}")
    stock_data = yf.download(ticker)
    logging.debug(f"Raw data fetched:\n{stock_data}")
    return stock_data

def resample_monthly(data):
    logging.info("Resampling data to monthly frequency")
    monthly_data = data.resample('M').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    logging.debug(f"Monthly resampled data:\n{monthly_data}")
    return monthly_data

def calculate_sma(data, window):
    logging.info(f"Calculating {window}-month Simple Moving Average (SMA)")
    sma = data['Close'].rolling(window=window).mean()
    logging.debug(f"Calculated SMA:\n{sma}")
    return sma

# def detect_crossover_points(monthly_data, sma):
#     logging.info("Detecting crossover points where the monthly low crosses under the SMA")
#     crossovers = (monthly_data['Low'] < sma)
#     crossover_points = crossovers[crossovers].index
#     if not crossover_points.empty:
#         logging.info(f"Crossover points detected:\n{crossover_points}")
#     else:
#         logging.info("No crossover points detected")
#     return crossover_points


def detect_crossover_points(monthly_data, sma):
    logging.info("Detecting crossover points where the monthly low touches and crosses under the SMA")
    
    # Ensure that the index aligns correctly
    monthly_data = monthly_data.reindex(sma.index)
    
    # Find where low price is below or equal to SMA
    below_sma = monthly_data['Low'] < sma
    logging.debug(f"Below SMA:\n{below_sma}")
    
    # Find where close price is above SMA (to detect crossover from above)
    above_sma = monthly_data['Close'] > sma
    logging.debug(f"Above SMA:\n{above_sma}")
    
    # Find crossover points where low price touches and then crosses under SMA
    crossover_points = monthly_data.index[below_sma & above_sma]
    logging.debug(f"Crossover points:\n{crossover_points}")
    
    if not crossover_points.empty:
        logging.info(f"Crossover points detected:\n{crossover_points}")
    else:
        logging.info("No crossover points detected")
    
    return crossover_points


def main():
    ticker = 'RELIANCE.NS'
    window = 20  # Change window as needed

    stock_data = fetch_stock_data(ticker)
    stock_data.index = pd.to_datetime(stock_data.index)

    if stock_data.empty:
        logging.error("No data fetched. Exiting.")
        return

    monthly_data = resample_monthly(stock_data)

    logging.info("Monthly Data (Close Prices):")
    logging.info(f"{monthly_data['Close']}")

    sma = calculate_sma(monthly_data, window)

    logging.info("Calculated SMA:")
    logging.info(f"{sma}")

    crossover_points = detect_crossover_points(monthly_data, sma)
    logging.info(f"Crossover Points where Low crosses under SMA:\n{crossover_points}")

if __name__ == "__main__":
    main()
