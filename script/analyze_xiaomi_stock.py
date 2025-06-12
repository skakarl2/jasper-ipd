import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def analyze_xiaomi_stock():
    # Xiaomi's stock ticker on HKEX
    ticker = "1810.HK"
    xiaomi = yf.Ticker(ticker)
    
    # Get historical data for the last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Fetch historical data
    df = xiaomi.history(start=start_date, end=end_date)
    
    # Calculate moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # Print basic statistics
    print("\nXiaomi Stock Analysis:")
    print(f"Current Price: ${df['Close'][-1]:.2f}")
    print(f"52-Week High: ${df['High'].max():.2f}")
    print(f"52-Week Low: ${df['Low'].min():.2f}")
    print(f"Average Volume: {df['Volume'].mean():.0f}")
    
    # Plot the stock data
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['MA20'], label='20-day MA')
    plt.plot(df.index, df['MA50'], label='50-day MA')
    plt.title('Xiaomi Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Price (HKD)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_xiaomi_stock()