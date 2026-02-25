# Project History: Climate Risk Impact on Banking Loan Portfolios

**Team:** Too Big to Melt
**Written:** February 25, 2026
---

## 1. Timeline — What Happened Each Session

### Session 1 (February 12) — Research & First Models

We started the day of the BofA kickoff. The first priority was understanding the problem: how do climate scenarios translate into loan portfolio outcomes? We read the two key Fed research papers (Acharya et al. 2023 on climate stress testing, Jung et al. 2024 on bank climate exposure), parsed the BofA project document, and pulled together everything we could find about NGFS scenarios, FRED data, and stress testing methods.

The initial results looked promising — the VAR appeared to beat a simple benchmark by about 10%.

### Session 2 (February 17) — Fixing Visualization Bugs

Short session. We found and fixed 5 bugs in the climate scenario exploration notebook that were causing blank plots. The underlying data was fine — it was just display issues. No impact on the modeling results.

### Session 3 (February 20) — BofA Q&A + Data Audit

The BofA Q&A session on Feb 20 answered all our major design questions. Key guidance: use dummy variables for COVID, train on at least 3 decades of data, try multiple frequencies, and expand the consumer loan drivers beyond just unemployment and interest rates (they specifically mentioned house prices, disposable income, and consumer sentiment).

After the Q&A, we ran a comprehensive data integrity audit — tracing every data file through every notebook to make sure nothing was corrupted. Result: zero problems found. We also wrote the first version of the notebook walkthrough document so teammates could understand the analysis without reading code.

### Session 4 (February 24) — Bug Discovery, New Models

This was a turning point. A code review uncovered a critical data bug: the 10-Year Treasury yield (DGS10) is published daily, but our code was treating it like monthly data. This caused about 36% of monthly observations to silently drop, inflating growth rates and giving the annual VAR artificial predictive power.

After fixing the bug, the annual VAR no longer beat the simple benchmark. With only 36 annual observations, it was overfitting. This forced us to rethink the approach:

- Built a **quarterly VAR** with 142 observations (4x the annual sample). This model does beat the benchmark: 11.7% better for C&I loans, 7.5% better for consumer loans.
- Built an **ADL-MIDAS model** attempting to use monthly data directly (a technique from Professor Pesavento's Week 7 lecture). The MIDAS results looked strong for consumer loans (+21% improvement) but the estimated weight functions had collapsed to extreme values — a red flag we would investigate later.

We also fixed a separate bug where a statistical test (Granger causality) was accidentally testing the wrong causal direction.

### Session 5 (February 25) — Satellite Model Breakthrough

This session produced the most important methodological advance. We started by researching why the MIDAS model's weights had collapsed. That research led to a bigger insight: **a literature review revealed that the Fed, ECB, and Bank of England don't use VARs for climate stress testing — they use single-equation "satellite models."**

A satellite model is simpler than a VAR. Instead of trying to forecast everything simultaneously (loans, unemployment, interest rates, inflation all interacting), a satellite model takes the climate scenario's macro paths as given and just asks: "if unemployment follows this path, what happens to loans?" This is conceptually cleaner and is exactly what regulators do in practice.

We also discovered that the NGFS database contains scenario paths for house prices and real disposable income — exactly the consumer drivers BofA had asked about. The satellite model could use these directly, whereas adding them to a VAR would have been prohibitively expensive in terms of parameters.

The satellite model outperformed every other approach:
- C&I loans: 22.8% better than the benchmark (statistically significant, p = 0.015)
- Consumer loans: 19.1% better than the benchmark (significant at 10%, p = 0.077)

We also tested the expanded consumer model with house prices and income — BofA's suggestion. The result: these variables don't improve the model. The Fed Funds rate alone is the dominant driver of consumer lending. This is itself a finding worth presenting.

---

## 2. The Modeling Journey

### Where We Started: VAR Models

We started with Vector Autoregression (VAR) models because that's the standard multivariate forecasting method from the course. A VAR models multiple variables simultaneously — loan growth, unemployment, interest rates, and inflation all affecting each other over time. This gives you impulse response functions (how does a shock to unemployment ripple through to loans?) and Granger causality tests (does unemployment statistically predict loan growth?).

The VAR was a natural first choice, and it produced genuine insights about transmission channels. But it had two problems for our specific task:

**Problem 1: Not enough data at annual frequency.** NGFS scenarios are annual, so our first VAR used annual data — only 36 observations from 1990 to 2025. With 4-5 variables and 20+ parameters, the model overfitted. After fixing a data bug, it actually performed *worse* than a simple benchmark.

**Problem 2: Awkward scenario conditioning.** When we plug NGFS scenario paths into the VAR to generate forecasts, we're overriding the VAR's own predictions for unemployment, inflation, etc. The VAR "wants" to forecast unemployment its own way based on its estimated dynamics, but we're telling it "no, use the NGFS number instead." This is conceptually inconsistent.

### The MIDAS Detour

Professor Pesavento taught a MIDAS lecture (Week 7) specifically to help with our frequency mismatch problem. MIDAS is designed to use high-frequency data (monthly) to predict low-frequency outcomes (annual) by learning which months within the year matter most.

We built a MIDAS model, but the estimated weight functions collapsed — all the weight landed on a single month, which defeats the purpose. Research into the academic literature revealed seven compounding causes, led by the wrong optimization algorithm and too many parameters for our small sample. MIDAS is a powerful technique, but with only 34 annual observations, it couldn't deliver on its promise.

### The Discovery: Satellite Models

The MIDAS research led us to the stress testing literature, where we found that **no major central bank uses a VAR as its primary scenario forecasting tool.** The Fed's DFAST stress tests, the ECB's climate stress tests, and the Bank of England's CBES all use "satellite models" — single-equation regressions that take the macro scenario path as a given input and translate it into a credit outcome.

This was the key insight. A satellite model:
- Takes the NGFS scenario paths directly as inputs (no override needed)
- Cheaply accommodates additional variables (each new driver costs 1-2 parameters instead of k-squared)
- Uses the same 142 quarterly observations as the VAR
- Follows established regulatory methodology

We built the satellite model, and it produced the best out-of-sample performance of any approach we tested.

### How the Models Work Together

The final architecture uses **two complementary models**:

1. **Satellite model** (primary, for scenario forecasts): "Given this NGFS macro path, what happens to loans?" Simple, transparent, best performance, follows industry practice.

2. **Quarterly VAR** (supporting, for causal narrative): "Why does unemployment drive C&I loans but not consumer loans? How do shocks propagate?" Provides the economic story through impulse responses and Granger causality.

Together they answer both "what happens?" and "why does it happen?" — which is what BofA asked for.

---

## 3. Key Decisions and Justifications

### Variable Selection

**C&I loan drivers: unemployment, Fed Funds rate, CPI inflation**
- Unemployment is the dominant driver (statistically significant at p < 0.001 in every model we tested). When unemployment rises, businesses borrow less. This is consistent across annual, quarterly, and satellite models.
- Fed Funds rate and CPI are included as controls but are not individually significant. They capture monetary policy and price dynamics that may affect lending conditions indirectly.

**Consumer loan drivers: unemployment, Fed Funds rate, 10-Year Treasury yield, CPI inflation**
- The Fed Funds rate is the dominant driver for consumer loans (p = 0.021). Consumer borrowing (mortgages, auto loans) prices off interest rates.
- The 10-Year Treasury yield is included because consumer loan products like mortgages are tied to long-term rates. It is marginally significant in the quarterly VAR (Granger p = 0.048).
- Unemployment is NOT significant for consumer loans (p = 0.49 in quarterly VAR, p = 0.86 in satellite). This is a key finding: C&I and consumer loans respond to different economic channels.

**Consumer drivers we tested but excluded:**
- House prices (Case-Shiller HPI): available from FRED and NGFS. Does not improve the model by BIC. Not significant.
- Real disposable income: available from FRED and NGFS. Does not improve the model. Not significant.
- These were tested specifically because BofA asked about them. The finding that they don't matter is itself useful — it tells us the interest rate channel dominates the consumer lending response.

### Frequency Handling

The NGFS scenarios are annual. FRED loan data is monthly. We tried four approaches:

1. **Annual aggregation** (average monthly to annual): Only 36 observations. Too few for reliable multivariate models.
2. **Quarterly aggregation** (average monthly to quarterly): 142 observations. Sweet spot — enough data for reliable estimation while still being relatively close to the NGFS annual frequency.
3. **MIDAS** (use monthly data directly to predict annual): Promising in theory but failed in practice with our sample size. Weight functions collapsed.
4. **Satellite at quarterly frequency** (our final choice): 142 observations with NGFS interpolated to quarterly. Best performance.

### COVID Treatment

BofA confirmed that **dummy variables** are the standard approach — "that's the way a lot of people have been doing it." We flag March 2020 through June 2021 as the COVID period. The dummy absorbs the COVID shock during estimation. COVID quarters are excluded from out-of-sample evaluation, per BofA's instruction.

An important finding: COVID hit C&I and consumer loans asymmetrically. C&I loans spiked upward (PPP lending), while consumer loans dropped. A single dummy variable treats both the same, which is a simplification. We note this as a limitation.

### Training Window

We use 1990 to 2025 (35 years, 142 quarterly observations). BofA said to include "at least three decades" to capture major business cycles: the early-1990s recession, the 2001 tech bubble, the 2008 financial crisis, and the COVID shock. Going back further would add data but from a structurally different monetary policy regime (pre-Great Moderation).

### Model Selection: Why Satellite Over VAR for Scenarios

Three reasons, in order of importance:

1. **Industry credibility.** The Fed, ECB, and BoE all use satellite models for stress testing. Saying "we follow the same methodology as the Fed" gives our analysis immediate credibility with a BofA audience.

2. **Better out-of-sample performance.** The satellite model beats every other approach we tested — including the VAR — in predicting loan growth on data the model hasn't seen.

3. **Cleaner scenario conditioning.** NGFS paths plug directly into the satellite equation as inputs. No need to override the model's own dynamics. The model never tries to forecast unemployment — it just translates a given unemployment path into a loan outcome.

---

## 4. Data Inventory

### FRED Economic Data (10 series, in `data/raw/`)

| File | What It Contains | Frequency | Date Range | Role |
|------|-----------------|-----------|------------|------|
| BUSLOANS.csv | Commercial & Industrial loan balances | Monthly | 1947-2025 | Target (C&I) |
| CONSUMER.csv | Consumer loan balances | Monthly | 1947-2025 | Target (Consumer) |
| UNRATE.csv | Unemployment rate | Monthly | 1948-2026 | Key C&I driver |
| FEDFUNDS.csv | Federal Funds rate (Fed's policy rate) | Monthly | 1954-2026 | Key consumer driver |
| DGS10.csv | 10-Year Treasury yield | Daily | 1962-2026 | Consumer driver |
| CPIAUCSL.csv | Consumer Price Index | Monthly | 1947-2026 | Inflation control |
| GDPC1.csv | Real GDP | Quarterly | 1947-2025 | Reference (not in models) |
| CSUSHPINSA.csv | Case-Shiller Home Price Index | Monthly | 1987-2025 | Tested, not significant |
| DSPIC96.csv | Real Disposable Personal Income | Monthly | 1959-2025 | Tested, not significant |
| UMCSENT.csv | Michigan Consumer Sentiment | Monthly | 1952-2026 | Downloaded, not used |

### NGFS Climate Scenario Data (2 files, in `data/raw/`)

| File | What It Contains | Size |
|------|-----------------|------|
| ngfs-phase5-nigem.xlsx | Macro-financial variables (GDP, unemployment, inflation, interest rates, house prices, income) under 7 climate scenarios, from 3 different climate models (GCAM, REMIND, MESSAGEix). Annual, 2022-2050. | 26 MB |
| ngfs-phase5-iam.xlsx | Climate/energy variables (carbon prices, emissions, energy mix, temperature). Annual or 5-year steps, 2020-2100. | 61 MB |

**Important:** The NiGEM file stores Baseline scenario as levels but all other scenarios as *differences from baseline*. You must reconstruct levels by adding the difference back to the baseline. This tripped us up early on.

### Three Scenarios We Focus On

| Scenario | What It Assumes | Key Feature |
|----------|----------------|-------------|
| **Net Zero 2050** | Early, gradual climate policy. Carbon price rises smoothly to hundreds of dollars per ton by 2050. | Orderly transition. Higher short-term costs, lower long-term physical damage. |
| **Delayed Transition** | No action until ~2030, then sudden, aggressive policy. Carbon price jumps abruptly. | Disorderly transition. Low short-term costs, then a shock. |
| **NDCs (Nationally Determined Contributions)** | Countries follow current pledges. Moderate policy. | Middle ground. Some transition costs, growing physical risk. |

---

## 5. Results Summary

### Model Performance (Out-of-Sample)

Out-of-sample means: we trained the model on data up to a certain point, then tested how well it predicted the next quarter — data the model had never seen. We repeated this for every quarter from 2005 through 2025 (excluding COVID), re-training each time. This is the honest test of whether a model actually works.

| Model | Purpose | C&I Improvement vs Benchmark | Consumer Improvement vs Benchmark |
|-------|---------|------------------------------|-----------------------------------|
| Annual VAR | Reference (failed) | -2.2% (worse) | -28.0% (worse) |
| Quarterly VAR | Causal narrative | +11.7% | +7.5% |
| ADL-MIDAS | Course method demo | +1.7% | +21.0% (unreliable) |
| **Satellite** | **Primary scenario model** | **+22.8% (p=0.015)** | **+19.1% (p=0.077)** |

The satellite model is the clear winner. The Diebold-Mariano statistical test confirms the C&I improvement is significant (p = 0.015) and the consumer improvement is significant at the 10% level (p = 0.077).

### Scenario Forecasts

Using the satellite model, here's what the three scenarios imply for loan balances by 2050 (starting from an index of 100 in 2025):

| Loan Type | Net Zero 2050 | Delayed Transition | NDCs |
|-----------|---------------|--------------------|----- |
| C&I Loans | **188** | 186 | 187 |
| Consumer Loans | 325 | 326 | 326 |

**The scenario differences are small** — roughly 2 index points for C&I and less than 1 for consumer. This is because the macro variables that drive lending (unemployment, interest rates) don't diverge dramatically across NGFS scenarios for the US. The US economy is projected to grow under all scenarios — the question is by how much, and through what channel.

### What the Drivers Look Like

**C&I Loans — Driven by the labor market:**
- A 1 percentage point increase in unemployment reduces C&I loan growth by 1.77 percentage points next quarter
- Net Zero keeps unemployment lower (gradual transition avoids sudden job losses), which is why C&I loans do slightly better under early action
- This makes intuitive sense: businesses borrow more when employment is strong

**Consumer Loans — Driven by interest rates:**
- A 1 percentage point increase in the Fed Funds rate increases consumer loan growth by 0.84 percentage points next quarter
- The positive sign may seem counterintuitive but reflects that rate hikes often accompany strong economies where consumers are borrowing more
- Consumer loans are insensitive to scenario choice because US interest rate paths are similar across NGFS scenarios

---

## 6. What We Tried That Didn't Work

These are not failures — they're part of the process, and each one taught us something important. BofA said they value critical thinking and honest methodology. Showing what didn't work and why is part of that.

### The Annual VAR (36 observations, failed out-of-sample)

We started with annual data because NGFS scenarios are annual — matching frequencies seemed natural. But 36 observations (1990-2025) is not enough to reliably estimate a VAR with 4-5 interacting variables. The model memorized patterns in the training data that didn't generalize. After fixing a data bug, the annual VAR performed *worse* than just using past loan growth to predict future loan growth.

**What we learned:** Sample size matters more than frequency matching. The quarterly approach (142 observations) was the right trade-off.

### The DGS10 Data Bug

The 10-Year Treasury yield is published daily (about 16,700 data points), while all our other variables are monthly. Our code treated it like monthly data, which caused roughly 36% of months to silently drop from the dataset. This inflated growth rates and made the annual VAR appear to beat the benchmark — an artifact of data corruption.

**What we learned:** Always check your data dimensions. The fix was two lines of code (aggregate daily to monthly before differencing), but finding it required a systematic code review. We documented the full impact in a corrections log.

### The MIDAS Weight Collapse

The ADL-MIDAS model, based on Professor Pesavento's Week 7 lecture, was designed to use monthly data directly without aggregating to quarterly. In theory, this preserves information about which months within the year matter most. In practice, the estimated weight functions collapsed — putting all weight on a single month, which defeats the purpose.

Research into the academic literature identified seven causes, including the wrong optimization algorithm, too many parameters for our small sample, and a CPI transformation error. The fundamental issue: with only 34 annual observations, the data simply cannot distinguish which months matter.

**What we learned:** MIDAS is a powerful technique for large datasets, but it needs more data than we have. The satellite model achieves the same goal (using macro data to predict loans) with a simpler, more robust approach. We also learned that diagnosing model failures is itself a valuable analytical exercise.

### Consumer Drivers That Didn't Add Value

BofA specifically asked us to explore house prices, disposable income, and consumer sentiment as additional consumer loan drivers. We fetched the data from FRED, discovered that NGFS even provides scenario paths for house prices and income, and tested them in the expanded satellite model.

Result: neither variable improves the model. The information criterion (BIC) prefers the simpler model without them. The Fed Funds rate alone captures the consumer lending signal.

**What we learned:** Not every variable that sounds relevant actually helps predict. Rigorous testing is what separates a good model from one that just has a lot of variables. The finding itself is actionable — it tells a bank that monitoring the Fed Funds rate is more important for consumer loan portfolios than monitoring house prices.

---

## 7. Limitations and Future Work

### Honest Limitations

1. **We're projecting 25 years into the future using 35 years of history.** The models assume the relationship between macro variables and loans stays constant over time. If climate change fundamentally alters how the economy works — which is kind of the point — our historical relationships may not hold. This is a limitation shared by every model in this space, including the Fed's.

2. **Scenario spreads are narrow.** The difference between Net Zero and Delayed Transition is only about 2 index points at 2050. This doesn't mean climate policy doesn't matter — it means the *aggregate US macro variables* (unemployment, rates) don't diverge much across scenarios. Sector-level or regional analysis might show larger differences. BofA told us to stay aggregate, so we did.

3. **Consumer model explains only 8% of in-sample variation.** Most consumer loan dynamics come from factors we can't observe — individual credit decisions, changing product mixes, regulatory shifts. The model captures the directional signal (Fed Funds rate matters) but misses the level. The out-of-sample improvement (+19.1%) shows it still adds value for forecasting.

4. **Linear models only.** We assume the same relationship holds in booms and recessions. A disorderly climate transition might produce nonlinear effects — tipping points where the relationship breaks down. This is acknowledged but not modeled (BofA said no black-box ML, and nonlinear models would need more data than we have).

5. **No feedback from loans to the economy.** The satellite model treats macro paths as given. In reality, a collapse in lending could worsen a recession, creating a feedback loop. The VAR captures this theoretically but can't be used for clean scenario conditioning. We note this as a simplification inherent in the satellite approach.

### Future Work (if continued)

- **Mincer-Zarnowitz test** for forecast optimality (checks whether our forecasts are unbiased)
- **Scenario narrative visualization** — a multi-panel figure walking through each scenario's economic story
- **Sector-level analysis** if data becomes available (would show larger scenario spreads)
- **Nonlinear extensions** if sample size grows (threshold models for different economic regimes)
- **Rolling stability analysis** — test whether the macro-to-loan relationship is changing over time

---

## 8. Executive Takeaways for BofA

These are the 5 headline findings to build the presentation around. Each one answers a question an executive would ask.

### 1. "We use the same methodology the Fed uses."

Our primary model follows the satellite equation approach used in the Fed's DFAST stress tests, the ECB's climate stress tests, and the Bank of England's CBES. This isn't an academic exercise — it's the industry standard for translating climate scenarios into credit outcomes. The model is transparent, explainable, and performs better than alternatives in out-of-sample evaluation.

### 2. "C&I and consumer loans respond to different macro channels."

This is the core finding. C&I loans are driven by the labor market (unemployment, p < 0.001). Consumer loans are driven by interest rates (Fed Funds, p = 0.021). Unemployment is *not* significant for consumer loans. This means a bank needs to monitor different indicators for different parts of its loan book — and the same climate scenario will affect each part differently.

### 3. "Early action (Net Zero) is slightly better for C&I lending."

Under Net Zero, the gradual climate transition keeps unemployment lower, which benefits business lending. C&I loan balances reach an index of 188 by 2050 under Net Zero vs. 186 under Delayed Transition. The difference is modest because US macro paths don't diverge dramatically across scenarios, but the direction is consistent across every model we tested.

### 4. "Consumer loans are largely insensitive to climate scenario choice."

Consumer loan projections are essentially identical across all three scenarios (325-326 by 2050). Consumer borrowing responds to interest rates, and US interest rate paths are similar across NGFS scenarios. This is itself an important finding for portfolio risk management — climate scenario analysis matters much more for the C&I book than the consumer book.

### 5. "House prices and disposable income don't improve consumer loan predictions."

We tested these drivers specifically because BofA asked about them. The data says the Fed Funds rate alone captures the consumer lending signal. This is actionable: for consumer loan stress testing, monitoring the policy rate path is more valuable than tracking house prices or income.

---

## Where to Find Things

| What You Need | Where It Lives |
|---------------|---------------|
| Presentation-ready figures (35 total, 300 DPI) | `outputs/figures/` |
| Satellite model scenario results | `outputs/tables/satellite_summary.csv` |
| VAR model scenario results | `outputs/tables/scenario_summary.csv` |
| Plain-English explanation of all code | `docs/notebook-walkthrough.md` |
| Everything BofA told us | `facts/by-source/feb20-qa-session.md` |
| Full research factbase (613 facts) | `facts/by-source/` (14 files) |
| MIDAS methodology research report | `artifacts/reports/2026-02-25-ardl-midas-report.md` |
| Bug fix documentation | `docs/corrections-log-2026-02-24.md` |
| This document | `docs/project-history.md` |
