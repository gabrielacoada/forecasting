# Problem Set 1: Time Series Properties and MA Processes

## Overview
This problem set focuses on fundamental time series properties, MA process theory, and empirical analysis of financial returns.

## Problems
1. **MA(1) Theoretical Constraints**: Why is corr(yt, yt-1) = 0.7 incompatible with MA(1)?
2. **White Noise Summation**: Under what conditions is the sum of two white noise processes also white noise?
3. **Financial Returns Analysis**: 
   - (a) Plot and describe high-frequency return series
   - (b) ACF/PACF analysis and interpretation
   - (c) Squared returns visualization
   - (d) Volatility persistence testing

## Data
- **Asset**: Bitcoin (BTC-USD)
- **Frequency**: Daily
- **Period**: Last 2 years
- **Source**: Yahoo Finance via yfinance
- **File**: `data/raw/btc_returns.csv`

## Files
- `Hwk1.pdf` - Original problem set
- `hwk1_analysis.ipynb` - Main deliverable (Jupyter notebook)
- `requirements.txt` - Python dependencies
- `data/raw/` - Raw data files
- `outputs/figures/` - Generated plots
- `outputs/tables/` - Results tables (if any)

## How to Run

### Using Claude Code (Recommended)
```bash
# From repo root
claude "Run the homework pipeline for Problem Set 1"
```

### Manual Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Run Jupyter notebook
jupyter notebook hwk1_analysis.ipynb
```

## Expected Outputs

### Figures
1. `returns_timeseries.png` - Time series plot of returns
2. `returns_correlogram.png` - ACF and PACF of returns
3. `squared_returns_analysis.png` - Squared returns and ACF analysis
4. `ma1_theoretical_bounds.png` - MA(1) feasibility visualization

### Analysis Results
- Summary statistics for returns
- White noise test results (Ljung-Box)
- Autocorrelation coefficients
- Volatility clustering assessment

## Key Concepts Covered
- MA(q) process properties and invertibility
- Theoretical autocorrelation bounds
- White noise testing
- ACF/PACF interpretation
- Volatility clustering and ARCH effects
- Financial returns stylized facts

## Skills Used
- `financial_data/SKILL.md` - Data acquisition
- `time_series_viz/SKILL.md` - Plotting and visualization
- `econometric_analysis/SKILL.md` - Statistical testing
- `jupyter_notebook_gen/SKILL.md` - Notebook generation

## Notes
- Bitcoin was chosen for its high liquidity and data availability
- Daily frequency provides sufficient observations for reliable inference
- Squared returns analysis reveals time-varying volatility common in financial data