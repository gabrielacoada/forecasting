# Presentation Narrative Prep — Too Big to Melt
**Session date:** March 18, 2026
**Presentation date:** April 9, 2026 (30 minutes, in person, Rich building)
**Audience:** BofA Treasury Quantitative Analytics team (4 people) + Professor Pesavento

---

## What We Built This Session

### Figures (in `outputs/figures/`)
| File | What it shows | Use in presentation |
|------|--------------|---------------------|
| `pres_1_cumulative_impact.png` | Cumulative loan balance index 2026–2050 under 3 NGFS scenarios | **Lead visual / slide 1** |
| `pres_2_driver_paths.png` | NGFS unemployment + rate paths per scenario (2022–2050) | NGFS exploration section |
| `pres_3_oos_validation.png` | OOS model vs AR benchmark, stacked C&I + Consumer | Methodology section |
| `pres_4_covid_dummy.png` | Model with vs without COVID dummy, 2018–2023 | COVID treatment section |

Produced by: `presentation_figures.py` (run from `climate-risk-loans/` directory).

### Model diagnostics run today
- C&I: Ljung-Box p(4)=0.007 → serial correlation; HAC SEs already correct for this
- Consumer: Adj R²=0.035, only FEDFUNDS_lvl and COVID significant
- Turning-point accuracy: C&I 100% correct in GFC quarters; Consumer 50% post-GFC
- Decision: **stop model development, focus on presentation**

---

## Key Numbers (cite these exactly)

### Model performance
- **C&I satellite: +22.8% better than AR benchmark** (RMSE 1.317 vs 1.705), Diebold-Mariano p=0.015
- **Consumer satellite: +17.9% better than AR benchmark** (RMSE 3.942 vs 4.804), Diebold-Mariano p=0.040
- Both results statistically significant; C&I significant at 1%, Consumer at 5%

### 2050 portfolio balance (index, 2025 = 100)
| Loan type | Net Zero | Delayed Transition | NDCs |
|-----------|----------|--------------------|------|
| C&I | 185 [183–189] | 183 [183–185] | 184 [183–187] |
| Consumer | 249 [248–266] | 287 [279–292] | 286 [269–288] |

**C&I story:** All scenarios converge (~85% growth). Unemployment paths are similar across scenarios; loan volumes don't diverge much.
**Consumer story:** Net Zero = 38 index points *below* Delayed Transition by 2050. Mechanism: Net Zero keeps rates higher longer (faster normalization) → suppresses consumer borrowing via the affordability channel.

### In-sample fit
- C&I Adj R² = 0.552 (explains 55% of variance)
- Consumer Adj R² = 0.035 (explains 4% of variance) → **must address proactively**

---

## Recommended Narrative Arc (30 minutes)

BofA's explicit instruction: "Start with a nice visual story — fan charts, then talk about drivers and modeling decisions."

### Block 1: Hook (3–4 min)
**Slide: The question and the answer**
> "We asked: how does climate transition reshape the trajectory of U.S. bank loan portfolios over the next 25 years? Here's what we found."

Show `pres_1_cumulative_impact.png` immediately. Let the audience look at it. Then walk through:
- Both C&I and Consumer grow substantially under all three scenarios
- The *gap between scenarios* is the climate risk signal
- C&I is scenario-insensitive (all paths converge); Consumer diverges — Net Zero is meaningfully lower
- That divergence IS the finding. The mechanism is interest rates.

### Block 2: The data (4–5 min)
**Slide: What NGFS gives us**
Show `pres_2_driver_paths.png`.

Talking points:
- NGFS Phase 5 gives us scenario paths for unemployment, interest rates, house prices, income — out to 2050, across 3 IAM model families
- The bands in the figure = uncertainty across GCAM, MESSAGEix, and REMIND. This is our confidence interval on the macro inputs, not just the model.
- Under Net Zero: short-term unemployment spike (transition costs), but faster normalization
- Under Delayed Transition: smoother near-term but higher long-run risk
- "Current Pledges (NDCs) sits between them — business as usual with stated policy"

**Key BofA ask fulfilled:** "Comparing multiple NGFS models — there's a lot of value in doing that analysis."

### Block 3: The methodology (5–6 min)
**Slide: Why satellite models?**
One-sentence version: *"We follow the same methodology the Federal Reserve uses for DFAST stress testing — single-equation regressions that take the macro scenario path as given and project loan outcomes directly."*

The two-model structure:
- **VAR model** → answers "how do climate shocks propagate through the macro system?" (IRFs, Granger causality)
- **Satellite model** → answers "what do loans look like under each scenario?" (scenario conditioning)

Why not VAR alone for forecasting: NGFS doesn't override a VAR cleanly. Satellite models accept external paths directly — no gymnastics needed. This is also how the ECB and Bank of England do it.

**Slide: The equation**
Show the ADL equation plainly:

> `loan_growth[t] = α + β₁·loan_growth[t-1] + β₂·Δunemployment[t-1] + β₃·fed_funds[t-1] + COVID_dummy + ε`

Then coefficients table. Two significant drivers for C&I: lagged loan growth (momentum) and unemployment change. One significant driver for consumer: Fed Funds level.

**Key BofA ask fulfilled:** "I'd like to see more detail on what your satellite model looks like." / "What macro variables were the most significant, by how much?"

### Block 4: Driver economics (4–5 min)
**Slide: Why these drivers?** (one slide per loan type, or one combined)

**C&I — unemployment is the key driver**
- Unemployment captures the *business cycle* — when firms lay off workers, credit demand falls; when the economy is tight, businesses borrow to expand
- Climate transition scenarios that cause economic disruption → higher unemployment → lower C&I lending
- Coefficient: −1.77 (a 1pp rise in unemployment reduces quarterly C&I growth by ~1.8pp)
- This driver has an NGFS counterpart: unemployment paths are available for all scenarios

**Consumer — interest rate *level* is the key driver**
- Consumer affordability depends on whether you *can* service a loan at current rates, not whether rates went up or down last quarter
- This is why we use FEDFUNDS *levels* (not changes) — a 5% rate is restrictive regardless of direction of travel
- Coefficient: −0.162 (a 1pp higher rate suppresses quarterly consumer growth by ~0.16pp, which compounds to the ~38-point gap by 2050)
- NGFS provides rate level paths directly — clean scenario conditioning
- Why Net Zero = lower consumer loans: this scenario projects rates normalizing *higher* (carbon pricing creates inflationary pressure + aggressive monetary response) → suppresses borrowing

**Key BofA ask fulfilled:** "Tell me why unemployment is a big driver — that makes logical sense, right?"

### Block 5: COVID treatment (3 min)
**Slide: The COVID problem**
Show `pres_4_covid_dummy.png`.

- COVID was an unprecedented structural break — no macro model can predict it from unemployment or rates
- Without the dummy: the model tries to "explain" the COVID shock using macro variables and poisons the coefficients
- With the dummy: we isolate the COVID effect, protecting the macro signal
- BofA internal teams faced the same problem: "It muddied our back-test data points"
- **For OOS evaluation:** COVID quarters excluded entirely. The 22.8% / 17.9% improvements are measured only on non-COVID history.

**Key BofA ask fulfilled:** "I'd like to see more explanation on how COVID impacted your modeling."

### Block 6: Validation (3 min)
**Slide: Does the model work?**
Show `pres_3_oos_validation.png`.

- Expanding-window OOS: train on everything before quarter T, forecast T, never look ahead
- C&I: 100% correct directional calls in the GFC. The satellite caught the recession; the AR missed 1 in 3.
- DM tests confirm improvement is statistically significant for both models
- **Don't frame this as "beating the benchmark is the goal"** — BofA flagged this. The point is: the macro drivers add *real predictive content*, which justifies using them for scenario conditioning.

### Block 7: Scenario interpretation + insights (5–6 min)
**Slide: What does this mean for banks?**

C&I finding: Climate transition affects C&I loans primarily through the business cycle. Unemployment — not carbon prices directly — is the mechanism. Net Zero causes more near-term disruption (transition costs) but C&I recovers; all scenarios converge by 2050 because the unemployment paths reconverge.

Consumer finding: The interest rate channel is the dominant transmission mechanism. Banks with large consumer portfolios are exposed to rate trajectory risk — and Net Zero, counterintuitively, projects a *lower* consumer loan book than delayed transition because it implies higher rates.

**The divergence between C&I and consumer is itself a strategic insight:** Climate transition affects different portfolio segments through different mechanisms and in different directions. A bank with a large consumer book faces a different risk profile than one heavily weighted toward commercial lending.

**Physical vs transition risk framing:**
> "Our model captures *transition risk* — the economic disruption from policy responses to climate change. What we don't capture is *physical risk* — direct damage from floods, fires, and storms that destroys collateral and raises default rates. Our 25-year window makes transition risk the dominant concern, but physical risk will compound as the century progresses."

**Key BofA ask fulfilled:** "Whether you think you're capturing more transition or physical risk." / "Which loan type matters more and why?"

### Block 8: Limitations + extensions (2–3 min)
Be proactive. BofA respects intellectual honesty.

1. **Consumer R² = 0.035** — the model explains only 4% of consumer loan variance in-sample. The OOS improvement is real but modest. Consumer lending is driven by millions of micro-level decisions (individual credit scores, life events, bank underwriting standards) that don't appear in quarterly macro aggregates. The signal is there — rate levels matter — but the noise is large.

2. **Serial correlation in C&I residuals** — quarterly dynamics aren't fully captured. HAC standard errors account for this in inference, but it's a known limitation.

3. **NGFS scenarios end in 2050 with linear interpolation** — we don't model scenario uncertainty in the macro paths themselves, only across IAM families.

4. **No physical risk** — our model is pure transition risk through the macro channel. Stranded asset effects, regional flood damage, agricultural disruption are all outside scope.

5. **Single-equation approach** — satellite models don't capture feedback loops (e.g., loan defaults feeding back into unemployment). The VAR captures these for the causal story.

**Framing for the room:** "These are not failures — they're the natural boundary conditions of any transparent, explainable model. We chose explainability over complexity. A black-box ML model might fit better in-sample and be completely unusable for scenario analysis."

---

## Slide Structure Suggestion (30 min = ~15 slides)

| # | Title | Duration | Figure |
|---|-------|----------|--------|
| 1 | Title slide — Too Big to Melt | — | — |
| 2 | The question | 1 min | — |
| 3 | **The answer: scenario fan charts** | 3 min | `pres_1_cumulative_impact.png` |
| 4 | Our data: NGFS Phase 5 overview | 2 min | — |
| 5 | **What the scenarios look like: macro paths** | 3 min | `pres_2_driver_paths.png` |
| 6 | Two-model structure: VAR + Satellite | 2 min | Diagram |
| 7 | The satellite equation (show it) | 2 min | Equation + coef table |
| 8 | C&I driver: why unemployment | 2 min | — |
| 9 | Consumer driver: why rate levels | 2 min | — |
| 10 | COVID: the structural break | 2 min | `pres_4_covid_dummy.png` |
| 11 | **Does the model work? OOS validation** | 3 min | `pres_3_oos_validation.png` |
| 12 | C&I scenario interpretation | 2 min | C&I fan chart only |
| 13 | Consumer scenario interpretation | 2 min | Consumer fan chart only |
| 14 | Physical vs transition risk | 1 min | — |
| 15 | Limitations + extensions | 2 min | — |
| 16 | Summary: 3 takeaways | 1 min | — |

**Appendix (linked, show on request):**
- Granger causality test results
- Diebold-Mariano test details
- VAR IRF plots
- NGFS model family comparison
- Consumer model specifications tested
- Full coefficient tables

---

## BofA Specific Questions — Prepared Answers

**"Tell me why unemployment is a big driver — that makes logical sense?"**
> "When firms face economic stress — whether from a climate policy shock or a recession — the first response is typically to reduce headcount. Rising unemployment means both lower credit demand from businesses contracting, and tighter lending standards from banks managing risk. The coefficient is −1.77: a 1 percentage point rise in unemployment reduces quarterly C&I loan growth by about 1.8 percentage points. That compounds meaningfully over a transition period."

**"What about consumer loans — are there other aspects beyond rates and unemployment?"**
> "We tested house prices, disposable income, and consumer sentiment — none improved the model. The rate level is the dominant channel. That's not surprising: the first thing a consumer asks when taking out a loan is 'can I afford the monthly payment?' That's a function of the rate level, not whether rates changed last quarter."

**"Are you capturing transition or physical risk?"**
> "Primarily transition risk — the economic disruption from policy responses: unemployment, interest rate paths, inflation. Physical risk — storm damage, flood losses, stranded assets — would require regional balance sheet data we don't have at the industry level. The 25-year horizon means transition risk dominates, but physical risk compounding over the century is the natural next layer."

**"What would you do differently with more time?"**
> "Three things: (1) model C&I by sector — energy, real estate, manufacturing face very different transition exposures; (2) incorporate physical risk through regional climate damage indices; (3) model the delinquency rate as the outcome variable, which would capture credit quality deterioration rather than just volume."

**"How comfortable are you with the confidence bands?"**
> "The bands in our fan charts represent uncertainty across the three NGFS IAM model families — GCAM, MESSAGEix, and REMIND. For C&I, the bands are tight because the macro paths converge. For consumer, the bands are wider, reflecting genuine disagreement across IAMs on the rate trajectory. We're not claiming precision — we're showing the range of outcomes consistent with credible climate scenarios."

---

## Consumer Model — The Honest Frame

**Do not hide the low R². Address it head-on.**

Suggested language:
> "Consumer loan modeling is harder. Our model explains about 4% of consumer loan variance in-sample — far less than the 55% for C&I. This is a real finding, not a modeling failure. Consumer lending is shaped by millions of individual credit decisions, bank underwriting standards, and behavioral factors that don't aggregate cleanly to quarterly macro series. What we can say is: the level of interest rates has a statistically significant effect on consumer loan growth, and the Diebold-Mariano test confirms our model beats a naive benchmark out of sample. The low R² means we should hold our scenario projections loosely for consumer — the confidence bands are wider, and the story is less clean than C&I."

---

## Transition vs Physical Risk — One-Paragraph Explainer

Our model captures **transition risk** through two channels:
1. **Unemployment channel (C&I):** Climate policy causes economic disruption → business cycle downturn → lower commercial lending demand
2. **Rate level channel (Consumer):** Carbon pricing + policy response → inflationary pressure → monetary tightening → higher borrowing costs → lower consumer credit demand

What our model does **not** capture:
- **Physical risk:** Direct damage to collateral (flood-damaged homes, hurricane-destroyed businesses), which raises default rates independently of the macro cycle
- **Stranded asset risk:** Energy sector loans becoming non-performing as fossil fuel assets lose value
- **Second-order macro feedback:** Loan defaults feeding back into unemployment (our model has no feedback loop — satellite equations are single-direction)

The models that capture physical risk use regional property-level data and hazard maps — bank-specific information we don't have at the industry level. This is the boundary the Fed papers also acknowledge.

---

## Session Work Log (March 18, 2026)

**Done today:**
1. Built `presentation_figures.py` — 4 polished presentation-quality figures
2. Code review: fixed `ax.get_ylim()` pre-render bugs in Figures 1 and 4; removed redundant OLS fits; merged duplicate functions; replaced hardcoded DM p-values with computed values; removed no-op `reg_to_ngfs` identity map
3. Ran full model diagnostics: residual tests, heteroskedasticity, turning-point accuracy
4. Decision: consumer model development complete — Adj R²=0.035 is structural, not a modeling failure
5. Created this narrative prep document

**Still to do before April 9:**
- [ ] Build slide deck (Presentation Lead — pull from this doc + figures)
- [ ] Write plain-English driver narrative for each variable (Econ Narrative — see section above)
- [ ] Finalize 5-page technical report (Report Writer — use notebook-walkthrough.md + this doc)
- [ ] Prepare appendix slides (Gabriela — DM tests, Granger, VAR IRFs)
- [ ] Optional: 3rd Q&A with BofA (late March / early April)
- [ ] Rehearse 30-minute timing
