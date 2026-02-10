# Week 5: Dynamic Causal Effects

## Main Topic
Estimating how the effect of a change in X on Y unfolds over time using distributed lag regressions, the assumptions required for causal interpretation (exogeneity), and why standard OLS standard errors are invalid with serially correlated errors — motivating Heteroskedasticity and Autocorrelation-Consistent (HAC) standard errors.

## Key Concepts

### 1. Dynamic Causal Effects
**Definition:** A dynamic causal effect is the effect on Y of a change in X measured over time — not just the immediate impact, but the response at 1, 2, ..., k periods into the future.

**Examples from class:**
- Effect of an increase in cigarette taxes on cigarette consumption this year, next year, in 5 years
- Effect of a change in the Fed Funds rate on inflation this month, in 6 months, and 1 year
- Effect of a freeze in Florida on the price of orange juice concentrate in 1 month, 2 months, 3 months

### 2. The Orange Juice Data (Running Example)
**Setup:** Monthly data, Jan. 1950 – Dec. 2000 ($T = 612$).
- **Price** = price of frozen OJ (sub-component of the PPI, Bureau of Labor Statistics)
- **%ChgP** = percentage change in price over a month: $\%ChgP_t = 100 \Delta \ln(\text{Price}_t)$
- **FDD** = freezing degree-days during the month, recorded in Orlando FL. Example: If November has 2 days with low temp below 32°, one at 30° and one at 25°, then $FDD_{\text{Nov}} = (32-30) + (32-25) = 2 + 7 = 9$

**Key observation:** Large month-to-month price changes coincide with freezing weather in Orlando.

### 3. Initial (Static) Regression
$$\widehat{\%ChgP}_t = -0.40 + 0.47 \cdot FDD_t$$
$\quad\quad\quad\quad\quad\quad\quad(0.22)\quad(0.13)$

- Statistically significant positive relationship: one additional freezing degree-day increases prices by 0.47%
- Standard errors are HAC (not the usual OLS SEs) — more on this below
- **Limitation:** This only captures the contemporaneous effect. What is the effect of FDD over time?

### 4. The Distributed Lag Model
**Definition:** A regression of $Y_t$ on current and lagged values of $X_t$:
$$Y_t = \beta_0 + \beta_1 X_t + \beta_2 X_{t-1} + \ldots + \beta_{r+1} X_{t-r} + u_t$$

**Coefficient interpretation:**
- $\beta_1$ = **impact effect** (effect of change in $X_t$ on $Y_t$, holding past $X$ constant)
- $\beta_2$ = **1-period dynamic multiplier** (effect of $X_{t-1}$ on $Y_t$, holding $X_t, X_{t-2}, \ldots$ constant)
- $\beta_3$ = **2-period dynamic multiplier** (effect of $X_{t-2}$ on $Y_t$, holding other $X$ values constant)
- **Cumulative dynamic multiplier:** Sum of coefficients up to a given lag. E.g., the 2-period cumulative dynamic multiplier = $\beta_1 + \beta_2 + \beta_3$

**OJ example with 6 lags:**
$$\widehat{\%ChgP}_t = -0.65 + 0.47 FDD_t + 0.14 FDD_{t-1} + 0.06 FDD_{t-2} + 0.07 FDD_{t-3} + 0.03 FDD_{t-4} + 0.05 FDD_{t-5} + 0.05 FDD_{t-6}$$

### 5. Ideal vs Feasible Experiments for Dynamic Causal Effects
**Ideal (cross-sectional):** Randomize treatment across subjects, measure outcomes over time (e.g., fertilizer on tomato yield across randomized plots).

**Time series problem:** We can't do this — there is only one US OJ market. We can't randomly assign FDD to different replicates.

**Alternative thought experiment:** Treat the same subject (OJ market) at different dates as different "subjects." If $Y_t, X_t$ are **stationary**, the dynamic causal effect can be estimated by OLS regression of $Y_t$ on $X_t$ and its lags. This is the **distributed lag estimator**.

### 6. Exogeneity in Time Series
**Exogeneity (past and present):** $X$ is exogenous if $E(u_t | X_t, X_{t-1}, X_{t-2}, \ldots) = 0$

**Strict exogeneity (past, present, and future):** $X$ is strictly exogenous if $E(u_t | \ldots, X_{t+1}, X_t, X_{t-1}, \ldots) = 0$

- Strict exogeneity implies exogeneity (but not vice versa)
- If $X$ is exogenous, OLS estimates the dynamic causal effect
- Exogeneity is often not plausible in time series due to **simultaneous causality**
- Strict exogeneity is rarely plausible due to **feedback**

**Exogeneity examples discussed in class:**
1. $Y$ = OJ prices, $X$ = FDD in Orlando — plausibly exogenous (traders can't change weather)
2. $Y$ = Australian exports, $X$ = US GDP — Australia is small relative to US, so plausibly exogenous
3. $Y$ = EU exports, $X$ = US GDP — EU is large enough to affect US GDP, so exogeneity is questionable
4. $Y$ = US inflation, $X$ = OPEC oil prices — plausibly exogenous (OPEC sets prices for its own reasons)
5. $Y$ = GDP growth, $X$ = Federal Funds rate — NOT exogenous (the Fed reacts to GDP)
6. $Y$ = change in inflation, $X$ = unemployment rate — NOT exogenous (Phillips curve: simultaneous causality)

### 7. Distributed Lag Model Assumptions
1. $E(u_t | X_t, X_{t-1}, X_{t-2}, \ldots) = 0$ — $X$ is exogenous
2. (a) $Y$ and $X$ have **stationary distributions** (time series counterpart of "identically distributed")
   (b) $(Y_t, X_t)$ and $(Y_{t-j}, X_{t-j})$ become **independent as $j$ gets large** (time series counterpart of "independently distributed")
3. $Y$ and $X$ have **eight nonzero finite moments** (needed for HAC estimators; compare four for cross-section)
4. No perfect multicollinearity

**Stationarity interpretation:**
- Assumption 2(a): Coefficients don't change within sample (internal validity) and results extrapolate outside sample (external validity)
- Assumption 2(b): Widely separated time periods act as separate experiments; a version of the CLT holds

### 8. Why Conventional OLS Standard Errors Fail
In time series, $u_t$ is typically **serially correlated**. This changes the variance formula for the OLS estimator.

**Simple case ($T = 2$, no lags):**
$$\text{var}\left(\frac{1}{2}\sum_{t=1}^{2} v_t\right) = \frac{1}{2}\sigma_v^2 \times f_2, \quad \text{where } f_2 = (1 + \rho_1)$$

- In i.i.d. (cross-section) data, $\rho_1 = 0$ so $f_2 = 1$ — gives the usual formula
- In time series data, $\rho_1 \neq 0$ — the usual formula is wrong

**General case:**
$$\text{var}(\hat{\beta}_1) = \left[\frac{1}{T} \frac{\sigma_v^2}{(\sigma_X^2)^2}\right] \times f_T, \quad \text{where } f_T = 1 + 2\sum_{j=1}^{T-1}\left(\frac{T-j}{T}\right)\rho_j$$

The OLS SEs are off by the factor $f_T$, which can be large.

### 9. HAC (Heteroskedasticity and Autocorrelation-Consistent) Standard Errors
**Problem:** We don't know $f_T$ because it depends on unknown autocorrelations $\rho_j$.

**Solution:** Estimate $f_T$ using the **Newey-West** estimator:
$$\hat{f}_T = 1 + 2\sum_{j=1}^{m-1}\left(\frac{m-j}{m}\right)\tilde{\rho}_j$$

- $\tilde{\rho}_j$ is an estimator of $\rho_j$
- $m$ is the **truncation parameter** — determines how many autocorrelation lags to include
- **Rule of thumb for $m$:** Use the Goldilocks method or try $m = 0.75 T^{1/3}$
- For the OJ data: $m = 0.75 \times 612^{1/3} = 6.4 \approx 7$ (or 8, rounded up)

**Key practical point:** HAC SEs are needed for distributed lag regressions. For AR and ADL models, HAC SEs are usually unnecessary if enough lags of $Y$ are included (because the errors become serially uncorrelated).

### 10. Estimation with Strictly Exogenous Regressors
If $X$ is **strictly** exogenous, more efficient estimators exist:
- Generalized Least Squares (GLS)
- Autoregressive Distributed Lag (ADL)

**But:** Strict exogeneity is rarely plausible in practice, so these methods are not emphasized (Section 13.5 is optional).

### 11. OJ Price Data Analysis Results
**Specification:** Distributed lag with $r = 18$ lags (Goldilocks method), Newey-West truncation $m = 7$.

**Key findings (from Table 13.1):**
| Lag | Dynamic Multiplier | Cumulative Multiplier |
|-----|-------------------|----------------------|
| 0   | 0.50 (0.14)       | 0.50 (0.14)          |
| 1   | 0.17 (0.09)       | 0.67 (0.14)          |
| 2   | 0.07 (0.06)       | 0.74 (0.17)          |
| 3   | 0.07 (0.04)       | 0.81 (0.18)          |
| 6   | 0.03 (0.05)       | 0.90 (0.20)          |
| 12  | -0.14 (0.08)      | 0.54 (0.27)          |
| 18  | 0.00 (0.02)       | 0.37 (0.30)          |

- A freeze leads to an **immediate** price increase (impact multiplier = 0.50)
- Future price rises are much smaller than the initial impact
- Cumulative multiplier peaks around 7 months after the freeze
- Adding monthly indicators does not significantly change results ($F = 1.01$, $p = 0.43$)

**Subsample instability:** The dynamic effect of freezes changed significantly over time. Freezes had a larger impact on prices during 1950–1966 than later periods, and the effect was less persistent during 1984–2000.

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| Distributed lag model | $Y_t = \beta_0 + \beta_1 X_t + \ldots + \beta_{r+1} X_{t-r} + u_t$ | Estimating dynamic causal effects |
| Impact effect | $\beta_1$ | Immediate effect of $X$ on $Y$ |
| $k$-period cumulative multiplier | $\sum_{j=1}^{k+1} \beta_j$ | Total effect through $k$ periods |
| Exogeneity condition | $E(u_t \| X_t, X_{t-1}, \ldots) = 0$ | Required for causal interpretation |
| Strict exogeneity | $E(u_t \| \ldots, X_{t+1}, X_t, X_{t-1}, \ldots) = 0$ | Stronger condition, rarely plausible |
| Variance with serial correlation | $\text{var}(\hat{\beta}_1) = \frac{1}{T}\frac{\sigma_v^2}{(\sigma_X^2)^2} \times f_T$ | Shows why OLS SEs are wrong |
| $f_T$ factor | $1 + 2\sum_{j=1}^{T-1}\left(\frac{T-j}{T}\right)\rho_j$ | Correction factor for serial correlation |
| Newey-West estimator | $\hat{f}_T = 1 + 2\sum_{j=1}^{m-1}\left(\frac{m-j}{m}\right)\tilde{\rho}_j$ | HAC standard error computation |
| Truncation parameter rule | $m = 0.75 T^{1/3}$ | Choosing Newey-West bandwidth |
| Percentage price change | $\%ChgP_t = 100\Delta\ln(\text{Price}_t)$ | Transforming price to growth rate |

## Examples from Class

### Example 1: Orange Juice Prices and Freezing Degree-Days
- **Setup:** Monthly data (1950–2000, $T=612$). $Y$ = percentage change in frozen OJ price, $X$ = FDD in Orlando.
- **Key finding:** One additional FDD increases current-month prices by 0.47–0.50%. The effect persists: cumulative multiplier peaks at ~0.90 at 6 months.
- **Takeaway:** Freezes have both an immediate and persistent dynamic effect on OJ prices, but the initial impact dominates.

### Example 2: Robust vs Newey-West Standard Errors
- **Setup:** Regress OJ price change on lagged FDD. Compare heteroskedasticity-robust SEs to Newey-West HAC SEs (with $m = 8$).
- **Key finding:** Robust SE = 0.077, Newey-West SE = 0.078 — small difference in this case (t-stat: 1.99 vs 1.96).
- **Takeaway:** The difference between robust and HAC SEs can be small, but not always. HAC SEs should be used as a default in distributed lag regressions.

### Example 3: Subsample Instability in OJ Dynamic Effects
- **Setup:** Estimate cumulative dynamic multipliers separately for 1950–1966, 1967–1983, and 1984–2000.
- **Key finding:** Freezes had a much larger and more persistent effect on prices in 1950–1966 (peak ~2.0) than in 1984–2000 (peak ~0.5, then negative).
- **Takeaway:** The relationship between freezes and OJ prices was not stable over time, suggesting the stationarity assumption may be violated.

### Example 4: Exogeneity Assessment
- **Setup:** Evaluate whether $X$ is exogenous in various macro relationships.
- **Key finding:** FDD is plausibly exogenous for OJ prices (traders can't change weather). The Fed Funds rate is NOT exogenous for GDP growth (the Fed reacts to GDP). Unemployment is NOT exogenous for inflation (Phillips curve: simultaneous causality).
- **Takeaway:** Exogeneity must be evaluated case by case; simultaneous causality and feedback are the main threats.

### Example 5: Ideal Experiment (Fertilizer on Tomato Yield)
- **Setup:** Randomize fertilizer across plots, measure yield over multiple harvests.
- **Key finding:** This is the ideal RCT approach to estimating dynamic causal effects, but it is infeasible in most time series settings (only one "subject").
- **Takeaway:** The distributed lag estimator is the time series substitute, relying on stationarity and exogeneity instead of randomization.

## Connections
- **Builds on:** Week 4 distinction between structural and time series models, exogeneity concepts, AR/ADL models
- **Related to:** SW Chapter 13 (Stock & Watson textbook, Appendix 13.1 for OJ data)
- **Prerequisite for:** VAR models (identification in VAR is about ensuring the shock of interest is exogenous)

## Questions to Consider
1. Why can't we use a standard differences estimator to measure dynamic causal effects in time series?
2. Under what conditions does the distributed lag estimator consistently estimate dynamic causal effects?
3. Why are conventional OLS standard errors wrong when errors are serially correlated? How big can the distortion be?
4. How do you choose the truncation parameter $m$ for Newey-West HAC standard errors?
5. Why are HAC SEs generally unnecessary for AR and ADL models (but needed for distributed lag models)?
6. For the OJ data, why is FDD plausibly exogenous but not strictly exogenous? Does the distinction matter?
7. What does the subsample instability in the OJ example imply about the stationarity assumption?
8. Why is the Federal Funds rate not exogenous when studying its effect on GDP growth?
9. How do you interpret a cumulative dynamic multiplier that first rises and then falls?
10. If strict exogeneity held, why would GLS or ADL be preferred over the distributed lag estimator?

## Review Checklist
- [ ] Understand what a dynamic causal effect is and how it differs from a static effect
- [ ] Can explain the distributed lag model and interpret its coefficients (impact effect, dynamic multipliers, cumulative multipliers)
- [ ] Know the four assumptions of the distributed lag model
- [ ] Understand the difference between exogeneity and strict exogeneity
- [ ] Can evaluate whether exogeneity is plausible in a given application
- [ ] Understand why conventional OLS SEs are wrong with serially correlated errors
- [ ] Can explain the $f_T$ correction factor and its role in the variance formula
- [ ] Know how Newey-West HAC SEs work (truncation parameter, weighting scheme)
- [ ] Can apply the rule of thumb $m = 0.75T^{1/3}$ for the truncation parameter
- [ ] Know when HAC SEs are needed (distributed lag) vs unnecessary (AR/ADL with enough lags)
- [ ] Can interpret the OJ price data results (Table 13.1 and multiplier graphics)
- [ ] Understand why the distributed lag approach requires stationarity
- [ ] Know that strict exogeneity enables more efficient estimation (GLS, ADL) but is rarely plausible
- [ ] Understand how subsample instability relates to the stationarity assumption
