"""
Exercise 1.7: Portfolio Optimization
====================================

(c) 2015 by Devpriya Dave and Tucker Balch.

TITLE: Portfolio Allocation and Performance Analysis

PURPOSE:
--------
This exercise demonstrates how to:
1. Build a portfolio with multiple stocks
2. Normalize prices and apply allocations
3. Calculate portfolio value over time
4. Compute portfolio statistics (cumulative return, daily returns, Sharpe ratio)
5. Optimize portfolio allocation

SCRIPT STRUCTURE:
-----------------
Part 1: Basic Portfolio Construction
  - Load stock data
  - Normalize prices
  - Apply allocations
  - Calculate position values
  - Compute portfolio value

Part 2: Portfolio Statistics
  - Calculate daily returns
  - Compute cumulative return
  - Calculate average daily return
  - Calculate standard deviation of daily returns

Part 3: Sharpe Ratio
  - Calculate Sharpe ratio
  - Compare different portfolios

Part 4: Portfolio Optimization
  - Find optimal allocation
  - Compare different allocation strategies

KEY FUNCTIONS:
--------------
1. get_data(symbols, dates)
   - Retrieves stock data from CSV files
   - Returns normalized DataFrame

2. normalize_data(df)
   - Normalizes prices to start at 1.0
   - Formula: prices / prices[0]

3. compute_portfolio_value(prices, allocs, start_val)
   - Applies allocations to normalized prices
   - Calculates position values
   - Returns portfolio value over time

4. compute_daily_returns(port_val)
   - Computes daily returns of portfolio
   - Formula: (port_val[t] / port_val[t-1]) - 1

5. compute_sharpe_ratio(daily_returns, k=252, risk_free_rate=0.0)
   - Calculates annualized Sharpe ratio
   - Formula: sqrt(k) * mean(daily_returns - risk_free_rate) / std(daily_returns)
"""

"""=================================================================================="""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import minimize

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
		
		# Drop dates where SPY did not traded (market holidays)
		if symbol == "SPY":
			df_final = df_final.dropna(subset=["SPY"])

	return df_final

def normalize_data(df):
	"""Normalize stock prices to start at 1.0."""
	return df / df.iloc[0]

def compute_portfolio_value(prices, allocs, start_val):
	"""
	Compute portfolio value over time.
	
	Parameters:
	- prices: DataFrame of normalized prices
	- allocs: List of allocations (must sum to 1.0)
	- start_val: Starting portfolio value
	
	Returns:
	- Series of portfolio values over time
	"""
	# Normalize prices if not already normalized
	normed = prices / prices.iloc[0]
	
	# Apply allocations
	alloced = normed * allocs
	
	# Calculate position values
	pos_vals = alloced * start_val
	
	# Portfolio value is sum of all positions
	port_val = pos_vals.sum(axis=1)
	
	return port_val

def compute_daily_returns(port_val):
	"""Compute and return the daily return values."""
	daily_returns = port_val.copy()
	daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
	daily_returns.iloc[0] = 0  # set daily returns for row 0 to 0
	return daily_returns

def compute_portfolio_stats(port_val, daily_rf=0.0, samples_per_year=252):
	"""
	Compute portfolio statistics.
	
	Parameters:
	- port_val: Series of portfolio values
	- daily_rf: Daily risk-free rate (default 0.0)
	- samples_per_year: Number of trading days per year (default 252)
	
	Returns:
	- Dictionary with statistics
	"""
	# Compute daily returns
	daily_rets = compute_daily_returns(port_val)
	daily_rets = daily_rets[1:]  # Remove first row (0)
	
	# Cumulative return
	cum_ret = (port_val.iloc[-1] / port_val.iloc[0]) - 1
	
	# Average daily return
	avg_daily_ret = daily_rets.mean()
	
	# Standard deviation of daily returns
	std_daily_ret = daily_rets.std()
	
	# Sharpe ratio (annualized)
	sharpe_ratio = np.sqrt(samples_per_year) * (avg_daily_ret - daily_rf) / std_daily_ret
	
	return {
		'cum_ret': cum_ret,
		'avg_daily_ret': avg_daily_ret,
		'std_daily_ret': std_daily_ret,
		'sharpe_ratio': sharpe_ratio
	}

"""==============================================================================="""
"""Part 1: Basic Portfolio Construction"""

def test_run_part1():
	"""Basic portfolio construction example."""
	# Parameters
	start_val = 1000000
	start_date = '2009-01-01'
	end_date = '2011-12-31'
	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	allocs = [0.4, 0.4, 0.1, 0.1]
	
	# Read data
	dates = pd.date_range(start_date, end_date)
	prices = get_data(symbols, dates)
	
	# Normalize prices
	normed = normalize_data(prices)
	print("Normalized prices (first few rows):")
	print(normed.head())
	
	# Apply allocations
	alloced = normed * allocs
	print("\nAllocated prices (first few rows):")
	print(alloced.head())
	
	# Calculate position values
	pos_vals = alloced * start_val
	print("\nPosition values (first few rows):")
	print(pos_vals.head())
	
	# Portfolio value
	port_val = pos_vals.sum(axis=1)
	print("\nPortfolio value (first few rows):")
	print(port_val.head())
	print("\nPortfolio value (last few rows):")
	print(port_val.tail())
	
	# Plot portfolio value
	port_val.plot(title="Portfolio Value Over Time", fontsize=12)
	plt.xlabel("Date")
	plt.ylabel("Portfolio Value ($)")
	plt.tight_layout()
	plt.show()

"""==============================================================================="""
"""Part 2: Portfolio Statistics"""

def test_run_part2():
	"""Calculate portfolio statistics."""
	# Parameters
	start_val = 1000000
	start_date = '2009-01-01'
	end_date = '2011-12-31'
	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	allocs = [0.4, 0.4, 0.1, 0.1]
	
	# Read data
	dates = pd.date_range(start_date, end_date)
	prices = get_data(symbols, dates)
	
	# Compute portfolio value
	port_val = compute_portfolio_value(prices, allocs, start_val)
	
	# Compute daily returns
	daily_rets = compute_daily_returns(port_val)
	daily_rets = daily_rets[1:]  # Remove first row
	
	# Calculate statistics
	stats = compute_portfolio_stats(port_val)
	
	print("Portfolio Statistics:")
	print("=" * 50)
	print(f"Cumulative Return: {stats['cum_ret']:.4f} ({stats['cum_ret']*100:.2f}%)")
	print(f"Average Daily Return: {stats['avg_daily_ret']:.6f} ({stats['avg_daily_ret']*100:.4f}%)")
	print(f"Std Daily Return: {stats['std_daily_ret']:.6f} ({stats['std_daily_ret']*100:.4f}%)")
	print(f"Sharpe Ratio: {stats['sharpe_ratio']:.4f}")
	
	# Plot daily returns
	daily_rets.plot(title="Portfolio Daily Returns", fontsize=12)
	plt.xlabel("Date")
	plt.ylabel("Daily Returns")
	plt.axhline(y=0, color='r', linestyle='--')
	plt.tight_layout()
	plt.show()

"""==============================================================================="""
"""Part 3: Sharpe Ratio Comparison"""

def test_run_part3():
	"""Compare different portfolios using Sharpe ratio."""
	# Parameters
	start_val = 1000000
	start_date = '2009-01-01'
	end_date = '2011-12-31'
	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	
	# Different allocation strategies
	allocs_list = [
		[0.4, 0.4, 0.1, 0.1],  # Equal weight SPY and XOM
		[0.25, 0.25, 0.25, 0.25],  # Equal weight all
		[0.0, 0.0, 0.0, 1.0],  # All in GLD
		[1.0, 0.0, 0.0, 0.0],  # All in SPY
	]
	
	allocs_names = [
		"SPY+XOM heavy",
		"Equal weight",
		"All GLD",
		"All SPY"
	]
	
	# Read data
	dates = pd.date_range(start_date, end_date)
	prices = get_data(symbols, dates)
	
	print("Portfolio Comparison:")
	print("=" * 70)
	print(f"{'Strategy':<20} {'Cum Ret':<12} {'Avg Daily Ret':<15} {'Sharpe Ratio':<12}")
	print("-" * 70)
	
	for allocs, name in zip(allocs_list, allocs_names):
		port_val = compute_portfolio_value(prices, allocs, start_val)
		stats = compute_portfolio_stats(port_val)
		
		print(f"{name:<20} {stats['cum_ret']*100:>10.2f}%  {stats['avg_daily_ret']*100:>12.4f}%  {stats['sharpe_ratio']:>10.4f}")
	
	# Plot all portfolios
	plt.figure(figsize=(12, 6))
	for allocs, name in zip(allocs_list, allocs_names):
		port_val = compute_portfolio_value(prices, allocs, start_val)
		# Normalize to start at 1.0 for comparison
		port_val_norm = port_val / port_val.iloc[0]
		port_val_norm.plot(label=name)
	
	plt.title("Portfolio Value Comparison (Normalized)", fontsize=14)
	plt.xlabel("Date")
	plt.ylabel("Normalized Portfolio Value")
	plt.legend(loc='best')
	plt.tight_layout()
	plt.show()

"""==============================================================================="""
"""Part 4: Portfolio Optimization"""

def negative_sharpe(allocs, prices, start_val, daily_rf=0.0, samples_per_year=252):
	"""Negative Sharpe ratio for minimization."""
	port_val = compute_portfolio_value(prices, allocs, start_val)
	stats = compute_portfolio_stats(port_val, daily_rf, samples_per_year)
	return -stats['sharpe_ratio']

def optimize_portfolio(prices, start_val, daily_rf=0.0, samples_per_year=252):
	"""
	Find optimal allocation that maximizes Sharpe ratio.
	
	Parameters:
	- prices: DataFrame of stock prices
	- start_val: Starting portfolio value
	- daily_rf: Daily risk-free rate
	- samples_per_year: Number of trading days per year
	
	Returns:
	- Optimal allocations
	"""
	num_stocks = len(prices.columns)
	
	# Initial guess: equal weights
	initial_allocs = np.array([1.0 / num_stocks] * num_stocks)
	
	# Constraints: allocations must sum to 1.0
	constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
	
	# Bounds: each allocation between 0 and 1
	bounds = tuple((0, 1) for _ in range(num_stocks))
	
	# Minimize negative Sharpe ratio (equivalent to maximizing Sharpe ratio)
	result = minimize(negative_sharpe, initial_allocs, 
	                  args=(prices, start_val, daily_rf, samples_per_year),
	                  method='SLSQP', bounds=bounds, constraints=constraints)
	
	return result.x

def test_run_part4():
	"""Optimize portfolio allocation."""
	# Parameters
	start_val = 1000000
	start_date = '2009-01-01'
	end_date = '2011-12-31'
	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	
	# Read data
	dates = pd.date_range(start_date, end_date)
	prices = get_data(symbols, dates)
	
	# Initial allocation
	initial_allocs = [0.4, 0.4, 0.1, 0.1]
	
	print("Initial Portfolio:")
	print("=" * 50)
	port_val_initial = compute_portfolio_value(prices, initial_allocs, start_val)
	stats_initial = compute_portfolio_stats(port_val_initial)
	print(f"Allocations: {dict(zip(symbols, initial_allocs))}")
	print(f"Cumulative Return: {stats_initial['cum_ret']*100:.2f}%")
	print(f"Sharpe Ratio: {stats_initial['sharpe_ratio']:.4f}")
	
	# Optimize
	print("\nOptimizing portfolio...")
	optimal_allocs = optimize_portfolio(prices, start_val)
	
	print("\nOptimal Portfolio:")
	print("=" * 50)
	print(f"Allocations: {dict(zip(symbols, optimal_allocs))}")
	port_val_optimal = compute_portfolio_value(prices, optimal_allocs, start_val)
	stats_optimal = compute_portfolio_stats(port_val_optimal)
	print(f"Cumulative Return: {stats_optimal['cum_ret']*100:.2f}%")
	print(f"Sharpe Ratio: {stats_optimal['sharpe_ratio']:.4f}")
	
	# Compare
	print("\nImprovement:")
	print("=" * 50)
	print(f"Sharpe Ratio improvement: {stats_optimal['sharpe_ratio'] - stats_initial['sharpe_ratio']:.4f}")
	print(f"Cumulative Return difference: {(stats_optimal['cum_ret'] - stats_initial['cum_ret'])*100:.2f}%")
	
	# Plot comparison
	plt.figure(figsize=(12, 6))
	port_val_initial_norm = port_val_initial / port_val_initial.iloc[0]
	port_val_optimal_norm = port_val_optimal / port_val_optimal.iloc[0]
	port_val_initial_norm.plot(label="Initial Portfolio", linestyle='--')
	port_val_optimal_norm.plot(label="Optimal Portfolio")
	plt.title("Portfolio Value Comparison", fontsize=14)
	plt.xlabel("Date")
	plt.ylabel("Normalized Portfolio Value")
	plt.legend(loc='best')
	plt.tight_layout()
	plt.show()

"""==============================================================================="""
"""Main execution - uncomment the part you want to run"""

if __name__ == "__main__":
	# Uncomment the part you want to run:
	
	# Part 1: Basic portfolio construction
	# test_run_part1()
	
	# Part 2: Portfolio statistics
	# test_run_part2()
	
	# Part 3: Sharpe ratio comparison
	# test_run_part3()
	
	# Part 4: Portfolio optimization
	test_run_part4()
