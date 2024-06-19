import logging

def detect_crossover_points(monthly_data, sma):
    logging.info("Detecting crossover points where the monthly low touches and crosses under the SMA")
    
    # Ensure that the index aligns correctly
    monthly_data = monthly_data.reindex(sma.index)
    
    # Find where low price is below or equal to SMA
    below_sma = monthly_data['Low'] < sma
    logging.debug(f"Below SMA:\n{below_sma}")
    
    # Find where close price is above SMA (to detect crossover from above)
    above_sma = monthly_data['High'] > sma
    logging.debug(f"Above SMA:\n{above_sma}")
    
    # Find crossover points where low price touches and then crosses under SMA
    crossover_points = monthly_data.index[below_sma & above_sma]
    logging.debug(f"Crossover points:\n{crossover_points}")
    
    if not crossover_points.empty:
        logging.info(f"Crossover points detected:\n{crossover_points}")
    else:
        logging.info("No crossover points detected")
    
    return crossover_points
