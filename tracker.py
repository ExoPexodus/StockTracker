import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Function to fetch stock data
def fetch_stock_data(ticker, period="10y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def calculate_sma(data, length=20, timeframe='M'):
    return data['Close'].resample(timeframe).mean().rolling(window=length).mean().dropna()

def send_email(subject, body, to_email, attachment_path=None):
    from_email = os.environ['GMAIL_USER']
    from_password = os.environ['GMAIL_APP_PASSWORD']  # Use the app password generated in Google Account

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Create HTML content for the email
    html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #ffffff;
            margin: 0;
            padding: 0;
          }}
          .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3);
          }}
          h2 {{
            color: #ff4d4d;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
          }}
          p {{
            font-size: 18px;
            line-height: 1.6;
            color: #ffffff; /* White text color */
          }}
          .graph-img {{
            display: block;
            margin: 20px auto;
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(255, 77, 77, 0.5);
          }}
          .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #999999; /* Light grey text color */
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>{subject}</h2>
          <p>{body}</p>
          <img src="cid:graph_image" class="graph-img">
        </div>
        <div class="footer">
          <p>Powered by Your Stock Tracker</p>
        </div>
      </body>
    </html>
    """

    # Attach HTML content to the email
    msg.attach(MIMEText(html, 'html'))

    # Attach graph image if provided
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
            msg.attach(part)

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
    print(f"Email sent to {to_email}!")
    
    
# Function to visualize data
def visualize_data(data, ticker, sma):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Closing Prices')
    plt.plot(sma, label='SMA', linestyle='--')
    plt.title(f'{ticker} Closing Prices and SMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    image_path = f"{ticker}_sma_plot.png"
    plt.savefig(image_path)
    plt.close()
    return image_path

# Function to find the buy point
def find_buy_point(ticker, sma_window):
    # Step 1: Fetch stock data
    data = fetch_stock_data(ticker, period="10y")  # Fetch last 10 years of data

    # Step 2: Calculate the Simple Moving Average (SMA)
    data['SMA'] = calculate_sma(data, length=sma_window, timeframe='M')

    # Step 3: Find where the closing price crosses below the SMA
    data['Below_SMA'] = data['Close'] < data['SMA']
    
    # Step 4: Identify the crossover points
    crossover_points = data.index[data['Below_SMA'] & ~data['Below_SMA'].shift(1).fillna(False)]

    if crossover_points.empty:
        return None, None, data

    # Step 5: Find the most recent crossover point
    recent_crossover_date = crossover_points[-1]

    # Step 6: Find the all-time high before the crossover date
    all_time_high = data.loc[:recent_crossover_date]['Close'].max()

    return recent_crossover_date, all_time_high, data

def main():
    ticker = "TCS.NS"
    sma_window = 20  # 20 months window
    to_email = os.environ['TO_GMAIL_USER']

    recent_crossover_date, all_time_high, data = find_buy_point(ticker, sma_window)
    
    if recent_crossover_date is not None:
        subject = f"Stock Buy Alert: {ticker}"
        body = (f"Stock: {ticker}<br>"
                f"Recent Crossover Date: {recent_crossover_date}<br>"
                f"All-Time High Before Crossover Date: {all_time_high}<br>"
                f"Suggested Buy Point: {all_time_high}")
    else:
        subject = f"No Recent Crossover Found for {ticker}"
        body = (f"Stock: {ticker}<br>"
                f"No recent crossover found where closing price went below SMA.<br>"
                f"Please check the attached graph for details.")

    # Visualize data and attach the plot to the email
    sma = calculate_sma(data, length=sma_window, timeframe='M')
    image_path = visualize_data(data, ticker, sma)
    send_email(subject, body, to_email, attachment_path=image_path)

if __name__ == "__main__":
    main()


