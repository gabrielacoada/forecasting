# Time Series Formulas - Quick Reference

This directory contains formula sheets organized by topic.

## Files

### arma-processes.md
- MA(q) properties and formulas
- AR(p) properties and formulas  
- ARMA(p,q) combined models
- ACF and PACF patterns
- Invertibility and stationarity conditions

### unit-roots.md
- Random walk and unit root processes
- ADF test (Augmented Dickey-Fuller)
- PP test (Phillips-Perron)
- KPSS test
- Critical values and interpretation

### var-models.md (if covered)
- Vector autoregression
- Granger causality
- Impulse response functions
- Forecast error variance decomposition

### forecasting-metrics.md
- MSFE (Mean Squared Forecast Error)
- MAE (Mean Absolute Error)
- MAPE (Mean Absolute Percentage Error)
- Diebold-Mariano test
- h-step ahead forecasts

### statistical-tests.md
- Ljung-Box test (white noise)
- Box-Pierce test
- Jarque-Bera test (normality)
- ARCH-LM test
- Likelihood ratio tests

## Usage

### During Homework
Quick lookup while working on problem sets:
```bash
# Working on ARMA identification
open reference/formulas/arma-processes.md
```

### Creating Study Materials
```bash
claude "Add these new formulas from week 5 to reference/formulas/unit-roots.md"
```

### Before Exam
```bash
# Print out formula sheet
cat reference/formulas/*.md > complete-formula-sheet.md
```

## Format

Each formula file follows this structure:

```markdown
# Topic Name

## Formula 1 Name
**Formula:**
[Mathematical expression]

**When to use:**
[Context and application]

**Interpretation:**
[What it means]

**Example:**
[Quick example]

---

## Formula 2 Name
[same structure]
```

## Building Your Formula Reference

### From Lectures
After each lecture:
```bash
claude "Extract formulas from week-3 slides and add to appropriate reference file"
```

### From Problem Sets
After completing homework:
```bash
claude "What formulas did I use in Problem Set 2? Add them to reference if missing"
```

### Auto-Update
```bash
claude "Review all my lecture notes and problem sets. Update reference/formulas/ with any missing formulas"
```

## LaTeX Support

Formulas use markdown math syntax:
- Inline: `$\rho_1 = \theta/(1+\theta^2)$`
- Display: `$$\rho_1 = \frac{\theta}{1+\theta^2}$$`

## Quick Reference Card

For a one-page cheat sheet:
```bash
claude "Create a one-page quick reference card with the 20 most important formulas from all topics"
```