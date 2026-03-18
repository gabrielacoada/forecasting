# Context Brief: Problem Set 3

## Topics Covered
1. **Forecasting scenario analysis** — decision environment, forecast object/type/horizon, loss function, information set, forecasting approaches (Week 1 + Week 6)
2. **Trend model estimation** — daily vs annual observations, stock vs flow variables, forecast horizon considerations (Week 2)
3. **Seasonality** — reasons for seasonal adjustment, Census Bureau procedures (Week 2)

## Key Professor Terminology & Frameworks

### Question 1: Forecasting Scenario Analysis
From Week 6 lectures, Pesavento's **10 General Considerations for Forecasting**:
1. Forecast Object — what are we forecasting?
2. Information Set — what data is available?
3. Model Uncertainty — all models are false
4. Forecast Horizon (h) — 1-step, 12-step, 120-step?
5. Structural Change — are approximations stable?
6. Forecast Statement — point, interval, density, scenarios?
7. Forecast Presentation — graphical methods valuable
8. Decision Environment and Loss Function — cost of errors? Symmetric or asymmetric?
9. Model Complexity and Parsimony — bigger ≠ better
10. Unobserved Components — trend, seasonality, cycles handled?

**Loss functions** (key Week 6 concept):
- Quadratic: L(e) = e² → optimal forecast = conditional mean (symmetric)
- Absolute: L(e) = |e| → optimal forecast = conditional median (symmetric)
- Linlin: asymmetric → optimal forecast = conditional quantile d = b/(a+b)

**Pesavento's examples**: Stock investing = asymmetric (happy about upside surprises, unhappy about downside). Bus stop = asymmetric (late much worse than early).

**Key insight**: Under asymmetric loss, optimal forecasts are deliberately biased.

### Question 2: Trend Model — Daily vs Annual
From Week 2 lectures on trend estimation:
- Deterministic trend model: y_t = c + βt + u_t
- The model is estimated via OLS on TIME variable
- Key issue: **forecast horizon matters** — forecasting 365 steps ahead with daily data vs 1 step ahead with annual data
- Stock variable = measured at a point in time (end-of-year), not accumulated over a period
- For stock variables observed daily, intra-year observations contain noise irrelevant to end-of-year forecasting
- Pesavento emphasized: "Deterministic trends do not have an economics interpretation, yet incredibly powerful for forecasting"
- DW statistic near 0 in trend models = serial correlation in residuals

### Question 3: Seasonality
From Week 2 lectures:
- "Seasonality is a pattern that repeats every year"
- "From a micro point of view, seasonality comes from links of technology, preferences and institutions to the calendar"
- Two choices: seasonally adjusted vs non-seasonally adjusted data
- "If we are interested in forecasting non-seasonal fluctuations we may want to remove seasonality"
- "In general we want to forecast all variations in the series"
- "Data that is SA is passed through a complicated filter"
- Pesavento noted: "Be careful when you download data which kind of data you really want"
- Modeling seasonality with dummy variables (one per season, minus one for dummy variable trap)
- Seasonal dummies are deterministic → perfectly forecastable

**Why use seasonally adjusted data** (from lecture context):
- In macroeconomics, interest often centers on nonseasonal fluctuations (business cycle analysis)
- Seasonal patterns can obscure underlying trends and cyclical movements
- Policy decisions (monetary/fiscal) focus on deseasonalized changes
- Comparing month-to-month or quarter-to-quarter changes is easier with SA data

## Discussion Style Notes
- Use the 10-item forecasting framework explicitly when analyzing scenarios
- Reference loss functions by name (quadratic, absolute, linlin/asymmetric)
- Connect forecast type to the decision environment
- Be specific about what the "information set" includes
- For Q2, emphasize the distinction between sample size and forecast horizon
- For Q3, reference both the theoretical reasons and the practical Census Bureau procedure
