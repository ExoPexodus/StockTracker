import logging

def calculate_sma(data, window):
    logging.info(f"Calculating {window}-month Simple Moving Average (SMA)")
    sma = data['Close'].rolling(window=window).mean()
    logging.debug(f"Calculated SMA:\n{sma}")
    return sma
