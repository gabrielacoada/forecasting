# Research Questions: How Do NGFS Climate Scenarios Impact Banking Loan Portfolios?

## Primary Question
**How can NGFS climate scenario data be used to forecast the impact of climate risk on aggregate commercial (BUSLOANS) and consumer (CONSUMER) loan portfolios in the U.S. banking industry?**

## Supporting Questions

### Q1: What are the NGFS climate scenarios and what variables do they contain?
- Type: factual
- Priority: high
- Likely sources: web (NGFS portal documentation), course materials
- Status: answered
- Answered by: web-ngfs-and-transmission, case-study-pdf, feb20-qa-session
- Summary: NGFS provides multiple scenario families (Net Zero 2050, Delayed Transition, Current Policies, Hot House World, etc.) across model families (GCAM, REMIND, MESSAGEix). Variables include carbon prices, GDP, temperature, CO2 emissions, energy costs. Different models may have different frequencies. BofA says use "any or all" scenarios and visualize how they differ in both climate and economic variables.

### Q2: What is the theoretical transmission mechanism from climate risk to bank loan portfolios?
- Type: analytical
- Priority: high
- Likely sources: academic papers (Acharya et al. 2023, Jung et al. 2024), web
- Status: answered
- Answered by: academic-papers, sr1058-jung-bank-climate-exposure, sr1059-acharya-climate-stress-testing, feb20-qa-session
- Summary: Two channels — physical risk (storms, property damage → direct asset impairment) and transition risk (carbon taxes, policy → macro variables → credit quality). For C&I loans: climate → GDP, yields, corporate activity → loan volumes. For consumer loans: climate → unemployment, interest rates, house prices, disposable income, consumer confidence → repayment capacity → loan portfolios. BofA approved the indirect macro channel approach for consumer loans but pushed for thoroughness on consumer drivers beyond just unemployment and rates.

### Q3: What macroeconomic variables mediate the climate-to-loans relationship?
- Type: analytical
- Priority: high
- Likely sources: academic papers, FRED documentation, course materials
- Status: answered
- Answered by: web-fred-data, feb20-qa-session, kickoff-transcript
- Summary: **C&I loans:** GDP, S&P 500/equity indices, corporate yields, interest rates (Fed Funds, 10Y Treasury). **Consumer loans:** Unemployment rate, interest rates, plus BofA pushed for house prices, disposable income, consumer confidence, and other consumer-specific drivers. Some series may not go back as far as others — trade-off to discuss. BofA warned about leading vs. lagging indicators: GDP is lagged (covers prior quarter), and accidentally including future data points is a real risk they've seen in practice.

### Q4: What are the key data characteristics and challenges for modeling this relationship?
- Type: methodological
- Priority: high
- Likely sources: FRED data exploration, NGFS data exploration, course materials
- Status: answered
- Answered by: feb20-qa-session, web-fred-data, case-study-pdf
- Summary: (1) **Frequency mismatch:** NGFS is annual, FRED loans monthly/quarterly — open modeling choice, try multiple, pick what works. Professor will teach MIDAS. (2) **Training window:** At least 3 decades (1990s+) to capture GFC, 2001, 1990s cycles, but more data ≠ better — relevant business cycles matter. (3) **COVID:** Use dummy variables (BofA-confirmed standard), exclude from OOS evaluation. (4) **Leading/lagging:** Must track when each variable was realized vs. published. (5) **Granularity:** Stay aggregate US — going regional/sectoral creates driver-matching problems. (6) **Variable availability:** Some series don't go back as far, creating trade-offs.

### Q5: What forecasting frameworks are appropriate for climate stress testing of loan portfolios?
- Type: methodological
- Priority: high
- Likely sources: course materials (AR, ARMA, ARIMA, VAR), academic papers, web
- Status: partially answered
- Answered by: course-materials, web-stress-testing-methods, feb20-qa-session
- Summary: Must be transparent and explainable (no black-box ML). Course methods: AR, ARMA, VAR. BofA is open-ended on methodology — they care about justification, not specific technique. Professor will teach MIDAS for mixed-frequency. BofA wants confidence bands, sensitivity analysis across approaches, and scenario comparison. **Still open:** Specific model specification (e.g., VAR lag order, which variables in which equations) pending empirical work in Phase 2.

### Q6: How have regulators and central banks approached climate stress testing?
- Type: factual
- Priority: medium
- Likely sources: web (ECB, Fed publications), academic papers
- Status: answered
- Answered by: web-stress-testing-methods, sr1058-jung-bank-climate-exposure, sr1059-acharya-climate-stress-testing
- Summary: ECB conducted climate stress tests; Fed ran a 2023 pilot exercise (later rescinded in 2025). Acharya et al. (2023) provide a comprehensive climate stress testing framework. Jung et al. (2024) estimated U.S. bank exposures, finding max ~14% even in worst scenarios — BofA says use this as "interesting context" and "guideline" only, not a target. Those papers used bank-specific balance sheet data and regional segmentation we don't have.

### Q7: How do loan portfolio outcomes differ across NGFS scenarios?
- Type: comparative
- Priority: medium
- Likely sources: analysis of model outputs, academic papers
- Status: partially answered
- Answered by: feb20-qa-session, web-ngfs-and-transmission
- Summary: BofA wants all scenarios explored ("any or all") and robust visualization of how they differ in both climate and economic variables. "Really try to show that you thought about what these variables mean, the story they're telling you." Different modeling approaches will yield different stories — use that. **Still open:** Actual empirical comparison pending model estimation in Phase 2.

### Q8: What are the implications for financial stability and risk management?
- Type: analytical
- Priority: medium
- Likely sources: synthesis of findings, academic papers, regulatory publications
- Status: partially answered
- Answered by: feb20-qa-session, academic-papers
- Summary: BofA wants actionable insights beyond point estimates. "Can you dig into that number? Answer some important policy questions or systemic risk questions?" Frame for executive decision-making: "If you're going to present this to an executive making strategic decisions about increasing loan exposures, you want to be able to derive granular suggestions." Confidence bands are explicitly valued. **Still open:** Specific insights pending model results.

---

## ARDL-MIDAS Deep Dive (added 2026-02-25)

### Q9: What is the formal ARDL-MIDAS specification and how does it extend standard ADL models?
- Type: methodological
- Priority: high
- Likely sources: Ghysels et al. (2004, 2007), Andreou et al. (2010), Week 7 lecture
- Status: answered
- Answered by: midas-touch-ghysels-2004, ghysels-sinko-valkanov-2007-midas, jss-midasr-ghysels-kvedaras-zemlys-2016, umidas-franses-midas-specification
- Summary: ADL-MIDAS: y_t = beta_0 + rho*y_{t-1} + beta_1 * SUM w(k;theta) * x_{t-k/m} + e_t. MIDAS replaces K free lag coefficients with 2 hyperparameters (Almon or Beta), making estimation feasible with small samples. Nests temporal aggregation (flat weights) as a special case. The ADL component (lagged y) enters at low frequency. Relationship to Week 5: MIDAS is a restricted distributed lag where the lag polynomial is parametrically constrained. Three main weighting schemes: exponential Almon (2 params), Beta (2 params), step function. U-MIDAS (unrestricted OLS) as alternative for small frequency gaps.

### Q10: Why do MIDAS weight functions collapse to degenerate solutions, and how can this be fixed?
- Type: diagnostic/methodological
- Priority: high
- Likely sources: MIDAS estimation literature, NLS convergence guidance, applied MIDAS papers
- Status: answered
- Answered by: midas-touch-ghysels-2004, ghysels-sinko-valkanov-2007-midas, jss-midasr-ghysels-kvedaras-zemlys-2016, umidas-franses-midas-specification, notebook diagnostics
- Summary: Seven compounding causes: (1) Nelder-Mead optimizer without bounds — should use BFGS or Ghysels-Qian grid+OLS profiling, (2) poor starting values, (3) 8 params from 32 obs (4:1 ratio), (4) CPI transformation bug (level/12 instead of differencing), (5) flat NGFS interpolation destroying within-year variation, (6) competing MIDAS polynomials for 2 regressors, (7) no robustness checks (Beta, U-MIDAS). Answer: primarily (a) and (b) — optimization failure + small sample + too many nonlinear params. Fix: grid search profiling, single-regressor models, fix CPI, add Beta/U-MIDAS comparison.

### Q12: What are best practices for MIDAS forecast evaluation and model comparison?
- Type: methodological
- Priority: medium
- Likely sources: Ghysels survey papers, forecast evaluation literature (Week 6), applied MIDAS studies
- Status: answered
- Answered by: ghysels-sinko-valkanov-2007-midas, jss-midasr-ghysels-kvedaras-zemlys-2016, umidas-franses-midas-specification
- Summary: Use recursive OOS with MSFE ratios relative to AR benchmark. Diebold-Mariano with Harvey-Leybourne-Newbold small-sample correction for pairwise tests (but low power with 16 eval periods). Mincer-Zarnowitz for optimality. AGK test (Andreou et al. 2010) for whether MIDAS weights add value over flat weights. Compare MIDAS vs. VAR at a common annual frequency. BIC-weighted forecast combination across model types. Current consumer MIDAS OOS result (+21%) should be re-evaluated after fixing degenerate weights. With 34 obs, improvements will be modest.
