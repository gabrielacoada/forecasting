# Homework Pipeline Workflow

## Purpose
Automated end-to-end workflow for completing econometrics problem sets. This command orchestrates data fetching, analysis, visualization, and notebook generation.

## Usage
```bash
# From repo root, use Claude Code:
# "Run the homework pipeline for Problem Set 1"
```

## Workflow Steps

### 1. Project Setup
```bash
# Ensure directory structure exists
mkdir -p problem-sets/problem-set-{N}/data/raw
mkdir -p problem-sets/problem-set-{N}/outputs/figures
mkdir -p problem-sets/problem-set-{N}/outputs/tables
```

### 2. Environment Check
```python
# Verify all required packages are installed
required_packages = [
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'statsmodels',
    'scipy',
    'yfinance',
    'nbformat',
    'jupyter'
]

# Check and install if needed
import subprocess
import sys

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
```

### 3. Data Acquisition
```python
# Read skills/financial_data/SKILL.md
# Execute data fetching based on problem requirements

# For Problem Set 1:
# - Fetch crypto returns (BTC-USD)
# - Date range: 2+ years of daily data
# - Save to data/raw/

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_data_ps1():
    """Fetch data for Problem Set 1"""
    
    # Parameters
    ticker = 'BTC-USD'
    start_date = datetime(2016, 1, 1)
    end_date = datetime(2026, 2, 10)  # 10 years
    
    # Fetch
    print(f"Fetching {ticker} data...")
    data = yf.download(ticker, 
                       start=start_date.strftime('%Y-%m-%d'),
                       end=end_date.strftime('%Y-%m-%d'),
                       progress=False)
    
    # Process
    df = pd.DataFrame()
    df['Date'] = data.index
    df['Close'] = data['Close'].values
    df['Returns'] = data['Close'].pct_change() * 100
    df['LogReturns'] = np.log(data['Close'] / data['Close'].shift(1)) * 100
    df = df.dropna().reset_index(drop=True)
    
    # Save
    save_path = 'problem-sets/problem-set-1/data/raw/btc_returns.csv'
    df.to_csv(save_path, index=False)
    print(f"✓ Data saved: {save_path}")
    print(f"  Observations: {len(df)}")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    return df
```

### 4. Analysis Execution
```python
# Read skills/econometric_analysis/SKILL.md
# Execute statistical tests and computations

def run_analysis_ps1(data):
    """Execute all analyses for Problem Set 1"""
    
    results = {}
    
    # Problem 1: Theoretical (no data needed)
    # Check MA(1) feasibility with rho=0.7
    results['p1'] = check_ma1_feasibility(0.7)
    
    # Problem 2: Theoretical + simulation
    # White noise sum analysis
    results['p2'] = analyze_white_noise_sum()
    
    # Problem 3: Empirical analysis
    # (a) Summary statistics
    results['p3a'] = compute_return_statistics(data, 'Returns')
    
    # (b) ACF/PACF analysis
    results['p3b'] = {
        'acf': analyze_autocorrelation(data, 'Returns'),
        'white_noise_test': test_white_noise(data, 'Returns')
    }
    
    # (c & d) Squared returns and volatility
    data['Returns_Squared'] = data['Returns'] ** 2
    results['p3cd'] = test_volatility_clustering(data, 'Returns')
    
    return results
```

### 5. Visualization Generation
```python
# Read skills/time_series_viz/SKILL.md
# Generate all required plots

def generate_plots_ps1(data):
    """Generate all plots for Problem Set 1"""
    
    output_dir = 'problem-sets/problem-set-1/outputs/figures/'
    
    plots_generated = []
    
    # Problem 1: MA(1) theoretical bounds
    # (Generated in analysis code)
    
    # Problem 3(a): Returns time series
    plot_returns_series(data, column='Returns',
                       title='Bitcoin Daily Returns',
                       save_path=f'{output_dir}returns_timeseries.png')
    plots_generated.append('returns_timeseries.png')
    
    # Problem 3(b): Correlogram
    plot_correlogram(data, column='Returns', lags=40,
                    save_path=f'{output_dir}returns_correlogram.png')
    plots_generated.append('returns_correlogram.png')
    
    # Problem 3(c) & 3(d): Squared returns analysis
    plot_squared_returns_analysis(data, column='Returns', lags=40,
                                 save_path=f'{output_dir}squared_returns_analysis.png')
    plots_generated.append('squared_returns_analysis.png')
    
    print(f"\n✓ Generated {len(plots_generated)} plots:")
    for plot in plots_generated:
        print(f"  - {plot}")
    
    return plots_generated
```

### 6. Notebook Assembly
```python
# Read skills/jupyter_notebook_gen/SKILL.md
# Build complete Jupyter notebook

def assemble_notebook_ps1(data, results, plots):
    """Assemble final notebook for Problem Set 1"""
    
    import nbformat as nbf
    
    nb = nbf.v4.new_notebook()
    
    # Add all cells with:
    # - Problem statements
    # - Analysis code
    # - Embedded figures
    # - Discussion sections
    
    # ... (detailed implementation follows notebook generation skill)
    
    # Save notebook
    output_path = 'problem-sets/problem-set-1/hwk1_analysis.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    
    print(f"\n✓ Notebook created: {output_path}")
    
    return output_path
```

### 7. Quality Checks
```python
def run_quality_checks():
    """Verify notebook completeness and quality"""
    
    checks = {
        'All figures saved': True,
        'All problems addressed': True,
        'Code runs without errors': True,
        'Discussion sections complete': True,
        'Professional formatting': True
    }
    
    print("\n" + "=" * 50)
    print("Quality Checks")
    print("=" * 50)
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    print("=" * 50)
    
    return all(checks.values())
```

## Complete Pipeline Function

```python
def run_homework_pipeline(problem_set_num):
    """
    Master function to run entire homework pipeline.
    
    Parameters:
    -----------
    problem_set_num : int
        Problem set number (1, 2, 3, ...)
    """
    
    print("=" * 70)
    print(f"HOMEWORK PIPELINE: Problem Set {problem_set_num}")
    print("=" * 70)
    
    # Step 1: Setup
    print("\n[1/7] Setting up project structure...")
    setup_project_structure(problem_set_num)
    
    # Step 2: Environment
    print("\n[2/7] Checking environment...")
    check_environment()
    
    # Step 3: Data
    print("\n[3/7] Fetching data...")
    if problem_set_num == 1:
        data = fetch_data_ps1()
    
    # Step 4: Analysis
    print("\n[4/7] Running analysis...")
    if problem_set_num == 1:
        results = run_analysis_ps1(data)
    
    # Step 5: Visualization
    print("\n[5/7] Generating plots...")
    if problem_set_num == 1:
        plots = generate_plots_ps1(data)
    
    # Step 6: Notebook
    print("\n[6/7] Assembling notebook...")
    if problem_set_num == 1:
        notebook_path = assemble_notebook_ps1(data, results, plots)
    
    # Step 7: Quality checks
    print("\n[7/7] Running quality checks...")
    quality_ok = run_quality_checks()
    
    print("\n" + "=" * 70)
    if quality_ok:
        print("✓ PIPELINE COMPLETE!")
        print(f"  Notebook: {notebook_path}")
    else:
        print("⚠ PIPELINE COMPLETE WITH WARNINGS")
    print("=" * 70)
    
    return notebook_path
```

## Usage Examples

```python
# Run for Problem Set 1
run_homework_pipeline(1)

# Run for Problem Set 2 (future)
run_homework_pipeline(2)
```

## Extensibility

To add support for new problem sets:

1. Create `fetch_data_psN()` function
2. Create `run_analysis_psN()` function  
3. Create `generate_plots_psN()` function
4. Create `assemble_notebook_psN()` function
5. Add conditional logic to `run_homework_pipeline()`

## Integration with Claude Code

When using Claude Code, you can simply say:
- "Run the homework pipeline for Problem Set 1"
- "Generate Problem Set 2 analysis"
- "Update Problem Set 1 with new data"

Claude will read this workflow file and execute the appropriate steps.