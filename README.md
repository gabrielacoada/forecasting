# Forecasting and Time Series - Problem Sets

Automated workflow for completing econometrics and time series forecasting homework assignments using Claude Code and reusable skills.

## 🎯 Purpose

This repository provides a scalable, automated system for:
- Fetching and processing financial/economic data
- Performing rigorous time series analysis
- Generating publication-quality visualizations
- Producing complete Jupyter notebooks with code, outputs, and discussion

## 📁 Repository Structure

```
forecasting-problemset0/
├── .claude/                          # Claude Code configuration
│   ├── skills/                       # Reusable analysis skills
│   │   ├── financial_data/           # Data acquisition
│   │   ├── time_series_viz/          # Visualization tools
│   │   ├── econometric_analysis/     # Statistical tests
│   │   └── jupyter_notebook_gen/     # Notebook generation
│   └── commands/                     # Workflow automation
│       └── homework_pipeline.md      # Master pipeline
│
├── problem-sets/                     # Individual assignments
│   ├── problem-set-0/                # Completed example
│   │   ├── hwk0_analysis.ipynb
│   │   └── ...
│   └── problem-set-1/                # Current assignment
│       ├── Hwk1.pdf                  # Problem statement
│       ├── hwk1_analysis.ipynb       # Main deliverable
│       ├── requirements.txt          # Dependencies
│       ├── data/raw/                 # Source data
│       └── outputs/figures/          # Generated plots
│
├── shared/                           # Shared utilities (future)
│   └── utils.py
│
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Claude Code CLI
- Git

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd forecasting-problemset0

# Install Claude Code (if not already installed)
# Follow: https://claude.ai/download

# Install dependencies for a problem set
cd problem-sets/problem-set-1
pip install -r requirements.txt
```

### Using Claude Code (Recommended)
```bash
# From repo root
claude "Run the homework pipeline for Problem Set 1"

# Or be more specific
claude "Fetch Bitcoin data for the last 2 years and save to problem-set-1"
claude "Generate all plots for Problem Set 1"
claude "Create the complete Jupyter notebook for Problem Set 1"
```

### Manual Workflow
```bash
cd problem-sets/problem-set-1

# 1. Review problem statement
open Hwk1.pdf

# 2. Run the notebook
jupyter notebook hwk1_analysis.ipynb

# 3. Execute all cells
# (Code, outputs, and discussion are pre-populated)
```

## 🛠️ Skills System

The `.claude/skills/` directory contains reusable, modular components:

### 1. Financial Data (`financial_data/SKILL.md`)
- Fetch crypto, stocks, economic indicators
- Calculate returns (simple, log)
- Handle missing data
- Export for reproducibility

**Key Functions:**
- `fetch_crypto_returns(ticker, start_date, end_date)`
- `fetch_stock_returns(ticker, start_date, end_date)`

### 2. Time Series Visualization (`time_series_viz/SKILL.md`)
- Publication-quality plots
- ACF/PACF correlograms
- Squared returns analysis
- Statistical significance bands

**Key Functions:**
- `plot_returns_series(data, column, title, save_path)`
- `plot_correlogram(data, column, lags, save_path)`
- `plot_squared_returns_analysis(data, column, lags, save_path)`

### 3. Econometric Analysis (`econometric_analysis/SKILL.md`)
- White noise testing (Ljung-Box)
- MA/AR identification
- Autocorrelation analysis
- Volatility clustering tests

**Key Functions:**
- `test_white_noise(data, column, lags)`
- `check_ma1_feasibility(rho1)`
- `test_volatility_clustering(data, column, lags)`

### 4. Notebook Generation (`jupyter_notebook_gen/SKILL.md`)
- Automated notebook assembly
- Problem statement integration
- Code + output + discussion sections
- Professional formatting

**Key Functions:**
- `create_homework_notebook(problem_set_num, problems_dict)`
- `save_notebook(nb, filepath)`

## 📊 Current Problem Sets

### Problem Set 0 ✅ (Completed)
- Trend and break testing
- Seasonality analysis
- ARMA model basics

### Problem Set 1 🔄 (In Progress)
**Topics**: MA process theory, white noise, volatility clustering

**Problems:**
1. MA(1) theoretical constraints
2. White noise summation properties
3. Financial returns empirical analysis

**Data**: Bitcoin daily returns (2 years)

**Status**: Skills created, ready for execution

### Future Problem Sets
- **PS2**: Unit roots and stationarity testing
- **PS3**: ARMA model selection and estimation
- **PS4**: Forecasting and evaluation
- **PS5**: VAR models and Granger causality
- **PS6**: Cointegration and ECM

## 🔧 Extending the System

### Adding a New Problem Set

1. **Create directory structure:**
```bash
mkdir -p problem-sets/problem-set-N/{data/raw,outputs/{figures,tables}}
```

2. **Add problem-specific functions** to relevant skills

3. **Update workflow command** in `.claude/commands/homework_pipeline.md`:
```python
def run_analysis_psN(data):
    # Problem-specific analysis
    pass
```

4. **Create README** for the problem set

5. **Use Claude Code** to execute:
```bash
claude "Run homework pipeline for Problem Set N"
```

### Adding a New Skill

1. Create `/.claude/skills/<skill-name>/SKILL.md`
2. Document:
   - Purpose and capabilities
   - Dependencies
   - Best practices
   - Code templates
   - Usage examples
3. Reference in workflow commands

## 📈 Best Practices

### Data Management
- Keep raw data in `data/raw/`
- Use descriptive filenames
- Include data source and date range
- Document any data transformations

### Code Quality
- Clear variable names
- Inline comments for complex logic
- Consistent style (PEP 8)
- Modular functions

### Visualization
- High DPI (300) for figures
- Clear labels and titles
- Appropriate font sizes
- Save to `outputs/figures/`

### Documentation
- Answer the specific question asked
- Connect results to theory
- Explain economic/statistical intuition
- Professional academic tone

## 🤖 Claude Code Integration

This repository is optimized for Claude Code workflows:

1. **Natural language commands**: "Fetch data for Problem Set 1"
2. **Skill-based execution**: Claude reads `.claude/skills/` before acting
3. **Automated pipelines**: Complete workflows with single command
4. **Intelligent defaults**: Bitcoin data, 2 years, daily frequency

## 📝 License

[Add your license here]

## 🙋 Support

For questions or issues:
1. Check the README for the specific problem set
2. Review the relevant skill documentation in `.claude/skills/`
3. Examine example code in completed problem sets

## 🔄 Updates

Last updated: February 10, 2026

**Recent changes:**
- ✅ Created comprehensive skills system
- ✅ Added Problem Set 1 structure
- 🔄 Implementing automated pipeline
- 📋 TODO: Generate PS1 notebook

---

**Note**: This is a living system designed to scale. Each problem set builds on the existing skills, and new skills are added as needed for future topics.