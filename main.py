import logging
import pandas as pd
from fetch_data import fetch_stock_data
from resample_data import resample_monthly
from calculate_sma import calculate_sma
from detect_crossover import detect_crossover_points
from find_high import find_high_before_crossover

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

    if not crossover_points.empty:
        latest_crossover_point = crossover_points[-1]
        logging.info(f"Latest crossover point: {latest_crossover_point}")
        all_time_high_date, all_time_high = find_high_before_crossover(monthly_data, latest_crossover_point)
        logging.info(f"All-time high before latest crossover point ({latest_crossover_point}): {all_time_high} on {all_time_high_date}")
    else:
        logging.info("No crossover points detected, hence no high before crossover to report.")

if __name__ == "__main__":
    main()
