# Econometric Analysis Skill

## Purpose
Perform statistical tests and diagnostics for time series models: white noise tests, MA/AR identification, stationarity tests, and model estimation. Designed for rigorous econometric homework analysis.

## Core Capabilities
- White noise testing (Ljung-Box, Box-Pierce)
- MA(q) and AR(p) process identification
- Stationarity assessment
- Summary statistics for financial returns
- Theoretical bounds for MA processes
- Model estimation and diagnostics (for future problem sets)

## Dependencies
```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')
```

## Best Practices

### 1. Summary Statistics Template
```python
def compute_return_statistics(data, column='Returns'):
    """
    Compute comprehensive summary statistics for financial returns.
    
    Returns:
    --------
    Dictionary with mean, std, skewness, kurtosis, min, max, etc.
    """
    series = data[column].dropna()
    
    stats_dict = {
        'Mean': series.mean(),
        'Std Dev': series.std(),
        'Variance': series.var(),
        'Skewness': series.skew(),
        'Kurtosis': series.kurtosis(),
        'Min': series.min(),
        'Max': series.max(),
        'Median': series.median(),
        'Q1': series.quantile(0.25),
        'Q3': series.quantile(0.75),
        'N_obs': len(series)
    }
    
    # Create formatted output
    print("=" * 50)
    print(f"Summary Statistics: {column}")
    print("=" * 50)
    for key, value in stats_dict.items():
        if key == 'N_obs':
            print(f"{key:.<30} {value}")
        else:
            print(f"{key:.<30} {value:.6f}")
    print("=" * 50)
    
    return stats_dict
```

### 2. White Noise Testing
```python
def test_white_noise(data, column='Returns', lags=20, alpha=0.05):
    """
    Test if series is white noise using Ljung-Box test.
    
    Null hypothesis: No autocorrelation up to lag k
    
    Returns:
    --------
    DataFrame with test statistics and p-values for each lag
    """
    series = data[column].dropna()
    
    # Ljung-Box test
    lb_test = acorr_ljungbox(series, lags=lags, return_df=True)
    
    print("=" * 70)
    print("Ljung-Box Test for White Noise")
    print("=" * 70)
    print("H0: Data is white noise (no autocorrelation)")
    print(f"Significance level: {alpha}")
    print("=" * 70)
    
    # Add significance indicator
    lb_test['Significant'] = lb_test['lb_pvalue'] < alpha
    
    print(lb_test.head(10))
    print("\n")
    
    if lb_test['lb_pvalue'].iloc[-1] < alpha:
        print(f"✗ Reject H0 at {alpha} level: Data is NOT white noise")
        print("  → Significant autocorrelation detected")
    else:
        print(f"✓ Fail to reject H0: Data appears to be white noise")
        print("  → No significant autocorrelation detected")
    
    print("=" * 70)
    
    return lb_test
```

### 3. MA(1) Theoretical Bounds (for Question 1)
```python
def check_ma1_feasibility(rho1):
    """
    Check if a given autocorrelation is feasible for MA(1) process.
    
    For MA(1): yt = εt + θεt-1
    Theoretical result: ρ1 = θ/(1+θ²)
    
    Maximum possible |ρ1| = 0.5 (when θ = ±1)
    
    Parameters:
    -----------
    rho1 : float
        Observed first-order autocorrelation
    
    Returns:
    --------
    dict with feasibility assessment and implied θ values
    """
    print("=" * 70)
    print("MA(1) Feasibility Check")
    print("=" * 70)
    print(f"Observed correlation: ρ₁ = {rho1:.4f}")
    print()
    
    # Theoretical maximum
    max_rho = 0.5
    print(f"Theoretical bound for MA(1): |ρ₁| ≤ {max_rho}")
    print()
    
    if abs(rho1) > max_rho:
        print("✗ INFEASIBLE for MA(1) process")
        print(f"  → |{rho1:.4f}| > {max_rho}")
        print("  → This correlation is too high for any MA(1) model")
        print()
        print("Possible explanations:")
        print("  • Data may be AR(p) process instead")
        print("  • Data may be ARMA(p,q) with p > 0")
        print("  • Data may have higher-order moving average terms")
        feasible = False
        theta_values = None
    else:
        print("✓ FEASIBLE for MA(1) process")
        print()
        
        # Solve for θ: ρ₁(1+θ²) - θ = 0
        # This is: ρ₁θ² - θ + ρ₁ = 0
        a = rho1
        b = -1
        c = rho1
        
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0:
            theta1 = (-b + np.sqrt(discriminant)) / (2*a)
            theta2 = (-b - np.sqrt(discriminant)) / (2*a)
            
            print(f"Implied θ values:")
            print(f"  θ₁ = {theta1:.4f} (invertible: {abs(theta1) < 1})")
            print(f"  θ₂ = {theta2:.4f} (invertible: {abs(theta2) < 1})")
            
            theta_values = [theta1, theta2]
            feasible = True
        else:
            print("  → No real solution (this shouldn't happen)")
            theta_values = None
            feasible = False
    
    print("=" * 70)
    
    return {
        'feasible': feasible,
        'rho1': rho1,
        'max_rho_ma1': max_rho,
        'theta_values': theta_values
    }
```

### 4. Sum of White Noise Processes (for Question 2)
```python
def analyze_white_noise_sum(n_obs=1000, n_simulations=1000):
    """
    Simulate to show when sum of white noise processes is white noise.
    
    Question: If xt and yt are white noise, is xt + yt white noise?
    Answer: Yes, IF xt and yt are independent.
           No, if xt and yt are dependent.
    
    This function demonstrates both cases.
    """
    print("=" * 70)
    print("Sum of White Noise Processes Analysis")
    print("=" * 70)
    
    # Case 1: Independent white noise
    np.random.seed(42)
    x1 = np.random.normal(0, 1, n_obs)
    y1 = np.random.normal(0, 1, n_obs)
    z1 = x1 + y1
    
    # Test for white noise
    lb_test1 = acorr_ljungbox(z1, lags=10, return_df=True)
    
    print("\nCase 1: Independent white noise processes")
    print(f"  xt ~ N(0, 1), yt ~ N(0, 1), independent")
    print(f"  zt = xt + yt")
    print(f"  Ljung-Box p-value (lag 10): {lb_test1['lb_pvalue'].iloc[-1]:.4f}")
    print(f"  → zt IS white noise ✓")
    
    # Case 2: Dependent white noise (e.g., yt = -xt)
    x2 = np.random.normal(0, 1, n_obs)
    y2 = -x2 + np.random.normal(0, 0.1, n_obs)  # Nearly -xt
    z2 = x2 + y2
    
    lb_test2 = acorr_ljungbox(z2, lags=10, return_df=True)
    
    print("\nCase 2: Dependent white noise processes")
    print(f"  xt ~ N(0, 1), yt ≈ -xt")
    print(f"  zt = xt + yt")
    print(f"  Ljung-Box p-value (lag 10): {lb_test2['lb_pvalue'].iloc[-1]:.4f}")
    print(f"  → zt may NOT be white noise ✗")
    
    print("\n" + "=" * 70)
    print("Conclusion:")
    print("  Sum of white noise is white noise IFF they are INDEPENDENT")
    print("  Independence is crucial, not just zero autocorrelation")
    print("=" * 70)
    
    return {'independent_pval': lb_test1['lb_pvalue'].iloc[-1],
            'dependent_pval': lb_test2['lb_pvalue'].iloc[-1]}
```

### 5. Autocorrelation Analysis
```python
def analyze_autocorrelation(data, column='Returns', max_lag=20):
    """
    Compute and display autocorrelation coefficients.
    
    Returns:
    --------
    DataFrame with lags, ACF values, standard errors, and significance
    """
    series = data[column].dropna()
    n = len(series)
    
    # Compute ACF
    acf_values = acf(series, nlags=max_lag, fft=False)
    
    # Standard error for ACF (under white noise null)
    # SE = 1/sqrt(n) for all lags under H0: white noise
    se = 1 / np.sqrt(n)
    
    # Critical value (95% confidence)
    critical_value = 1.96 * se
    
    # Create results dataframe
    results = pd.DataFrame({
        'Lag': range(0, max_lag + 1),
        'ACF': acf_values,
        'SE': se,
        'Lower_CI': -critical_value,
        'Upper_CI': critical_value,
        'Significant': np.abs(acf_values) > critical_value
    })
    
    # Exclude lag 0 (always 1)
    results = results[results['Lag'] > 0]
    
    print("=" * 70)
    print("Autocorrelation Analysis")
    print("=" * 70)
    print(f"Sample size: {n}")
    print(f"Standard error (under H0): {se:.4f}")
    print(f"95% confidence bands: ±{critical_value:.4f}")
    print("=" * 70)
    print(results.head(10))
    print("=" * 70)
    
    sig_count = results['Significant'].sum()
    print(f"\nSignificant autocorrelations: {sig_count} out of {max_lag}")
    
    if sig_count == 0:
        print("→ Data appears to be white noise")
    else:
        print(f"→ Data shows autocorrelation at lags: {results[results['Significant']]['Lag'].values}")
    
    return results
```

### 6. Volatility Clustering Detection
```python
def test_volatility_clustering(data, column='Returns', lags=20):
    """
    Test for volatility clustering using squared returns.
    
    Volatility clustering: Large changes tend to be followed by large changes
    (of either sign), and small changes by small changes.
    
    This is detected by significant autocorrelation in squared returns.
    """
    series = data[column].dropna()
    series_squared = series ** 2
    
    print("=" * 70)
    print("Volatility Clustering Analysis")
    print("=" * 70)
    
    # Test original returns
    lb_returns = acorr_ljungbox(series, lags=lags, return_df=True)
    pval_returns = lb_returns['lb_pvalue'].iloc[-1]
    
    # Test squared returns
    lb_squared = acorr_ljungbox(series_squared, lags=lags, return_df=True)
    pval_squared = lb_squared['lb_pvalue'].iloc[-1]
    
    print(f"Ljung-Box test on returns:        p-value = {pval_returns:.4f}")
    print(f"Ljung-Box test on squared returns: p-value = {pval_squared:.4f}")
    print()
    
    if pval_returns > 0.05 and pval_squared < 0.05:
        print("✓ VOLATILITY CLUSTERING DETECTED")
        print("  → Returns show no autocorrelation")
        print("  → Squared returns show significant autocorrelation")
        print("  → This indicates time-varying volatility (ARCH/GARCH effects)")
    elif pval_returns < 0.05:
        print("→ Returns show autocorrelation")
        print("  → May need ARMA modeling first")
    else:
        print("→ No significant volatility clustering detected")
    
    print("=" * 70)
    
    return {
        'returns_pval': pval_returns,
        'squared_returns_pval': pval_squared,
        'clustering_detected': (pval_returns > 0.05 and pval_squared < 0.05)
    }
```

## Interpretation Guidelines

### For Problem Set 1, Question 1
**Why surprising if MA(1) has ρ₁ = 0.7?**
- Use `check_ma1_feasibility(0.7)` to show it violates theoretical bounds
- MA(1) maximum correlation is 0.5
- Such high correlation suggests AR or ARMA process

### For Problem Set 1, Question 2
**Is sum of white noise processes white noise?**
- Use `analyze_white_noise_sum()` to demonstrate
- Answer: Yes, if independent
- Answer: Not necessarily, if dependent
- Independence is key, not just marginal white noise

### For Problem Set 1, Question 3
Use the functions to:
- (a) Compute and display summary statistics
- (b) Perform ACF/PACF analysis and white noise tests
- (c) Analyze squared returns
- (d) Test volatility clustering

## Future Problem Sets
These functions extend to:
- Unit root tests (ADF, PP, KPSS)
- Cointegration tests (Engle-Granger, Johansen)
- ARMA model selection (AIC, BIC)
- Forecast evaluation (RMSE, MAE, Diebold-Mariano)
- Structural break tests (Chow, QLR)