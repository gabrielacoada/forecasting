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

## Current State (checkpoint 2026-02-20, session 3)

### Data (9 files in data/raw/)
- **FRED series (7):** BUSLOANS.csv, CONSUMER.csv, GDPC1.csv, UNRATE.csv, FEDFUNDS.csv, DGS10.csv, CPIAUCSL.csv
- **NGFS scenario data (2):** ngfs-phase5-iam.xlsx (61MB), ngfs-phase5-nigem.xlsx (26MB)
- Status: Downloaded, validated, all clean (see data integrity audit)

### NGFS Data Structure (critical for debugging)
- **NiGEM** (`ngfs-phase5-nigem.xlsx`): Macro-financial variables (GDP, unemployment, inflation, rates, equity/house prices). **Baseline stores levels; other scenarios store % or absolute diffs from baseline.** Must reconstruct levels via `baseline * (1 + pct_diff/100)` or `baseline + abs_diff`. 160 variables, 3 IAM models, 7 scenarios, 2022-2050.
- **IAM** (`ngfs-phase5-iam.xlsx`): Climate/energy variables (carbon prices, emissions, energy mix). Stores levels directly. GDP damage estimates only available for REMIND (not GCAM). 2020-2100.
- **Known gotchas**: Not all variable x scenario x model combinations exist. Current Policies has no `(transition)` decomposition. GDP levels in NiGEM are Baseline-only.

### Notebooks (3)
- `empirical_analysis.ipynb` — FRED data exploration, unit root tests, ACF/PACF, AR baselines, cross-correlations, COVID analysis
- `ngfs_exploration.ipynb` — NGFS scenario parsing, visualization, IAM model comparison, macro path extraction. **All 5 plots validated (fixed 5 bugs in session 2).**
- `scenario_forecasting.ipynb` — VAR estimation, scenario-conditional forecasts, IRFs, OOS evaluation, fan charts

### Outputs (21 figures, 1 table)
- **Empirical (NB1, 7):** levels_overview, growth_rates, acf_pacf_growth, covid_zoom, bic_ar_selection, cross_correlations, rolling_stats
- **NGFS (NB2, 6):** ngfs_scenario_paths, ngfs_scenario_diffs, ngfs_model_uncertainty, ngfs_iam_us, ngfs_risk_decomposition, ngfs_macro_paths_transformed
- **Forecasting (NB3, 8):** annual_data_panel, irf_ci_loans, irf_consumer_loans, oos_evaluation, scenario_fan_charts, cumulative_impact, scenario_comparison_full, ngfs_macro_paths_transformed
- **Table:** scenario_summary.csv — 18 rows (2 loan types x 3 scenarios x 3 horizons), zero NaN

### Documentation (docs/)
- `notebook-walkthrough.md` — Detailed walkthrough of all 3 notebooks: purpose, step-by-step, data in/out, decisions, limitations, pipeline overview
- `data-integrity-audit.md` — Full audit of every data handoff point across the pipeline. Result: **zero red flags**. Each notebook reads raw source files independently, so NB2's blank-plot bugs had zero impact on NB3's results.

### Scenario Forecast Results (from scenario_summary.csv)
| Loan Type | Scenario | 2030 Growth | 2050 Growth | 2050 Balance Index |
|-----------|----------|-------------|-------------|-------------------|
| C&I | Net Zero | +3.64% | +3.60% | 243.1 |
| C&I | Delayed Trans. | +3.19% | +3.50% | 225.8 |
| C&I | NDCs | +3.19% | +3.40% | 229.2 |
| Consumer | Net Zero | +5.03% | +5.42% | 350.9 |
| Consumer | Delayed Trans. | +5.32% | +5.58% | 410.0 |
| Consumer | NDCs | +5.32% | +5.59% | 385.1 |

### Facts & Analysis
- 444 facts across 10 source files (latest: feb20-qa-session.md, Feb 20)
- 3 analysis runs (comprehensive v1, comprehensive v2, gap analysis)
- 1 summary report
- Questions: 5 answered, 3 partially answered

### What Was Done This Session (Feb 20, session 3)
- Completed full data integrity audit across all 3 notebooks
  - Verified every input CSV, NGFS Excel file, intermediate DataFrame, and output file
  - Confirmed NB2 exports zero data files — NB3 reads raw sources independently
  - Confirmed NB2's 5 blank-plot bugs had zero downstream impact on NB3 results
  - Confirmed scenario_summary.csv: 18 rows, 7 columns, zero NaN, all scenarios present
  - Result: **no red flags**
- Created comprehensive notebook walkthrough documentation (32 KB)
- Created data integrity audit report (8 KB)

### What's Next
1. **Consumer driver expansion** — Test house prices (CSUSHPINSA), Michigan sentiment (UMCSENT), real disposable income (DSPIC96) in consumer VAR
2. **Leading/lagging indicator audit** — Document timing properties of all variables per BofA warning
3. **Forecast evaluation** — Apply Mincer-Zarnowitz regression and DM test (from Week 6) to OOS results
4. **Scenario narrative visualization** — Multi-panel figure showing NGFS variables with annotations
5. **Actionable insights framework** — Develop 3-5 executive-level takeaways for presentation
6. **Next Q&A ~March 3** — Prepare to show preliminary results and get BofA feedback

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