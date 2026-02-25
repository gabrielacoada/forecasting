# Comprehensive Analysis: ARDL-MIDAS Methodology for Climate Risk Loan Forecasting

**Date**: 2026-02-25
**Analysis run**: ardl-midas-deep-dive
**Questions addressed**: Q9, Q10, Q12
**Sources**: 4 fact files (160+ facts), notebook diagnostic observations, course materials (Weeks 5, 7)

---

## 1. Q9: The Formal ARDL-MIDAS Specification and Its Relationship to the ADL Framework

### 1.1 The Core MIDAS Regression

The MIDAS (Mixed Data Sampling) regression model, introduced by Ghysels, Santa-Clara, and Valkanov (2004), relates a low-frequency dependent variable to high-frequency regressors through a parametrically weighted distributed lag:

```
y_t = beta_0 + beta_1 * SUM_{k=1}^{K} w(k; theta) * x_{t-k/m} + epsilon_t
```

where:
- `y_t` is the low-frequency dependent variable (e.g., annual loan growth)
- `x_{t-k/m}` is the k-th high-frequency lag of the predictor (e.g., monthly unemployment)
- `m` is the frequency ratio (m=12 for annual-to-monthly)
- `K` is the maximum number of high-frequency lags
- `w(k; theta)` are normalized weights satisfying `SUM w(k; theta) = 1`
- `theta` is a low-dimensional parameter vector (typically 2 parameters)

[Source: Ghysels et al. (2004) Fact 2; Pesavento Week 7 slides, slide 6]

The model separates the effect of the high-frequency variable into two components: (1) `beta_1`, the total magnitude and direction, and (2) `theta`, the shape of the lag distribution. This separation is a key design feature. [Ghysels (2004) Fact 4]

### 1.2 The ADL-MIDAS Extension

The ADL-MIDAS (Autoregressive Distributed Lag MIDAS) specification adds lags of the low-frequency dependent variable:

```
y_t = beta_0 + rho * y_{t-1} + beta_1 * SUM_{k=1}^{K} w(k; theta) * x_{t-k/m} + epsilon_t
```

The `rho * y_{t-1}` term captures persistence in the low-frequency series at its own frequency, while the MIDAS polynomial exploits within-period high-frequency variation. Multiple AR lags can be included:

```
y_t = beta_0 + SUM_{j=1}^{p} rho_j * y_{t-j} + beta_1 * SUM_{k=1}^{K} w(k; theta) * x_{t-k/m} + epsilon_t
```

[Source: Ghysels (2004) Fact 17-18; Ghysels (2007) Fact 8-9]

Including the lagged dependent variable is strongly recommended -- Franses (2016) demonstrates through simulation that omitting it causes substantial bias in the coefficients of the explanatory variables, particularly when the true autoregressive parameter is large. [Franses (2016) Fact 17-18]

### 1.3 Connection to the Week 5 Distributed Lag Framework

The MIDAS framework is a direct descendant of the distributed lag model from Week 5:

```
Y_t = beta_0 + beta_1 * X_t + beta_2 * X_{t-1} + ... + beta_{r+1} * X_{t-r} + u_t
```

[Source: Course Materials Fact 27]

The key differences are:

1. **Frequency mismatch**: In the Week 5 DL model, Y and X are at the same frequency. MIDAS allows X to be at higher frequency than Y.

2. **Parametric parsimony**: The Week 5 DL model estimates one free coefficient per lag (K parameters total). MIDAS replaces these K coefficients with `beta_1 * w(k; theta)`, using only 2 parameters in theta regardless of K. For our annual-to-monthly case (K=12), this means 4 total parameters (beta_0, rho, beta_1, theta_1, theta_2 = 5 parameters) instead of 14+ parameters.

3. **Nesting**: When m=1 (same frequency), MIDAS reduces to a standard DL model with parsimoniously parameterized lag coefficients. [Ghysels (2004) Fact 15]

4. **Standard errors**: The Week 5 material emphasizes HAC (Newey-West) standard errors for distributed lag models because errors are serially correlated. [Course Materials Fact 31-32] This applies equally to MIDAS, though with the ADL specification and sufficient AR lags, serial correlation in residuals is typically reduced. [Course Materials Fact 33]

When MIDAS weights collapse to flat/uniform values, the model degenerates to `y_t = beta_0 + rho * y_{t-1} + beta_1 * x_bar_t + epsilon_t`, which is a standard ADL(1,0) on temporally aggregated data -- exactly the approach MIDAS was designed to improve upon. [Ghysels (2004) Fact 40]

### 1.4 Weight Function Specifications

**Exponential Almon** (most common):
```
w(k; theta_1, theta_2) = exp(theta_1*k + theta_2*k^2) / SUM_j exp(theta_1*j + theta_2*j^2)
```
- theta_1 < 0: declining weights (recent observations weighted more)
- theta_2 < 0: reinforces decline
- theta_1 = theta_2 = 0: flat/equal weights (degenerate case)
- Always positive due to exponential transformation
[Source: Ghysels (2007) Fact 2-4]

**Beta weighting**:
```
w(k; theta_1, theta_2) = (k/K)^{theta_1-1} * (1-k/K)^{theta_2-1} / SUM_j (j/K)^{theta_1-1} * (1-j/K)^{theta_2-1}
```
- Can produce monotonically decreasing, increasing, flat, hump-shaped, or U-shaped patterns
- Weights naturally bounded in [0,1]
- theta_1 = theta_2 = 1: flat/uniform weights (degenerate case)
- One-parameter restriction (theta_1 = 1, theta_2 = omega) gives monotonic decay -- recommended default
[Source: Ghysels (2004) Fact 9-11; Ghysels (2007) Fact 5-7]

**Step function** (polystep in midasr):
- Piecewise-constant weights: different weight for groups of lags
- Intermediate between fully restricted and unrestricted
- Useful as a diagnostic bridge
[Source: JSS (2016) Fact 8, 22]

### 1.5 U-MIDAS: The Unrestricted Alternative

U-MIDAS (Foroni, Marcellino, Schumacher, 2015) removes the parametric weight function entirely:
```
y_t = alpha + SUM_p rho_p * y_{t-p} + SUM_{k=0}^{K-1} beta_k * x_{t-k/m} + epsilon_t
```

Each lag gets a free coefficient estimated by OLS. Key findings:
- At m=3 (quarterly-to-monthly): U-MIDAS matches or beats parametric MIDAS
- At m=12 (annual-to-monthly): **ambiguous** -- neither clearly dominates
- At m=60+ (daily-to-quarterly): parametric MIDAS strongly preferred
[Source: Foroni (2015) Fact 1-5, 11; Ghysels (2004) Fact 16]

For our project (annual-to-monthly, m=12), we are in the ambiguous zone where empirical comparison is needed. With only 34 annual observations, the unrestricted model has 12 lag coefficients for each regressor, which is a substantial parameter burden (approximately 3:1 ratio of observations to parameters for a single-regressor model). This argues for at least some form of restriction, but the parametric form should be validated against U-MIDAS.

### 1.6 Franses's Complete Specification

Franses (2016) argues the correctly specified MIDAS model should include three components:
1. Lagged dependent variable (AR term) -- omitting it causes substantial bias
2. High-frequency explanatory variables with lags
3. Moving average (MA) term -- omitting is less harmful but still recommended

[Source: Franses (2016) Fact 16, 26]

The current notebook includes components 1 and 2 but not component 3. This is a gap, though Franses notes the MA term's omission is less harmful than omitting the AR term. [Franses (2016) Fact 20]

### 1.7 Estimation

MIDAS is estimated by Nonlinear Least Squares (NLS) because theta enters the weight function nonlinearly:
```
min_{beta_0, rho, beta_1, theta} SUM_t [y_t - beta_0 - rho*y_{t-1} - beta_1*SUM_k w(k;theta)*x_{t-k/m}]^2
```

The five-step procedure from Professor Pesavento (Week 7):
1. Choose weighting scheme
2. Choose maximum lag K
3. Set starting values (critical!)
4. Optimize via NLS
5. Compute HAC standard errors

[Source: Ghysels (2004) Fact 20-21]

Gradient-based methods (Newton-Raphson, BFGS) are preferred over derivative-free methods. Conditional on theta, the remaining parameters (beta_0, rho, beta_1) are linear, enabling the profiling approach. [Ghysels (2007) Fact 16; Ghysels & Qian (2019)]

---

## 2. Q10: Why MIDAS Weight Functions Collapse and How to Fix Them

### 2.1 Diagnosing the Current Notebook: What Went Wrong

The current `scenario_forecasting_midas.ipynb` exhibits severe weight function degeneracy. All four estimated weight functions (2 loan types x 2 regressors) collapse to point masses, with theta values in the hundreds:

| Model | Regressor | theta_1 | theta_2 | Behavior |
|-------|-----------|---------|---------|----------|
| C&I | UNRATE_chg | -870 | (extreme) | All weight on single month |
| C&I | CPI_pchg | +815 | (extreme) | All weight on single month |
| Consumer | UNRATE_chg | (extreme) | (extreme) | All weight on single month |
| Consumer | CPI_pchg | (extreme) | (extreme) | All weight on single month |

Additional diagnostic red flags:
- Consumer model: gamma = -0.179 (negative persistence, economically questionable for a highly persistent series like consumer loan growth)
- Consumer R-squared = 0.192 (only 19% variance explained)
- No standard errors computed
- No convergence diagnostics
- Warnings globally suppressed

### 2.2 Root Cause Analysis: Why the Weights Collapsed

The degeneracy has multiple compounding causes. Each alone might cause problems; together they virtually guarantee failure.

**Cause 1: Nelder-Mead optimizer without bounds or gradients**

The notebook uses `scipy.optimize.minimize(method='Nelder-Mead')` with no bounds constraints. Nelder-Mead is a derivative-free simplex algorithm that:
- Cannot use gradient information (ignoring the known analytical gradient of the Almon polynomial)
- Has no mechanism to prevent theta from drifting to extreme values
- Is not recommended for MIDAS by any reference source

The MIDAS literature consistently recommends gradient-based methods (BFGS, Newton-Raphson) or the Ghysels-Qian profiling approach. [Ghysels (2004) Fact 22; Ghysels (2007) Fact 15-17; JSS (2016) Fact 12]

Evidence: EViews uses gradient-based NLS; the midasr R package default is `optim(method="BFGS")`; Ghysels and Qian propose grid search + OLS profiling specifically to avoid the pathologies of unconstrained NLS. The choice of Nelder-Mead is a primary cause of the extreme theta values.

**Cause 2: No starting value strategy**

Proper starting values are described as "critical" by every source. The standard approach is:
- Initialize theta at (0, 0) for flat weights as baseline
- Or grid search over theta with OLS for linear parameters at each grid point
- Or use shape-restricted models first to get initial theta estimates

[Source: Ghysels (2004) Fact 21-23; Ghysels (2007) Fact 17; JSS (2016) Fact 13]

The notebook appears to use arbitrary or default starting values without a systematic strategy. With a non-convex objective function and no gradient guidance, poor starting values lead Nelder-Mead straight to local minima.

**Cause 3: Severe parameter-to-observation ratio**

The notebook estimates approximately 8 parameters (beta_0, rho, beta_1_UNRATE, theta_1_UNRATE, theta_2_UNRATE, beta_1_CPI, theta_1_CPI, theta_2_CPI) from ~32 effective observations after losing data to lags and the train/test split. This gives a 4:1 ratio of observations to parameters.

For context: Ghysels et al. (2007) report well-behaved finite-sample properties at T >= 100 low-frequency observations. [Ghysels (2007) Fact 23] Franses (2016) shows unrestricted OLS works at T=50, but that is with a simpler specification and quarterly-to-monthly (m=3) frequency. [Franses (2016) Fact 23]

With only 32 observations, the NLS objective surface is likely very flat in the theta dimensions, meaning the data simply cannot distinguish between different weight shapes. The optimizer responds by finding extreme solutions that overfit to noise.

**Cause 4: Multiple MIDAS polynomials competing**

Estimating separate weight functions for two regressors simultaneously (UNRATE_chg and CPI_pchg) doubles the nonlinear parameters (4 theta parameters instead of 2). With 32 observations, this creates severe collinearity in the nonlinear parameter space. The optimizer can achieve similar fit by shifting weight between the two regressors' timing, leading to compensating extreme solutions.

**Cause 5: CPI transformation bug**

The notebook divides the CPI level by 12 instead of computing proper month-over-month or year-over-year percent changes. This produces a variable that is essentially a rescaled price level, not an inflation measure. A rescaled level has different time series properties (unit root, different persistence structure) than an inflation rate, confounding the estimation.

**Cause 6: NGFS interpolation creates flat within-year profiles**

The NGFS scenarios provide annual data that is interpolated to monthly frequency. If the interpolation method produces flat within-year values (e.g., step interpolation or linear interpolation that is constant within each year), then there is no within-year variation for the MIDAS weights to exploit. The weight function becomes unidentified because `SUM w(k;theta) * x_{t-k/m}` produces the same value for any theta when x is constant within the year. This is a fundamental identification problem: MIDAS requires within-period variation in the high-frequency variable to identify the lag structure.

[Related: Ghysels (2004) Fact 25 -- theta is unidentified when beta_1 = 0; analogously, theta is unidentified when x has no within-period variation]

**Cause 7: Missing Beta weighting as robustness check**

The notebook uses only exponential Almon weights. Best practice is to estimate with multiple weight functions and compare. [Ghysels (2004) Fact 37; Ghysels (2007) Fact 32] The Beta weight function is inherently bounded and less prone to explosive parameters. [Ghysels (2004) Fact 10; Ghysels (2007) Fact 6]

### 2.3 Theoretical Framework for Degeneracy

Weight function degeneracy arises from the intersection of several theoretical issues:

1. **The Davies problem**: When beta_1 = 0 (no predictive power), theta is unidentified. Near-zero beta_1 creates a flat objective surface in the theta dimension. [Ghysels (2004) Fact 26]

2. **Boundary solutions**: For exponential Almon, the flat-weight solution (theta = 0) is at the interior of the parameter space, creating a ridge or plateau in the objective function around it. Standard NLS theory requires interior solutions; boundary solutions violate regularity conditions. [Ghysels (2007) Fact 12]

3. **Beta explosive behavior**: For Beta weights, parameters approaching 0 or negative values produce infinite weights at the boundaries (j=0 or j=K), causing numerical overflow. [JSS (2016) Fact 20; Ghysels (2007) Fact 31]

4. **Small-sample amplification**: All of the above problems are amplified in small samples because (a) the objective function surface is noisier, (b) there is less information to distinguish weight shapes, and (c) the asymptotic theory that justifies NLS inference breaks down. [JSS (2016) Fact 23; Franses (2016) Fact 28]

### 2.4 Concrete Fixes (Ordered by Priority)

**Fix 1 (Critical): Switch optimizer to L-BFGS-B with bounds**

Replace Nelder-Mead with `scipy.optimize.minimize(method='L-BFGS-B')` with bounds on theta:
```python
# For exponential Almon:
bounds_theta = [(-5, 0.1), (-0.5, 0.01)]  # theta_1, theta_2
# Enforce declining weights (theta_1 < 0) and non-humped shape (theta_2 <= 0)
```

L-BFGS-B supports bounds constraints, uses gradient information (provide analytical gradients or use finite differences), and is the closest scipy equivalent to the BFGS default used in midasr.

**Fix 2 (Critical): Implement grid search + OLS profiling (Ghysels-Qian approach)**

This is the most robust approach and completely avoids NLS pathologies:
```python
# Grid over theta
theta1_grid = np.linspace(-3, 0, 30)
theta2_grid = np.linspace(-0.5, 0, 20)
best_ssr = np.inf

for t1 in theta1_grid:
    for t2 in theta2_grid:
        weights = exp_almon_weights(t1, t2, K=12)
        # Construct weighted regressor: X_weighted = SUM w(k)*x_{t-k/m}
        X_weighted = compute_weighted_regressor(X_hf, weights)
        # OLS for linear parameters
        X_ols = np.column_stack([ones, y_lag, X_weighted])
        beta_hat = np.linalg.lstsq(X_ols, y, rcond=None)[0]
        ssr = np.sum((y - X_ols @ beta_hat)**2)
        if ssr < best_ssr:
            best_ssr = ssr
            best_theta = (t1, t2)
            best_beta = beta_hat
```

This guarantees finding the global optimum over the grid and is computationally trivial for 2D theta. [Ghysels & Qian (2019); JSS (2016) Fact 16-17]

**Fix 3 (Critical): Fix the CPI transformation**

Replace:
```python
CPI_pchg = CPI_level / 12  # WRONG: divides level by 12
```
With:
```python
CPI_pchg = CPI_level.pct_change(12) * 100  # Year-over-year percent change
# Or for monthly inflation:
CPI_pchg = CPI_level.pct_change(1) * 100 * 12  # Annualized month-over-month
```

**Fix 4 (High priority): Reduce model to single regressor per loan type**

With 32 observations, estimating two separate MIDAS polynomials is asking too much of the data. Options:
- Estimate separate single-regressor MIDAS models and compare
- Use the principal component of UNRATE_chg and CPI_pchg as a single composite regressor
- Use U-MIDAS for the second regressor (unrestricted lags) while applying MIDAS to the primary regressor

**Fix 5 (High priority): Add Beta weighting as robustness check**

Implement the one-parameter restricted Beta specification (theta_1 = 1, theta_2 = omega):
```python
def beta_weights_restricted(omega, K):
    k = np.arange(1, K+1) / K
    w = (1 - k)**(omega - 1)
    return w / w.sum()
```

This is the recommended default starting specification. [Ghysels (2007) Fact 7] With only one nonlinear parameter, the grid search becomes one-dimensional and trivially fast.

**Fix 6 (Important): Implement multi-start NLS**

If NLS is retained (in addition to profiling), use multiple starting values:
```python
starting_points = [
    (0, 0),       # flat weights baseline
    (-0.5, 0),    # moderate exponential decay
    (-1.0, -0.1), # fast decay with curvature
    (-0.1, -0.01),# slow decay
    (-2.0, 0),    # fast exponential decay
]
results = [minimize(objective, start, method='L-BFGS-B', bounds=bounds) for start in starting_points]
best = min(results, key=lambda r: r.fun)
```

**Fix 7 (Important): Add U-MIDAS comparison**

Estimate the unrestricted model by OLS as a diagnostic benchmark:
```python
# U-MIDAS: each monthly lag gets its own coefficient
X_umidas = np.column_stack([y_lag] + [x_lag_k for k in range(12)])
beta_umidas = np.linalg.lstsq(np.column_stack([ones, X_umidas]), y, rcond=None)[0]
```

Compare restricted MIDAS weights to unrestricted coefficients to diagnose whether the parametric form is appropriate. [JSS (2016) Fact 22]

**Fix 8 (Important): Compute HAC standard errors**

Professor Pesavento's five-step procedure explicitly includes HAC standard errors as Step 5. [Ghysels (2004) Fact 21] Currently the notebook computes no standard errors at all. Use:
```python
from statsmodels.stats.sandwich_covariance import cov_hac
# Or implement Newey-West with m = 0.75 * T^(1/3) truncation
```

[Source: Course Materials Fact 32]

**Fix 9 (Moderate): Implement convergence diagnostics**

After NLS estimation, check:
- Gradient norm near zero (necessary condition for minimum)
- Hessian positive definite (sufficient condition for local minimum)
- Compare SSR from multiple starting points

[Source: JSS (2016) Fact 14, 41]

**Fix 10 (Moderate): Investigate NGFS interpolation method**

If the NGFS scenario data is interpolated to monthly with flat within-year profiles, the MIDAS identification is fundamentally compromised. Options:
- Use monthly FRED data as high-frequency regressors (unemployment, CPI, interest rates) -- these have genuine within-year variation
- Treat NGFS as low-frequency exogenous scenario parameters, not as high-frequency regressors
- If NGFS must be monthly, use cubic spline interpolation to create smooth within-year variation (but acknowledge this is artificial)

The economically correct approach is: estimate the MIDAS model using historical FRED data (monthly) as high-frequency regressors, then for scenario forecasting, generate the monthly FRED paths implied by the NGFS scenarios and feed those through the estimated MIDAS model.

**Fix 11 (Moderate): Add Franses's MA term**

Include a lagged error or moving average component:
```python
# After initial estimation, compute residuals
residuals = y - y_fitted
# Re-estimate including lagged residual
X_augmented = np.column_stack([X_ols, residuals_lagged])
```

This is a quasi-MA approach that Franses shows reduces bias in the AR coefficient. [Franses (2016) Fact 16, 19]

### 2.5 What Can MIDAS Realistically Achieve with 34 Observations?

Honest assessment: **MIDAS will not perform miracles with this sample.** The literature suggests:

- Ghysels et al. (2007) find well-behaved properties at T >= 100. We have T = 34 (less than half the minimum).
- Franses (2016) shows unrestricted OLS works at T = 50, but with m = 3 (quarterly-to-monthly), not m = 12.
- The informational gain from MIDAS over simple aggregation depends on there being genuine within-year timing effects. For slow-moving macro variables like unemployment, the within-year variation may be modest, limiting the potential gain.

The realistic expectation is:
- MIDAS may provide modest improvement over temporal aggregation for variables with meaningful within-year dynamics (e.g., federal funds rate, which moves in discrete steps)
- For very persistent variables (unemployment), the MIDAS gain will be small because last year's value already captures most of the information
- The main value of MIDAS for this project is methodological: it demonstrates we are handling the frequency mismatch correctly and using course methods (Week 7 material)
- U-MIDAS with 12 monthly lags may actually perform comparably given the moderate frequency ratio

---

## 3. Q12: Best Practices for MIDAS Forecast Evaluation and Model Comparison

### 3.1 Out-of-Sample Evaluation Framework

Both Foroni et al. (2015) and Franses (2016) emphasize out-of-sample evaluation over in-sample fit. [Foroni (2015) Fact 15; Franses (2016) Fact 29] The midasr package implements three OOS schemes:

1. **Fixed**: Estimate once on training data, forecast all OOS periods without re-estimation
2. **Rolling window**: Re-estimate at each OOS origin using a fixed-width window
3. **Recursive (expanding)**: Re-estimate using all data up to each OOS origin

[Source: JSS (2016) Fact 32]

For our 34-observation sample with ~16 OOS periods, **recursive** is preferred because rolling windows would have very few training observations early in the OOS period. Fixed estimation is inappropriate given the long forecast horizon (out to 2050).

### 3.2 Primary Accuracy Metric: MSFE Ratio

The standard metric is the Mean Squared Forecast Error (MSFE) ratio relative to a benchmark:

```
MSFE_ratio = MSFE_MIDAS / MSFE_AR
```

Values < 1 indicate MIDAS outperforms the AR benchmark. [Ghysels (2007) Fact 20; Foroni (2015) Fact 15]

The AR benchmark is appropriate because:
- It uses only lagged values of the dependent variable
- Any MIDAS improvement over AR represents the value added by high-frequency information
- Comparison is straightforward since both produce low-frequency forecasts
[Source: JSS (2016) Fact 43]

### 3.3 Formal Statistical Tests

**Diebold-Mariano Test**: Tests H0: equal predictive accuracy between two models.
- Loss differential: d_t = e_{1,t}^2 - e_{2,t}^2
- Test statistic: DM = mean(d_t) / se(d_t)
- Asymptotically N(0,1) under the null
- **Critical caveat**: With ~16 OOS observations, the DM test has very low power. Use the Harvey, Leybourne, and Newbold (1997) small-sample correction.
[Source: Ghysels (2007) Fact 21; JSS (2016) Fact 35]

**Mincer-Zarnowitz Regression**: Tests forecast optimality (unbiasedness + efficiency):
```
actual_t = alpha + beta * forecast_t + error_t
```
Under H0 (optimal forecasts): alpha = 0 and beta = 1. Joint F-test with 2 d.f.
With 16 OOS points, power is limited but can detect gross departures.
[Source: JSS (2016) Fact 46]

**AGK Test** (Andreou, Ghysels, Kourtellos, 2010): Formal LM test of H0: theta = 0 (flat weights) vs. H1: non-trivial MIDAS weighting. This is the theoretically appropriate test for whether MIDAS weighting adds value over simple temporal aggregation. Implemented in midasr as `agk.test`. [Ghysels (2007) Fact 13]

**hAh Test** (Kvedaras and Zemlys, 2012): Tests whether the parametric weight function restriction is supported by the data. Compares restricted MIDAS to unrestricted U-MIDAS. Rejection means the parametric form is too restrictive. [JSS (2016) Fact 26-27]

### 3.4 Cross-Frequency Model Comparison

Comparing MIDAS (annual) vs. Quarterly VAR vs. Annual VAR requires aligning all forecasts to a common evaluation frequency. The natural approach:

1. All models produce annual-level forecasts (quarterly VAR forecasts are aggregated to annual)
2. Apply the same evaluation metric (MSFE) and the same evaluation sample
3. Use DM test on aligned forecast error series

[Source: JSS (2016) Fact 44]

The project currently has a three-model comparison:
- Annual AR baseline (MSFE denominator)
- Quarterly VAR (C&I: +11.7%, Consumer: +7.5% over AR)
- ADL-MIDAS (C&I: +1.7%, Consumer: +21.0% over AR)

The MIDAS consumer improvement (+21.0%) is notable but should be scrutinized given the degenerate weights. If the weights are concentrating on a single month that happens to correlate with the evaluation sample, this improvement may not generalize.

### 3.5 Information Criteria for Specification Selection

Within the MIDAS framework, use information criteria to select:
- Weight function family (exponential Almon vs. Beta vs. step function)
- Polynomial degree (Q = 1, 2, or 3 for Almon)
- Number of high-frequency lags K
- Number of AR lags p

[Source: JSS (2016) Fact 28-30; Ghysels (2007) Fact 22]

AIC and BIC treat theta parameters as regular parameters in the count. BIC tends to favor more parsimonious models, which may be appropriate given our small sample.

### 3.6 Forecast Combination

The literature supports BIC-weighted or MSFE-weighted forecast combination across MIDAS specifications:
- Equal weights (EW)
- BIC weights (BICW) -- models with lower BIC get higher weight
- MSFE weights -- based on OOS forecast errors from evaluation period
- Discounted MSFE (DMSFE) -- more weight on recent forecast performance

[Source: JSS (2016) Fact 33, 45]

For the BofA presentation, forecast combination across model types (VAR, MIDAS, AR) could hedge against model uncertainty and is directly aligned with BofA's request for uncertainty quantification. [Feb 20 Q&A F26-27]

### 3.7 Recommended Evaluation Protocol for This Project

Given our constraints (34 annual observations, 3 scenarios, ~16 OOS periods), the practical evaluation protocol is:

1. **Primary metric**: Recursive OOS MSFE ratio vs. AR benchmark, reported for each model
2. **Statistical test**: DM test with small-sample correction (HLN), acknowledging low power
3. **Diagnostic**: Mincer-Zarnowitz regression to check for systematic forecast bias
4. **Within-MIDAS**: Compare exponential Almon vs. Beta vs. U-MIDAS via AIC/BIC and OOS MSFE
5. **Weight validation**: hAh test of parametric restriction + visual comparison of restricted vs. unrestricted weights
6. **Cross-frequency**: Align annual, quarterly, and MIDAS forecasts and apply DM test
7. **Combination**: Report BIC-weighted average forecast across all models as a hedge

---

## 4. Concrete Recommendations for the Notebook

### 4.1 Priority 1: Must-Fix (before any results can be trusted)

| # | What | Why | Code Change |
|---|------|-----|-------------|
| 1 | Replace Nelder-Mead with L-BFGS-B + bounds | Primary cause of degenerate weights | `minimize(..., method='L-BFGS-B', bounds=[(-5,0.1),(-0.5,0.01)])` |
| 2 | Implement Ghysels-Qian grid search + OLS profiling | Most robust MIDAS estimation approach | 30x20 grid over theta, OLS for linear params at each point |
| 3 | Fix CPI transformation | Current formula (level/12) is economically wrong | `CPI_pchg = cpi.pct_change(12) * 100` |
| 4 | Reduce to single-regressor models initially | 8 params / 32 obs is over-parameterized | Estimate separate UNRATE-only and CPI-only models |
| 5 | Un-suppress warnings | Hiding convergence warnings masks problems | Remove `warnings.filterwarnings('ignore')` |

### 4.2 Priority 2: Should-Fix (for methodological rigor)

| # | What | Why | Code Change |
|---|------|-----|-------------|
| 6 | Add Beta weighting (one-parameter restricted) | Robustness check, less prone to explosive params | `w(k) = (1-k/K)^(omega-1) / sum(...)` |
| 7 | Add U-MIDAS comparison | Diagnostic for whether parametric weights are appropriate | OLS with 12 monthly lag dummies |
| 8 | Compute HAC standard errors | Required by Pesavento's five-step procedure (Step 5) | Newey-West with m = 0.75*T^(1/3) |
| 9 | Add multi-start NLS | Check for local minima | 5+ starting points, compare SSR |
| 10 | Add convergence diagnostics | Verify gradient ~0 and Hessian positive definite | Gradient norm + Hessian eigenvalues |

### 4.3 Priority 3: Should-Add (for evaluation completeness)

| # | What | Why | Code Change |
|---|------|-----|-------------|
| 11 | Diebold-Mariano test (HLN corrected) | Formal comparison vs. benchmarks | `dm_test(e_midas, e_ar, h=1)` |
| 12 | Mincer-Zarnowitz regression | Forecast unbiasedness check | OLS: actual ~ const + forecast |
| 13 | AGK test for flat weights | Test if MIDAS weighting adds value | `agk.test` equivalent in Python |
| 14 | hAh test for restriction validity | Test if Almon specification is appropriate | Compare restricted vs. unrestricted RSS |
| 15 | BIC/AIC table across specifications | Systematic model selection | Grid over {weight_fn, K, p} |
| 16 | Forecast combination | Hedge across models | BICW or MSFE-weighted average |

### 4.4 Priority 4: Nice-to-Have (presentation quality)

| # | What | Why |
|---|------|-----|
| 17 | Side-by-side weight function plot (restricted vs. unrestricted) | Visual diagnostic for BofA |
| 18 | Add MA term per Franses (2016) | Complete specification |
| 19 | Monte Carlo simulation at T=34 | Show expected performance limits |
| 20 | Step function weights as intermediate check | Diagnostic bridge between restricted and unrestricted |

---

## 5. Synthesis: What This Means for the Project

### 5.1 The Current MIDAS Results Are Not Reliable

The degenerate weight functions mean the current MIDAS notebook is not producing valid MIDAS estimates. The +21% consumer improvement is likely an artifact of overfitting -- a single month's value happening to correlate with the evaluation sample -- rather than genuine exploitation of within-year timing patterns. The negative consumer gamma (-0.179) is economically implausible for a series with known strong positive persistence.

### 5.2 The Fix Is Feasible

The recommended fixes are implementable in a single notebook revision session. The Ghysels-Qian profiling approach (Fix 2) is particularly straightforward -- it replaces the NLS optimizer with a simple nested loop and OLS, which is pedagogically clearer and numerically robust.

### 5.3 Realistic Expectations

With 34 annual observations and a 12:1 frequency ratio, MIDAS will provide:
- **Methodological value**: Demonstrates correct handling of the frequency mismatch using course material
- **Modest improvement**: Potentially a few percentage points improvement over temporal aggregation, primarily for variables with genuine within-year dynamics
- **Diagnostic insight**: The estimated weight functions (if properly estimated) reveal which months of macro data are most predictive of annual loan outcomes -- a genuinely interesting economic finding for the BofA presentation

### 5.4 The Quarterly VAR Remains the Primary Model

The quarterly VAR notebook has 142 observations (vs. 34 annual), well-identified dynamics, and clean OOS improvement (+11.7% C&I, +7.5% Consumer). It should remain the primary model for scenario forecasting. The MIDAS notebook serves as a complementary analysis that:
- Addresses the frequency mismatch explicitly
- Demonstrates a course method (Week 7)
- Provides a robustness check against the quarterly aggregation approach
- Potentially improves consumer forecasts if weights can be properly estimated

### 5.5 Alignment with BofA Expectations

BofA explicitly values:
- Multiple modeling approaches [Q&A F43: "They'll tell you very different stories"]
- Creativity in solving data problems [Q&A F13: "Be creative"]
- Uncertainty quantification [Q&A F26: "A lot of value from the confidence bands"]
- Justification of modeling choices [Q&A F5: "justify why you did that variable transformation"]

A properly estimated MIDAS model alongside the quarterly VAR and annual VAR creates a three-frequency comparison that directly demonstrates these qualities. Even if the MIDAS improvement is modest, the diagnostic analysis (why the weights collapsed, how we fixed it, what the weights tell us about monthly timing) is itself valuable presentation material.

---

## Appendix: Fact Attribution Index

| Section | Key Claims | Primary Sources |
|---------|-----------|----------------|
| 1.1 MIDAS specification | Ghysels (2004) Facts 1-4; Pesavento Week 7 slides | midas-touch-ghysels-2004.md |
| 1.2 ADL-MIDAS | Ghysels (2004) Facts 17-19; Ghysels (2007) Fact 8 | midas-touch-ghysels-2004.md, ghysels-sinko-valkanov-2007-midas.md |
| 1.3 Week 5 connection | Course Materials Facts 27, 31-33 | course-materials.md |
| 1.4 Weight functions | Ghysels (2007) Facts 2-7; Ghysels (2004) Facts 5-11 | ghysels-sinko-valkanov-2007-midas.md, midas-touch-ghysels-2004.md |
| 1.5 U-MIDAS | Foroni (2015) Facts 1-5, 11 | umidas-franses-midas-specification.md |
| 1.6 Franses spec | Franses (2016) Facts 16, 20, 26 | umidas-franses-midas-specification.md |
| 1.7 Estimation | Ghysels (2004) Facts 20-23; JSS (2016) Facts 12-17 | midas-touch-ghysels-2004.md, jss-midasr-ghysels-kvedaras-zemlys-2016.md |
| 2.2 Root causes | Ghysels (2004) Facts 22-28, 40; Ghysels (2007) Facts 12, 15, 31; Franses (2016) Facts 17, 28 | All four MIDAS fact files |
| 2.4 Fixes | Ghysels & Qian (2019) via JSS Facts 16-17; Ghysels (2007) Facts 7, 17 | jss-midasr-ghysels-kvedaras-zemlys-2016.md, ghysels-sinko-valkanov-2007-midas.md |
| 3.1-3.7 Evaluation | JSS (2016) Facts 32-36, 43-46; Ghysels (2007) Facts 20-22; Foroni (2015) Facts 15 | jss-midasr-ghysels-kvedaras-zemlys-2016.md, ghysels-sinko-valkanov-2007-midas.md, umidas-franses-midas-specification.md |
