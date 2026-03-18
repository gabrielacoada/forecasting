# Gap Analysis — March 3, 2026

**Scope:** Full project gap assessment post-Q&A 2, with emphasis on modeling completeness before pivoting to presentation/deliverables.

---

## Gap Status from Previous Analysis (Feb 20)

| # | Gap | Status | Notes |
|---|-----|--------|-------|
| G1 | Consumer loan drivers | **CLOSED** | Tested CSUSHPINSA, DSPIC96, UMCSENT. BIC prefers base model. BofA accepted null result. |
| G2 | Leading/lagging indicator audit | **OPEN** | Satellite uses lag=1, but no formal documentation of timing properties for all variables. |
| G3 | Confidence interval methodology | **PARTIALLY CLOSED** | Fan charts built for satellite + VAR. But no parametric forecast intervals (±1.96σ) on satellite yet. BofA prefers fan charts, so this may be sufficient. |
| G4 | Scenario visualization & narrative | **OPEN** | Have NGFS figures from NB2, but no annotated narrative figure showing the economic story behind each scenario. BofA specifically asked for this. |
| G5 | Within-model-family comparison | **PARTIALLY CLOSED** | Satellite forecasts use all 3 IAM families. Cross-IAM spread visible in fan charts. But no dedicated figure or analysis isolating IAM family divergence. |
| G6 | Actionable insights framework | **OPEN** | No executive-level takeaways developed yet. BofA: "tell a story someone can take action on." |
| G7 | Course material integration (weeks 5-7) | **PARTIALLY CLOSED** | MIDAS (week 7 lab) attempted in Python + R. Satellite model applies ADL concepts. But no explicit tie-back to distributed lag lecture content. |
| G8 | Short-term NGFS scenarios | **NOT NEEDED** | BofA didn't ask for short-horizon forecasts. Full 2026–2050 horizon is fine. |
| G9 | Revenue recycling assumptions | **NOT NEEDED** | Too granular. BofA wants story, not NGFS internals. |

---

## NEW GAPS — Modeling

### M1. Satellite Model Robustness Testing [P1 — HIGH]
**What's missing:** The satellite model is our primary model, confirmed by BofA, but it has only been tested with one specification per loan type. No robustness checks have been performed.

**Specific tests needed:**
- **Lag sensitivity:** Current model uses lag=1. Test lag=2 and lag=3 to confirm BIC still prefers lag=1 (the C&I notebook does test lag=1 vs lag=2, but consumer doesn't).
- **Rolling window stability:** Re-estimate over rolling or expanding windows to check if coefficients are stable over time. If unemployment's coefficient flips sign in certain sub-periods, that undermines the narrative.
- **Recursive OOS:** Currently using pseudo-OOS from a fixed start date. Confirm the evaluation window choice doesn't drive the result (try starting 2010, 2012, 2015).
- **Residual diagnostics:** Check for heteroskedasticity (Breusch-Pagan or White test), serial correlation (Ljung-Box on satellite residuals), normality (Jarque-Bera). If residuals are non-normal or heteroskedastic, HAC standard errors may not be sufficient.

**Why it matters:** BofA said they're "pretty interested in how you benchmark your models." If someone asks "how robust is this?" and we only have one specification, that's weak.

### M2. Satellite Coefficient Interpretation [P1 — HIGH]
**What's missing:** We have the satellite OOS results and scenario forecasts, but we haven't extracted and presented the actual coefficient estimates, standard errors, and economic magnitudes.

**Specific deliverables:**
- Table of coefficients with HAC standard errors, t-stats, and p-values for each satellite model
- Economic interpretation: "A 1 percentage point increase in unemployment is associated with X% change in loan growth, controlling for other factors"
- Comparison of driver magnitudes across C&I vs consumer models
- COVID dummy coefficient: what is the estimated magnitude of the COVID shock?

**Why it matters:** BofA explicitly asked: "What macro variables were the most significant, by how much? Why does that make logical sense?" This is the core of the presentation narrative.

### M3. Model Comparison Framework [P1 — HIGH]
**What's missing:** We have 4 model families (AR, VAR, MIDAS, satellite) across 2 frequencies, but no single unified comparison table or figure that tells the story of WHY we ended up at the satellite model.

**Specific deliverables:**
- Unified OOS comparison table (already exists in CLAUDE.md but not as a presentation-ready figure)
- Forecast comparison plot: actual vs predicted for all models overlaid, showing where satellite wins
- Model selection narrative: "We started with VARs because X, found limitation Y, pivoted to satellite because Z"
- DM test matrix: pairwise comparisons (satellite vs VAR, satellite vs MIDAS, VAR vs AR, etc.)

**Why it matters:** BofA corrected our AR benchmark framing. The comparison isn't about beating a bar — it's about showing the progression of understanding. They also said they want to see "why a specific model framework like satellite model is telling you that these drivers are significant."

### M4. Mincer-Zarnowitz Forecast Efficiency Tests [P2 — MEDIUM]
**What's missing:** Listed as TODO since session 5. The MZ test checks whether forecasts are unbiased and efficient (regress actuals on forecasts — intercept should be 0, slope should be 1).

**Why it matters:** Complements the DM test. DM tells you which model is better; MZ tells you if your best model is actually any good in absolute terms. If the satellite model's MZ test rejects efficiency, that's a limitation to discuss honestly.

### M5. Structural Break / Parameter Stability [P2 — MEDIUM]
**What's missing:** No formal test for parameter stability across the sample. The 1990–2025 training window spans multiple regimes (1990s expansion, dot-com bust, GFC, post-GFC, COVID, post-COVID tightening). Coefficients estimated over the full sample may not reflect current relationships.

**Possible approaches:**
- Chow test at known break points (2008, 2020)
- CUSUM or CUSUMSQ test for gradual instability
- Rolling coefficient plot (estimate satellite over expanding window, plot coefficient path)

**Why it matters:** BofA raised this implicitly — "how different is COVID from historical patterns?" If the unemployment→loans relationship fundamentally changed after 2020, a model estimated over 1990–2025 may not be reliable for 2026–2050 projections.

### M6. MIDAS — Final Assessment [P3 — LOW]
**What's missing:** R-based MIDAS was completed but still doesn't beat the AR baseline. We should make a clear decision: is MIDAS in the presentation or not?

**Options:**
- Include as "we tried it, here's why it didn't work" (demonstrates rigor)
- Drop entirely and focus presentation time on satellite + VAR
- Brief mention in the report only

**Why it matters:** Time is finite. If MIDAS isn't adding value, spending more time on it trades off against robustness testing and narrative building for the satellite model.

---

## NEW GAPS — Data & Variables

### D1. Variable Mapping Completeness [P1 — HIGH]
**What's missing:** BofA said: "Be sure that the variable you use can be mapped to the scenario." We need an explicit mapping table showing:

| Satellite Regressor | FRED Source | NGFS NiGEM Variable | Transformation Match? |
|---------------------|------------|---------------------|----------------------|
| Unemployment change | UNRATE | Unemployment rate | Yes — both are rate levels, we difference |
| Fed Funds change | FEDFUNDS | Short-term interest rate | Yes — both are rate levels |
| GDP growth | GDPC1 | Real GDP | Yes — both in levels, we log-growth |
| CPI inflation | CPIAUCSL | CPI / Inflation rate | Needs verification — NiGEM may give inflation rate directly vs CPI level |
| 10Y Treasury change | DGS10 | Long-term interest rate | Yes — both are rate levels |

**Why it matters:** If there's a mismatch between how we transform FRED data for estimation vs how we transform NGFS data for scenario forecasting, the projections are invalid. This is the most dangerous silent bug.

### D2. Transition vs Physical Risk Decomposition [P2 — MEDIUM]
**What's missing:** BofA asked directly: "Whether you think you're capturing more transition or physical risk." We need to articulate this clearly.

**Assessment:** Our macro variables (unemployment, rates, GDP, CPI) primarily capture **transition risk** — policy-driven economic disruption. Physical risk (storms, property damage) would require regional data, insurance losses, or physical damage indices that we don't have. The NGFS scenarios themselves mostly model transition pathways; physical risk is embedded in the temperature/GDP damage channels (only available for REMIND, not GCAM).

**Deliverable:** A clear 2-3 paragraph explanation in the report + a slide or talking point for the presentation.

### D3. Historical Fit Visualization [P2 — MEDIUM]
**What's missing:** We have OOS evaluation plots but no in-sample fitted values plot showing how well the satellite model tracks actual loan growth over the full 1990–2025 period. This would make the COVID dummy impact visually obvious and help explain residual patterns.

---

## NEW GAPS — Interpretation & Narrative

### N1. Economic Intuition for Every Driver [P1 — HIGH]
**What's missing:** Plain-English explanation of WHY each variable drives loan growth, grounded in economic theory, not just statistical significance.

**Needed for each driver:**
- Unemployment → Consumer loans: When people lose jobs, they can't make payments → delinquencies rise → new lending contracts → portfolio shrinks
- Unemployment → C&I loans: Higher unemployment signals recession → businesses reduce investment → less demand for commercial credit
- Fed Funds → Consumer: Higher rates → higher borrowing costs → less consumer credit demand + more defaults on variable-rate debt
- Fed Funds → C&I: Higher rates → higher cost of capital → businesses delay investment, reduce credit line utilization
- GDP → C&I: Economic growth → business expansion → more demand for commercial credit
- CPI → Both: Inflation erodes real income, but also inflates nominal loan balances
- DGS10 → Consumer: Long-term rates directly affect mortgage rates, auto loan rates

**Why it matters:** BofA's #1 request from Q&A 2. This is the core of the presentation.

### N2. C&I vs Consumer Divergence Narrative [P2 — MEDIUM]
**What's missing:** Our results show C&I and consumer loans respond differently to climate scenarios. We mentioned this to BofA but didn't have a prepared explanation. Need:
- Which scenarios favor C&I vs consumer?
- WHY do they diverge? (Different driver sensitivities, different business cycle dynamics)
- What does this mean for a bank managing both portfolios?

### N3. Scenario Narrative — What Each Scenario MEANS [P2 — MEDIUM]
**What's missing:** We can generate forecasts under Net Zero, Delayed Transition, and NDCs, but we haven't written up what each scenario actually implies in human terms:
- **Net Zero 2050:** Aggressive early action. Short-term economic pain (carbon taxes, stranded assets) but long-term stability.
- **Delayed Transition:** Procrastination then panic. Low cost now, sharp adjustment later (post-2030).
- **NDCs / Current Policies:** Status quo. No additional policy. Manageable transition risk but escalating physical risk.

---

## CLOSED / NOT NEEDED

| Gap | Status | Rationale |
|-----|--------|-----------|
| Consumer driver expansion | CLOSED | Tested 3 variables, BIC prefers base. BofA accepted. |
| Diebold-Mariano tests | CLOSED | Implemented with HLN correction. |
| Q&A 2 preparation | CLOSED | Completed, satellite confirmed. |
| Sub-model / loan segmentation | NOT PURSUING | BofA said "not required," time better spent elsewhere. |
| Bank-specific analysis | NOT PURSUING | BofA: "Stay aggregate." |
| NGFS short-term scenarios | NOT NEEDED | Full horizon is fine. |
| M1: Satellite robustness testing | **CLOSED** | Full robustness analysis completed (session 6). Lag sensitivity, recursive OOS, residual diagnostics, coefficient stability, Mincer-Zarnowitz. |
| M2: Coefficient interpretation | **CLOSED** | Full coefficient tables with HAC SE, economic magnitudes. In robustness report. |
| D1: Variable mapping verification | **CLOSED** | FRED→NGFS mapping audit. One CPI approximation flagged. All others match. |
| M4: Mincer-Zarnowitz tests | **CLOSED** | C&I: marginal rejection (p=0.068), conservative forecasts. Consumer: cannot reject (p=0.54). |
| Consumer model post-GFC weakness | **CLOSED** | Rate levels specification fixes the problem. OOS from 2015Q1: +16% (DM p=0.031). See `artifacts/reports/2026-03-03-consumer-improvement-report.md`. |
| Delinquency rate alternative | **CLOSED (REJECTED)** | R²=0.97 is persistence inflation. OOS worse than AR by 52–141%. |

---

## Priority Matrix

### Must-Do Before Presentation (Modeling)
| # | Gap | Type | Effort | Status |
|---|-----|------|--------|--------|
| ~~M1~~ | ~~Satellite robustness testing~~ | ~~Modeling~~ | ~~Medium~~ | **DONE** (session 6) |
| ~~M2~~ | ~~Satellite coefficient interpretation~~ | ~~Modeling~~ | ~~Low~~ | **DONE** (session 6) |
| M3 | Model comparison framework | Modeling | Low-Medium | **OPEN** — unify into presentation figure |
| ~~D1~~ | ~~Variable mapping verification~~ | ~~Data~~ | ~~Low~~ | **DONE** (session 6) |
| N1 | Economic intuition for drivers | Narrative | Medium | **OPEN** — rate levels narrative drafted in report, needs presentation form |

### Should-Do If Time Permits
| # | Gap | Type | Effort | Status |
|---|-----|------|--------|--------|
| ~~M4~~ | ~~Mincer-Zarnowitz tests~~ | ~~Modeling~~ | ~~Low~~ | **DONE** (session 6) |
| M5 | Structural break tests | Modeling | Medium | OPEN |
| D2 | Transition vs physical risk explanation | Narrative | Low | OPEN |
| D3 | Historical fit visualization | Visualization | Low | OPEN |
| N2 | C&I vs consumer divergence narrative | Narrative | Low | PARTIALLY DONE — rate levels improvement clarifies the narrative |
| N3 | Scenario narratives | Narrative | Low | OPEN |
| G2 | Leading/lagging indicator audit | Documentation | Low | OPEN |

### Can Skip
| # | Gap | Type | Rationale |
|---|-----|------|-----------|
| M6 | MIDAS further work | Modeling | Doesn't beat AR. Brief mention in report is sufficient. |
| G5 | Dedicated IAM family comparison | Analysis | Already visible in fan charts. |
| G8-G9 | Short-term scenarios, revenue recycling | Data | Not needed per BofA. |

---

## Recommended Session Plan (Updated)

**Sessions 6-7 completed:** M1, M2, M4, D1 all done. Consumer model improved with rate levels. All modeling work is now locked down.

**Session 8 (next):** Focus on M3 + N1 + N2 + N3
- Build unified model comparison figure for presentation
- Write driver intuition narratives (both C&I and consumer rate levels channel)
- Draft C&I vs consumer divergence explanation
- Scenario narrative writing (Net Zero, Delayed, NDCs)

**Session 9:** Focus on presentation materials
- Presentation-quality fan charts
- COVID impact visualization
- NGFS scenario comparison section
- Slide content and talking points

---

*Generated from 613 facts, 15 sources, 6 notebooks, 43 figures, Q&A 1 + Q&A 2 feedback, and full project CLAUDE.md.*
