# Gap Analysis: Climate Risk Impact on Banking Loan Portfolios
Date: 2026-02-20
Factbase: ~444 facts from 10 sources (including 43 new facts from Feb 20 Q&A)

---

## Gaps Closed Since v2 Analysis (Feb 12)

The Feb 20 Q&A session with BofA resolved several open questions, closing or narrowing the following v2 gaps:

| v2 Gap | Status | Resolution |
|--------|--------|------------|
| COVID treatment approach | **Closed** | BofA confirmed dummy variables. Exclude COVID from OOS evaluation. (F1-F3) |
| Frequency choice | **Closed** | Open-ended — try multiple, pick best. Professor will teach MIDAS. (F11-F14) |
| Consumer loan approach | **Narrowed** | Indirect macro channel approved, but need MORE consumer drivers. (F15-F17) |
| Granularity level | **Closed** | Stay aggregate US. Sector exploration optional. (F20-F23) |
| Training window | **Closed** | At least 3 decades (1990s+), cover GFC, 2001, 1990s cycles. (F7-F10) |
| Scenarios & horizon | **Closed** | "Any or all" scenarios, any horizon. (F24-F25) |
| Fed paper benchmarks | **Closed** | Use as context only, not targets. (F18-F19) |

---

## Remaining Open Gaps

### ~~Gap 1: NGFS NiGEM Data~~ [CLOSED]
- **Status:** Data downloaded. `data/raw/ngfs-phase5-iam.xlsx` (61MB) and `data/raw/ngfs-phase5-nigem.xlsx` (26MB) are in place. NGFS exploration completed in `ngfs_exploration.ipynb` with 6 figures produced. Scenario-conditional forecasts generated in `scenario_forecasting.ipynb`.

### ~~Gap 2: BUSLOANS and CONSUMER~~ [CLOSED]
- **Status:** Both series downloaded to `data/raw/`. Empirical analysis completed in `empirical_analysis.ipynb` — includes unit root tests, ACF/PACF, AR baselines (BIC selection), cross-correlations, COVID zoom, rolling stats. 7 empirical figures produced. VAR models estimated and OOS evaluation completed in `scenario_forecasting.ipynb`.

### Gap 3: Consumer Loan Driver Set Is Incomplete [HIGH]
- **What's missing:** BofA explicitly pushed for more consumer drivers beyond unemployment and interest rates. "Are there other aspects of it that matter to consumers?" (F16-F17)
- **Why it matters:** BofA evaluation criteria include "thorough" feature selection with justification. Using only 2 drivers for consumer loans looks thin.
- **What we know:** Suggested additions: house prices, disposable income, consumer confidence. Available FRED series: CSUSHPINSA (Case-Shiller HPI), DSPIC96 (real disposable personal income), UMCSENT (Michigan consumer sentiment), TOTALSL (total consumer credit).
- **Recommended action:** Research and test 2-3 additional consumer drivers. Candidates: Case-Shiller HPI, Michigan consumer sentiment, real disposable income. Test significance in preliminary regressions.
- **Priority:** P1 — needed for model specification.

### Gap 4: Leading vs. Lagging Indicator Audit Not Done [HIGH]
- **What's missing:** BofA gave a critical warning about leading vs. lagging indicators (F34-F37). No systematic audit of the timing properties of each candidate variable has been done.
- **Why it matters:** "I've seen it in practice — your model ends up being so good, and you just don't realize that you ended up using tomorrow's data to predict today." Accidentally including future information would invalidate results.
- **What we know:** GDP is lagged (covers prior quarter). UNRATE is contemporaneous (same month). Interest rates are real-time. NGFS data is annual and forward-looking by nature.
- **Recommended action:** Create a table documenting for each candidate variable: (a) release lag, (b) reference period, (c) whether it's leading, coincident, or lagging. Align all variables to ensure no look-ahead bias.
- **Priority:** P1 — must be done before finalizing model specification.

### Gap 5: Confidence Interval Methodology Not Specified [HIGH]
- **What's missing:** BofA explicitly wants confidence bands (F26-F27). No methodology for producing forecast intervals under scenario conditioning has been specified.
- **Why it matters:** "A lot of times there's a lot of value from the confidence bands around the estimate." This is an explicit deliverable expectation.
- **What we know:** Week 6 course material covers forecast intervals: $\hat{y}_{T+h} \pm 1.96\sigma_h$. For scenario-conditional forecasts, uncertainty comes from: (a) parameter estimation uncertainty, (b) shock variance, (c) model uncertainty across IAM families. The three IAM families naturally provide a range.
- **Recommended action:** (1) Produce parametric forecast intervals from the estimated model. (2) Show cross-IAM-family ranges as a complementary uncertainty band. (3) Consider fan charts for visualization.
- **Priority:** P1 — needed for presentation.

### Gap 6: Scenario Visualization and Narrative Understanding [MEDIUM-HIGH]
- **What's missing:** BofA wants to see that we understand what each scenario's story is (F28-F30). No visualization of NGFS scenario paths (climate variables AND economic variables) has been produced.
- **Why it matters:** "Really try to show that you thought about what these variables mean, the story they're telling you." This is explicitly about demonstrating domain understanding, not just model outputs.
- **Recommended action:** Create a multi-panel figure showing key NGFS variables (carbon price, GDP, temperature, unemployment) across all scenarios. Annotate with narrative descriptions of what drives the divergences.
- **Priority:** P1 — this is a presentation deliverable.

### Gap 7: Within-Model-Family Scenario Comparison [MEDIUM]
- **What's missing:** The NGFS NiGEM outputs across GCAM, REMIND, MESSAGEix for the same scenario have not been compared for U.S.-specific macro variables.
- **Why it matters:** v2 analysis (Theme 3) showed that model choice matters as much as scenario choice — Jorgenson yields 0.5-3.5%, Goulder yields -1% to 1%, G-Cubed yields 2-6.4%. Showing cross-IAM variation demonstrates methodological awareness.
- **Recommended action:** After downloading NGFS data (Gap 1), compare at least 2 IAM families for Net Zero 2050 and Current Policies. Visualize the differences.
- **Priority:** P2 — nice to have but not blocking.

### Gap 8: Actionable Insights Framework Not Defined [MEDIUM]
- **What's missing:** BofA wants insights beyond point estimates: "Answer some important policy questions or systemic risk questions" (F31-F33). No framework for translating model outputs into strategic recommendations has been defined.
- **Why it matters:** This is what separates a technical exercise from a BofA-quality deliverable. "If you're going to present this to an executive making strategic decisions about increasing loan exposures, you want to be able to derive granular suggestions."
- **What we know from literature:** v2 analysis provides benchmarks (0.5-6.4% exposure, max 14%), the "act early" finding is universal, risk migration from signatory to non-signatory banks is documented.
- **Recommended action:** After model results are available, develop 3-5 strategic takeaways framed for an executive audience. Use scenario comparison to tell a story about the cost of delayed action.
- **Priority:** P2 — needed for presentation but depends on model results.

### Gap 9: Course Weeks 5-6 Not Yet Integrated Into Methodology [MEDIUM]
- **What's missing:** The course-materials fact file only covers Weeks 1-4. Weeks 5 (dynamic causal effects, HAC SEs, distributed lag models) and 6 (forecasting mechanics, forecast evaluation, Mincer-Zarnowitz, DM test) are directly relevant to the project but not yet in the factbase.
- **Why it matters:** Week 5's distributed lag model is the exact framework for Stage 1 estimation. Week 6's forecast evaluation methods (MZ regression, DM test, pseudo-OOS) should be applied to validate results.
- **Recommended action:** Extract relevant facts from Weeks 5-6 key-concepts.md into the course-materials factbase. Apply MZ regression and DM test to project OOS results.
- **Priority:** P2 — methodology enrichment.

### Gap 10: Short-Term NGFS Scenarios Availability [LOW]
- **What's missing:** Phase IV introduced quarterly macro-financial scenarios for 1-5 year horizons (stress-testing Fact 30). Whether these are available for download has not been confirmed.
- **Why it matters:** Would partially resolve the frequency mismatch and be more relevant for near-term forecasting.
- **Recommended action:** Check IIASA portal for short-term scenario availability during Gap 1 data download.
- **Priority:** P3 — investigate opportunistically.

### Gap 11: Revenue Recycling Assumptions in NGFS NiGEM [LOW]
- **What's missing:** Jung et al. show revenue recycling policy swings exposures by 2-3 percentage points (sr1058 Facts 20, 22). The NGFS NiGEM macro projections' embedded recycling assumptions are unknown.
- **Why it matters:** Could materially affect interpretation of scenario results.
- **Recommended action:** Check NGFS Phase IV documentation for revenue recycling assumptions. Note as a limitation if not specified.
- **Priority:** P3 — discuss as limitation if unclear.

---

## Recommended Research Extension Plan

### Immediate (This Week — Feb 20-23)
1. **Download NGFS data** from IIASA portal → closes Gap 1
2. **Download and analyze BUSLOANS + CONSUMER** from FRED → closes Gap 2
3. **Create leading/lagging indicator table** → closes Gap 4
4. **Research additional consumer drivers** (HPI, sentiment, income) → narrows Gap 3

### Phase 2 Modeling (Feb 24 - March)
5. **Estimate VAR/ADL models** with macro variables → addresses Gap 9
6. **Generate scenario-conditional forecasts** with confidence bands → addresses Gap 5
7. **Produce NGFS scenario visualization panel** → closes Gap 6
8. **Compare IAM families** for key scenarios → closes Gap 7

### Pre-Presentation (March - April)
9. **Apply forecast evaluation** (MZ regression, DM test, pseudo-OOS) → addresses Gap 9
10. **Develop actionable insights framework** → closes Gap 8

---

## Factbase Coverage Summary

| Question | Facts | Sources | Confidence | Gaps Remaining |
|----------|-------|---------|-----------|----------------|
| Q1: NGFS scenarios | 40+ | 4 | Strong | Gap 1 (need actual data) |
| Q2: Transmission mechanism | 30+ | 4 | Strong | None significant |
| Q3: Macro mediators | 25+ | 5 | Strong | Gap 3 (consumer drivers), Gap 4 (timing) |
| Q4: Data challenges | 40+ | 6 | Strong | Gap 2 (need to analyze series) |
| Q5: Frameworks | 30+ | 4 | Strong | Gap 5 (CI methodology), Gap 9 (Weeks 5-6) |
| Q6: Regulatory approaches | 25+ | 3 | Strong | None significant |
| Q7: Scenario outcomes | 30+ | 3 | Moderate | Gap 7 (IAM comparison), depends on modeling |
| Q8: Implications | 20+ | 4 | Moderate | Gap 8 (framework), depends on modeling |

**Bottom line:** The research foundation is solid (444 facts, all major questions answered). The remaining gaps are primarily **execution gaps** (download data, run models, produce outputs) rather than **knowledge gaps**. The project is ready to transition from research to modeling.
