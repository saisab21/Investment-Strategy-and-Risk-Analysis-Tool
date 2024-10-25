import yfinance as yf
import pandas as pd
from datetime import datetime

# Function to fetch financial data for Indian stocks/indices from Yahoo Finance
def fetch_financial_data(tickers, period="5y", interval="1d"):
    """
    Fetches historical financial data for the provided tickers from Yahoo Finance.
    
    Parameters:
    - tickers (list): List of asset tickers (e.g., ['RELIANCE.NS', '^BSESN']).
    - period (str): Period for historical data (e.g., '5y' for five years).
    - interval (str): Data interval (e.g., '1d' for daily).
    
    Returns:
    - data (DataFrame): Historical data of all tickers.
    """
    try:
        data = yf.download(tickers, period=period, interval=interval, group_by='ticker')
        return data
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        return None

# Function to fetch placeholder sentiment data specific to the Indian market
def fetch_sentiment_data(tickers, source="news"):
    """
    Fetches sentiment data for Indian stocks or indexes using a placeholder.

    Parameters:
    - tickers (list): List of asset tickers (e.g., ['RELIANCE.NS', 'NSEI']).
    - source (str): Source type ('news' or 'social' for future extensions).

    Returns:
    - sentiment_df (DataFrame): DataFrame containing sentiment scores.
    """
    sentiment_rows = []
    
    for ticker in tickers:
        today = datetime.now().date()
        # Placeholder sentiment score; to be replaced with real sentiment score from Indian sources
        sentiment_rows.append({
            "ticker": ticker,
            "date": today,
            "sentiment_score": 0.05  # Placeholder sentiment score
        })
    
    sentiment_df = pd.DataFrame(sentiment_rows)
    return sentiment_df

# Combined fetcher for financial and sentiment data tailored to Indian market
def fetch_data(tickers):
    """
    Fetches both financial and sentiment data for a comprehensive dataset.

    Parameters:
    - tickers (list): List of asset tickers (e.g., ['RELIANCE.NS', 'NSEI']).

    Returns:
    - combined_data (dict): Dictionary containing financial and sentiment data.
    """
    financial_data = fetch_financial_data(tickers)
    sentiment_data = fetch_sentiment_data(tickers)

    combined_data = {
        "financial_data": financial_data,
        "sentiment_data": sentiment_data
    }
    
    return combined_data

# Example usage
tickers = ["RELIANCE.NS", "TCS.NS", "NSEI", "^BSESN"]  # Example Indian stocks and indices
result = fetch_data(tickers)
print(result)


# Explanation
# Tickers for Indian Stocks and Indices: Examples include RELIANCE.NS, TCS.NS, NSEI (NIFTY 50), and ^BSESN (SENSEX).
# Sentiment Data Placeholder: Uses a placeholder score for Indian tickers, which can be updated to fetch sentiment from an Indian finance news API or service in the future.
# This module is ready to pull Indian market data. Let me know when you’re ready to proceed with the next component, Risk Profiling and Dynamic Allocation.