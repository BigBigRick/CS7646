"""
Exercise 1.6: Histograms and Scatterplots
==========================================

(c) 2015 by Devpriya Dave and Tucker Balch.

TITLE: Stock Return Distribution Analysis and Correlation Visualization

PURPOSE:
--------
This exercise demonstrates how to:
1. Compute and visualize daily returns using histograms
2. Calculate statistical measures (mean, std, kurtosis)
3. Compare multiple stocks using overlapping histograms
4. Analyze correlations using scatterplots with regression lines

SCRIPT STRUCTURE:
-----------------
Part 1: Basic Histogram Plotting
  - Compute daily returns
  - Plot histogram with different bin counts

Part 2: Histogram Statistics
  - Calculate mean and standard deviation
  - Visualize statistics on histogram
  - Compute kurtosis

Part 3: Multiple Histograms Comparison
  - Plot separate histograms
  - Overlay histograms on same chart

Part 4: Scatterplots and Correlation
  - Create scatterplots between stocks
  - Fit regression lines (beta and alpha)
  - Analyze relationships between assets

KEY FUNCTIONS:
--------------
1. compute_daily_returns(df)
   - Computes daily return values
   - Formula: (price[t] / price[t-1]) - 1
   - Returns DataFrame with daily returns

2. get_data(symbols, dates)
   - Retrieves stock data from CSV files
   - Returns normalized DataFrame

3. plot_data(df, title, ylabel)
   - Visualizes time series data
"""

"""=================================================================================="""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def symbol_to_path(symbol, base_dir="data"):
	"""Return CSV file path given ticker symbol."""
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
	"""Read stock data (adjusted close) for given symbols from CSV files."""
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

def plot_data(df, title="Stock prices", ylabel="Price"):
	"""Plot stock prices with a custom title and meaningful axis labels."""
	ax = df.plot(title=title, fontsize=12)
	ax.set_xlabel("Date")
	ax.set_ylabel(ylabel)
	plt.tight_layout()
	try:
		plt.show(block=False)
		plt.pause(0.1)
	except:
		plt.show()

def compute_daily_returns(df):
	"""Compute and return the daily return values."""
	daily_returns = df.copy()
	daily_returns[1:] = (df[1:] / df[:-1].values) - 1
	daily_returns.iloc[0, :] = 0  # set daily returns for row 0 to 0 (updated from .ix to .iloc)
	return daily_returns

"""==============================================================================="""
"""Part 1: Plot a histogram."""

def test_run_part1():
	"""Basic histogram plotting example."""
	# Read data
	dates = pd.date_range('2009-01-01', '2012-12-31')
	symbols = ['SPY']
	df = get_data(symbols, dates)
	plot_data(df)
	
	# Compute daily returns
	daily_returns = compute_daily_returns(df)
	plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")
	
	# Plot a histogram
	daily_returns.hist()  # default number of bins, 10
	daily_returns.hist(bins=20)  # changing no. of bins to 20
	plt.show()

"""==============================================================================="""
"""Part 2: Computing Histogram Statistics"""

def test_run_part2():
	"""Histogram with statistics (mean, std, kurtosis)."""
	# Read data
	dates = pd.date_range('2009-01-01', '2012-12-31')
	symbols = ['SPY']
	df = get_data(symbols, dates)
	plot_data(df)
	
	# Compute daily returns
	daily_returns = compute_daily_returns(df)
	plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")
	
	# Plot a histogram
	daily_returns.hist(bins=20)  # changing no. of bins to 20
	
	# Get mean and standard deviation
	mean = daily_returns['SPY'].mean()
	print("mean=", mean)
	std = daily_returns['SPY'].std()
	print("std=", std)
	
	plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
	plt.axvline(std, color='r', linestyle='dashed', linewidth=2)
	plt.axvline(-std, color='r', linestyle='dashed', linewidth=2)
	plt.show()
	
	# Compute kurtosis
	print(daily_returns.kurtosis())

"""==============================================================================="""	
"""Part 3: Plot Two Histograms together"""

def test_run_part3():
	"""Compare multiple stocks using histograms."""
	# Read data
	dates = pd.date_range('2009-01-01', '2012-12-31')
	symbols = ['SPY', 'XOM']
	df = get_data(symbols, dates)
	plot_data(df)
	
	""" Two separate histograms ==========="""
	# Compute daily returns
	daily_returns = compute_daily_returns(df)
	plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")
	
	# Plot a histogram
	daily_returns.hist(bins=20) 
	plt.show()

	""" Histograms on the same graph ======"""
	# Compute daily returns
	daily_returns = compute_daily_returns(df)
	
	# Compute and plot both histograms on the same chart
	daily_returns['SPY'].hist(bins=20, label="SPY")
	daily_returns['XOM'].hist(bins=20, label="XOM")
	plt.legend(loc='upper right')
	plt.show()

"""==============================================================================="""	
"""Part 4: Scatterplots."""

def test_run_part4():
	"""Scatterplots with regression lines."""
	# Read data
	dates = pd.date_range('2009-01-01', '2012-12-31')
	symbols = ['SPY', 'XOM', 'GLD']
	df = get_data(symbols, dates)
	
	# Compute daily returns
	daily_returns = compute_daily_returns(df)
	
	# Scatterplot SPY vs XOM
	daily_returns.plot(kind='scatter', x='SPY', y='XOM')
	beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'], 1)
	print("beta_XOM= ", beta_XOM)
	print("alpha_XOM=", alpha_XOM)
	plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY'] + alpha_XOM, '-', color='r')
	plt.show()
	
	# Scatterplot SPY vs GLD
	daily_returns.plot(kind='scatter', x='SPY', y='GLD')
	beta_GLD, alpha_GLD = np.polyfit(daily_returns['SPY'], daily_returns['GLD'], 1)
	print("beta_GLD= ", beta_GLD)
	print("alpha_GLD=", alpha_GLD)
	plt.plot(daily_returns['SPY'], beta_GLD*daily_returns['SPY'] + alpha_GLD, '-', color='r')
	plt.show()

"""==============================================================================="""
"""Main execution - uncomment the part you want to run"""

if __name__ == "__main__":
	# Uncomment the part you want to run:
	
	# Part 1: Basic histogram
	# test_run_part1()
	
	# Part 2: Histogram with statistics
	# test_run_part2()
	
	# Part 3: Multiple histograms
	# test_run_part3()
	
	# Part 4: Scatterplots
	test_run_part4()
