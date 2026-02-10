# Time Series Visualization Skill

## Purpose
Generate publication-quality plots for time series analysis: ACF, PACF, correlograms, and diagnostic plots. Designed for econometrics homework with proper statistical formatting.

## Core Capabilities
- Plot time series data with proper date formatting
- Generate ACF (Autocorrelation Function) plots
- Generate PACF (Partial Autocorrelation Function) plots
- Combined correlogram analysis
- Statistical significance bands (95% confidence intervals)
- Squared returns analysis for volatility persistence
- Export high-quality figures for reports

## Dependencies
```python
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
import numpy as np
import pandas as pd

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
```

## Best Practices

### 1. Time Series Plot Template
```python
def plot_returns_series(data, column='Returns', title='Financial Asset Returns', 
                       figsize=(14, 5), save_path=None):
    """
    Plot time series of returns with proper formatting.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Date' and returns column
    column : str
        Column name to plot (e.g., 'Returns', 'LogReturns')
    title : str
        Plot title
    figsize : tuple
        Figure size (width, height)
    save_path : str or None
        Path to save figure (e.g., 'outputs/figures/returns_plot.png')
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(data['Date'], data[column], linewidth=0.8, alpha=0.8)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel(f'{column} (%)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    plt.show()
    
    return fig, ax
```

### 2. ACF Plot (Autocorrelation Function)
```python
def plot_acf_analysis(data, column='Returns', lags=40, alpha=0.05, 
                     title='Autocorrelation Function (ACF)', save_path=None):
    """
    Plot ACF with statistical significance bands.
    
    Parameters:
    -----------
    data : pd.Series or array-like
        Time series data
    lags : int
        Number of lags to display
    alpha : float
        Significance level (0.05 for 95% confidence)
    title : str
        Plot title
    save_path : str or None
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    plot_acf(data[column], lags=lags, alpha=alpha, ax=ax, 
             title=title, zero=False)
    
    ax.set_xlabel('Lag', fontsize=12)
    ax.set_ylabel('Autocorrelation', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    plt.show()
    
    return fig, ax
```

### 3. PACF Plot (Partial Autocorrelation Function)
```python
def plot_pacf_analysis(data, column='Returns', lags=40, alpha=0.05,
                      title='Partial Autocorrelation Function (PACF)', save_path=None):
    """
    Plot PACF with statistical significance bands.
    
    Parameters are identical to plot_acf_analysis.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    plot_pacf(data[column], lags=lags, alpha=alpha, ax=ax, 
              title=title, zero=False, method='ywm')
    
    ax.set_xlabel('Lag', fontsize=12)
    ax.set_ylabel('Partial Autocorrelation', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    plt.show()
    
    return fig, ax
```

### 4. Combined Correlogram (ACF + PACF)
```python
def plot_correlogram(data, column='Returns', lags=40, alpha=0.05, 
                    figsize=(14, 8), save_path=None):
    """
    Plot ACF and PACF side by side for comprehensive analysis.
    
    This is the preferred format for homework assignments.
    """
    fig, axes = plt.subplots(2, 1, figsize=figsize)
    
    # ACF
    plot_acf(data[column], lags=lags, alpha=alpha, ax=axes[0], 
             title='Autocorrelation Function (ACF)', zero=False)
    axes[0].set_xlabel('Lag', fontsize=11)
    axes[0].set_ylabel('ACF', fontsize=11)
    axes[0].grid(True, alpha=0.3)
    
    # PACF
    plot_pacf(data[column], lags=lags, alpha=alpha, ax=axes[1],
              title='Partial Autocorrelation Function (PACF)', 
              zero=False, method='ywm')
    axes[1].set_xlabel('Lag', fontsize=11)
    axes[1].set_ylabel('PACF', fontsize=11)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    plt.show()
    
    return fig, axes
```

### 5. Squared Returns Analysis (for volatility)
```python
def plot_squared_returns_analysis(data, column='Returns', lags=40, 
                                 figsize=(14, 10), save_path=None):
    """
    Comprehensive analysis of squared returns for volatility persistence.
    Includes: et plot, et^2 plot, and correlogram of et^2.
    
    This addresses Problem Set 1, Questions 3(c) and 3(d).
    """
    # Calculate squared returns
    data['Returns_Squared'] = data[column] ** 2
    
    fig, axes = plt.subplots(3, 1, figsize=figsize)
    
    # Plot 1: Original returns
    axes[0].plot(data['Date'], data[column], linewidth=0.6, alpha=0.7)
    axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    axes[0].set_xlabel('Date', fontsize=11)
    axes[0].set_ylabel('Returns (%)', fontsize=11)
    axes[0].set_title('Returns (et)', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Squared returns
    axes[1].plot(data['Date'], data['Returns_Squared'], linewidth=0.6, 
                alpha=0.7, color='orange')
    axes[1].set_xlabel('Date', fontsize=11)
    axes[1].set_ylabel('Squared Returns (%²)', fontsize=11)
    axes[1].set_title('Squared Returns (et²)', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: ACF of squared returns
    plot_acf(data['Returns_Squared'], lags=lags, alpha=0.05, ax=axes[2],
             title='ACF of Squared Returns (et²)', zero=False)
    axes[2].set_xlabel('Lag', fontsize=11)
    axes[2].set_ylabel('ACF', fontsize=11)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    
    plt.show()
    
    return fig, axes
```

## Interpretation Guidelines

### ACF Interpretation
- **Slow decay**: Suggests non-stationarity or long memory (AR process)
- **Sharp cutoff at lag q**: Suggests MA(q) process
- **All within bands**: White noise (no autocorrelation)
- **Spike at lag 1 only**: Potential MA(1) process

### PACF Interpretation
- **Sharp cutoff at lag p**: Suggests AR(p) process
- **Gradual decay**: Suggests MA process
- **All within bands**: White noise

### For Problem Set 1, Question 1
If someone claims MA(1) with corr(yt, yt-1) = 0.7:
- MA(1) should show: ACF spike at lag 1 only, PACF gradual decay
- The correlation of 0.7 is suspiciously high for MA(1)
- MA(1): ρ₁ = θ/(1+θ²), maximum possible is 0.5 (when θ=1)

### Squared Returns ACF (Question 3d)
- High autocorrelation in et² indicates volatility clustering
- Persistence in et² suggests ARCH/GARCH effects
- Even if et shows no autocorrelation, et² can show strong persistence

## Output Organization
Always save figures to `outputs/figures/` with descriptive names:
- `returns_timeseries.png`
- `returns_acf.png`
- `returns_pacf.png`
- `returns_correlogram.png`
- `squared_returns_analysis.png`

## Common Use Cases

### Problem Set 1
1. Plot et (returns) - Question 3(a)
2. ACF and PACF of et - Question 3(b)
3. Plot et² - Question 3(c)
4. ACF of et² - Question 3(d)

### Future Problem Sets
- Unit root diagnostics
- Residual analysis
- Forecast error plots
- Cointegration visualization