# Week 7: Unit Root Tests — Lecture Summary & Key Concepts

## Overview

This lecture addresses one of the most important questions in applied time series: **does your data have a unit root (stochastic trend) or is it trend stationary?** The answer determines how you transform the data, how you forecast, and how you interpret the effect of shocks. Professor Pesavento emphasizes that this is genuinely hard to detect and has been a central research question in econometrics since the 1980s.

---

## 1. Why Non-Stationarity Matters

Everything covered so far in the course (Wold decomposition, ARMA models, CLT) **requires stationarity**. Sources of non-stationarity include:

- **Deterministic trend** — data moves along a predictable path (trend stationary)
- **Structural breaks** — parameters change at a point in time
- **Time-varying variance** — heteroskedasticity over time
- **Stochastic trend (unit root)** — the most common reason in macro data

The critical issue: **the correct transformation to achieve stationarity depends on which type of non-stationarity you have**, and there is no single solution that works for all cases.

---

## 2. Core Definitions

### Random Walk (Unit Root)
```
y_t = y_{t-1} + epsilon_t
```
- This is an AR(1) with rho = 1
- Also called: unit root process, martingale, integrated process
- First difference: Delta_y_t = epsilon_t (stationary)

### Random Walk with Drift
```
y_t = c + y_{t-1} + epsilon_t
```
- Same as above but with a constant `c` that creates a linear trend in the mean
- First difference: Delta_y_t = c + epsilon_t (stationary)

### Integration Order
- y_t is **integrated of order d**, written I(d), if the d-th difference is stationary
- A random walk is I(1) — one differencing makes it stationary
- If rho > 1, the process is **explosive** (not realistic for most economic data)

### Connection to Python's ARIMA
- In `ARIMA(p, d, q)`: the middle parameter `d` is the integration order
- `ARIMA(2, 1, 2)` means: take first difference, then fit ARMA(2,2) on the differenced data

---

## 3. Properties of a Random Walk

### By back-substitution:
```
y_t = y_0 + SUM(epsilon_j, j=1 to t)
```

### Key properties:
| Property | Random Walk | Random Walk with Drift |
|---|---|---|
| **Mean** | E(y_t) = 0 | E(y_t) = ct |
| **Variance** | Var(y_t) = t * sigma^2 | Var(y_t) = t * sigma^2 |
| **Autocovariance** | gamma_k = (t-k) * sigma^2 | gamma_k = (t-k) * sigma^2 |
| **Autocorrelation** | rho_k = sqrt((t-k)/t) -> 1 | rho_k -> 1 |

**Why it's not stationary:**
- Variance depends on time `t` (grows without bound)
- Covariance depends on `t`, not just the lag `k`
- Autocorrelation converges to 1 as t grows large
- The initial condition y_0 never disappears
- The AR polynomial alpha(z) = 1 - z is not invertible at z = 1

### Professor Pesavento's "drunk person" analogy:
> Imagine a drunk person walking down the street, stumbling randomly. You cannot predict which direction they'll go. They hit a curb and drift one way for a long time, then a pebble sends them the other way. Your best guess for where they'll be? Where they are right now.

---

## 4. Deterministic Trend vs. Stochastic Trend — Forecasting Implications

This is the central comparison of the lecture. The two models **look similar visually** but have **completely different implications**.

### Deterministic Trend: y_t = alpha + ct + Psi(L) * epsilon_t

**Forecast:** as horizon s -> infinity, forecast converges to `alpha + c(t+s)`
- The forecast **does not depend on where y is today**
- You project the trend line forward regardless of current value
- The trend is a fixed rail the data returns to

### Stochastic Trend: Delta_y_t = c + Psi(L) * epsilon_t

**Forecast:** as horizon s -> infinity, forecast converges to `sc + y_t`
- The forecast **depends entirely on today's value y_t**
- Starting point matters: a forecast made in February 2026 differs from one made in January 2026
- Each new data point can shift the entire forecast path

### Professor Pesavento's GDP example:
> With a deterministic trend, it doesn't matter when you start your forecast — you always end up at the same projected trend value. With a stochastic trend, your forecast made from a different starting point gives a different answer every time. The starting point is everything.

### MSE Comparison:
- **Deterministic trend:** MSE converges to the unconditional variance of y_t (finite)
- **Stochastic trend:** MSE does not converge — grows without bound as forecast horizon increases

---

## 5. Dynamic Multipliers — Permanent vs. Temporary Shocks

### Deterministic trend:
```
dy_{t+s}/d(epsilon_t) = psi_s -> 0 as s -> infinity
```
**The effect of a shock vanishes eventually.**

### Stochastic trend:
```
dy_{t+s}/d(epsilon_t) = 1 + psi_1 + psi_2 + ... + psi_s -> Psi(1) as s -> infinity
```
**The effect of a shock is permanent** (converges to long-run multiplier Psi(1)).

This has major policy implications. As Pesavento puts it:
> Suppose I'm a policymaker and I want to surprise the economy by doing a policy shock. I need to know if the effect is going to be permanent or temporary. And even if temporary, how quickly it disappears.

---

## 6. Transformations to Achieve Stationarity

### Option 1: Detrend (subtract the trend)
- **Works for trend stationary:** y_t - ct = mu + epsilon_t (stationary)
- **Fails for unit root with drift:** y_t - ct = y_0 + SUM(epsilon_j) — still has variance t*sigma^2. Detrending removes the trend in the mean but **not in the variance**.

### Option 2: Take the first difference
- **Works for unit root:** Delta_y_t = c + epsilon_t (stationary)
- **Fails for trend stationary:** Delta_y_t = c + epsilon_t + epsilon_{t-1} — introduces a **unit root in the MA part** (non-invertible)

**Bottom line:** There is no universal fix. You must determine which model fits your data before choosing the transformation.

---

## 7. The Dickey-Fuller (DF) Test

### Setup
Start from AR(1): y_t = rho * y_{t-1} + epsilon_t

Reparameterize by subtracting y_{t-1} from both sides:
```
Delta_y_t = alpha * y_{t-1} + epsilon_t    where alpha = (rho - 1)
```

### Hypotheses
```
H0: rho = 1  =>  alpha = 0   (unit root)
H1: rho < 1  =>  alpha < 0   (stationary)
```

### The Test Statistic
```
t = alpha_hat / SE(alpha_hat)
```
This looks like a standard t-test, **but the distribution under the null is NOT normal**. It is the **Dickey-Fuller distribution**, which is shifted to the left relative to the normal. This is because random walks have fundamentally different statistical behavior (related to Brownian motions in continuous time).

### Critical Values (Dickey-Fuller, not Normal!)

| Specification | 10% | 5% | 1% |
|---|---|---|---|
| Intercept only | -2.57 | -2.86 | -3.43 |
| Intercept + trend | -3.12 | -3.41 | -3.96 |

**Decision rule:** Reject H0 (no unit root) if the test statistic is **more negative** than the critical value. This is a **one-sided test** (left tail only).

### The test is "non-pivotal"
Unlike standard t-tests, what you include in the regression (constant, trend) **changes the critical values**. This is why you must decide the specification before testing.

### How to choose intercept vs. intercept + trend:
- **Intercept only:** when the data looks like it fluctuates around a constant (no obvious trend)
- **Intercept + trend:** when the data has a visible upward or downward drift that could be either deterministic or stochastic

---

## 8. Augmented Dickey-Fuller (ADF) Test

Real data has more complex dynamics than AR(1). The ADF test adds lagged differences:

```
Delta_Y_t = mu + alpha * Y_{t-1} + gamma_1 * Delta_Y_{t-1} + gamma_2 * Delta_Y_{t-2} + ... + gamma_{p-1} * Delta_Y_{t-p+1} + u_t
```

- The test on alpha = 0 is the same, using the same DF critical values
- **Choosing the number of lags:** Use AIC or BIC with a reasonable maximum (e.g., 12 for monthly data, 4 for quarterly). Most software packages can auto-select.

---

## 9. Worked Example: US Inflation Rate

- **Visual inspection:** No obvious trend, fluctuates around a level -> use **intercept only**
- **Lag selection:** AIC with max=8, selects 8 lags
- **ADF statistic:** -3.94
- **Critical values (intercept only):** 1% = -3.44, 5% = -2.87, 10% = -2.57
- **p-value:** 0.0018
- **Conclusion:** Reject the null of a unit root at all significance levels

**But Pesavento cautions:** the statistic (-3.94) is close to the 1% critical value (-3.44). The result could change with different sample sizes. Inflation is a topic of genuine debate — it's very persistent (rho around 0.9-0.95) but probably not exactly a unit root. Historically, many researchers modeled inflation as I(1), though more recent consensus leans toward "persistent but stationary."

**Key insight from class discussion:** If there are structural breaks in the data and you ignore them, the unit root test can falsely conclude there is a unit root when there isn't one. Some tests allow for breaks, or you can include break dummies in the test regression.

---

## 10. Stationarity Tests (Reverse Approach)

The DF/ADF test has the unit root as the **null** hypothesis. But we might want to reverse this:
- **Stationarity tests** (e.g., KPSS): H0 = stationary, H1 = unit root
- The two types of tests **may not give the same answer** — this is expected and reflects the difficulty of the problem
- Running both kinds of tests is good practice

---

## 11. Practical Decision Framework (Professor Pesavento's Recommended Steps)

1. **Plot your data.** Always look at it first.
2. **Does a trend look plausible?** If yes, include the trend in your test regression.
3. **If no obvious trend** but you suspect a unit root, test with intercept only.
4. **Use a software package** — run the ADF test (and other tests if available: DF-GLS, ERS).
5. **If you clearly reject:** data does not have a unit root. Model in levels.
6. **If you clearly fail to reject:** data has a unit root. Work with first differences.
7. **If results are ambiguous** (borderline rejection, conflicting tests): Stop. Think. Make a defensible decision and justify it.
8. **If unit root is confirmed:** take the first difference and proceed with ARMA modeling on Delta_y_t.

---

## 12. Which Test to Use?

- **ADF** is the baseline, available everywhere
- **DF-GLS and ERS (Elliott-Rothenberg-Stock)** are more powerful — use them if available
- Present a **battery of tests** for robustness (this is what appendices are for)
- **MAIC** (Modified AIC) is recommended for lag selection in the test regression
- Consider confounders: structural breaks, heteroskedasticity, seasonality
- Filters (HP, BK) **should not be applied to non-stationary data**

---

## 13. The Current Consensus (Per Pesavento)

- In the 1980s (Nelson & Plosser): "everything has a unit root"
- Early tests had low power and over-concluded unit roots
- Better tests in the 1990s (Pesavento's own dissertation topic) revealed many series are **persistent but not unit root** (rho around 0.9-0.95)
- Most macro data is probably **near-unit-root** — the shock effect lasts a very long time but eventually dies out
- In practice, with finite samples (e.g., 20 years), rho = 0.95 is nearly indistinguishable from rho = 1
- Recent consensus favors **robust methods** that work whether or not there is a unit root, especially in VARs
- **When in doubt, don't impose restrictions that may be wrong** — better to not difference if you're unsure

---

## Key Formulas Quick Reference

| Concept | Formula |
|---|---|
| Random walk | y_t = y_{t-1} + epsilon_t |
| Random walk with drift | y_t = c + y_{t-1} + epsilon_t |
| Back-substitution | y_t = y_0 + SUM(epsilon_j) |
| Variance of RW | Var(y_t) = t * sigma^2 |
| Autocorrelation of RW | rho_k = sqrt((t-k)/t) -> 1 |
| DF reparameterization | Delta_y_t = alpha * y_{t-1} + epsilon_t, alpha = rho - 1 |
| DF test hypotheses | H0: alpha = 0 (unit root) vs H1: alpha < 0 (stationary) |
| ADF regression | Delta_Y_t = mu + alpha*Y_{t-1} + SUM(gamma_j * Delta_Y_{t-j}) + u_t |
| Dynamic multiplier (trend) | dy_{t+s}/d(eps_t) = psi_s -> 0 |
| Dynamic multiplier (unit root) | dy_{t+s}/d(eps_t) -> Psi(1) (permanent) |

---

## Key Terminology

| Term | Meaning |
|---|---|
| **Unit root** | AR coefficient rho = 1; the "root" of the AR polynomial equals one |
| **Random walk** | Equivalent to unit root process: y_t = y_{t-1} + noise |
| **I(d)** | Integrated of order d: needs d differences to become stationary |
| **Trend stationary** | Has a deterministic trend; detrending makes it stationary |
| **Difference stationary** | Has a stochastic trend; differencing makes it stationary |
| **Dickey-Fuller distribution** | Non-normal distribution of the t-statistic under the unit root null |
| **Non-pivotal** | The test distribution changes depending on what's in the regression |
| **ADF** | Augmented Dickey-Fuller: DF test with lagged differences added |
| **Near unit root** | rho close to 1 (e.g., 0.95) — very persistent but eventually mean-reverting |
| **Psi(1)** | Long-run multiplier: permanent effect of a shock in a unit root process |
