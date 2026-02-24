# Data Integrity Audit

Audit date: 2026-02-20
Scope: All data handoff points across the 3-notebook pipeline

---

## Executive Summary

**No red flags found.** All data flows are clean:

- NB1 produces no data files — handoff is via methodology decisions only
- NB2 produces no data files — handoff is via visualizations only
- NB3 reads raw source files independently — no cross-notebook data contamination
- NB2's blank-plot bugs (now fixed) were visualization-only and did not affect NB3's inputs or outputs
- The final output (`scenario_summary.csv`) has 18 complete rows with zero NaN values

---

## Handoff Point 1: Raw FRED CSVs → NB1 and NB3

### What is passed
7 FRED CSV files in `data/raw/`, each with a `date` column and one value column.

### Verification

| File | Shape | NaN | Date Range | Status |
|------|-------|-----|------------|--------|
| BUSLOANS.csv | (948, 1) | 0 | 1947-01 to 2025-12 | OK |
| CONSUMER.csv | (948, 1) | 0 | 1947-01 to 2025-12 | OK |
| GDPC1.csv | (315, 1) | 0 | 1947-01 to 2025-07 | OK |
| UNRATE.csv | (937, 1) | 1 | 1948-01 to 2026-01 | OK (1 NaN is latest pending release) |
| FEDFUNDS.csv | (859, 1) | 0 | 1954-07 to 2026-01 | OK |
| DGS10.csv | (16727, 1) | 715 | 1962-01 to 2026-02 | OK (daily series, NaN = weekends/holidays) |
| CPIAUCSL.csv | (949, 1) | 1 | 1947-01 to 2026-01 | OK (1 NaN is latest pending release) |

Both NB1 and NB3 load these files independently with `.replace('.', np.nan).dropna()`, so the handful of NaN values are handled correctly.

### Issues: None

---

## Handoff Point 2: NB1 → NB3 (Methodology Decisions)

### What is passed
NB1 does not export any data files. It does not call `to_csv`, `to_pickle`, `to_excel`, or any file-writing function (confirmed by scanning all code cells). The handoff is purely informational — NB1 establishes:

1. **Transformation**: Use `100 * ln(Y_t / Y_{t-1})` for growth rates
2. **Stationarity**: Levels are I(1), growth rates are stationary (ADF p < 0.001)
3. **AR baseline**: AR(4) selected by BIC for both loan types
4. **COVID treatment**: Dummy variable for Mar 2020 - Jun 2021
5. **Sample window**: Post-1990

### Verification
NB3 implements all 5 decisions independently in its own code. Reproduced NB1's key computations:
- BUSLOANS growth: n=947, mean=0.5787, std=1.0585, zero NaN — matches NB1 output
- CONSUMER growth: n=947, mean=0.6443, std=1.1804, zero NaN — matches NB1 output
- COVID spike: BUSLOANS +13.02% (Apr 2020), CONSUMER -3.51% (Apr 2020) — matches
- ADF stationarity: both p < 0.000001 — matches

### Issues: None

---

## Handoff Point 3: Raw NGFS Excel → NB2 and NB3

### What is passed
Two Excel files in `data/raw/`:

| File | Size | Contents |
|------|------|----------|
| ngfs-phase5-nigem.xlsx | 25.9 MB | Macro-financial variables (NiGEM) |
| ngfs-phase5-iam.xlsx | 60.4 MB | Climate/energy variables (IAM) |

### Verification
Both files load successfully. NiGEM U.S. data:
- 1,824 rows (deduplicated) for Region = `NiGEM NGFS v1.24.2|United States`
- 3 IAM model families, 7 scenarios, 160 variables
- Year columns: 29 string-typed columns ("2022" through "2050")

### Issues: None

---

## Handoff Point 4: NB2 → NB3 (Critical Check)

### What is passed
**Nothing.** NB2 does not export any data files to disk. It saves only PNG figures to `outputs/figures/`. NB3 reads the raw `ngfs-phase5-nigem.xlsx` file independently.

### Why this matters
NB2 had multiple bugs that produced blank plots:
1. Baseline NaN from index type mismatch (string vs int)
2. `pivot_nigem()` undefined — diff variables came back empty
3. GDP damage queried for GCAM (doesn't exist, REMIND-only)
4. GDP levels queried directly for non-Baseline scenarios (only Baseline has levels)
5. Current Policies used for risk decomposition (lacks transition component)

**If NB2 had exported data files with these bugs, NB3 would have consumed corrupted inputs.** But because there is no file coupling, these were visualization-only issues with zero impact on NB3's results.

### Verification
Scanned all NB3 code cells for references to NB2 output files or NB2 variable names (`nigem_levels`, `diff_pivoted`, etc.). Found none. NB3 reads raw Excel and reconstructs paths from scratch.

### Issues: None — the architectural decision to have NB3 read raw files independently is what prevented contamination.

---

## Handoff Point 5: NB3 Internal — NGFS Path Reconstruction

### What is passed
NB3 reconstructs scenario-conditional macro paths from the NiGEM data. For each of 3 models x 3 scenarios = 9 paths, it needs 5 variables:

| Variable | Baseline Level | Scenario Diff | Reconstruction |
|----------|---------------|---------------|----------------|
| GDP | Gross Domestic Product (GDP) | (combined) suffix | `base * (1 + pct/100)` |
| Unemployment | Unemployment rate ; % | (combined) suffix | `base + abs_diff` |
| Fed Funds | Central bank Intervention rate... | (combined) suffix | `base + abs_diff` |
| CPI Inflation | Inflation rate ; % | (combined) suffix | `base + abs_diff` |
| 10Y Yield | Long term interest rate ; % | (combined) suffix | `base + abs_diff` |

### Verification
Checked all 9 paths (3 models x 3 scenarios) x 5 variables = 45 data extractions:
- **All 45 baseline-level queries return exactly 1 row** (no missing, no duplicates)
- **All 45 diff queries return exactly 1 row** (no missing, no duplicates)
- **Zero NaN values** in any reconstructed path
- All paths span 2022-2050 (29 annual values each)

Spot-checked values:
- GCAM / Net Zero 2050 / GDP 2025: $22,572.8 Bn — economically reasonable
- GCAM / Net Zero 2050 / GDP 2050: $31,460.2 Bn — reasonable growth
- GCAM / Delayed Transition / Unemployment 2050: 4.55% — reasonable
- GCAM / Net Zero 2050 / Policy Rate 2050: 4.02% — reasonable

### Issues: None

---

## Handoff Point 6: NB3 Internal — VAR Estimation Inputs

### What is passed
Annual panel from 1990-2025, 36 observations, used as VAR training data.

### Verification

C&I VAR input panel (4 endogenous + 1 exogenous):

| Column | NaN | Mean | Std | Status |
|--------|-----|------|-----|--------|
| BUSLOANS_g | 0 | 3.82 | 8.13 | OK |
| UNRATE_chg | 0 | 0.01 | 0.96 | OK |
| FEDFUNDS_chg | 0 | -0.04 | 1.94 | OK |
| CPIAUCSL_g | 0 | 2.63 | 1.56 | OK |
| COVID (exog) | 0 | 0.06 | 0.23 | OK (2 years flagged) |

Consumer VAR input panel (5 endogenous + 1 exogenous):

| Column | NaN | Mean | Std | Status |
|--------|-----|------|-----|--------|
| CONSUMER_g | 0 | 5.00 | 7.94 | OK |
| UNRATE_chg | 0 | 0.01 | 0.96 | OK |
| FEDFUNDS_chg | 0 | -0.04 | 1.94 | OK |
| CPIAUCSL_g | 0 | 2.63 | 1.56 | OK |
| DGS10_chg | 0 | -0.01 | 1.00 | OK |
| COVID (exog) | 0 | 0.06 | 0.23 | OK |

### Issues: None — zero NaN in all columns, 36 observations as expected

---

## Handoff Point 7: NB3 Final Outputs

### scenario_summary.csv

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Rows | 18 (2 types x 3 scenarios x 3 horizons) | 18 | OK |
| Columns | 7 | 7 | OK |
| NaN values | 0 | 0 | OK |
| Loan types | {C&I, Consumer} | {C&I, Consumer} | OK |
| Scenarios | {Net Zero, Delayed Trans., NDCs} | {Net Zero, Delayed Trans., NDCs} | OK |
| Horizons | {2030, 2040, 2050} | {2030, 2040, 2050} | OK |

All growth rates have confidence bands. All balance indices have confidence bands. No silently dropped scenarios or variables.

### Output Figures (8 total)

| Figure | Size | Status |
|--------|------|--------|
| annual_data_panel.png | 424 KB | OK |
| ngfs_macro_paths_transformed.png | 716 KB | OK |
| irf_ci_loans.png | 251 KB | OK |
| irf_consumer_loans.png | 282 KB | OK |
| oos_evaluation.png | 437 KB | OK |
| scenario_fan_charts.png | 493 KB | OK |
| cumulative_impact.png | 638 KB | OK |
| scenario_comparison_full.png | 950 KB | OK |

No figures are missing. No figures are suspiciously small (all > 200 KB).

---

## Red Flags

**None found.**

---

## Architectural Notes

The pipeline's data integrity is robust because of one key design decision: **each notebook reads from raw source files independently**. NB1 and NB3 both load the FRED CSVs from `data/raw/`. NB2 and NB3 both load the NGFS Excel files from `data/raw/`. No notebook reads another notebook's intermediate outputs.

This means:
- A bug in NB1 cannot corrupt NB3's inputs
- A bug in NB2 cannot corrupt NB3's inputs (confirmed — NB2's blank-plot bugs had zero downstream impact)
- The only way to corrupt NB3's results is to corrupt the raw source files in `data/raw/`

The tradeoff is redundant computation — NB3 re-parses the NGFS Excel file and re-applies FRED transformations. But for data integrity, this isolation is worth it.
