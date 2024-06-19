import logging
import pandas as pd
import os
from fetch_data import fetch_stock_data
from resample_data import resample_monthly
from calculate_sma import calculate_sma
from detect_crossover import detect_crossover_points
from find_high import find_high_before_crossover
from send_email import send_email_alert, create_email_body

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration (replace with your actual configuration)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.environ['GMAIL_USER']
SMTP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
FROM_EMAIL = os.environ['GMAIL_USER']
TO_EMAIL = os.environ['TO_GMAIL_USER']

def main():
    ticker = 'RELIANCE.NS'
    window = 20  # Change window as needed
    last_crossover_point_file = 'last_crossover.txt'

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

        # Check for duplicate crossover points
        try:
            with open(last_crossover_point_file, 'r') as file:
                last_crossover_point = file.read().strip()
        except FileNotFoundError:
            last_crossover_point = None

        if str(latest_crossover_point) != last_crossover_point:
            # Update the last crossover point file
            with open(last_crossover_point_file, 'w') as file:
                file.write(str(latest_crossover_point))
            
            all_time_high_date, all_time_high = find_high_before_crossover(monthly_data, latest_crossover_point)
            logging.info(f"All-time high before latest crossover point ({latest_crossover_point}): {all_time_high} on {all_time_high_date}")

            current_price = stock_data['Close'].iloc[-1]
            crossover_point_low = monthly_data.loc[latest_crossover_point, 'Low']

            stock_info = {
                'ticker': ticker,
                'current_price': current_price,
                'latest_crossover_point': latest_crossover_point,
                'crossover_point_low': crossover_point_low,
                'all_time_high': all_time_high,
                'all_time_high_date': all_time_high_date
            }

            # Create the email body
            email_body = create_email_body(stock_info)

            # Send email alert
            subject = f"Stock Alert: Crossover Detected for {ticker}"
            send_email_alert(subject, email_body, TO_EMAIL, FROM_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
        else:
            logging.info("No new crossover point detected, alert not sent.")
    else:
        logging.info("No crossover points detected, hence no high before crossover to report.")

if __name__ == "__main__":
    main()