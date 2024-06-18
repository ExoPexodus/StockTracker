import logging

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
