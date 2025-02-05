#!/usr/bin/env python3
"""
Price Analysis and Signal Visualization Tool

This script:
  1. Loads historical price data from a CSV file.
  2. Plots the time series.
  3. Computes and plots the FFT (frequency spectrum) to detect dominant frequencies.
  4. Computes and plots the rolling variance to highlight spikes/transients.
  5. Estimates the Hurst exponent as an indicator of fractal/chaotic behavior.
  
Requirements:
  - pandas
  - numpy
  - matplotlib
  - scipy

Usage:
  python signalviz.py historical_data.csv
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# ---------------------------
# Data Loading and Preprocessing
# ---------------------------
def load_csv_data(filename):
    """
    Load CSV data and return a DataFrame.
    The CSV is expected to have at least 'Date' and 'Price' columns.
    """
    try:
        df = pd.read_csv(filename)
        # Convert Date column to datetime and sort
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print("Error loading CSV:", e)
        sys.exit(1)

# ---------------------------
# Time Series Plotting
# ---------------------------
def plot_time_series(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Price'], label='Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Asset Price Over Time')
    plt.legend()
    plt.grid(True)

# ---------------------------
# FFT Analysis
# ---------------------------
def plot_fft(df):
    """
    Compute FFT on the price series and plot the amplitude spectrum.
    """
    # Use the Price series as a numpy array.
    prices = df['Price'].values
    n = len(prices)
    
    # Compute FFT and frequency bins.
    yf = fft(prices - np.mean(prices))  # remove mean to focus on oscillations
    xf = fftfreq(n, d=1)  # assume uniform sampling (d=1 day or index unit)
    
    # Only take the positive frequencies
    pos_mask = xf > 0
    xf_pos = xf[pos_mask]
    yf_pos = np.abs(yf[pos_mask])
    
    plt.figure(figsize=(12, 6))
    plt.plot(xf_pos, yf_pos, color='red')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title('FFT Spectrum of Price Series')
    plt.grid(True)

# ---------------------------
# Rolling Variance Analysis
# ---------------------------
def plot_rolling_variance(df, window=20):
    """
    Compute and plot the rolling variance of the price series.
    """
    df['RollingVariance'] = df['Price'].rolling(window=window).var()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['RollingVariance'], label=f'Rolling Variance (window={window})', color='green')
    plt.xlabel('Date')
    plt.ylabel('Variance')
    plt.title('Rolling Variance of Price Series')
    plt.legend()
    plt.grid(True)

# ---------------------------
# Hurst Exponent Estimation
# ---------------------------
def hurst_exponent(ts):
    """
    Estimate the Hurst exponent of a time series ts.
    A simple method based on the rescaled range (R/S) analysis.
    Returns a value between 0 and 1.
    """
    lags = range(2, min(100, len(ts)//2))
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    # Fit a line to log-log plot
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    hurst = poly[0] * 2.0
    return hurst

def print_hurst_exponent(df):
    prices = df['Price'].values
    h = hurst_exponent(prices)
    print(f"Estimated Hurst Exponent: {h:.4f}")
    if h < 0.5:
        print("Indication: Mean-reverting behavior (anti-persistent)")
    elif h == 0.5:
        print("Indication: Random walk (Brownian motion)")
    else:
        print("Indication: Trending behavior (persistent)")

# ---------------------------
# Main Routine
# ---------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python signalviz.py <csv_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    df = load_csv_data(filename)
    
    # Plot the original time series.
    plot_time_series(df)
    
    # Plot FFT spectrum.
    plot_fft(df)
    
    # Plot rolling variance to highlight transients/spikes.
    plot_rolling_variance(df, window=20)
    
    # Estimate and print the Hurst exponent.
    print_hurst_exponent(df)
    
    # Show all plots.
    plt.show()

if __name__ == '__main__':
    main()
