# Jupyter Notebook Generation Skill

## Purpose
Automatically generate well-structured Jupyter notebooks for econometrics homework with code, outputs, and discussion sections. Ensures consistent formatting and academic quality across all problem sets.

## Core Capabilities
- Generate notebook structure with markdown and code cells
- Include problem statements from PDF
- Insert analysis code with inline comments
- Add interpretation and discussion sections
- Format tables and figures professionally
- Export to .ipynb format

## Notebook Structure Template

### Standard Homework Notebook Layout
```
1. Title and Setup
   - Homework title and course info
   - Import statements
   - Configuration (plot settings, random seeds)

2. Data Loading
   - Load or fetch data
   - Initial data inspection
   - Summary statistics

3. Problem-by-Problem Analysis
   For each problem:
   - Problem statement (from PDF)
   - Analysis code
   - Output (tables, figures)
   - Discussion/interpretation

4. Conclusion
   - Summary of findings
   - Key insights

5. References (if needed)
```

## Best Practices

### 1. Markdown Cell Formatting
```python
# Use hierarchical headers
# H1 for main title
# H2 for major sections
# H3 for individual problems
# H4 for sub-questions

markdown_cell = """
# Problem Set 1: Time Series Analysis

**Course**: Forecasting and Time Series  
**Student**: [Your Name]  
**Date**: February 10, 2026

---

## Setup and Configuration
"""
```

### 2. Code Cell Organization
```python
# Each code cell should:
# 1. Have a clear purpose (comment at top)
# 2. Be self-contained when possible
# 3. Produce visible output
# 4. Include brief inline comments

code_cell = """
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
np.random.seed(42)

print("Setup complete!")
"""
```

### 3. Discussion Sections
```python
discussion_template = """
### Discussion

**Findings:**
- [Key observation 1]
- [Key observation 2]

**Interpretation:**
[Explain what the results mean in the context of time series theory]

**Economic Intuition:**
[Connect to real-world phenomena if applicable]
"""
```

### 4. Programmatic Notebook Generation
```python
import nbformat as nbf

def create_homework_notebook(problem_set_num, problems_dict):
    """
    Generate a Jupyter notebook for a homework assignment.
    
    Parameters:
    -----------
    problem_set_num : int
        Problem set number
    problems_dict : dict
        Dictionary with problem numbers as keys and content as values
        Example: {1: {'statement': '...', 'code': '...', 'discussion': '...'}}
    
    Returns:
    --------
    Notebook object that can be written to file
    """
    nb = nbf.v4.new_notebook()
    
    # Title cell
    title = f"# Problem Set {problem_set_num}: Time Series Analysis\n\n"
    title += "**Course**: Forecasting and Time Series\n"
    title += "**Date**: " + pd.Timestamp.now().strftime('%B %d, %Y') + "\n\n"
    title += "---"
    
    nb.cells.append(nbf.v4.new_markdown_cell(title))
    
    # Setup cell
    setup_code = """# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings('ignore')

# Configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
np.random.seed(42)

print("✓ Setup complete")"""
    
    nb.cells.append(nbf.v4.new_code_cell(setup_code))
    
    # Add each problem
    for prob_num, content in problems_dict.items():
        # Problem statement
        prob_statement = f"## Problem {prob_num}\n\n"
        prob_statement += content.get('statement', '')
        nb.cells.append(nbf.v4.new_markdown_cell(prob_statement))
        
        # Analysis code
        if 'code' in content:
            nb.cells.append(nbf.v4.new_code_cell(content['code']))
        
        # Discussion
        if 'discussion' in content:
            discussion = f"### Discussion\n\n{content['discussion']}"
            nb.cells.append(nbf.v4.new_markdown_cell(discussion))
    
    return nb

def save_notebook(nb, filepath):
    """Save notebook to file"""
    with open(filepath, 'w') as f:
        nbf.write(nb, f)
    print(f"✓ Notebook saved: {filepath}")
```

### 5. Problem Set 1 Specific Template
```python
def create_ps1_notebook():
    """
    Generate notebook specifically for Problem Set 1.
    """
    problems = {
        1: {
            'statement': """
**Question**: Why would you be surprised if I told you that $y_t$ was MA(1) but that 
$\\text{corr}(y_t, y_{t-1}) = 0.7$?

**Approach**: We'll examine the theoretical constraints on MA(1) autocorrelations.
""",
            'code': """# Theoretical analysis of MA(1) constraints
# For MA(1): y_t = ε_t + θε_{t-1}
# ρ_1 = θ/(1+θ²)

# Function to compute maximum possible correlation
def max_ma1_correlation():
    # Maximum occurs when θ = ±1
    theta = 1
    rho_max = theta / (1 + theta**2)
    return rho_max

max_rho = max_ma1_correlation()
observed_rho = 0.7

print("MA(1) Theoretical Bounds Analysis")
print("=" * 50)
print(f"Observed correlation: ρ₁ = {observed_rho}")
print(f"Maximum possible for MA(1): ρ₁ ≤ {max_rho}")
print(f"Feasible? {abs(observed_rho) <= max_rho}")
print("=" * 50)

# Visualization
import matplotlib.pyplot as plt
theta_range = np.linspace(-3, 3, 1000)
rho_values = theta_range / (1 + theta_range**2)

plt.figure(figsize=(10, 6))
plt.plot(theta_range, rho_values, linewidth=2, label='ρ₁(θ) = θ/(1+θ²)')
plt.axhline(y=max_rho, color='red', linestyle='--', label=f'Maximum = {max_rho}')
plt.axhline(y=observed_rho, color='orange', linestyle='--', label=f'Observed = {observed_rho}')
plt.xlabel('θ (MA parameter)', fontsize=12)
plt.ylabel('ρ₁ (First-order autocorrelation)', fontsize=12)
plt.title('MA(1) Autocorrelation as Function of θ', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('outputs/figures/ma1_theoretical_bounds.png', dpi=300, bbox_inches='tight')
plt.show()""",
            'discussion': """
**Key Finding**: The observed correlation of 0.7 is **impossible** for an MA(1) process.

**Explanation**: 
- For MA(1), the first-order autocorrelation is $\\rho_1 = \\frac{\\theta}{1+\\theta^2}$
- The maximum value of $|\\rho_1|$ is 0.5, occurring when $\\theta = \\pm 1$
- An observed correlation of 0.7 exceeds this theoretical bound

**Why surprising**:
- This violates fundamental MA(1) properties
- Such high persistence suggests an AR component
- The process is likely AR(p), ARMA(p,q), or contains a unit root

**Alternative explanations**:
1. The process may be AR(1) or AR(p)
2. The process may be ARMA(p,1) with p ≥ 1
3. There may be measurement error or model misspecification
"""
        },
        2: {
            'statement': """
**Question**: If $x_t$ and $y_t$ are each white noise, is $x_t + y_t$ white noise? 
Is this true in general?

**Approach**: We'll examine this theoretically and through simulation.
""",
            'code': """# Code for Question 2 goes here""",
            'discussion': """Discussion for Question 2 goes here"""
        },
        3: {
            'statement': """
**Question**: Financial asset returns analysis.

(a) Find high frequency financial asset return series, plot it and discuss.
(b) Perform correlogram analysis (ACF and PACF) and discuss.
(c) Plot $e_t^2$ and discuss.
(d) Perform correlogram analysis of $e_t^2$ and discuss volatility persistence.
""",
            'code': """# Code for Question 3 goes here""",
            'discussion': """Discussion for Question 3 goes here"""
        }
    }
    
    nb = create_homework_notebook(1, problems)
    return nb
```

## Output Quality Standards

### Code Quality
- ✓ Clear variable names
- ✓ Inline comments for complex operations
- ✓ Consistent style (PEP 8)
- ✓ Error handling where appropriate

### Figure Quality
- ✓ High DPI (300 for papers)
- ✓ Clear labels and titles
- ✓ Appropriate font sizes
- ✓ Saved to outputs/figures/

### Discussion Quality
- ✓ Answers the specific question asked
- ✓ Connects results to theory
- ✓ Explains economic/statistical intuition
- ✓ Appropriate level of technical detail
- ✓ Professional academic tone

### Table Formatting
```python
# Use pandas styling for nice tables
def format_results_table(df):
    """Format dataframe for professional presentation"""
    styled = df.style\
        .format(precision=4)\
        .set_caption("Results Summary")\
        .set_table_styles([
            {'selector': 'th', 'props': [('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('text-align', 'center')]}
        ])
    return styled
```

## Extensibility for Future Problem Sets

This skill is designed to handle:
- **Problem Set 2**: Unit root and stationarity testing
- **Problem Set 3**: ARMA model selection and estimation
- **Problem Set 4**: Forecasting and evaluation
- **Problem Set 5**: VAR models and Granger causality
- **Problem Set 6**: Cointegration and error correction models

Each new problem set can use the same `create_homework_notebook()` function
by providing appropriate `problems_dict`.

## Integration with Other Skills

This skill works seamlessly with:
- `financial_data/SKILL.md` - for data fetching code
- `time_series_viz/SKILL.md` - for plotting code
- `econometric_analysis/SKILL.md` - for statistical tests

Simply reference functions from those skills in the generated code cells.