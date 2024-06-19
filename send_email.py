import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

def send_email_alert(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    logging.info("Preparing to send email alert")
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logging.info("Email alert sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def create_email_body(stock_info):
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
                color: #e0e0e0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                width: 400px;
                padding: 20px;
                transition: transform 0.2s;
            }}
            .card:hover {{
                transform: scale(1.05);
            }}
            .header {{
                background-color: #008080;
                border-radius: 10px 10px 0 0;
                padding: 10px;
                text-align: center;
                color: #fff;
            }}
            .content {{
                padding: 20px;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .label {{
                font-weight: bold;
                color: #80cbc4;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Stock Alert: {stock_info['ticker']}</h2>
            </div>
            <div class="content">
                <p><span class="label">Current Price:</span> {stock_info['current_price']}</p>
                <p><span class="label">Latest Crossover Point:</span> {stock_info['latest_crossover_point']}</p>
                <p><span class="label">Crossover Point Low:</span> {stock_info['crossover_point_low']}</p>
                <p><span class="label">All-time High Before Crossover:</span> {stock_info['all_time_high']} on {stock_info['all_time_high_date']}</p>
            </div>
        </div>
    </body>
    </html>
    """
