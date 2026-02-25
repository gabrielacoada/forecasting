# Corrections Log — February 24, 2026

This document tracks all bugs found, fixes applied, and how the results changed. Created during a code review of both `scenario_forecasting.ipynb` (annual) and `scenario_forecasting_quarterly.ipynb` (quarterly).

---

## Bug 1: DGS10 Daily Data Not Aggregated to Monthly (CRITICAL)

### What was wrong

DGS10 (10-Year Treasury Yield) is a **daily** series (16,727 observations). UNRATE and FEDFUNDS are monthly. The original code treated all three the same:

```python
for ticker in ['UNRATE', 'FEDFUNDS', 'DGS10']:
    monthly[f'{ticker}_chg'] = fred[ticker][ticker].diff()
```

This computed **day-to-day** changes for DGS10 and tried to assign them to a monthly-indexed DataFrame. Pandas aligned by date index, keeping only dates where a trading day happened to fall on the 1st of the month (~50% of months). The rest became NaN.

### Why it was critical

The `monthly.dropna()` that followed deleted **all columns** (BUSLOANS, CONSUMER, UNRATE, etc.) for any month where DGS10 was NaN. This meant:

- **Annual notebook:** Monthly panel shrank from ~762 to ~488 observations. Only 6-9 months per year survived instead of 12. The `mean * 12` multiplier then inflated annual growth rates by up to ~5%.
- **Quarterly notebook:** DGS10_chg values were ~100x too small (daily diffs instead of monthly diffs), making the consumer model's key variable essentially noise.

### Affected notebooks

| Notebook | Status |
|----------|--------|
| `scenario_forecasting.ipynb` (annual) | **Fixed Feb 24** |
| `scenario_forecasting_quarterly.ipynb` (quarterly) | **Fixed Feb 24** |
| `empirical_analysis.ipynb` (NB1) | **Not affected** — computes DGS10 level cross-correlations, not changes |
| `ngfs_exploration.ipynb` (NB2) | **Not affected** — doesn't use FRED data |

### The fix

```python
# Before (WRONG):
for ticker in ['UNRATE', 'FEDFUNDS', 'DGS10']:
    monthly[f'{ticker}_chg'] = fred[ticker][ticker].diff()

# After (CORRECT):
for ticker in ['UNRATE', 'FEDFUNDS']:
    monthly[f'{ticker}_chg'] = fred[ticker][ticker].diff()

dgs10_monthly = fred['DGS10'].resample('MS').last()
monthly['DGS10_chg'] = dgs10_monthly['DGS10'].diff()
```

### Impact on annual model results

| Metric | Before Fix | After Fix | Change |
|--------|-----------|-----------|--------|
| Monthly panel size | ~488 obs | 762 obs | +56% more data |
| C&I: UNRATE coefficient | -5.82 (p<0.001) | -5.08 (p<0.001) | Still dominant driver |
| C&I: FEDFUNDS coefficient | +2.04 (p=0.085) | +0.82 (p=0.285) | No longer significant |
| C&I: COVID coefficient | +11.9 (p=0.025) | +6.26 (p=0.154) | No longer significant |
| C&I: OOS AR RMSE | 10.09 | 10.10 | ~same |
| C&I: OOS VAR RMSE | 9.05 | **10.32** | VAR now WORSE than AR |
| C&I: VAR vs AR improvement | +10.4% | **-2.2%** | Reversed |
| Consumer: OOS AR RMSE | 16.85 | 9.78 | Much better |
| Consumer: OOS VAR RMSE | 14.03 | **12.52** | VAR now WORSE than AR |
| Consumer: VAR vs AR improvement | +16.7% | **-28.1%** | Reversed |
| Consumer: DGS10 Granger p-value | 0.023 | **0.084** | Weaker but still marginal |

**Key takeaway:** The "VAR beats AR at annual frequency" result was an artifact of the data corruption. With correct data, the annual VAR does NOT generalize better than a simple AR. This is because 36 annual observations is insufficient to reliably estimate a 4-5 variable VAR.

### Impact on quarterly model results

| Metric | Before Fix | After Fix | Change |
|--------|-----------|-----------|--------|
| DGS10_chg std deviation | 0.07 (daily scale) | proper monthly scale | Order of magnitude |
| Consumer: DGS10 Granger p | 0.052 (marginal) | **0.048** (significant) | Improved |
| Consumer: FEDFUNDS Granger p | 0.634 | **0.040** (significant) | Now significant |
| C&I: OOS VAR vs AR | +4.7% | **+11.7%** | Larger improvement |
| Consumer: OOS VAR vs AR | +33.7% | **+7.5%** | Smaller but still positive |

**Key takeaway:** With the fix, the quarterly consumer model now has two significant interest rate drivers (Fed Funds and DGS10), making it more credible. The quarterly VAR still beats the AR baseline for both loan types.

### Impact on scenario forecasts (cumulative balance index at 2050)

**Annual model (corrected):**

| Loan Type | Scenario | Before Fix | After Fix |
|-----------|----------|-----------|-----------|
| C&I | Net Zero | 243.1 | 246.5 |
| C&I | Delayed Trans. | 225.8 | 231.7 |
| C&I | NDCs | 229.2 | 234.5 |
| Consumer | Net Zero | 350.9 | 346.4 |
| Consumer | Delayed Trans. | 410.0 | 352.0 |
| Consumer | NDCs | 385.1 | 349.3 |

The C&I results are broadly similar. The consumer results changed substantially — the previously large gap between scenarios (~60 points) has narrowed to ~6 points. Consumer loan forecasts are now much less sensitive to scenario choice in the annual model.

**Quarterly model (corrected):**

| Loan Type | Scenario | 2050 Balance |
|-----------|----------|-------------|
| C&I | Net Zero | 185.3 |
| C&I | Delayed Trans. | 183.3 |
| C&I | NDCs | 183.7 |
| Consumer | Net Zero | 325.5 |
| Consumer | Delayed Trans. | 327.9 |
| Consumer | NDCs | 326.4 |

Quarterly scenario spreads are narrow (~2 points for C&I, ~2 points for consumer). The quarterly model's autoregressive dynamics dominate, dampening the scenario-conditional effects.

---

## Bug 2: Granger Causality Column Order Reversed (QUARTERLY ONLY)

### What was wrong

In `scenario_forecasting_quarterly.ipynb`, the Granger causality test had the columns in the wrong order:

```python
# WRONG (was in quarterly notebook):
test_data = ci_data_q[[var, 'BUSLOANS_g']].dropna()

# CORRECT (as in annual notebook):
test_data = ci_data_q[['BUSLOANS_g', var]].dropna()
```

`statsmodels.grangercausalitytests` tests whether the **second column** Granger-causes the **first column**. The reversed order meant the tests were answering "does loan growth predict unemployment?" instead of "does unemployment predict loan growth?"

### Affected notebooks

| Notebook | Status |
|----------|--------|
| `scenario_forecasting.ipynb` (annual) | **Not affected** — column order was already correct |
| `scenario_forecasting_quarterly.ipynb` (quarterly) | **Fixed Feb 24** |

### Impact

All Granger p-values reported in the pre-fix quarterly notebook were answering the wrong question. The corrected results:

**C&I Granger causality (quarterly, corrected):**

| Variable | Pre-fix p-value (wrong question) | Corrected p-value |
|----------|--------------------------------|-------------------|
| UNRATE → BUSLOANS | 0.385 | **0.000** *** |
| FEDFUNDS → BUSLOANS | 0.171 | **0.032** ** |
| CPI → BUSLOANS | 0.393 | **0.023** ** |

**Consumer Granger causality (quarterly, corrected):**

| Variable | Pre-fix p-value (wrong question) | Corrected p-value |
|----------|--------------------------------|-------------------|
| UNRATE → CONSUMER | 0.732 | 0.490 |
| FEDFUNDS → CONSUMER | 0.634 | **0.040** ** |
| CPI → CONSUMER | 0.533 | 0.407 |
| DGS10 → CONSUMER | 0.052 * | **0.048** ** |

The corrected results tell a much clearer story: all three macro variables predict C&I loans; both interest rates (but not unemployment) predict consumer loans.

**No impact on model estimation or forecasts** — Granger tests are diagnostic only.

---

## Bug 3: C&I Ljung-Box Failure at Quarterly Frequency (ACKNOWLEDGED)

### What it was

In the pre-fix quarterly notebook, the C&I VAR(1) residuals failed the Ljung-Box test at all lags (p=0.000), indicating significant leftover autocorrelation.

### Status after DGS10 fix

With the corrected data (762→142 quarterly obs with proper DGS10):
- Lag 4: p = 0.047 (marginal)
- Lag 8: p = 0.166 (pass)
- Lag 12: p = 0.300 (pass)

The problem was largely caused by the corrupted data. The remaining marginal result at lag 4 is acceptable — the model captures most of the serial dependence. The consumer model passes cleanly at all lags.

### Recommendation

Acknowledge the marginal lag-4 result in the report. If needed, try VAR(2) for C&I as a robustness check (AIC selected lag 5, suggesting richer dynamics exist).

---

## Other Findings (Not Bugs, Methodological Notes)

### 1. Annual VAR does not beat AR baseline (with correct data)

With the DGS10 fix, the annual VAR is worse than the AR for both loan types in OOS evaluation. This is not a bug — it's a sample size problem. 36 annual observations cannot reliably estimate a VAR with 4-5 endogenous variables + COVID dummy (24+ parameters). The quarterly model (142 obs) has enough data for the VAR to generalize.

**Implication for presentation:** Use the quarterly model as the primary forecasting framework. Present the annual model for its cleaner interpretability (annual growth rates are more intuitive), but do not claim it beats simple benchmarks.

### 2. GDP excluded from both VARs

GDP growth is available from both FRED and NGFS but not included in either VAR. The rationale (documented in CLAUDE.md) is that GDP is lagged — a quarterly GDP print covers the previous quarter, creating a look-ahead risk. At annual frequency this is less concerning but the decision is defensible. Worth mentioning in the report as a design choice.

### 3. CPI transformation mismatch between FRED and NGFS

FRED CPI growth is computed as a log-growth rate: `100 * ln(CPI_t / CPI_{t-1})`. NGFS inflation is a percentage rate. For typical inflation (2-5%), the difference is <30 basis points. Not worth fixing but worth noting in limitations.

### 4. Consumer model weakness at annual frequency

After the DGS10 fix, no macro variable is individually significant in the annual consumer VAR. DGS10 is marginally significant in Granger testing (p=0.084). With 36 observations and 7 parameters, there isn't enough statistical power. At quarterly frequency, both interest rates are significant, confirming the theoretical channel works — it just needs more data.

### 5. Scenario spread narrows at quarterly frequency

The quarterly model produces tighter scenario spreads than the annual model (2-3 point range vs 15+ points at 2050). This is because the quarterly VAR's stronger autoregressive component (own-lag coefficient 0.65, p<0.001) dominates the scenario-conditional macro inputs. The scenarios affect the *level* of the forecast path but the *differences between scenarios* are dampened.

This is actually more realistic — macro variables across NGFS scenarios don't diverge dramatically, especially for the US. The annual model's wider spreads were partly inflated by data corruption.

---

## Updated File Inventory

### Modified files (Feb 24, 2026)

| File | Change |
|------|--------|
| `scenario_forecasting.ipynb` | DGS10 fix in cell 8, re-executed. All outputs updated. |
| `scenario_forecasting_quarterly.ipynb` | DGS10 fix + Granger column fix, re-executed. All outputs updated. |
| `outputs/tables/scenario_summary.csv` | Regenerated with corrected annual results. |
| `outputs/figures/*.png` | All 21 annual + 7 quarterly figures regenerated. |
| `PROJECT-STATUS.md` | Updated earlier this session (before bug fixes). **Needs update** — OOS results and some numbers are now stale. |
| `CLAUDE.md` | Updated team structure earlier. Scenario results section now has stale numbers. |

### Files that should be updated next

1. `PROJECT-STATUS.md` — Update OOS results, scenario forecasts, and the "headline finding" to reflect corrected data
2. `CLAUDE.md` — Update the "Current State" section with corrected scenario forecast results
3. `docs/notebook-walkthrough.md` — Several numbers referenced are now outdated (OOS RMSE, cumulative impacts)
4. `docs/notebook-walkthrough-simplified.md` — Same: numbers in the OOS and cumulative impact sections are outdated

---

## Summary of What Changed for the Presentation

### Still true after corrections
- Unemployment is the dominant driver of C&I loans (confirmed at both frequencies)
- Consumer loans respond to interest rates, not unemployment (confirmed at both frequencies)
- Net Zero produces better long-run C&I outcomes than Delayed Transition
- The opposite-direction finding (C&I prefers Net Zero, consumer less sensitive) still holds directionally
- COVID had asymmetric effects on C&I vs consumer loans
- Model uncertainty across 3 IAMs is ~3% spread

### Changed after corrections
- **Annual VAR does NOT beat AR baseline** — cannot claim this anymore
- **Quarterly VAR DOES beat AR** — this is now the headline model comparison
- Consumer scenario spreads are much narrower than previously reported
- The "consumer loans do best under Delayed Transition" finding is weaker — the gap between scenarios is only ~2-6 points instead of ~60
- The "opposite directions" story is still directionally true but less dramatic

### New strengths from quarterly model
- 142 observations (4x annual), more reliable inference
- All three macro variables significantly predict C&I loans
- Both interest rate types significantly predict consumer loans
- VAR beats AR by 11.7% (C&I) and 7.5% (consumer) in OOS
- Cleaner residual diagnostics
