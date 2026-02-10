# Week 3: Univariate Time Series Introduction

## Main Topic
Introduction to the foundations of univariate time series analysis: definitions, transformations, dependence structures, stationarity conditions, and the theoretical basis for ARMA modeling.

## Key Concepts

### 1. Time Series Definition
**Definition:** A time series $y_t \in \mathbb{R}^m$ is a process observed sequentially over time $t = 1, \ldots, n$. Univariate if $m=1$, multivariate if $m>1$.
**Intuition:** Unlike cross-sectional data, observations close in time are expected to be dependent. This dependence structure is what distinguishes time series econometrics and requires different distributional theory.
**Example:** GDP measured quarterly ($s=4$), stock prices measured daily ($s=252$).

### 2. Differences and Growth Rates
**Definition:** Common transformations applied to time series before analysis.
- First difference: $\Delta y_t = y_t - y_{t-1}$
- Second difference: $\Delta^2 y_t = \Delta y_t - \Delta y_{t-1}$ (acceleration)
- Year-on-year change: $\Delta_s y_t = y_t - y_{t-s}$
- Growth rate: $q_t = 100(\Delta y_t / y_{t-1}) \approx \log(y_t) - \log(y_{t-1})$

**Intuition:** Log transformations flatten exponential growth. Growth rates approximate log differences. You lose one observation when you lag.

### 3. The Lag Operator
**Definition:** $Ly_t = y_{t-1}$, with $L^k y_t = y_{t-k}$.
**Key properties:**
- Polynomials: $a(L) = a_0 + a_1 L + a_2 L^2 + \ldots + a_p L^p$
- Commutative multiplication: $a(L)b(L) = b(L)a(L)$
- Inversion: If $|\rho| < 1$, then $(1 - \rho L)^{-1} = \sum_{i=0}^{\infty} \rho^i L^i$
- First difference: $(1 - L) = \Delta$

**Example (from class annotation):** $y_t - 3y_{t-1} + 2y_{t-2} = (1 - 3L + 2L^2)y_t = a(L)y_t$

### 4. White Noise (WN)
**Definition:** A sequence $\{e_t\}$ such that $E(e_t) = 0$, $E(e_t e_s) = 0$ for $t \neq s$, and $E(e_t^2) = \sigma^2$.
**Intuition:** Completely random, serially uncorrelated by definition. The best forecast of a WN process is zero (its mean). WN is the building block for AR and MA models.
**Key distinction (from annotations):** Correlation = 0 does NOT imply independence. Correlation only captures linear relationships. The equivalence holds only under normality.

### 5. Martingale Difference Sequence (MDS)
**Definition:** $\{Y_t\}$ with $E(Y_t) = 0$ and $E(Y_t | \Omega_t) = 0$ where $\Omega_t$ is the information set at time $t$.
**Intuition:** Stronger than serially uncorrelated (rules out all nonlinear predictability from past), but weaker than independence because $E(Y_t^2 | Y_{t-1}, \ldots) \neq 0$ is allowed (conditional heteroskedasticity is OK).
**Hierarchy:** Independent WN > MDS > Uncorrelated WN

### 6. Autocovariance Function
**Definition:** $\gamma(k) = \text{COV}(y_t, y_{t-k})$
**Properties:**
- $\gamma(0) = \text{VAR}(y_t) = \sigma^2$ (constant, doesn't depend on $t$)
- $\gamma(s) = \gamma(-s)$ (symmetric)

**Example (from annotation):** $\gamma(3)$ tells you how GDP today is correlated with GDP 3 quarters ago.

### 7. Autocorrelation Function (ACF)
**Definition:** $\rho(s) = \gamma(s) / \gamma(0)$
**Properties:** $0 \leq |\rho(s)| \leq 1$ and $\rho(0) = 1$
**Estimation (correlogram):**
$$\hat{\rho}(s) = \frac{\sum_{t=s+1}^{T}(y_t - \bar{y})(y_{t-s} - \bar{y})}{\sum_{t=1}^{T}(y_t - \bar{y})^2}$$
**Large sample distribution:** $\hat{\rho}(s) \sim N(0, 1/T)$
**Joint test:** Box-Pierce Q-statistic: $Q_{BP} = T \sum_{s=1}^{m} \hat{\rho}^2(s)$

### 8. Partial Autocorrelation Function (PACF)
**Definition:** $p(s)$ is the coefficient of $y_{t-s}$ in a population regression of $y_t$ on $y_{t-1}, y_{t-2}, \ldots, y_{t-s}$.
**Intuition:** Measures correlation at lag $s$ after controlling for intermediate lags. ACF and PACF together are the main tools for identifying time series models.
**From annotation:** ACF = total correlation (like simple regression coefficient); PACF = partial correlation (like multiple regression coefficient). "Two different types of correlation."

### 9. Stationarity
**Strong stationarity:** The joint distribution of $\{y_t, \ldots, y_{t+k}\}$ is identical to $\{y_{t+n}, \ldots, y_{t+k+n}\}$ for all $k, t, n$. Very restrictive.
**Weak (covariance) stationarity:** $E(y_t) = \mu$ and $\text{cov}(y_t, y_{t-s}) = \gamma_s$ do not depend on $t$. This is what we usually work with in practice.
**Key insight:** We need stability so that past patterns help predict the future.

**Non-stationary examples:**
- **Structural break:** $y_t = \beta + e_t$ for $t \leq k$, $y_t = \beta + \lambda + e_t$ for $t > k$ (mean changes, from annotation: "mean is not constant, so it's not stationary")
- **Random walk:** $y_t = y_{t-1} + e_t$ where $\text{Var}(y_t) > \text{Var}(y_{t-1})$ (variance grows with time)
- Annotation also notes the difference between outliers and structural breaks

### 10. Ergodic Theorem
**Definition:** A covariance stationary process is ergodic for the mean if $\bar{y} = \frac{1}{T}\sum_{t=1}^{T} y_t \xrightarrow{p} E(Y_t)$ as $T \to \infty$.
**Sufficient condition:** $\sum_{j=0}^{\infty} |\gamma_j| < \infty$ (autocovariances decay fast enough)
**Intuition:** Ergodicity justifies using time averages to estimate population moments. For practical purposes, stationarity and ergodicity often go hand in hand.

### 11. Wold Representation Theorem
**Statement:** Any zero-mean covariance-stationary process can be written as:
$$Y_t = \sum_{j=0}^{\infty} \psi_j \varepsilon_{t-j} + k_t$$
where $k_t$ is deterministic, $\psi_0 = 1$, $\sum \psi_j^2 < \infty$, and $\varepsilon_t$ is white noise.
**Intuition:** Every stationary process has an infinite MA representation. In practice, we approximate with finite-order ARMA models.

### 12. Models for Cycles (Preview)
- **AR (Autoregressive):** Current value depends on past values
- **MA (Moving Average):** Current value depends on past shocks
- **ARMA:** Combination of AR and MA
- **White Noise:** No dependence with the past
- From annotation: WN has ACF/PACF that are 1 at lag 0 and 0 everywhere else

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| First difference | $\Delta y_t = y_t - y_{t-1}$ | Removing trends, computing changes |
| Growth rate | $q_t \approx \log(y_t) - \log(y_{t-1})$ | Percentage changes |
| Lag operator | $L^k y_t = y_{t-k}$ | Compact notation for TS models |
| Lag poly inversion | $(1-\rho L)^{-1} = \sum_{i=0}^{\infty} \rho^i L^i$ if $|\rho|<1$ | Converting AR to MA representation |
| Autocovariance | $\gamma(k) = \text{COV}(y_t, y_{t-k})$ | Measuring dependence at lag $k$ |
| ACF | $\rho(s) = \gamma(s)/\gamma(0)$ | Normalized dependence measure |
| Sample ACF | $\hat{\rho}(s) \sim N(0, 1/T)$ | Testing significance of correlations |
| Box-Pierce | $Q_{BP} = T\sum_{s=1}^{m} \hat{\rho}^2(s)$ | Joint test for white noise |
| Wold decomposition | $Y_t = \sum_{j=0}^{\infty}\psi_j \varepsilon_{t-j} + k_t$ | Theoretical basis for ARMA models |

## Examples from Class

### Example 1: US Inflation Rate
- **Setup:** Annual US inflation rate from ~1955 to ~2024
- **Observation:** Highly persistent series (high ACF values that decay slowly)
- **Annotation:** "Inflation today has a correlation with inflation 1 month ago by 0.8"
- **Takeaway:** Persistent ACF pattern suggests AR-type dynamics, not white noise

### Example 2: Structural Break
- **Setup:** $y_t = \beta + e_t$ for $t \leq k$, $y_t = \beta + \lambda + e_t$ for $t > k$
- **Annotation:** Mean jumps from $\beta$ to $\beta + \lambda$, so it's not stationary. Drew diagram showing two different mean levels.
- **Takeaway:** Non-constant mean violates weak stationarity

### Example 3: Random Walk
- **Setup:** $y_t = y_{t-1} + e_t$
- **Key result:** $\text{Var}(y_t) = \text{Var}(y_{t-1}) + \text{Var}(e_t) > \text{Var}(y_{t-1})$
- **Takeaway:** Variance grows over time, violating stationarity

## Connections
- **Builds on:** Week 1-2 concepts of time series decomposition (trend, seasonal, cyclical components)
- **Related to:** Problem Set 1, especially Questions 1 (MA(1) feasibility) and 3 (testing for white noise in financial returns)
- **Prerequisite for:** Week 4+ coverage of specific AR, MA, and ARMA model properties, estimation, and identification

## Questions to Consider
1. Why can't we divide a time series sample into independent groups the way we can with cross-sectional data?
2. If a process is uncorrelated (WN), does that mean it's unpredictable? What about nonlinear predictability?
3. Why is weak stationarity sufficient for most practical applications while strong stationarity is rarely needed?
4. How does the Wold theorem justify using finite-order ARMA models in practice?
5. Looking at an ACF plot, how would you distinguish between a WN process and a highly persistent AR process?

## Review Checklist
- [ ] Understand the difference between strong and weak stationarity
- [ ] Can explain why WN, MDS, and independence are different concepts
- [ ] Can compute and interpret autocovariance and ACF
- [ ] Understand the distinction between ACF and PACF
- [ ] Can use the lag operator to express differences and polynomials
- [ ] Can identify non-stationary processes (break, random walk)
- [ ] Understand the Wold Representation Theorem and its practical implications
- [ ] Know the properties of white noise (ACF = 0 for all $s > 0$)
- [ ] Can interpret a correlogram and Box-Pierce Q-statistic
- [ ] Understand ergodicity and why it matters for estimation
