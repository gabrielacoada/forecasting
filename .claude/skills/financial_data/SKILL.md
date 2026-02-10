# Financial Data Acquisition Skill

## Purpose
Fetch high-frequency financial data (crypto, stocks, forex) for time series analysis in econometrics homework. Designed to work across multiple problem sets with different data requirements.

## Core Capabilities
- Fetch daily/hourly cryptocurrency returns (Bitcoin, Ethereum, etc.)
- Fetch stock market data (S&P 500, individual stocks)
- Fetch economic indicators from FRED (when needed for future problem sets)
- Calculate log returns automatically
- Handle missing data appropriately
- Export to CSV for reproducibility

## Dependencies
```python
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
```

## Best Practices

### 1. Data Fetching Template
```python
def fetch_crypto_returns(ticker='BTC-USD', start_date='2020-01-01', end_date=None):
    """
    Fetch cryptocurrency data and compute returns.
    
    Parameters:
    -----------
    ticker : str
        Yahoo Finance ticker (e.g., 'BTC-USD', 'ETH-USD')
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str or None
        End date in 'YYYY-MM-DD' format (None = today)
    
    Returns:
    --------
    pd.DataFrame with columns: ['Date', 'Close', 'Returns', 'LogReturns']
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    # Calculate returns
    df = pd.DataFrame()
    df['Date'] = data.index
    df['Close'] = data['Close'].values
    df['Returns'] = data['Close'].pct_change() * 100  # Percentage returns
    df['LogReturns'] = np.log(data['Close'] / data['Close'].shift(1)) * 100
    
    # Remove first NaN observation
    df = df.dropna()
    df = df.reset_index(drop=True)
    
    return df
```

### 2. For Stock Data
```python
def fetch_stock_returns(ticker='SPY', start_date='2020-01-01', end_date=None):
    """Same structure as crypto but for stocks"""
    # Use same logic as fetch_crypto_returns
    pass
```

### 3. Data Quality Checks
Always include these checks after fetching:
```python
# Check for missing values
print(f"Missing values: {df.isnull().sum().sum()}")

# Check for outliers (returns > 50% unusual for daily data)
outliers = df[abs(df['Returns']) > 50]
if len(outliers) > 0:
    print(f"Warning: {len(outliers)} potential outliers detected")

# Summary statistics
print(df[['Returns', 'LogReturns']].describe())
```

### 4. Save Data for Reproducibility
```python
# Save to data/raw/ directory
df.to_csv('data/raw/crypto_returns.csv', index=False)
print(f"Data saved: {len(df)} observations from {df['Date'].min()} to {df['Date'].max()}")
```

## Common Use Cases

### Problem Set 1: MA(1) Analysis, Volatility
- Fetch 2-5 years of daily crypto returns
- Focus on Bitcoin (most liquid, least missing data)
- Need squared returns for volatility analysis

### Future Problem Sets: Unit Roots, Cointegration
- May need level data (prices) not returns
- May need multiple series for cointegration
- May need economic indicators from FRED

## Recommended Data Sources by Asset Type

### Cryptocurrency (via yfinance)
- **Bitcoin**: 'BTC-USD' (most liquid, best for homework)
- **Ethereum**: 'ETH-USD' (second most liquid)
- **Others**: Available but may have missing data issues

### Stock Indices (via yfinance)
- **S&P 500**: 'SPY' or '^GSPC'
- **NASDAQ**: 'QQQ' or '^IXIC'
- **Individual stocks**: Use ticker symbol (e.g., 'AAPL')

### Economic Data (for future problem sets)
- Use `pandas_datareader` with FRED API
- Free API key from FRED website
- Examples: GDP, inflation, unemployment

## Error Handling
```python
try:
    df = fetch_crypto_returns('BTC-USD', start_date='2020-01-01')
except Exception as e:
    print(f"Error fetching data: {e}")
    print("Trying alternative ticker or date range...")
```

## Output Format
Always return/save data with these columns at minimum:
- **Date**: Timestamp index
- **Close**: Price level (for plotting)
- **Returns**: Simple returns in percentage
- **LogReturns**: Log returns in percentage (preferred for analysis)

For Problem Set 1, the main series is returns (et), so focus on 'Returns' or 'LogReturns' column.