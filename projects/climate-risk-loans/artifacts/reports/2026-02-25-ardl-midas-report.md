# ARDL-MIDAS Research Report: Diagnosis, Fixes, and Evaluation Framework

**Date**: 2026-02-25
**For**: Climate Risk Loan Forecasting Project Team ("Too Big to Melt")
**Context**: Research into why the ADL-MIDAS notebook's weight functions collapsed and how to fix them

---

## 1. Executive Summary

We investigated the ARDL-MIDAS methodology through 160+ extracted facts from five academic sources (Ghysels et al. 2004, 2007; Ghysels, Kvedaras & Zemlys 2016; Foroni et al. 2015; Franses 2016) and Professor Pesavento's Week 7 lecture, then diagnosed why the current MIDAS notebook produces degenerate weight functions.

**Key findings:**

- The current notebook's weight functions are collapsed (theta values of -870, +815) due to seven compounding errors, led by the use of Nelder-Mead optimization without bounds, no starting-value strategy, and a CPI transformation bug.
- The fix is straightforward: replace the optimizer with the Ghysels-Qian grid search + OLS profiling approach, fix the CPI variable, and reduce the model to single-regressor specifications.
- With only 34 annual observations, MIDAS will provide modest (not dramatic) improvements over temporal aggregation. The quarterly VAR (142 observations) remains the primary model.
- The corrected MIDAS analysis adds methodological value: it demonstrates proper handling of frequency mismatch, applies Week 7 course material, and can reveal which months of macro data matter most for loan outcomes.

---

## 2. The ARDL-MIDAS Framework

The ADL-MIDAS model combines autoregressive dynamics with mixed-frequency distributed lags:

```
y_t = beta_0 + rho * y_{t-1} + beta_1 * SUM_{k=1}^{12} w(k; theta) * x_{t-k/12} + epsilon_t
```

For our project, `y_t` is annual loan growth, `x` is monthly macro data (unemployment, CPI), and the MIDAS weights `w(k; theta)` determine how each of the 12 monthly observations within a year contributes to the annual outcome. The weights are controlled by just 2 parameters (theta_1, theta_2) in the exponential Almon specification, regardless of how many monthly lags are included.

This is a direct extension of the Week 5 distributed lag framework. The standard DL model from that lecture estimates one coefficient per lag -- for 12 monthly lags, that means 12 free parameters from 34 observations (infeasible). MIDAS replaces those 12 parameters with 2, making estimation feasible.

The framework nests temporal aggregation (simple averaging) as a special case: when theta_1 = theta_2 = 0, all months receive equal weight and the model reduces to a standard regression on the annual average of the monthly data. MIDAS lets the data decide whether some months matter more than others.

---

## 3. Diagnosis: Why Our Weights Collapsed

All four weight functions in the current notebook collapsed to point masses. The root causes, in order of severity:

**1. Wrong optimizer.** The notebook uses Nelder-Mead (derivative-free simplex) with no bounds. Every source in the literature recommends gradient-based methods (BFGS, Newton-Raphson) or grid search + OLS profiling. Nelder-Mead cannot prevent theta from drifting to extreme values (-870, +815) and ignores the known analytical gradient of the Almon polynomial.

**2. No starting-value strategy.** The NLS objective function is non-convex with multiple local minima. Without a systematic grid search or multiple starting points, the optimizer landed in degenerate solutions. Professor Pesavento's five-step procedure lists starting values as Step 3 -- they are not optional.

**3. Too many parameters for the data.** The notebook estimates ~8 parameters from ~32 effective observations (4:1 ratio). With two separate MIDAS polynomials (UNRATE + CPI), the nonlinear parameters compete, and the optimizer resolves the ambiguity by sending both to extreme values. Ghysels et al. (2007) find well-behaved estimation at T >= 100; we have T = 34.

**4. CPI transformation bug.** The CPI variable is computed as the level divided by 12, which produces a rescaled price level rather than an inflation rate. This confounds the estimation with a unit-root variable.

**5. Flat NGFS interpolation.** If the NGFS annual scenarios are interpolated to monthly with constant within-year values, the MIDAS weights become unidentified -- there is no within-year variation to exploit.

**6. No robustness checks.** Only exponential Almon weights were tried. The Beta specification and U-MIDAS (unrestricted OLS) were not used as checks. No convergence diagnostics were computed.

The negative consumer gamma (-0.179) and low R-squared (0.192) are symptoms, not causes. They result from the distorted parameter estimates.

---

## 4. Recommended Fixes (Prioritized)

### Tier 1: Must-Fix (required before results can be trusted)

1. **Implement Ghysels-Qian grid search + OLS profiling.** Search over a 30x20 grid of (theta_1, theta_2) values in [-3, 0] x [-0.5, 0], running OLS for the linear parameters at each grid point. Select the grid point with lowest sum of squared residuals. This is computationally trivial (600 OLS regressions) and guaranteed to find the global optimum over the grid.

2. **Fix CPI: use year-over-year percent change.** Replace `CPI_level / 12` with `CPI_level.pct_change(12) * 100`.

3. **Start with single-regressor models.** Estimate separate models: loan_growth ~ AR(1) + MIDAS(UNRATE) and loan_growth ~ AR(1) + MIDAS(CPI). This cuts nonlinear parameters in half (2 theta instead of 4) and lets each regressor's contribution be assessed independently.

4. **Un-suppress warnings.** Remove the global `warnings.filterwarnings('ignore')`.

### Tier 2: Should-Fix (methodological rigor)

5. **Add Beta weighting** with the one-parameter restricted specification (theta_1 = 1, theta_2 = omega). This has only one nonlinear parameter and is inherently bounded.

6. **Add U-MIDAS comparison** (unrestricted OLS with 12 monthly lag dummies). This provides a diagnostic check: if U-MIDAS and restricted MIDAS give very different weight patterns, the parametric restriction is suspect.

7. **Compute HAC standard errors** (Newey-West). This is Step 5 of Pesavento's procedure. Use truncation parameter m = 0.75 * T^(1/3).

8. **Run multi-start NLS** from 5+ starting points to verify the profiling solution.

### Tier 3: For Evaluation Completeness

9. **Diebold-Mariano test** with Harvey-Leybourne-Newbold small-sample correction for formal MIDAS vs. AR and MIDAS vs. VAR comparison.

10. **Mincer-Zarnowitz regression** to test forecast unbiasedness.

11. **AIC/BIC table** comparing: exponential Almon (2-param), Beta restricted (1-param), Beta unrestricted (2-param), U-MIDAS, and step function weights.

12. **Forecast combination** (BIC-weighted average) across all model types as a hedge against model uncertainty.

---

## 5. Forecast Evaluation: How to Compare MIDAS vs. VAR vs. AR

The evaluation protocol for the three-model comparison should follow these principles:

**Common evaluation frequency.** Align all forecasts to annual: the quarterly VAR forecasts are aggregated to annual before comparison. Apply the same MSFE metric and evaluation sample to all models.

**Recursive OOS evaluation.** Re-estimate each model as data arrives (expanding window). With 34 total observations and ~16 OOS periods, a fixed training window would be too short in the early OOS periods.

**MSFE ratio as primary metric.** Report each model's MSFE relative to the AR benchmark. Values below 1.0 indicate improvement.

Current results (to be updated after fixes):

| Model | C&I MSFE Ratio | Consumer MSFE Ratio |
|-------|----------------|---------------------|
| Annual VAR | 1.022 (worse) | 1.280 (worse) |
| Quarterly VAR | 0.886 (better) | 0.926 (better) |
| ADL-MIDAS (current, unreliable) | 0.983 (slightly better) | 0.790 (much better) |

The MIDAS consumer result (0.790) should be treated with skepticism until the degenerate weights are fixed. Post-fix, it may improve, stay the same, or deteriorate -- we do not know until we re-estimate.

**Formal tests to report:**
- Diebold-Mariano (HLN-corrected) for pairwise model comparisons
- Mincer-Zarnowitz for forecast optimality
- AGK test for whether MIDAS weighting adds value over flat weights

**Honest caveat for presentation:** With 16 OOS observations, the DM test has low power. We cannot claim statistically significant superiority unless the improvement is large. Reporting confidence intervals on the MSFE ratio is as important as the point estimate.

---

## 6. Implications for the BofA Presentation

### What the MIDAS Analysis Adds to Our Story

1. **Frequency mismatch narrative.** MIDAS directly addresses one of the project's core challenges: NGFS scenarios are annual, FRED data is monthly. We can explain that simple averaging loses information, and show what the estimated MIDAS weights reveal about which months matter.

2. **Three-frequency robustness.** Presenting results at annual (VAR), quarterly (VAR), and monthly (MIDAS) frequencies demonstrates methodological thoroughness. Even if the three approaches agree broadly, showing convergence across methods strengthens the conclusion.

3. **Diagnostic transparency.** BofA values transparent, defensible models. Showing that we initially got degenerate weights, diagnosed the problem, and fixed it demonstrates exactly the kind of critical thinking they described valuing. The collapsed-weights story is itself presentation material -- it shows we understand what can go wrong with nonlinear estimation.

4. **Within-year timing insights.** If the corrected MIDAS weights show that, say, Q4 unemployment changes are most predictive of next-year C&I loan growth, that is a genuinely interesting economic finding. It moves beyond "unemployment affects loans" to "the *timing* of unemployment changes within the year matters."

### What to Present

- The quarterly VAR remains the headline model (most observations, cleanest identification)
- MIDAS is the supporting act: same story, different angle, exploiting monthly data
- Show the before/after: degenerate weights vs. corrected weights
- Report three-frequency MSFE comparison table
- Include the honest caveat about 34-observation limitations

### What NOT to Present

- Do not present the current (uncorrected) MIDAS results as reliable
- Do not oversell MIDAS as dramatically better -- the improvement, if real, is likely modest
- Do not spend presentation time on NLS technical details -- focus on the economic insight (which months matter and why)

### Framing for Executives

The MIDAS framework answers a question a bank executive would naturally ask: "Does it matter *when* during the year macro conditions change, or just the annual average?" If MIDAS shows that late-year unemployment spikes are more predictive than mid-year ones, that has direct implications for monitoring and early-warning systems. This is the kind of "granular suggestion" BofA asked for in the Q&A session.

---

## Appendix: Key References

1. Ghysels, E., Santa-Clara, P., & Valkanov, R. (2004). "The MIDAS Touch: Mixed Data Sampling Regression Models." CIRANO Working Paper 2004s-20.
2. Ghysels, E., Sinko, A., & Valkanov, R. (2007). "MIDAS Regressions: Further Results and New Directions." *Econometric Reviews*, 26(1), 53-90.
3. Ghysels, E., Kvedaras, V., & Zemlys, V. (2016). "Mixed Frequency Data Sampling Regression Models: The R Package midasr." *Journal of Statistical Software*, 72(4), 1-35.
4. Foroni, C., Marcellino, M., & Schumacher, C. (2015). "Unrestricted Mixed Data Sampling (MIDAS)." *JRSS Series A*, 178(1), 57-82.
5. Franses, P.H. (2016). "Yet Another Look at MIDAS Regression." Econometric Institute Research Papers EI2016-32.
6. Ghysels, E. & Qian, H. (2019). "Estimating MIDAS Regressions via OLS with Polynomial Parameter Profiling." *Econometrics and Statistics*, 9, 1-16.
7. Andreou, E., Ghysels, E., & Kourtellos, A. (2010). "Regression Models with Mixed Sampling Frequencies." *Journal of Econometrics*, 158(2), 246-261.
8. Kvedaras, V. & Zemlys, V. (2012). "Testing the Functional Constraints on Parameters in Regressions with Variables of Different Frequency." *Economics Letters*, 116, 250-254.
