# Answer Keys — All 6 Practice Exams

Use these to check your work AFTER attempting each exam under timed conditions.

---

# Practice Exam 1 Answers

## Q1: MA(1) Autocovariance
(a) $\text{Var}(y_t) = (1 + 0.6^2)\sigma^2 = (1 + 0.36)\sigma^2 = 1.36\sigma^2$

(b) $\gamma(1) = \theta_1 \sigma^2 = 0.6\sigma^2$

(c) $\gamma(2) = 0$ — MA(1) has autocovariance cutoff after lag 1.

(d) $\rho(1) = \gamma(1)/\gamma(0) = 0.6\sigma^2 / 1.36\sigma^2 = 0.441$

## Q2: ACF/PACF → AR(1)
The ACF decays gradually (exponentially). The PACF has one significant spike at lag 1, then cuts off. This is the classic **AR(1)** signature. ACF decay = AR; PACF cutoff at 1 = order 1. So p = 1.

## Q3: F-Test
(a) $SSR_R = 1820.6$, $SSR_U = 590.8$, $q = 2$, $n = 80$, $k_U = 4$

$F = \frac{(1820.6 - 590.8)/2}{590.8/(80-4)} = \frac{1229.8/2}{590.8/76} = \frac{614.9}{7.774} = 79.1$

$F(2, 76)$ at 5% $\approx 3.12$. **Reject** — lags are jointly highly significant.

(b) ADSPEND coefficient drops from 0.342 (significant) to 0.085 (not significant). Once you account for sales persistence (past sales predict future sales), the additional effect of advertising is small. Most of the variation is explained by the autoregressive dynamics.

## Q4: Forecasting
(a) h=1: $\hat{y}_{2025:Q1} = 3.45 + 0.085(14.0) + 0.612(51.7) + 0.245(48.2) = 3.45 + 1.19 + 31.64 + 11.81 = 48.09$

(b) h=2: $\hat{y}_{2025:Q2} = 3.45 + 0.085(13.5) + 0.612(\mathbf{48.09}) + 0.245(51.7) = 3.45 + 1.15 + 29.43 + 12.67 = 46.70$

Key: at h=2, the L1 term uses the FORECAST (48.09), but L2 uses actual $y_T = 51.7$.

## Q5: Unit Root
(a) Test stat (-2.45) is NOT more negative than CV (-3.44). Fail to reject → unit root present. Should take first differences.

(b) Detrending is correct if the data is **trend stationary** (deterministic trend). It is WRONG if the data has a **unit root** (stochastic trend) — detrending removes the trend in the mean but not the variance, leaving the variance growing with time.

---

# Practice Exam 2 Answers

## Q1: MA(2) Autocovariance
(a) $\text{Var} = (1 + 0.8^2 + 0.2^2)\sigma^2 = (1 + 0.64 + 0.04)\sigma^2 = 1.68\sigma^2$

(b) $\gamma(1) = (\theta_1 + \theta_1\theta_2)\sigma^2 = (0.8 + 0.8 \times 0.2)\sigma^2 = (0.8 + 0.16)\sigma^2 = 0.96\sigma^2$

$\gamma(2) = \theta_2\sigma^2 = 0.2\sigma^2$

(c) $\gamma(3) = 0$. MA(2) has zero autocovariance beyond lag 2 — the "memory" only extends 2 periods.

(d) $\rho(1) = 0.96/1.68 = 0.571$. $\rho(2) = 0.2/1.68 = 0.119$.

## Q2: ACF/PACF → MA(2)
The ACF has significant spikes at lags 1 and 2, then cuts off sharply to zero. The PACF decays gradually. ACF cutoff = MA; cutoff at lag 2 = MA(2). Can forecast 2 steps ahead; beyond that, forecast = mean.

## Q3: Mincer-Zarnowitz
(a) $t = 0.45/0.20 = 2.25$, p = 0.031 < 0.05. **Significant** — evidence of constant bias (forecast too low by ~0.45).

(b) $t = (0.78 - 1)/0.11 = -0.22/0.11 = -2.00$. Significant at 5% — forecast is too smooth ($\beta_1 < 1$).

(c) $F = \frac{(10.85 - 8.42)/2}{8.42/(36-2)} = \frac{2.43/2}{8.42/34} = \frac{1.215}{0.2476} = 4.91$

$F(2, 34)$ at 5% $\approx 3.28$. Since $4.91 > 3.28$, **reject**. Forecast is NOT optimal.

## Q4: ARMA(1,1) Forecast
(a) $\hat{\pi}_{T+1} = 0.15 + 0.72(2.8) + 0.35(0.42) = 0.15 + 2.016 + 0.147 = 2.313$

(b) $\hat{\pi}_{T+2} = 0.15 + 0.72(2.313) + 0 = 0.15 + 1.665 = 1.815$

MA component dies at h=2: $\theta\varepsilon_{T+1}$ is future → zero. Only AR part survives.

(c) 2-step has larger variance. $\sigma_2^2 = \sigma^2(1 + (\phi + \theta)^2) = \sigma^2(1 + (0.72 + 0.35)^2) = \sigma^2(1 + 1.1449) = 2.1449\sigma^2$. Compare to 1-step: $\sigma_1^2 = \sigma^2$.

## Q5: Unit Roots
(a) (i) Det. trend: temporary (shock dies out). Stoch. trend: permanent ($\to \Psi(1)$).
(ii) Det: converges to trend line regardless of today. Stoch: depends on $y_t$ (starting point matters).
(iii) Det: detrend. Stoch: take first difference.

(b) -3.15 < -2.89 → **reject** unit root. Series is stationary. Model in levels (no differencing needed).

---

# Practice Exam 3 Answers

## Q1: Structural Break
(a) Before: slope = 1.85. After: slope = 1.85 + (-0.45) = **1.40**. The trend growth slowed after the crisis.

(b) $F = \frac{(4180.2 - 3245.8)/2}{3245.8/136} = \frac{934.4/2}{23.87} = \frac{467.2}{23.87} = 19.57$

$F(2, 136)$ at 5% $\approx 3.06$. **Reject** — strong evidence of a structural break.

(c) DBROKEN significant (p = 0.029) → **level shift** (sales jumped down by 12.4 at the break). TDBROKEN not significant (p = 0.110) → slope change is NOT significant. The break is primarily a one-time level drop, not a change in the growth rate.

## Q2: ACF/PACF → AR(2)
The PACF has two significant spikes (lag 1 and lag 2) then cuts off. The ACF decays. This is **AR(2)**. BIC selects AR(2) (238.7 lowest AIC, though BIC would also favor AR(2) over ARMA(1,1) since 245.2 < 246.8). Yes, it agrees.

## Q3: AR(1) Forecast
(a) $\hat{y}_{T+1} = 0.35 + 0.82(3.60) = 0.35 + 2.952 = 3.302$

(b) $\hat{y}_{T+2} = 0.35 + 0.82(3.302) = 0.35 + 2.708 = 3.058$

(c) $\mu = c/(1-\phi) = 0.35/(1-0.82) = 0.35/0.18 = 1.944$. As $h \to \infty$: $\hat{y}_{T+h} \to \mu = 1.944$.

## Q4: Forecast Errors
(a) Three properties: (1) Mean zero (unbiased), (2) 1-step errors are white noise, (3) h-step errors are at most MA(h-1).

(b) Bias = mean = $(0.8 - 1.2 + 0.5 + 1.4 - 0.3 - 0.9 + 0.7 - 0.5)/8 = 0.5/8 = 0.0625$

MSE = $(0.64 + 1.44 + 0.25 + 1.96 + 0.09 + 0.81 + 0.49 + 0.25)/8 = 5.93/8 = 0.741$

(c) $y_{t+h} = \beta_0 + \beta_1 \hat{y}_{t+h,t} + u_t$. $H_0: (\beta_0, \beta_1) = (0, 1)$. Reject means forecast is not optimal — there's systematic bias or inefficiency that could be improved.

## Q5: Random Walk
(a) $y_t = \sum_{j=1}^t \varepsilon_j$. $E(y_t) = 0$. $\text{Var}(y_t) = t \cdot 4$.

(b) $\text{Var}(y_{50}) = 200$. $\text{Var}(y_{200}) = 800$. Variance depends on $t$ → violates stationarity (which requires constant variance).

(c) Best forecast: $\hat{y}_{T+h} = y_T = 15$ for all $h$. Error variance at $h=10$: $10 \times 4 = 40$. For AR(1) with $\rho=0.8$: $\sigma_h^2 = \frac{1-0.8^{20}}{1-0.64} \times 4 \approx \frac{0.988}{0.36} \times 4 \approx 10.98$. The random walk ($\text{Var} = 40$) has **much larger** uncertainty at $h=10$.

---

# Practice Exam 4 Answers

## Q1: AR(1) Autocovariance
(a) $\gamma(0) = \sigma^2/(1-\rho^2) = \sigma^2/(1-0.49) = \sigma^2/0.51 = 1.961\sigma^2$

(b) $\gamma(1) = \rho\gamma(0) = 0.7 \times 1.961\sigma^2 = 1.373\sigma^2$. $\gamma(2) = \rho^2\gamma(0) = 0.49 \times 1.961\sigma^2 = 0.961\sigma^2$.

(c) $\rho(1) = \rho = 0.7$. $\rho(2) = \rho^2 = 0.49$. Pattern: geometric decay $\rho(k) = 0.7^k$.

(d) Effect at $t+1$: $0.7$. At $t+2$: $0.7^2 = 0.49$. At $t+5$: $0.7^5 = 0.168$. Shock decays but never fully disappears (asymptotically). This is called the **impulse response function** (or dynamic multiplier).

## Q2: ACF/PACF → MA(1)
ACF: one significant spike at lag 1, then cuts off. PACF: gradual decay. Classic **MA(1)** pattern. Can forecast 1 step beyond the mean; for $h \geq 2$, forecast = $\mu$.

## Q3: CI + Serial Correlation
(a) $\Delta\text{WAGE} = 2.45 \times 4 = 9.80$. CI: $[1.70 \times 4, 3.20 \times 4] = [6.80, 12.80]$.

(b) DW = 0.85, far below 2. Indicates strong **positive serial correlation**. The SEs are likely **underestimated**, making the CI artificially narrow. The true CI may be wider than reported.

(c) Add a lagged dependent variable ($\text{WAGE}_{t-1}$) to the regression. This absorbs the serial correlation, producing valid standard errors (like the AR(1) correction in the past exam Q3).

## Q4: AR(2) Forecast
(a) $\hat{y}_{2025:Q1} = 85.2 + 0.42(3400) + 0.55(1480) + 0.20(1420) = 85.2 + 1428 + 814 + 284 = 2611.2$

(b) $\hat{y}_{2025:Q2} = 85.2 + 0.42(3500) + 0.55(\mathbf{2611.2}) + 0.20(1480) = 85.2 + 1470 + 1436.2 + 296 = 3287.4$

At h=2: L1 uses **forecast** 2611.2; L2 uses **actual** 1480.

## Q5: DF Interpretation
(a) CPI (price level) likely has a unit root — prices accumulate over time and don't revert. Inflation (rate of change) is more likely stationary.

(b) CPI: -1.12 > -3.44 → fail to reject → **unit root**. Inflation: -3.85 < -2.88 → reject → **no unit root (stationary)**.

(c) CPI: use **first differences** ($\Delta$CPI = inflation). Inflation: model in **levels** — it's already stationary.

---

# Practice Exam 5 Answers

## Q1: Unit Root
(a) Series shows long persistent swings without mean reversion. ACF decays extremely slowly (still significant at lag 30). Both suggest non-stationarity / possible unit root.

(b) -1.78 > -2.88 → fail to reject → **data has a unit root**.

(c) Take first difference ($\Delta y_t$). The differenced series should be stationary. Fit ARMA to $\Delta y_t$. The ACF of $\Delta y_t$ should decay much faster (no slow-decay pattern) since differencing removes the unit root.

## Q2: MA(2) with numbers
(a) $E(y_t) = 3$ (the constant).

(b) $\text{Var} = (1 + (-0.5)^2 + 0.4^2) \times 9 = (1 + 0.25 + 0.16) \times 9 = 1.41 \times 9 = 12.69$

(c) $\gamma(1) = (\theta_1 + \theta_1\theta_2)\sigma^2 = (-0.5 + (-0.5)(0.4)) \times 9 = (-0.5 - 0.2) \times 9 = -0.7 \times 9 = -6.3$

$\gamma(2) = \theta_2 \sigma^2 = 0.4 \times 9 = 3.6$

(d) $\rho(1) = -6.3/12.69 = -0.496$

## Q3: Loss Functions
(a) Quadratic ($e^2$) → conditional mean. Absolute ($|e|$) → conditional median. Linlin (asymmetric) → conditional quantile.

(b) **Linlin loss** — under-prediction is costlier. You should penalize negative errors (stockouts) more than positive errors (excess inventory). Your forecast should be **biased upward** (over-predict slightly) to avoid the costlier stockout scenario.

## Q4: DM Test
(a) AR(4) has lower RMSE (0.318 < 0.342) and lower MAE (0.258 < 0.271).

(b) DM p = 0.153 > 0.05 → **cannot reject** equal predictive ability. The RMSE difference is not statistically significant. You can't just compare raw numbers because forecast errors are random variables — the observed difference could be noise.

(c) Since the DM test says they're statistically equivalent, choose the **more parsimonious** model: **AR(2)**. It has fewer parameters (less overfitting risk) and performs statistically the same.

## Q5: MA(2) Forecast
(a) $\hat{y}_{T+1} = 2.1 + 0 + 0.7(1.5) + (-0.3)(-0.8) = 2.1 + 1.05 + 0.24 = 3.39$

(b) $\hat{y}_{T+2} = 2.1 + 0 + 0 + (-0.3)(1.5) = 2.1 - 0.45 = 1.65$

(c) $\hat{y}_{T+3} = 2.1$. All three $\varepsilon$ terms are future → all zero. Beyond $q = 2$ steps, the MA(2) forecast collapses to the unconditional mean.

---

# Practice Exam 6 Answers

## Q1: ARMA(1,1) Autocovariance
Set up the system:
- $\gamma(0) = \phi\gamma(1) + \sigma^2 + \theta\sigma^2$
- $\gamma(1) = \phi\gamma(0) + \theta\sigma^2$

From the second equation: $\gamma(1) = 0.8\gamma(0) + 0.5\sigma^2$

Substitute into the first: $\gamma(0) = 0.8(0.8\gamma(0) + 0.5\sigma^2) + \sigma^2 + 0.5\sigma^2$

$\gamma(0) = 0.64\gamma(0) + 0.4\sigma^2 + 1.5\sigma^2$

$0.36\gamma(0) = 1.9\sigma^2$

(a) $\gamma(0) = 1.9/0.36 \cdot \sigma^2 = 5.278\sigma^2$

(b) $\gamma(1) = 0.8(5.278\sigma^2) + 0.5\sigma^2 = 4.222\sigma^2 + 0.5\sigma^2 = 4.722\sigma^2$

(c) $\rho(1) = 4.722/5.278 = 0.895$. This is LARGER than $\phi = 0.8$ because the positive MA coefficient ($\theta = 0.5$) adds extra correlation at lag 1. The MA component boosts short-run persistence.

## Q2: ACF/PACF → ARMA(1,1)
Both ACF and PACF show gradual decay without sharp cutoffs. Neither cuts off cleanly. This is the **ARMA** signature — when both decay, you need both AR and MA components. ARMA(1,1) is the simplest.

(b) An AR(1) would be a reasonable approximation — it would capture the dominant persistence. But the ARMA(1,1) would likely have a lower BIC/AIC because the MA component adds short-term structure that a pure AR(1) misses.

## Q3: Forecast + Evaluation
(a) $\hat{y}_{T+1} = 1.2 + 0.65(8.0) = 1.2 + 5.2 = 6.4$

$\hat{y}_{T+2} = 1.2 + 0.65(6.4) = 1.2 + 4.16 = 5.36$

(b) 95% CI: $6.4 \pm 1.96 \times 2.0 = 6.4 \pm 3.92 = [2.48, 10.32]$

(c) $e_{T+1} = 7.2 - 6.4 = 0.8$. $e_{T+2} = 6.8 - 5.36 = 1.44$.

(d) $\beta_0 = 0$: $t = 0.95/0.60 = 1.58$. Not significant (|t| < 1.96). No evidence of bias.

$\beta_1 = 1$: $t = (0.82 - 1)/0.10 = -1.80$. Not significant at 5% (|t| < 1.96), but marginally significant at 10%. Mild evidence the forecast is too smooth (under-reacts), but not conclusive.

## Q4: Structural Break + Seasonality
(a) Before break: 0.0042. After break: 0.0042 + (-0.0059) = **-0.0017**. The trend reversed — from positive growth to slight decline after the break.

(b) $D_1 = 0.041$ means Q1 has electricity demand that is, on average, **0.041 log units higher** than Q4 (the base quarter), holding everything else constant.

(c) Restricted model: replace D2 and D3 with a single dummy D23 = D2 + D3 (or equivalently, impose $\delta_2 = \delta_3$ in the estimation). $q = 1$ restriction. Compare $SSR_R$ (restricted) to $SSR_U$ (unrestricted) using $F = \frac{(SSR_R - SSR_U)/1}{SSR_U/(n-k_U)}$.

## Q5: Unit Root Comprehensive
(a) (i) Model A: recession shock is temporary — economy returns to trend. Model B: recession is permanent — GDP never recovers to old path.
(ii) Model A: forecast converges to trend line regardless of today. Model B: forecast starts from today's value — different starting point = different forecast.
(iii) Model A: detrend (include TIME in regression). Model B: difference ($\Delta y_t$).

(b) ADF: fail to reject (p = 0.54) → unit root. KPSS: reject (0.85 > 0.46) → not stationary. Both agree: **unit root present**. (When they conflict, think carefully and consider structural breaks.)

(c) If GDP truly has a unit root, then $\Delta\text{GDP}$ should be stationary and could be WN or have some MA structure — MA(1) in the ACF is consistent with a simple ARIMA(0,1,1) model. If she over-differenced a trend-stationary series, the differencing introduces an MA unit root — the MA(1) coefficient would be near **-1** (non-invertible boundary). If $\hat{\theta} \approx -1$, that's a red flag for over-differencing.
