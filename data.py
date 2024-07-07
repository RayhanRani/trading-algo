'''
import yfinance as yf
import pandas as pd
import numpy as np

# Function to fetch historical data
def get_historical_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if not data.empty:
            return data
        else:
            print(f"No data for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to calculate True Range
def true_range(data):
    data['high_low'] = data['High'] - data['Low']
    data['high_close'] = np.abs(data['High'] - data['Close'].shift())
    data['low_close'] = np.abs(data['Low'] - data['Close'].shift())
    data['true_range'] = data[['high_low', 'high_close', 'low_close']].max(axis=1)
    return data

# Function to calculate ATR
def average_true_range(data, window=14):
    data = true_range(data)
    data['atr'] = data['true_range'].rolling(window=window).mean()
    return data

# Get a list of S&P 500 stock symbols
sp500_symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

start_date = '2023-07-04'
end_date = '2024-07-04'

# Dictionary to store ATR values and 52-week high/low
stock_metrics = {}

# Fetch data and calculate ATR and 52-week high/low for each stock
for symbol in sp500_symbols:
    data = get_historical_data(symbol, start_date, end_date)
    if data is not None:
        data = average_true_range(data)
        latest_atr = data['atr'].iloc[-1]  # Get the latest ATR value
        high_52week = data['High'].max()
        low_52week = data['Low'].min()
        current_price = data['Close'].iloc[-1]
        
        stock_metrics[symbol] = {
            'ATR': latest_atr,
            '52_Week_High': high_52week,
            '52_Week_Low': low_52week,
            'Current_Price': current_price
        }
    else:
        stock_metrics[symbol] = {
            'ATR': None,
            '52_Week_High': None,
            '52_Week_Low': None,
            'Current_Price': None
        }

# Convert to DataFrame for easier analysis
metrics_df = pd.DataFrame.from_dict(stock_metrics, orient='index')

# Filter stocks with high volatility (for example, top 10% by ATR value)
high_volatility_stocks = metrics_df.sort_values(by='ATR', ascending=False).head(int(len(metrics_df) * 0.10))

print(high_volatility_stocks)
'''
'''
#Benchmark for Stocks Algo Using S&P 500

# Define the ticker symbol for the S&P 500 Index
ticker_symbol = '^GSPC'

# Get data for the last 10 years
sp500_data = yf.download(ticker_symbol, start='2013-01-01', end='2023-01-01')

# Select the required columns: Open, High, Low, Close
sp500_data = sp500_data[['Open', 'High', 'Low', 'Close']]

# Save Data to a CSV File
sp500_data.to_csv('sp500_10_years_data.csv')

# Display the first few rows of the data
print(sp500_data.head())

#Testing AAPL Stock in S&P 500

'''

import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    volume_traded = stock.history(period="10y")['Volume']
    return volume_traded

def main():
    ticker = input("Enter a stock ticker: ")
    volume_traded = get_stock_data(ticker)

    print(f"Volume Traded for {ticker}:")
    print(volume_traded)
    
    # Prepare the data for DataFrame
    data = {
        "Volume Traded": volume_traded
    }

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(f'{ticker}_volume_traded.csv', index=False)
    print(f'Data for {ticker} has been saved to {ticker}_volume_traded.csv')

if __name__ == "__main__":
    main()

