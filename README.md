# Problem Set 0: Time Series Analysis - Retail Sales for Used Car Dealers

This repository contains the solution to Problem Set #0 for Time Series Analysis/Forecasting.

## Overview

Analysis of monthly retail sales data for used car dealers from FRED (Federal Reserve Economic Data), covering January 1992 to January 2024.

## Data

- **Source**: FRED (Federal Reserve Economic Data)
- **Series ID**: MRTSSM44112USN
- **Frequency**: Monthly, Not Seasonally Adjusted
- **Period**: January 1992 - January 2024
- **Observations**: 385 data points

## Assignment Tasks

1. **Data Acquisition**: Download data from FRED using pandas_datareader
2. **Visualization**: Graph and analyze the time series
3. **Trend Analysis**: Identify the best trend model (linear, quadratic, etc.)
4. **Structural Break Test**: Test for break in 2008
5. **Residual Analysis**: Plot residuals and correlogram
6. **COVID Impact**: Handle the COVID period appropriately
7. **Seasonality**: Include seasonal dummies and test for seasonality
8. **Model Simplification**: Find the best parsimonious model
9. **Final Diagnostics**: Analyze detrended and deseasonalized residuals
10. **Generalization**: Create a reusable function for any FRED series

## Files

- `hwk0_analysis.ipynb`: Main Jupyter notebook with complete analysis
- `Hwk0.pdf`: Assignment instructions
- `retail_sales_used_cars.csv`: Downloaded data from FRED
- `requirements.txt`: Python package dependencies

## Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run Jupyter:
```bash
jupyter notebook hwk0_analysis.ipynb
```

## Dependencies

- pandas < 3.0
- numpy
- matplotlib
- seaborn
- statsmodels
- scipy
- pandas-datareader
- ipykernel

## Author

Gabriela Acoada

## Course

Time Series Analysis - Emory University
Professor: Elena Pesavento
