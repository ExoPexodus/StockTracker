import logging

def find_high_before_crossover(monthly_data, latest_crossover_point):
    logging.info(f"Finding highest stock price before {latest_crossover_point}")
    # Filter data before the latest crossover point
    data_before_crossover = monthly_data[monthly_data.index < latest_crossover_point]
    # Find the all-time high and its date
    all_time_high = data_before_crossover['High'].max()
    all_time_high_date = data_before_crossover['High'].idxmax()
    logging.info(f"All-time high before {latest_crossover_point} is {all_time_high} on {all_time_high_date}")
    return all_time_high_date, all_time_high
