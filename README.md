# StockTracker

A Simple Python based Stock Tracking app serving a specific purpose, a simple father's day gift for my dad who loves getting into stock market <3

## Overview

This application fetches stock data, resamples it to a monthly frequency, calculates the Simple Moving Average (SMA), and detects crossover points where the stock's monthly low touches and crosses under the SMA. Additionally, it finds the highest stock price before the latest crossover point and sends email alerts for new crossover points.

## Project Structure

- `fetch_data.py`: Fetches the stock data using Yahoo Finance.
- `resample_data.py`: Resamples the data to a monthly frequency.
- `calculate_sma.py`: Calculates the Simple Moving Average (SMA).
- `detect_crossover.py`: Detects crossover points where the monthly low touches and crosses under the SMA.
- `find_high.py`: Finds the highest stock price before the latest crossover point.
- `send_email.py`: Sends email alerts.
- `main.py`: Main script to run the application.

## Requirements

- Python 3.x
- `pandas` library
- `yfinance` library
- `smtplib` library (included in Python standard library)

You can install the required libraries using:

```bash
pip install pandas yfinance
