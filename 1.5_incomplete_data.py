"""
Exercise 1.5: Handling Incomplete Data
========================================

TITLE: Stock Data Missing Value Handling and Filling Techniques

PURPOSE:
--------
This exercise demonstrates how to handle missing data in stock price datasets.
Real-world financial data often has gaps due to:
- Market holidays (no trading)
- Data collection issues
- Stock delistings or new listings
- Corporate actions

The script covers two main techniques for filling missing values:
1. Forward Fill (ffill): Propagate last valid value forward
2. Backward Fill (bfill): Fill remaining gaps with next valid value

SCRIPT STRUCTURE:
-----------------
Part 1: Basic Forward Fill Example (commented out - requires test data)
  - Demonstrates simple forward fill using fillna()
  - Shows how to handle incomplete data for a single symbol

Part 2: Complete Fill Missing Values Implementation (active)
  - Implements fill_missing_values() function
  - Uses both forward and backward fill for complete coverage
  - Processes multiple stock symbols simultaneously
  - Includes data validation and visualization

KEY FUNCTIONS:
--------------
1. symbol_to_path(symbol, base_dir="data")
   - Constructs file path for stock CSV data

2. get_data(symbols, dates)
   - Reads multiple stock CSV files
   - Joins data into single DataFrame
   - Handles SPY as reference stock
   - Removes non-trading days

3. fill_missing_values(df_data)
   - Main function: fills all missing values
   - Strategy: forward fill first, then backward fill
   - Modifies DataFrame in place

4. plot_data(df_data)
   - Visualizes stock price data
   - Shows filled data for verification

5. test_run()
   - Main execution function
   - Demonstrates complete workflow
   - Prints before/after statistics

DATA FILLING STRATEGY:
----------------------
1. Forward Fill (ffill):
   - Fills gaps with previous valid value
   - Example: [NaN, NaN, 100, NaN, 200] -> [NaN, NaN, 100, 100, 200]
   - Cannot fill values at the beginning (no previous value)

2. Backward Fill (bfill):
   - Fills remaining gaps with next valid value
   - Example: [NaN, NaN, 100, 100, 200] -> [100, 100, 100, 100, 200]
   - Handles gaps at the start of dataset

COMBINED APPROACH:
------------------
Using both methods ensures:
- All missing values are filled
- Data continuity is maintained
- No gaps remain in the dataset

USAGE:
------
Run: python 1.5_incomplete_data.py

The script will:
1. Load stock data (SPY, XOM, GOOG, GLD)
2. Display statistics before filling
3. Apply fill_missing_values()
4. Display statistics after filling
5. Generate visualization plot

OUTPUT:
-------
- Console output showing missing value statistics
- Before/after comparison
- Interactive plot of stock prices

(c) 2015 by Devpriya Dave and Tucker Balch.
"""

"""=================================================================================="""

"""
Part 1: Using Fillna() - Basic Forward Fill Example
----------------------------------------------------
This section demonstrates a simple approach to fill missing values using forward fill.
Forward fill propagates the last valid observation forward to fill missing values.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

def symbol_to_path(symbol, base_dir="data"):
	"""
	Return CSV file path given ticker symbol.
	
	Args:
		symbol: Stock ticker symbol (e.g., 'SPY', 'FAKE2')
		base_dir: Base directory containing CSV files (default: "data")
	
	Returns:
		Full path to the CSV file for the given symbol
	"""
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbollist, dates):
	"""
	Read stock data from CSV files and combine into a single DataFrame.
	
	This function:
	- Creates an empty DataFrame with the specified date range as index
	- Ensures SPY is included as a reference stock
	- Reads adjusted close prices for each symbol
	- Joins all data together
	- Removes dates where SPY did not trade (market holidays)
	
	Args:
		symbollist: List of stock ticker symbols to read
		dates: Date range (pandas DatetimeIndex) for the data
	
	Returns:
		DataFrame with dates as index and stock symbols as columns
		May contain NaN values for missing data
	"""
	df_final = pd.DataFrame(index=dates)
	
	# Add SPY as reference if not already in the list
	if "SPY" not in symbollist:
		symbollist.insert(0, "SPY")
	
	# Read data for each symbol
	for symbol in symbollist:
		file_path = symbol_to_path(symbol)
		# Read CSV: parse dates, use Date as index, only get Adj Close column
		df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
		                     usecols=["Date", "Adj Close"], na_values=["nan"])
		# Rename column to match symbol name
		df_temp = df_temp.rename(columns={'Adj Close': symbol})
		# Join with main dataframe (left join on index)
		df_final = df_final.join(df_temp)
		
		# Remove dates where SPY didn't trade (market holidays/weekends)
		if symbol == "SPY":
			df_final = df_final.dropna(subset=['SPY'])
	
	return df_final

def plot(df_data):
	"""
	Plot stock price data with appropriate labels.
	
	Args:
		df_data: DataFrame with dates as index and stock prices as columns
	"""
	ax = df_data.plot(title="Incomplete Data", fontsize=2)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	plt.show()

# Main execution block for Part 1
# Note: This section is commented out because FAKE2.csv doesn't exist
# Uncomment and modify to use actual stock symbols if needed
"""
if __name__ == '__main__':
	# List of stock symbols to analyze
	# Note: FAKE1 and FAKE2 are test symbols with intentionally missing data
	# symbollist = ["PSX", "FAKE1", "FAKE2"]  # Alternative: multiple symbols
	symbollist = ["FAKE2"]  # Using single symbol for demonstration
	
	# Define date range for analysis
	start_date = '2005-12-31'
	end_date = '2014-12-07'
	
	# Create date range index
	idx = pd.date_range(start_date, end_date)
	
	# Get adjusted close prices for each symbol
	df_data = get_data(symbollist, idx)
	
	# Fill missing values using forward fill (ffill)
	# Forward fill: propagate last valid observation forward
	# This fills gaps with the most recent known value
	# Note: Using ffill() for pandas 2.0+ compatibility
	df_data.ffill(inplace=True)
	
	# Plot the data
	plot(df_data)
"""

 

"""================================================================="""

"""
Part 2: Fill Missing Values - Complete Implementation
------------------------------------------------------
This section implements a more robust fill_missing_values() function that:
1. First uses forward fill (ffill) to fill gaps with previous values
2. Then uses backward fill (bfill) to fill any remaining gaps with next values

This two-step approach ensures all missing values are filled, even at the
beginning of the dataset where forward fill cannot work.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def fill_missing_values(df_data):
	"""
	Fill missing values in data frame using forward and backward fill.
	
	Strategy:
	1. Forward fill (ffill): Fill missing values with the last valid observation
	   - Works for gaps in the middle and end of the dataset
	   - Cannot fill values at the beginning (no previous value exists)
	
	2. Backward fill (bfill): Fill remaining missing values with the next valid observation
	   - Fills any remaining gaps at the beginning of the dataset
	   - Ensures complete data coverage
	
	Args:
		df_data: DataFrame with missing values (modified in place)
	
	Example:
		Original: [NaN, NaN, 100, NaN, 200, NaN]
		After ffill: [NaN, NaN, 100, 100, 200, 200]
		After bfill: [100, 100, 100, 100, 200, 200]
	
	Note: Updated for pandas 2.0+ compatibility
	- Old syntax: fillna(method="ffill") is deprecated
	- New syntax: Use ffill() and bfill() methods directly
	"""
	##########################################################
	# QUIZ: Your code here (DO NOT modify anything else)
	# Step 1: Forward fill - propagate last valid value forward
	# Updated for pandas 2.0+: use ffill() instead of fillna(method="ffill")
	df_data.ffill(inplace=True)
	
	# Step 2: Backward fill - fill any remaining gaps (typically at start)
	# with the next valid value
	# Updated for pandas 2.0+: use bfill() instead of fillna(method="bfill")
	df_data.bfill(inplace=True)
	##########################################################

def symbol_to_path(symbol, base_dir="data"):
	"""
	Return CSV file path given ticker symbol.
	
	Args:
		symbol: Stock ticker symbol (e.g., 'SPY', 'JAVA')
		base_dir: Base directory containing CSV files (default: "data")
	
	Returns:
		Full path to the CSV file for the given symbol
	"""
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
	"""
	Read stock data (adjusted close) for given symbols from CSV files.
	
	This function:
	- Creates a DataFrame with the specified date range
	- Automatically adds SPY as a reference if not present
	- Reads each symbol's CSV file and joins the data
	- Removes dates where SPY did not trade
	
	Args:
		symbols: List of stock ticker symbols
		dates: Date range (pandas DatetimeIndex)
	
	Returns:
		DataFrame with dates as index and symbols as columns
		Contains NaN values for missing data points
	"""
	df_final = pd.DataFrame(index=dates)
	
	# Add SPY for reference if absent
	if "SPY" not in symbols:
		symbols.insert(0, "SPY")

	# Read and join data for each symbol
	for symbol in symbols:
		file_path = symbol_to_path(symbol)
		# Read CSV with Date as index, only Adj Close column
		df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
		                     usecols=["Date", "Adj Close"], na_values=["nan"])
		# Rename column to symbol name
		df_temp = df_temp.rename(columns={"Adj Close": symbol})
		# Join with main dataframe
		df_final = df_final.join(df_temp)
		
		# Drop dates where SPY did not trade (market holidays)
		if symbol == "SPY":
			df_final = df_final.dropna(subset=["SPY"])

	return df_final

def plot_data(df_data):
	"""
	Plot stock data with appropriate axis labels.
	
	Args:
		df_data: DataFrame with dates as index and stock prices as columns
	"""
	ax = df_data.plot(title="Stock Data", fontsize=12)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	plt.tight_layout()  # Adjust layout to prevent label cutoff
	# Use non-blocking mode for better compatibility
	try:
		plt.show(block=False)
		plt.pause(0.1)  # Brief pause to allow plot to render
	except:
		plt.show()  # Fallback to blocking mode if non-blocking fails

def test_run():
	"""
	Main test function that demonstrates filling missing values.
	
	This function:
	1. Reads stock data for multiple symbols (including test symbols with missing data)
	2. Applies fill_missing_values() to handle incomplete data
	3. Plots the results to visualize the filled data
	
	Note: Modified to use actual available stock symbols (SPY, XOM, GOOG, GLD)
	instead of test symbols (JAVA, FAKE1, FAKE2) which don't exist in the data directory.
	"""
	# Read data
	# Original: symbol_list = ["JAVA", "FAKE1", "FAKE2"]  # Test symbols with missing data
	# Modified to use actual available symbols
	symbol_list = ["XOM", "GOOG", "GLD"]  # List of symbols to analyze (SPY added automatically)
	start_date = "2010-01-01"  # Adjusted to match available data range
	end_date = "2012-12-31"    # Adjusted to match available data range
	dates = pd.date_range(start_date, end_date)  # Create date range index
	df_data = get_data(symbol_list, dates)  # Get data for each symbol

	print("=" * 70)
	print("BEFORE FILLING MISSING VALUES:")
	print("=" * 70)
	print(f"DataFrame shape: {df_data.shape}")
	print(f"Total missing values: {df_data.isna().sum().sum()}")
	print(f"Missing values per column:")
	print(df_data.isna().sum())
	print("\nFirst few rows with missing values:")
	print(df_data.head(10))
	
	# Fill missing values using forward and backward fill
	fill_missing_values(df_data)
	
	print("\n" + "=" * 70)
	print("AFTER FILLING MISSING VALUES:")
	print("=" * 70)
	print(f"Total missing values: {df_data.isna().sum().sum()}")
	print(f"Missing values per column:")
	print(df_data.isna().sum())
	print("\nFirst few rows after filling:")
	print(df_data.head(10))
	print("=" * 70)

	# Plot the filled data
	print("\nGenerating plot...")
	plot_data(df_data)
	print("Plot displayed. Close the plot window to continue.")

if __name__ == "__main__":
	test_run()
