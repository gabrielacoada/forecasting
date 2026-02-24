# Notebook Pipeline Walkthrough

## Pipeline Overview

The three notebooks form a sequential analysis pipeline that takes raw data and produces scenario-conditional loan forecasts under NGFS climate scenarios. Each notebook's outputs feed into the next.

```
empirical_analysis.ipynb          ngfs_exploration.ipynb          scenario_forecasting.ipynb
─────────────────────────         ──────────────────────          ──────────────────────────
FRED CSVs (7 series)              NGFS Excel files (2)            Outputs from NB1 + NB2
        │                                 │                               │
        ▼                                 ▼                               ▼
Stationarity tests               Parse NiGEM + IAM data          Build VAR models
Growth rate transforms            Reconstruct scenario levels     Pseudo OOS evaluation
COVID break analysis              Scenario comparison viz         Conditional forecasts
AR baseline models                Variable mapping table          Cumulative impact
Cross-correlations                Risk decomposition              Summary tables
        │                                 │                               │
        ▼                                 ▼                               ▼
OUTPUTS:                          OUTPUTS:                        OUTPUTS:
- 7 figures                       - 6 figures                     - 8 figures
- AR order selections             - Reconstructed level paths     - scenario_summary.csv
- Variable transformation         - NGFS → FRED mapping           - 9 forecast paths/loan type
  decisions                       - Data source documentation     - Differential impact analysis
```

**Why this ordering matters:** You cannot build a VAR (Notebook 3) without first establishing that the target series are stationary and choosing appropriate transformations (Notebook 1). You cannot generate scenario-conditional forecasts without first understanding what the NGFS data contains and how to map it to FRED equivalents (Notebook 2). Notebook 3 synthesizes both.

---

## Notebook 1: empirical_analysis.ipynb

### Purpose

Establish the empirical foundation by answering: What are the statistical properties of U.S. loan and macro data, and what baseline models should any multivariate approach beat?

This notebook is necessary because:
- You cannot model a series without first knowing if it's stationary (Week 3)
- The COVID structural break must be quantified before deciding how to treat it (BofA requirement)
- AR baselines set the benchmark — a VAR is only justified if it improves on a simple AR (Pesavento's parsimony principle)
- Cross-correlations guide which macro variables to include in the VAR (feature selection)

### Data In

| File | Contents | Frequency | Range |
|------|----------|-----------|-------|
| `BUSLOANS.csv` | C&I loan balances ($Bn) | Monthly | 1947-2025 |
| `CONSUMER.csv` | Consumer loan balances ($Bn) | Monthly | 1947-2025 |
| `GDPC1.csv` | Real GDP ($Bn 2017) | Quarterly | 1947-2025 |
| `UNRATE.csv` | Unemployment rate (%) | Monthly | 1948-2026 |
| `FEDFUNDS.csv` | Fed Funds rate (%) | Monthly | 1954-2026 |
| `DGS10.csv` | 10-Year Treasury yield (%) | Daily→Monthly | 1962-2026 |
| `CPIAUCSL.csv` | CPI index | Monthly | 1947-2026 |

### Step-by-Step Walkthrough

**Section 1-2: Load & Visual Inspection (cells 1-5)**

Loads all 7 FRED CSVs and plots levels in a 3-panel figure (loans, rates, macro). This is pure visual exploration — identifying trends, structural breaks, and scale differences. The COVID period (Mar 2020 - Jun 2021) is shaded in red on every panel. The BUSLOANS series shows a dramatic PPP-driven spike; CONSUMER shows a drop.

**Section 3: Log Growth Rates (cells 6-8)**

Transforms loan levels to growth rates using the course convention: `g_t = 100 * ln(Y_t / Y_{t-1})`. This is the critical transformation decision — all downstream modeling works in growth rates, not levels.

Why log growth instead of `pct_change()`: Professor Pesavento uses log differences throughout the course; they're approximately equal to percentage changes for small values but have better statistical properties (additivity over time, symmetric treatment of gains/losses).

Output: Monthly growth rate series for BUSLOANS and CONSUMER, with summary statistics. Mean monthly growth is ~0.58% for C&I, ~0.64% for consumer. The COVID spike (+13.0% in Apr 2020 for C&I) is clearly visible.

**Section 4: Stationarity Tests (cells 9-10)**

Runs ADF (H0: unit root) and KPSS (H0: stationary) on both levels and growth rates. The dual-test approach follows the course methodology — both tests agreeing provides stronger evidence than either alone.

Results:
- **Levels**: Both BUSLOANS and CONSUMER are I(1) — ADF fails to reject unit root (p > 0.99), KPSS rejects stationarity (p < 0.01). This confirms we must work in growth rates.
- **Growth rates**: Both are stationary — ADF rejects unit root (p < 0.001). KPSS results are marginal (BUSLOANS p=0.018, CONSUMER p=0.01), likely due to COVID contamination. ADF is the primary test here.
- **Macro variables**: UNRATE and FEDFUNDS are borderline — ADF rejects at 5% but this may reflect structural breaks rather than true stationarity. The notebook recommends using changes (first differences) in the VAR to be safe.

**Section 5: ACF/PACF Analysis (cells 11-12)**

Plots ACF and PACF for both loan growth series out to 36 lags. This is the Box-Jenkins identification step from Weeks 3-4. The patterns suggest AR processes (PACF cuts off, ACF decays) rather than MA. The ACF shows significant autocorrelation at lags 1-5+ for C&I, consistent with the AR(5) and AR(12) selections that follow.

**Section 6: COVID Structural Break Investigation (cells 13-16)**

Quantifies the COVID break by computing z-scores relative to pre-COVID statistics. Key finding: the break is **asymmetric** across loan types:
- C&I: 8 months exceed 3 sigma (max: +13.9 sigma in Apr 2020) — PPP lending caused a massive positive spike followed by reversal as loans were forgiven
- Consumer: Only 1 month exceeds 3 sigma (-3.5 sigma in Apr 2020) — lockdowns caused a modest drop

This asymmetry matters for modeling — a single COVID dummy treats both series the same, but the economic mechanisms are different. The notebook flags this as a Q&A question for BofA (subsequently confirmed: use dummy variables).

The zoom plot (bar chart of 2019-2022) makes the asymmetry visually clear.

**Section 7-8: AR Baseline Models (cells 17-21)**

Fits AR(1) through AR(12) on three sample variants (full, post-1990, ex-COVID) and selects by BIC. Key decisions:
- **BIC over AIC**: BIC penalizes complexity more heavily, appropriate for the small macro samples Pesavento works with. "Start large, go small" — but let BIC enforce parsimony.
- **Three samples tested**: Shows sensitivity of lag selection to COVID and sample period. BUSLOANS switches from AR(5) on full sample to AR(12) on ex-COVID (seasonal lending patterns emerge without COVID noise). CONSUMER is stable at AR(4) across all samples.
- **Ljung-Box residual test**: Confirms no remaining serial correlation in AR residuals (all p > 0.27). This is Pesavento's "most important thing" — the residual correlogram check.

The BIC grid plot (BIC vs AR order for 3 samples) is saved for reference.

**Section 9: Cross-Correlations (cells 22-23)**

Computes cross-correlation between loan growth and three macro variables (UNRATE change, FEDFUNDS change, CPI growth) at lags -12 to +12 months, using post-1990 data. This guides feature selection for the VAR:
- C&I loans show meaningful cross-correlation with unemployment changes (negative, as expected — rising unemployment reduces lending)
- Consumer loans show cross-correlation with Fed Funds and unemployment
- 95% confidence bands (1.96/sqrt(n)) help distinguish signal from noise

**Section 10: Rolling Statistics (cells 24-25)**

24-month rolling mean and standard deviation for both growth series. This reveals:
- The Great Moderation (lower volatility post-1984)
- A post-2008 regime of lower mean growth
- The COVID spike standing out as a clear outlier
- Post-COVID mean growth is materially lower than pre-COVID (0.17% vs 0.61% for C&I)

### Data Out

| Output | Used By |
|--------|---------|
| Growth rate transformation decision (log-difference) | Notebook 3 applies same transform |
| AR(4) baseline for both loan types | Notebook 3 uses as OOS benchmark |
| Stationarity confirmation (work in growth rates) | Notebook 3 models growth rates |
| Cross-correlation patterns | Notebook 3's VAR variable selection |
| COVID dummy recommendation | Notebook 3 includes COVID exogenous variable |
| 7 figures saved to `outputs/figures/` | Report and presentation |

### Key Decisions and Rationale

1. **Log growth rates over percentage change**: Course convention, better statistical properties
2. **BIC for AR selection over AIC**: Enforces parsimony with limited macro samples
3. **Post-1990 sample for cross-correlations**: BofA requirement ("at least 3 decades"), avoids pre-Great-Moderation regime
4. **COVID as dummy variable**: BofA confirmed this approach; asymmetric effects documented but single dummy used for simplicity

### Assumptions and Limitations

- Growth rate stationarity assumes no further structural breaks beyond COVID
- KPSS rejections for growth rates suggest possible remaining heterogeneity (COVID contamination or post-2008 regime shift)
- Cross-correlations are bivariate — they don't control for other variables (the VAR handles this)
- AR baselines are estimated on ex-COVID data but evaluated on the full sample in Notebook 3

---

## Notebook 2: ngfs_exploration.ipynb

### Purpose

Parse, understand, and visualize the NGFS Phase 5 scenario data, establishing how climate scenarios translate into the same macro variables we have in FRED. This notebook answers: What do the scenarios contain, how do they differ, and how do we map them to our modeling variables?

This notebook is necessary because:
- NGFS data has a non-obvious structure (baseline stores levels, other scenarios store diffs) that must be understood before use
- Two separate files (IAM and NiGEM) contain different variable types — confusing them causes blank plots
- BofA explicitly asked to "show a robust understanding of what different data sets are telling you"
- The variable mapping (NiGEM → FRED) is the bridge that makes scenario-conditional forecasting possible

### Data In

| File | Contents | Frequency | Range |
|------|----------|-----------|-------|
| `ngfs-phase5-nigem.xlsx` | Macro-financial variables under climate scenarios | Annual | 2022-2050 |
| `ngfs-phase5-iam.xlsx` | Climate/energy system variables | Annual (5-yr steps) | 2020-2100 |

### Step-by-Step Walkthrough

**Section 0: Data Source Map (cell 0, markdown)**

Documents the critical distinction between the two NGFS files:
- **NiGEM**: Macro-financial variables (GDP, unemployment, inflation, rates, equity/house prices). 160 variables, 3 IAM model families, 7 scenarios. Baseline stores levels; other scenarios store differences from baseline.
- **IAM**: Climate/energy variables (carbon prices, emissions, energy mix). Thousands of variables. All scenarios store levels directly. GDP damage estimates only for REMIND, not GCAM.

This documentation exists because these data structure differences caused multiple bugs (blank plots from querying the wrong file or misunderstanding the level/diff structure).

**Section 1: Load & Filter NiGEM (cells 1-3)**

Loads the NiGEM Excel file, filters to U.S. region (`NiGEM NGFS v1.24.2|United States`), deduplicates, and summarizes. Key discovery printed to output: GDP level data only exists for the `Baseline` scenario — all other scenarios store percentage differences. This is the structural insight that drives the reconstruction logic.

Inventory: 1,824 U.S. rows, 3 IAM models (GCAM, MESSAGEix, REMIND), 7 scenarios, 160 variables, annual 2022-2050.

**Section 2: Reconstruct Level Paths (cell 4)**

The core data engineering step. Defines `reconstruct_levels()` which:
1. Gets the Baseline level for a variable from one IAM model
2. Gets the percentage/absolute difference for each non-Baseline scenario
3. Reconstructs levels: `level = baseline * (1 + pct_diff/100)` for quantities, `level = baseline + abs_diff` for rates

Maps 9 variables:
- GDP, Equity Prices, House Prices, Private Investment → percentage diffs
- Unemployment, Inflation, Policy Rate, Long-Term Rate, Carbon Price → absolute diffs

**Implementation detail**: Uses `.values` on the baseline Series to avoid a pandas index alignment bug (string year column names vs integer DataFrame index). This was a bug that caused Baseline columns to show NaN.

All 9 variables successfully reconstructed with 6 scenarios each (Baseline + 5 non-baseline).

**Section 3: Verification (cell 5)**

Prints a full table of reconstructed levels at 2025, 2030, and 2050 for every variable and scenario. This is a validation step — confirms no NaN values and that numbers are economically reasonable (GDP ~$23-34 trillion, unemployment ~3.8-4.7%, etc.).

**Section 4: Scenario Paths Plot (cell 7)**

6-panel figure showing reconstructed levels for GDP, Unemployment, Inflation, Policy Rate, Equity Prices, and Carbon Price across all scenarios. Baseline shown as a thicker gray line; scenarios color-coded. Validation guard: asserts each variable exists and has non-NaN data before plotting.

Key visual insight: Carbon Price diverges dramatically (Net Zero reaches $14,535/tCO2 by 2050; Delayed Transition reaches $9,248 but stays at $0 until 2030). GDP and macro variables show much narrower spreads.

**Section 5: Scenario Divergence from Baseline (cells 9-10)**

Pivots the raw difference variables (without level reconstruction) to show how each scenario deviates from baseline. 6-panel plot showing GDP % diff, Unemployment pp diff, Inflation pp diff, Policy Rate pp diff, Equity Prices % diff, House Prices % diff.

This view is more useful for modeling because it isolates the marginal climate impact. GDP under Net Zero is ~5% below baseline by 2030, ~7% by 2050. Unemployment deviations are tiny (< 0.2 pp).

**Implementation note**: This cell previously called an undefined function `pivot_nigem()` which silently produced empty data (caught by try/except). Fixed by inlining the pivot logic.

**Section 6: Model Uncertainty (cell 12)**

Two-panel figure comparing the 3 IAM models:
- Left: Reconstructed GDP levels under Net Zero 2050, showing how GCAM, MESSAGEix, and REMIND diverge. REMIND produces the most pessimistic short-term GDP path; GCAM the most optimistic long-term.
- Right: GDP % deviation from baseline for 3 models x 3 scenarios (9 lines), using line styles to distinguish models and colors for scenarios.

**Implementation note**: The left panel previously tried to query GDP levels directly for Net Zero 2050, which returned empty because levels only exist for Baseline. Fixed by reconstructing levels per model from baseline + diff.

**Section 7: IAM Data — Carbon Prices & Emissions (cells 14-15)**

Switches to the IAM file for climate-system variables not available in NiGEM. 3-panel figure:
- Panel 1: U.S. carbon price by scenario (GCAM) — dramatic divergence, with Net Zero reaching $800+/tCO2 by 2100
- Panel 2: U.S. CO2 emissions by scenario (GCAM) — Net Zero drops to near zero by 2060; Current Policies stays flat
- Panel 3: U.S. GDP with physical damage (REMIND, because GCAM lacks this variable) — shows GDP drag from chronic climate damage across scenarios

**Data availability gotcha**: GDP damage estimates (`GDP|MER|including medium chronic physical risk damage estimate`) only exist for REMIND, not GCAM. The notebook handles this by switching to the REMIND region for panel 3 and labeling it accordingly.

**Section 8: NGFS → FRED Mapping Table (cell 16, markdown)**

The critical bridge table:

| NGFS NiGEM Variable | FRED Equivalent | Mapping Type |
|---|---|---|
| GDP (2017 PPP $Bn) | GDPC1 | Scale/level adjustment |
| Unemployment rate (%) | UNRATE | Direct |
| Inflation rate (%) | CPI growth | Direct (concept match) |
| Policy rate (%) | FEDFUNDS | Direct |
| Long-term rate (%) | DGS10 | Direct |

This mapping is what makes scenario-conditional forecasting possible — it connects the NGFS future paths to the same variables the VAR is estimated on.

**Section 9: Summary Table (cell 17)**

Prints endpoint values at 2030, 2040, 2050 for 5 key variables across 6 scenarios. This is a reference table for quick comparison and fact-checking.

**Section 10: Risk Decomposition (cell 19)**

3-panel figure showing GDP impact decomposed into Transition Risk, Physical Risk, and Combined for three scenarios:
- Net Zero 2050: Large transition drag (~4% by 2030), small physical drag, combined ~5-7%
- Delayed Transition: Zero transition until 2030 (no policy), then sharp jump; physical accumulates gradually
- NDCs: Moderate transition, growing physical risk

**Implementation note**: Current Policies was originally used but only has `(physical)` data (no transition policy exists in that scenario). Replaced with NDCs which has all three components.

### Data Out

| Output | Used By |
|--------|---------|
| Reconstructed level paths (`nigem_levels` dict) | Not directly consumed by NB3 (NB3 re-reads the Excel) |
| Variable mapping (NiGEM → FRED) | NB3 uses same mapping to extract scenario paths |
| Data structure documentation | Prevents bugs in NB3's scenario path extraction |
| 6 figures saved to `outputs/figures/` | Report and presentation |

### Key Decisions and Rationale

1. **GCAM as primary model**: Used for most visualizations because it has the broadest variable coverage. REMIND and MESSAGEix shown in comparison plots.
2. **Percentage vs absolute diffs**: GDP, equity, house prices use percentage diffs (multiplicative reconstruction). Rates use absolute diffs (additive reconstruction). This matches the economic meaning — a "2% GDP decline" is multiplicative; a "0.5pp rate increase" is additive.
3. **NDCs instead of Current Policies for decomposition**: Current Policies has no transition risk component by definition. NDCs has all three (transition + physical + combined).

### Assumptions and Limitations

- NiGEM's Baseline is model-specific — each IAM has a different Baseline, so cross-model comparison of levels is comparing different counterfactuals
- The reconstruction assumes the percentage/absolute diff interpretation is correct (verified against documentation)
- Carbon prices in NiGEM differ significantly from those in IAM — NiGEM processes IAM outputs through NiGEM's own macro model, which can amplify or dampen the original signals
- No Current Policies scenario in the NiGEM combined-diff data, limiting the "hot house world" analysis

---

## Notebook 3: scenario_forecasting.ipynb

### Purpose

Build VAR models linking loan growth to macro variables, validate them against AR baselines, and generate 25-year scenario-conditional forecasts under NGFS climate paths. This is where the modeling from Notebook 1 and the scenario data from Notebook 2 come together.

This notebook is necessary because:
- The AR baselines from Notebook 1 are univariate — they can't incorporate climate scenario information
- The NGFS paths from Notebook 2 are macro variables, not loan forecasts — a model is needed to translate them
- BofA needs conditional loan projections with uncertainty bands across scenarios
- The course requires demonstrating VAR methodology, forecast evaluation, and scenario analysis

### Data In

| Source | Contents | Role |
|--------|----------|------|
| `BUSLOANS.csv`, `CONSUMER.csv` | Loan balances | Target variables (transformed to growth) |
| `GDPC1.csv`, `UNRATE.csv`, `FEDFUNDS.csv`, `DGS10.csv`, `CPIAUCSL.csv` | Macro series | VAR endogenous variables |
| `ngfs-phase5-nigem.xlsx` | Scenario macro paths | Conditional forecast inputs (2026-2050) |

### Step-by-Step Walkthrough

**Section 1: Setup & Data Loading (cells 0-6)**

Re-loads all 7 FRED series and the NGFS NiGEM file independently (doesn't depend on Notebook 1 or 2 being in memory). This makes the notebook self-contained and reproducible. Prints inventory of both data sources.

**Section 2: Data Preparation (cells 7-10)**

Applies transformations from Notebook 1's findings:
- Log growth rates (x100) for BUSLOANS, CONSUMER, CPIAUCSL
- GDP: forward-fills quarterly to monthly, then computes log growth
- First differences for UNRATE, FEDFUNDS, DGS10
- COVID dummy: 1 for Mar 2020 - Jun 2021

Then aggregates monthly to annual frequency (year-end mean) and restricts to 1990+. This produces a 36-observation annual panel.

**Why annual?** NGFS scenarios are annual. Rather than interpolating NGFS to monthly (adding noise), the notebook aggregates FRED to annual (losing precision but matching frequency exactly). This is the simpler of the two approaches BofA suggested.

COVID years (2020, 2021) are identified for later exclusion from evaluation.

The annual data panel is visualized as a 2x2 bar chart with COVID years highlighted.

**Section 3: NGFS Scenario Path Extraction (cells 12-16)**

Re-implements the level reconstruction from Notebook 2, but targeted at the 5 VAR-relevant variables and converted to the same transformations as FRED:
- GDP: reconstructed levels → log growth rates
- UNRATE: reconstructed levels → year-on-year change
- FEDFUNDS, DGS10: reconstructed levels → year-on-year change
- CPI inflation: taken directly from NiGEM (already a rate)

Produces 9 scenario paths (3 models x 3 scenarios: Net Zero, Delayed Transition, NDCs). Each path is a DataFrame of annual macro variable values from 2023 to 2050 in the same units as the FRED transformations.

Sample output for GCAM: GDP growth ranges from 1.18% (NDCs) to 1.31% (Net Zero) — Net Zero actually has higher long-run growth despite higher transition costs, because physical damage is lower.

A 2x3 figure shows the NGFS macro paths for GCAM, with scenario lines diverging after ~2030.

**Section 4: AR Baselines (cell 18)**

Fits AR(1) through AR(4) on ex-COVID annual data for both loan types, selects by BIC. Both select AR(4). In-sample RMSE is ~7% for both. Ljung-Box tests confirm clean residuals.

These are the benchmarks the VAR must beat.

**Section 5: VAR Model — C&I Loans (cells 19-27)**

Specifies and estimates a VAR for C&I loans:
- **Endogenous**: BUSLOANS_g, UNRATE_chg, FEDFUNDS_chg, CPIAUCSL_g
- **Exogenous**: COVID dummy
- **Lag selection**: BIC selects VAR(1) from candidates 0-4

Key results from the BUSLOANS_g equation:
- `L1.UNRATE_chg`: coefficient -5.82, p < 0.001 — a 1 percentage point increase in unemployment reduces next-year C&I loan growth by 5.8 percentage points. This is the strongest and most significant predictor.
- `COVID`: +11.9, p = 0.025 — PPP lending boosted C&I growth by ~12pp
- `L1.FEDFUNDS_chg`: +2.04, p = 0.085 — rate hikes weakly boost C&I growth (banks earn more on new loans)
- `L1.BUSLOANS_g`: +0.09, not significant — minimal autocorrelation at annual frequency
- `L1.CPIAUCSL_g`: -0.76, not significant

Granger causality tests confirm: unemployment strongly Granger-causes C&I loan growth (p = 0.0004), Fed Funds weakly (p = 0.019), inflation does not (p = 0.39).

IRFs show: a positive unemployment shock depresses C&I loan growth for ~4 years before fading. A Fed Funds shock has a smaller, positive initial effect.

Residual diagnostics: Ljung-Box p > 0.72 at all lags — no serial correlation. Residual std = 5.7pp.

**Section 6: VAR Model — Consumer Loans (cells 28-33)**

Specifies a VAR for consumer loans with one additional variable:
- **Endogenous**: CONSUMER_g, UNRATE_chg, FEDFUNDS_chg, CPIAUCSL_g, **DGS10_chg**
- DGS10 is added because BofA pushed for "more thorough consumer drivers" and consumer loans (auto, mortgage) are sensitive to long-term rates

BIC selects VAR(1). Key results from the CONSUMER_g equation:
- `L1.CONSUMER_g`: -0.40, p = 0.02 — mean reversion (consumer loan growth oscillates)
- `COVID`: -12.87, p = 0.04 — opposite sign from C&I! Consumer lending contracted during COVID while C&I surged (PPP)
- `L1.UNRATE_chg`: -3.0, p = 0.21 — negative but not significant (weaker than C&I)
- `L1.DGS10_chg`: +1.07, p = 0.25 — positive but not significant individually

Granger causality reveals a different pattern from C&I: only the 10-year yield Granger-causes consumer loan growth (p = 0.023). Unemployment does *not* (p = 0.81). This makes economic sense — consumer lending is driven by financing cost (long-term rates affect auto/mortgage affordability) while C&I lending is driven by business conditions (unemployment proxies economic health).

Residuals clean: Ljung-Box p > 0.43.

**Section 7: Pseudo Out-of-Sample Evaluation (cells 34-36)**

Expanding-window 1-step-ahead forecasts from 2006 to 2025, excluding COVID years (2020-2021) from evaluation per BofA's instruction.

Results:
| | AR(4) RMSE | VAR(1) RMSE | Improvement |
|---|---|---|---|
| C&I | 10.09% | 9.05% | 10.4% |
| Consumer | 16.85% | 14.03% | 16.7% |

The VAR improves on the AR baseline for both loan types. The improvement is larger for consumer loans (16.7%), justifying the inclusion of macro variables and especially the 10-year yield.

A 1x2 figure plots actual vs. forecast for both models and loan types over the evaluation period.

**Section 8: Scenario-Conditional Forecasts (cells 37-40)**

The core output. Uses the estimated VAR coefficients but replaces future macro variable paths with NGFS scenario values:

For each year t in [2026, 2050]:
1. Construct the lagged endogenous vector from the previous year (using actual data for history, forecasted values for future years)
2. **Replace the macro variables** (UNRATE_chg, FEDFUNDS_chg, CPIAUCSL_g, DGS10_chg) with the NGFS scenario values for year t
3. Apply VAR coefficients to produce the forecast for all endogenous variables
4. The **loan growth forecast** is the element we extract; the macro variable forecasts are discarded (overridden by NGFS paths)

This produces 9 paths per loan type (3 models x 3 scenarios).

Fan charts show the median forecast with model uncertainty bands (min/max across the 3 IAMs) for each scenario.

**Section 9: Cumulative Impact (cells 41-44)**

Converts annual growth rate forecasts to cumulative balance indices (2025 = 100) using: `level_t = level_{t-1} * exp(g_t / 100)`.

Key results at 2050:

| Loan Type | Net Zero | Delayed Trans. | NDCs |
|---|---|---|---|
| C&I | 243.1 [236.6-246.1] | 225.8 [224.9-226.2] | 229.2 [228.6-233.2] |
| Consumer | 350.9 [313.2-398.9] | 410.0 [403.7-417.9] | 385.1 [352.2-391.6] |

Striking finding: C&I and Consumer loans respond in **opposite directions** to scenario choice:
- **C&I**: Net Zero produces the *highest* balance (best for C&I lending). Delayed Transition is 7.1% lower.
- **Consumer**: Delayed Transition produces the *highest* balance (+16.8% above Net Zero).

This makes economic sense through the Granger causality findings: C&I is driven by unemployment (lower under Net Zero's gradual transition), while consumer lending is driven by long-term rates (higher under Net Zero, suppressing consumer borrowing).

Differential impact plots show the divergence growing after ~2035.

**Section 10: Scenario Comparison Visualization (cell 46)**

A 2x3 presentation-quality figure with macro scenarios on top and loan forecasts on bottom, showing the causal chain from climate policy → macro variables → loan portfolios.

**Section 11: Summary Table & Diagnostics (cells 47-50)**

Exports `scenario_summary.csv` with 18 rows (2 loan types x 3 scenarios x 3 horizons), columns for median growth rate, growth band, balance index, and index band.

Final diagnostics verification:
- Ljung-Box: no serial correlation in either model's residuals
- ADF on residuals: stationary (p < 0.0001 for both)
- All 9 paths per loan type generated successfully
- All 8 figures saved

### Data Out

| Output | Purpose |
|--------|---------|
| `outputs/tables/scenario_summary.csv` | Master results table for report |
| 8 figures in `outputs/figures/` | Presentation visuals |
| VAR(1) coefficients and diagnostics | Report methodology section |
| OOS RMSE comparison (AR vs VAR) | Justifies model choice |
| Differential impact analysis | Executive-level insight |

### Key Decisions and Rationale

1. **Annual aggregation over NGFS interpolation**: Matches frequencies exactly. Avoids introducing interpolation artifacts. Cost: smaller sample (36 obs vs ~400 monthly). BofA said "try different frequencies" — this is the simpler starting point.

2. **VAR(1) by BIC**: With 4-5 endogenous variables and 36 annual observations, higher-order VARs consume degrees of freedom rapidly. BIC's parsimony penalty is appropriate. VAR(1) still captures the key dynamics.

3. **Different variable sets for C&I vs Consumer**: C&I uses 4 variables; Consumer adds DGS10. This reflects the Granger causality results and BofA's push for "thorough consumer drivers." Long-term rates matter for consumer lending (auto, mortgage) but not for C&I (which is more sensitive to business conditions).

4. **COVID as exogenous dummy, not excluded**: The dummy absorbs the COVID effect while preserving the information in COVID-era macro relationships. Evaluation excludes COVID years per BofA's instruction.

5. **3 scenarios x 3 models**: Captures both scenario uncertainty (what policy path) and model uncertainty (which IAM). The min/max across IAMs provides natural uncertainty bands without parametric assumptions.

6. **Cholesky ordering**: For IRFs, the ordering is: loan growth, unemployment, Fed Funds, inflation (and DGS10 for consumer). This assumes macro variables don't respond contemporaneously to loan growth — reasonable since loan data is released with a lag.

### Assumptions and Limitations

- **36 annual observations** is a small sample for a VAR with 4-5 endogenous variables. Parameter estimates have wide confidence intervals. The pseudo-OOS evaluation partially addresses this by testing generalization.
- **Linear VAR** assumes the macro-to-loans relationship is constant over time. The rolling statistics in Notebook 1 show this may not hold (post-2008 regime shift, post-COVID lower growth).
- **Conditional forecasting replaces macro paths entirely** with NGFS values, ignoring any feedback from loans to macro variables. This is the standard approach in stress testing but means the model can't capture second-round effects.
- **No Mincer-Zarnowitz test** on OOS forecasts. This was identified in the gap analysis as a next step (Week 6 course material).
- **No Diebold-Mariano test** for the AR-vs-VAR comparison. The 10-17% RMSE improvement is suggestive but not formally tested for statistical significance.
- **Consumer model Granger causality is surprising**: unemployment does NOT Granger-cause consumer loans in this annual sample, which conflicts with conventional wisdom. This could be a small-sample artifact or reflect that annual aggregation washes out the within-year dynamics.

---

## Cross-Notebook Dependencies

```
NB1 findings ──────────────────────────── NB3 uses
  Stationarity → work in growth rates     Same transformation applied
  AR(4) baseline order                    OOS benchmark: AR(4) vs VAR
  COVID = structural break                COVID dummy in VAR
  Cross-corr: UNRATE, FEDFUNDS matter     VAR variable selection
  Post-1990 sample recommended            Annual panel starts 1990

NB2 findings ──────────────────────────── NB3 uses
  NiGEM = macro variables (not IAM)       NB3 reads NiGEM file
  Baseline = levels, others = diffs       NB3 reconstructs scenario paths
  5 key variables mapped to FRED          Same 5 variables in VAR
  3 IAM models available                  3 models x 3 scenarios = 9 paths
  Annual frequency, 2022-2050             NB3 forecasts 2026-2050
```

### Output Validation Status

All outputs verified non-empty:
- **NB1**: 7/7 figures have image data, all summary statistics print valid numbers
- **NB2**: 6/6 figures have image data after bug fixes, all 9 variables reconstructed successfully, no NaN in Baseline
- **NB3**: 8/8 figures saved (verification checklist passes), scenario_summary.csv has 18 rows with complete data, all 9 forecast paths per loan type reach 2050
