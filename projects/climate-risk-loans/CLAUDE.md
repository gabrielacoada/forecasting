# Project: Climate Risk Impact on Banking Loan Portfolios

## Domain Context

This is a semester-long case study project for Professor Pesavento's Forecasting and Time Series course (Spring 2026) at Emory University, sponsored by Bank of America's Treasury Quantitative Analytics team.

### The Core Question
How does climate change/climate risk impact commercial and consumer loan portfolios in the banking industry?

### Two Types of Climate Risk
- **Physical risk**: Immediate effects — more powerful storms, storm surges, property damage
- **Transition risk**: How humanity reacts — carbon taxes, regulatory changes, policy shifts, GDP impacts, interest rate changes

### Project Sponsors
- Bank of America Treasury team (4 people)
- They do NOT currently work on climate risk for the bank — this is exploratory
- Contact: `emory_climate_case_study@bofa.com` (underscores between words)
- Keep analysis industry-level, NOT specific to Bank of America

### Key Evaluation Criteria (from kickoff + Q&A)

**Methodology & Modeling Decisions**
- Variable/feature selection WITH justification
- Forecasting framework design given NGFS + FRED data
- Handling uncertainty, missing data, different frequencies, regions, imperfect data

**Transparency & Explainability**
- Models must be transparent, explainable, defensible — NOT black-box ML
- Must justify each modeling choice logically and in business terms

**Critical Thinking & Framing**
- This is ambiguous with no single correct answer — they know that
- They care about: problem framing, framework trade-offs, sample period decisions, COVID treatment, business cycle coverage, training/test split design

**Communication & Presentation Quality**
- Translate technical work into high-level insights for non-technical decision-makers
- Strategic implications (financial stability, portfolio risk)
- Clear, compelling visualizations
- Don't fill 5 pages just to fill them — concise and clear communication wins

**What they explicitly said they do NOT care about:**
- Raw model accuracy
- Code syntax or coding details
- Perfect results

### Deliverables
1. **Presentation** (30 min): High-level insights, strategic decisions, visualizations. At least some BofA team in person.
2. **Technical report** (max 5 pages): Methodology, variable selection reasoning, limitations, refinements. Concise > long.
3. **Code**: NOT required for grading. Professor grades report + presentation.

### Timeline
- Feb 12: Kickoff (completed)
- Feb 20: First Q&A session (completed) — see "Q&A Session 1" section below
- Throughout semester: Up to 2 optional Q&A sessions per team (on demand, business hours)
- April 9: Final presentations (30 min per team, likely in person at Emory, Rich building)

### Class Integration
- Professor Pesavento grades based on report + presentation
- Technical report uploaded to Canvas
- Two teams competing — rubric TBD, winner gets a prize (TBD)
- Team names required (creativity = bonus points)
- Tuesday class will discuss team logistics

## Data Sources

### Primary
- **BUSLOANS** (FRED): Commercial & Industrial loans — explicitly specified as the main target
- **CONSUMER** (FRED): Consumer loans — confirmed in Q&A (ticker is "CONSUMER", uppercase)
  - Teams can do C&I only, consumer only, or BOTH (doing both is "an even more interesting challenge")
- **NGFS climate scenarios**: https://data.ene.iiasa.ac.at/ngfs/#/downloads
  - Downloaded as zip file with multiple model outputs
  - Multiple model families: GCAM, REMIND, MESSAGEix
  - Variables: carbon prices, GDP, temperature, CO2 emissions, energy costs
  - Scenarios: Net Zero 2050, Delayed Transition, Current Policies, etc.
  - Note: macro variables will differ slightly depending on whether modeling commercial vs consumer loans

### Supporting
- FRED macroeconomic data: unemployment, CPI, interest rates, GDP
- Historical economic data for model training
- FRED data goes back to 1940s in some series, 1990s in others

### Known Data Challenges
- NGFS scenarios are **annual** frequency
- FRED loan data is **monthly/quarterly**
- Frequency mismatch must be addressed (interpolation vs. aggregation)
- Different NGFS model families may give different results
- Regional vs. national granularity questions

### Training Window & COVID (from Q&A)
- Training window is YOUR DESIGN CHOICE — part of the modeling process
- Must cover enough **business cycles** for good results
- **COVID structural break** is a major question they actively discuss at BofA
  - How do you treat the COVID shock period?
  - How different is it from historical patterns?
  - This is something they regularly ask modelers — good topic for presentation
- Need to think about training/test split design

## Constraints
- Python only (course requirement)
- Models must be transparent and explainable — no black-box ML
- Analysis must be industry-level, not bank-specific
- Focus on time series / forecasting methods from the course
- Open-ended question — no single correct answer

## Applicable Course Methods
- Time series forecasting (AR, ARMA, ARIMA)
- VAR models (for multivariate relationships)
- Unit root testing (ADF, PP, KPSS) for stationarity
- Information Criteria for model selection
- Trend analysis and structural breaks
- Scenario-based forecasting

## Source Preferences
- Prioritize: NGFS documentation, Fed staff reports, academic papers on climate stress testing
- Key papers cited in project doc:
  - Acharya et al., "Climate Stress Testing" (2023): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1059.pdf
  - Jung et al., "U.S. Banks' Exposures to Climate Transition Risks" (2024): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1058.pdf
- Also useful: NGFS scenario portal documentation, European Banking Authority climate risk publications

## Analysis Priorities
1. Understanding what NGFS scenarios contain and how to use them
2. Establishing the link between macro/climate variables and loan portfolios
3. Choosing and justifying the right forecasting framework
4. Feature selection with economic rationale
5. Clear scenario comparison and visualization
6. Honest discussion of limitations and uncertainty

## Q&A Session 1 — Feb 20, 2026

### COVID Treatment → USE DUMMY VARIABLES
- BofA confirmed: **dummy variables are the right approach**. "That's the way a lot of people have been doing it."
- When they went through COVID internally (2021-2022), it "muddled the back test data points" — they couldn't use those observations.
- **Critical:** When presenting out-of-sample results, make sure COVID is excluded from the evaluation period. "If you're giving us your out-of-sample period, make sure you have it out."

### Outcome Variable → OPEN-ENDED, JUSTIFY YOUR CHOICE
- They're fine with cumulative balance, growth rates, or any transformation.
- "It really depends on what you think your model will be able to predict best, and be able to justify why you did that variable transformation."
- **Key:** Whatever you model, make sure the final insights translate clearly. "If your final conclusion is 'we see the industry dropping' or 'the growth rate is negative,' how are you going to explain your final conclusion? Make sure you're able to derive it."

### Training Window → AT LEAST 3 DECADES (1990s+)
- "You want to make sure you include enough business cycles."
- Must include: 2008 GFC, 2001 tech bubble, 1990s effects. "At least the last three decades."
- **But:** "Just because you have more historical data doesn't necessarily mean your models perform better. What matters more is that your historical data captures relevant business cycles."
- Some variables may not go back as far — that's a trade-off to discuss.

### Frequency → TRY MULTIPLE, PICK WHAT WORKS BEST
- Open-ended. "You could just give it a try with different frequencies and see what makes your model perform the best."
- They acknowledged different NGFS models may have different frequencies.
- "Be creative with your approach to solving these data problems."
- Professor Pesavento will teach a MIDAS class (mixed-frequency data analysis) earlier than planned to help with this.

### Consumer Loan Approach → INDIRECT MACRO CHANNEL APPROVED, BUT DIG DEEPER ON DRIVERS
- Our approach (unemployment + interest rates → consumer loans) was approved: "I think that makes sense."
- **But they pushed for more:** "Just make sure that you're very thorough about consumer drivers. Rates is important. Unemployment is obviously very important, but are there other aspects of it that matter to consumers?" — Think about: house prices, disposable income, consumer confidence, etc.

### Fed Paper Benchmarks → USE AS CONTEXT, NOT AS TARGETS
- The 14% max exposure from Jung et al. is "interesting context" and a "guideline."
- They don't expect us to replicate those results — those papers use bank-specific balance sheet data we don't have.
- "I think that one or both of the papers had maybe more complex modeling frameworks that included a wider variety of data sources, including bank specific balance sheet information, regional segmentation."

### Industry Granularity → STAY AGGREGATE
- **Do NOT go to firm level.** "We don't want you to go to the firm level — like, do you want to make it about America or Citi? That's not something we want."
- "We want you to make statements about industry."
- If you find sector data, you can explore it for extra interest, but core analysis should be aggregate US.
- Going granular creates a driver-matching problem: "If you start to break out the sectors or the regions, then do you need region specific unemployment?"

### Scenarios & Time Horizon → ALL SCENARIOS, ANY HORIZON, OPEN-ENDED
- No preference on which scenarios. "Any or all?"
- No preference on forecast horizon. "As long as you have your model, you can just plug in the numbers."

### Confidence Intervals & Uncertainty → THEY WANT TO SEE BANDS
- "A lot of times there's a lot of value from the confidence bands around the estimate."
- "It is about how comfortable we are with the number within certain bounds."
- This aligns with showing model uncertainty across the 3 IAM families.

### Scenario Visualization → SHOW YOU UNDERSTAND THE STORIES
- "It would be great if you guys show a robust understanding of what different data sets are telling you."
- "Visualize what each climate scenario — Hot House, Current Policies — how they differ, in terms of climate variables and economic variables."
- "Really try to show that you thought about what these variables mean, the story they're telling you, and how they're applicable to your forecasting model."

### Actionable Insights → GO BEYOND THE NUMBER
- Don't just say "loans drop 2%." "Can you dig into that number? Answer some important policy questions or systemic risk questions?"
- "If you're going to present this to an executive making strategic decisions about increasing loan exposures, you want to be able to derive granular suggestions."
- "Try to be creative."

### Leading vs. Lagging Indicators → WATCH YOUR TIMESTAMPS
- **Critical warning from BofA:** "Make sure you understand which ones are leading and which ones are lagging."
- GDP is lagged — a GDP print covers the previous quarter, not the current one.
- "The one thing you don't want to do when you're building a forecast is accidentally include a future point in your time series."
- "I've seen it in practice — your model ends up being so good, and you just don't realize that you ended up using tomorrow's data to predict today."

### Updated Timeline
- Midterm: **March 5**
- Spring break: March 10-12
- Next possible Q&A: around **March 3** (before spring break)
- April 9: Final presentations

### Team Names
- **Too Big to Melt** (our team)
- **Green Horizon** (other team)

## Research Phases
- **Phase 1** (Feb 12 - Feb 20): Understand NGFS data, explore FRED series, formulate framework ideas, prepare Q&A questions — COMPLETE
- **Phase 2** (Feb 20 - March): Build models, iterate on feature selection — IN PROGRESS
- **Phase 3** (March - April): Refine, visualize, prepare presentation

## Current State (checkpoint 2026-02-25, session 5)

### Data (12 files in data/raw/)
- **FRED series (10):** BUSLOANS.csv, CONSUMER.csv, GDPC1.csv, UNRATE.csv, FEDFUNDS.csv, DGS10.csv, CPIAUCSL.csv, CSUSHPINSA.csv (Case-Shiller HPI), DSPIC96.csv (real disposable income), UMCSENT.csv (Michigan sentiment)
- **NGFS scenario data (2):** ngfs-phase5-iam.xlsx (61MB), ngfs-phase5-nigem.xlsx (26MB)
- Status: Downloaded, validated, all clean

### NGFS Data Structure (critical for debugging)
- **NiGEM** (`ngfs-phase5-nigem.xlsx`): Macro-financial variables (GDP, unemployment, inflation, rates, equity/house prices). **Baseline stores levels; other scenarios store % or absolute diffs from baseline.** Must reconstruct levels via `baseline * (1 + pct_diff/100)` or `baseline + abs_diff`. 160 variables, 3 IAM models, 7 scenarios, 2022-2050.
- **IAM** (`ngfs-phase5-iam.xlsx`): Climate/energy variables (carbon prices, emissions, energy mix). Stores levels directly. GDP damage estimates only available for REMIND (not GCAM). 2020-2100.
- **Known gotchas**: Not all variable x scenario x model combinations exist. Current Policies has no `(transition)` decomposition. GDP levels in NiGEM are Baseline-only.

### Notebooks (6)
- `empirical_analysis.ipynb` — FRED data exploration, unit root tests, ACF/PACF, AR baselines, cross-correlations, COVID analysis
- `ngfs_exploration.ipynb` — NGFS scenario parsing, visualization, IAM model comparison, macro path extraction. **All 5 plots validated (fixed 5 bugs in session 2).**
- `scenario_forecasting.ipynb` — Annual VAR estimation, scenario-conditional forecasts, IRFs, OOS evaluation, fan charts. **DGS10 bug fixed Feb 24. Annual VAR no longer beats AR baseline (was artifact of data bug).**
- `scenario_forecasting_quarterly.ipynb` — Quarterly VAR (142 obs vs 36 annual), same pipeline at quarterly frequency. **Built Feb 24.** DGS10 fix + Granger column order fix applied. Provides IRFs and Granger causality for the causal narrative.
- `scenario_forecasting_midas.ipynb` — ADL-MIDAS model using monthly FRED data directly (no aggregation loss). **Built Feb 24.** Uses Almon polynomial distributed lags on monthly regressors to predict annual loan growth. **Has degenerate weight issues — see ARDL-MIDAS analysis report.**
- `satellite_forecasting.ipynb` — **PRIMARY SCENARIO MODEL. Built Feb 25.** Satellite ADL equations following Fed DFAST / ECB / BoE stress testing methodology. Single-equation OLS with HAC standard errors. NGFS paths plug in directly as regressors. Includes expanded consumer model with house prices and income from NGFS. **Beats both AR baseline and quarterly VAR in OOS. C&I: +22.8% vs AR (DM p=0.015). Consumer: +19.1% vs AR (DM p=0.077).**

### Outputs (35 figures, 2 tables)
- **Empirical (NB1, 7):** levels_overview, growth_rates, acf_pacf_growth, covid_zoom, bic_ar_selection, cross_correlations, rolling_stats
- **NGFS (NB2, 5):** ngfs_scenario_paths, ngfs_scenario_diffs, ngfs_model_uncertainty, ngfs_iam_us, ngfs_risk_decomposition
- **Annual Forecasting (NB3, 8):** annual_data_panel, ngfs_macro_paths_transformed, irf_ci_loans, irf_consumer_loans, oos_evaluation, scenario_fan_charts, cumulative_impact, scenario_comparison_full
- **Quarterly Forecasting (NB4, 7):** quarterly_data_panel, quarterly_ngfs_paths, quarterly_irf_ci, quarterly_irf_consumer, quarterly_oos_evaluation, quarterly_scenario_fan_charts, quarterly_cumulative_impact
- **MIDAS (NB5, 5):** midas_weights_ci, midas_weights_consumer, midas_oos_evaluation, midas_scenario_fan_charts, midas_cumulative_impact
- **Satellite (NB6, 3):** satellite_oos_evaluation, satellite_scenario_fan_charts, satellite_cumulative_impact
- **Tables:** scenario_summary.csv (18 rows, VAR-based), satellite_summary.csv (18 rows, satellite-based)

### Documentation (docs/, 4 files)
- `notebook-walkthrough.md` — Detailed walkthrough of all notebooks: purpose, step-by-step, data in/out, decisions, limitations, pipeline overview. Updated Feb 24 for 5-notebook pipeline.
- `notebook-walkthrough-simplified.md` — Simplified walkthrough for non-technical teammates.
- `data-integrity-audit.md` — Full audit of every data handoff point across the pipeline. Result: **zero red flags**. Each notebook reads raw source files independently, so NB2's blank-plot bugs had zero impact on NB3's results.
- `corrections-log-2026-02-24.md` — Full corrections log documenting DGS10 bug, Granger column order fix, and impact on all results.

### Scenario Forecast Results (from scenario_summary.csv, corrected Feb 24)
| Loan Type | Scenario | 2030 Growth | 2050 Growth | 2050 Balance Index |
|-----------|----------|-------------|-------------|-------------------|
| C&I | Net Zero | +3.64% | +3.68% | 246.5 |
| C&I | Delayed Trans. | +3.25% | +3.50% | 231.7 |
| C&I | NDCs | +3.19% | +3.40% | 234.5 |
| Consumer | Net Zero | +5.03% | +5.42% | 346.4 |
| Consumer | Delayed Trans. | +5.32% | +5.58% | 352.0 |
| Consumer | NDCs | +5.32% | +5.59% | 349.3 |

### Facts & Analysis
- 613 facts across 14 source files (added 4 MIDAS source files, Feb 25)
- 4 analysis runs (comprehensive v1, v2, gap analysis, ARDL-MIDAS deep dive)
- 2 reports (original summary, ARDL-MIDAS report)
- Questions: 8 answered, 3 partially answered
- 6 notebooks total (added satellite model Feb 25). Bug fixes applied Feb 24 — see `docs/corrections-log-2026-02-24.md`.
- 35 figures across all notebooks, 2 summary tables

### What Was Done This Session (Feb 20, session 3)
- Completed full data integrity audit across all 3 notebooks
  - Verified every input CSV, NGFS Excel file, intermediate DataFrame, and output file
  - Confirmed NB2 exports zero data files — NB3 reads raw sources independently
  - Confirmed NB2's 5 blank-plot bugs had zero downstream impact on NB3 results
  - Confirmed scenario_summary.csv: 18 rows, 7 columns, zero NaN, all scenarios present
  - Result: **no red flags**
- Created comprehensive notebook walkthrough documentation (32 KB)
- Created data integrity audit report (8 KB)

### What Was Done Session 4 (Feb 24)
- Code review found and fixed **DGS10 daily data bug** in both `scenario_forecasting.ipynb` and `scenario_forecasting_quarterly.ipynb`
- Fixed **Granger causality column order** in quarterly notebook
- Built **quarterly VAR notebook** and **ADL-MIDAS notebook**
- Three-frequency comparison: Annual VAR, Quarterly VAR, ADL-MIDAS
- Full corrections log: `docs/corrections-log-2026-02-24.md`

### What Was Done Session 5 (Feb 25)
- **ARDL-MIDAS research pipeline** — Extracted 160+ facts from 5 academic sources (Ghysels 2004, 2007; JSS 2016; Foroni 2015; Franses 2016). Diagnosed 7 root causes of degenerate MIDAS weights. Analysis + report written.
- **Literature review of stress testing methods** — Found that Fed DFAST, ECB, and BoE all use **single-equation satellite models** for scenario-conditional forecasting, not VARs. VARs are used for causal analysis (IRFs/Granger), satellite models for scenario projection.
- **Fetched 3 new FRED consumer driver series**: CSUSHPINSA (Case-Shiller HPI), DSPIC96 (real disposable income), UMCSENT (Michigan sentiment) — per BofA request for expanded consumer drivers
- **Discovered NGFS has house prices and income paths** — `House prices (residential)` and `Real personal disposable income` are in NiGEM with full scenario coverage. This means the satellite model can use these as scenario-conditional regressors.
- **Built satellite model notebook** (`satellite_forecasting.ipynb`): Industry-standard ADL satellite equations with HAC standard errors. Three models: C&I, Consumer base, Consumer expanded (+ house prices, income).
- **Satellite model results** — Best OOS performance of any model:
  - C&I: RMSE 1.32, **+22.8% vs AR** (DM p=0.015, statistically significant)
  - Consumer: RMSE 3.89, **+19.1% vs AR** (DM p=0.077, significant at 10%)
  - Both outperform the quarterly VAR (+11.7% and +7.5%)
- **Consumer driver expansion**: House prices and income did NOT improve BIC over the base consumer model. Fed Funds rate remains the dominant consumer driver.
- **Diebold-Mariano tests implemented** with Harvey-Leybourne-Newbold small-sample correction
- Updated project.yaml, CLAUDE.md, PROJECT-STATUS.md, notebook-walkthrough.md

### OOS Results Summary (updated Feb 25)
| Frequency | Model | C&I RMSE | C&I vs AR | Consumer RMSE | Consumer vs AR |
|-----------|-------|----------|-----------|---------------|----------------|
| Annual | AR baseline | 10.10 | -- | 9.78 | -- |
| Annual | VAR | 10.32 | -2.2% (worse) | 12.52 | -28.0% (worse) |
| Annual | ADL-MIDAS | 9.93 | +1.7% | 7.72 | +21.0% |
| Quarterly | AR baseline | 1.71 | -- | 4.80 | -- |
| Quarterly | VAR | 1.32 | +11.7% | 3.89 | +7.5% |
| **Quarterly** | **Satellite** | **1.32** | **+22.8%** | **3.89** | **+19.1%** |

Key takeaway: **Satellite model is the best-performing approach** for both loan types. It follows the Fed/ECB/BoE stress testing methodology (single-equation ADL), beats both AR and VAR in OOS, and handles scenario conditioning cleanly (direct plug-in of NGFS paths). Quarterly VAR provides the causal narrative (IRFs, Granger). MIDAS has degenerate weight issues but demonstrates course material.

### What's Next
1. ~~**Consumer driver expansion**~~ — DONE (session 5). Tested house prices (CSUSHPINSA) and real disposable income (DSPIC96) in expanded consumer satellite model. BIC prefers base model — Fed Funds is the dominant consumer driver. House prices and income don't add OOS predictive power.
2. **Leading/lagging indicator audit** — Document timing properties of all variables per BofA warning about accidentally including future data. Satellite model uses lag=1 for all regressors, which addresses this.
3. ~~**Diebold-Mariano formal tests**~~ — DONE (session 5). C&I satellite: DM p=0.015 (significant). Consumer satellite: DM p=0.077 (significant at 10%). Mincer-Zarnowitz still TODO.
4. **Scenario narrative visualization** — Multi-panel figure showing NGFS variables with annotations telling the economic story behind each scenario
5. **Actionable insights framework** — Develop 3-5 executive-level takeaways for presentation (BofA: "Can you dig into that number? Answer some important policy questions?")
6. **Prepare for Q&A ~March 3** — Show satellite vs. VAR comparison, expanded consumer driver results, and DM test results to BofA for feedback before midterm

## Team Structure

Gabriela (me) — Technical Lead
- Owns all code, modeling, and technical decisions
- Presents the methodology section (12-15 min)
- Handles technical Q&A from BofA
- Currently refining models (consumer drivers, forecast evaluation)

[Name] — Presentation Lead
- Owns the slide deck, narrative arc, visuals
- Uses notebook-walkthrough.md and figures/ as source material
- Does NOT need to read code

[Name] — Report Writer
- Owns the 5-page technical report
- Uses notebook-walkthrough.md, analysis runs, and research reports
- Does NOT need to read code

[Name] — Economic Narrative
- Owns feature selection justification, policy implications, limitations
- Uses facts/by-source/ as source material
- Does NOT need to read code

Shared materials are on [Google Drive / GitHub — wherever you decide].
All teammates work from the docs/ and artifacts/ directories, not from notebooks directly.
Meeting planned for [date] to walk through results.