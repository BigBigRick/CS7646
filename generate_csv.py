import pandas as pd
import numpy as np

# Generate trading dates (exclude weekends)
dates = pd.bdate_range('2010-01-01', '2012-12-31')

# Base prices for each symbol
base_prices = {
    'SPY': 100,
    'XOM': 60,
    'GOOG': 300,
    'GLD': 100
}

# Set random seed once for reproducibility (before the loop)
np.random.seed(42)

# Generate data for each symbol
for symbol, base_price in base_prices.items():
    # Generate price series with random walk
    prices = [base_price]
    
    for i in range(1, len(dates)):
        # Random daily change (normal distribution)
        change = np.random.normal(0, 0.015)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1))  # Ensure price doesn't go below 1
    
    # Create DataFrame with all required columns
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(dates)),
        'Adj Close': prices
    })
    
    # Save to CSV
    df.to_csv(f'data/{symbol}.csv', index=False)
    print(f'Generated {symbol}.csv with {len(dates)} rows')

print('All CSV files generated successfully!')
