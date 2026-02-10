# Week 4: Cycles Modeling, Structural vs Time Series Models & ARMA Models

## Main Topic
Understanding cyclical dynamics in time series, the role of autocorrelation in detecting persistence, why stationarity is a prerequisite for modeling cycles, the critical distinction between structural econometric models (causality) and pure time series models (forecasting), and the formal properties and identification of AR, MA, and ARMA models.

## Key Concepts

### 1. Cycles Definition
**Definition:** Cycles capture any dynamics not explained by trend and seasonality. This includes persistence, momentum, and any way the present is linked to the past or future.
**Intuition:** The economy is subject to shocks that persist over time. Good years tend to follow good years, bad follow bad. Eventually something unusual happens (end of recession, start of boom). Think of technology shocks slowly diffusing across sectors.
**Example:** GDP growth, inflation rates, business cycles.

### 2. Autocorrelation as Evidence of Cycles
**Definition:** Serial correlation (autocorrelation) is the correlation of a series with its own lagged values. High autocorrelation = strong cyclical behavior.

**Key examples from class:**

| Series | $\rho(1)$ | $\rho(2)$ | Interpretation |
|--------|-----------|-----------|----------------|
| Inflation (Philippines) | 0.983 | 0.952 | Very high persistence (annotation: "very high") |
| Log GDP | 0.991 | 0.982 | Extremely persistent (still 0.82 at lag 20) |
| GDP Growth ($\Delta \log$ GDP) | 0.261 | 0.255 | Much less persistent after differencing, but still significant |
| Change in Inflation | 0.444 | 0.312 | Moderately persistent |

**Key insight:** Taking log differences eliminates much of the persistence (from 0.99 to 0.26), but remaining autocorrelation is still statistically significant and worth modeling.

### 3. Modeling Cycles in Practice
**How:** Include lagged dependent variables as explanatory variables (autoregressive terms).
- AR(1): $y_t = c + \phi y_{t-1} + \varepsilon_t$ — simplest, often sufficient
- AR(2): $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$ — rarely need more than this
- Can also use MA or ARMA models

**Practical notes:**
- Most time series need **at least** an AR(1), often not more than AR(2)
- Adding lags may make other coefficients insignificant (multicollinearity intuition)
- $R^2$ increases significantly when you add AR terms
- "AR terms are your best friends when it comes to forecasting"

### 4. Stationarity as Prerequisite
**Why it matters for cycles:** We can only model cycles if the data is stationary. We observe a finite window of an infinite process — we need the underlying probabilistic structure to be stable over time.
**Key quote:** "If the underlying probabilistic structure of the series were changing over time, we'd be doomed — there would be no way to relate the future to the past."
**Limitation:** We cannot forecast a structural break. We can model it and forecast the detrended data.

### 5. Structural vs Time Series Models
**This is a major conceptual distinction for the course.**

**Structural models** (causal interpretation):
- Goal: estimate specific parameters (e.g., price elasticity of demand)
- Requires: exogenous/predetermined regressors ($E[p|\varepsilon] = 0$)
- Problem: simultaneity bias when both variables are endogenous (supply & demand example)

**Time series models** (forecasting):
- Goal: predict future values
- Do NOT need causal interpretation of coefficients
- Endogeneity doesn't ruin forecasts — biased coefficients can still produce good predictions
- From annotation: "OLS assumes regressor is exogenous... for forecasting, it doesn't matter"

**Key takeaway (from annotation, circled in class):** "If we only care about **forecasting** prices and/or quantities, then we could just regress q on p or vice-versa and get good forecasts even if we can't exactly estimate the demand function."

### 6. Supply/Demand Simultaneity Example
**Setup:** Regress price (p) on quantity (q).
**Problem:** Is the estimated line the demand curve or supply curve?
**Answer (annotation):** "Neither — combination." The estimated slope is a mixture of true supply and demand slopes. There is simultaneity bias.
**But for forecasting:** This doesn't matter! The biased regression still captures the correlation structure needed for prediction.
**From annotation:** "Think about what question you're asking."

### 7. Exogeneity and Causal Interpretation
**Rule:** To interpret coefficients causally (e.g., price elasticity), the RHS variable must be exogenous: $E[p|\varepsilon] = 0$
**Example:** Use weather as an instrument — it's truly exogenous to demand.
**If unsure:** Do NOT give too much weight to estimated elasticities — bias is probably there.
**Bottom line:** Endogeneity affects causal interpretation but NOT forecast quality.

### 8. MA (Moving Average) Models
**Definition:** Current value depends on current and past shocks (not past values of the series itself).
- MA(1): $y_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$
- MA(2): $y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2}$
- MA(q): $y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \ldots + \theta_q \varepsilon_{t-q}$

**Key property:** MA processes are **always stationary** regardless of parameter values, because they are finite sums of white noise.

**MA(1) properties (solved in class):**
- $E(Y_t) = \mu$
- $\text{Var}(Y_t) = \sigma^2(1 + \theta^2)$
- $\gamma(1) = \theta \sigma^2$
- $\gamma(k) = 0$ for $k \geq 2$
- $\rho(1) = \theta / (1 + \theta^2)$

### 9. AR (Autoregressive) Models
**Definition:** Current value depends on past values of the series.
- AR(1): $y_t = c + \rho y_{t-1} + \varepsilon_t$, or $(1 - \rho L)y_t = c + \varepsilon_t$
- AR(2): $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$
- AR(p): $\phi(L) y_t = c + \varepsilon_t$ where $\phi(L) = 1 - \phi_1 L - \ldots - \phi_p L^p$

**AR(1) properties (solved in class):**
- $E(Y_t) = c / (1 - \rho)$ (requires $|\rho| < 1$)
- $\text{Var}(Y_t) = \sigma^2 / (1 - \rho^2)$
- $\rho(s) = \rho^s$ (ACF decays geometrically)

**AR to MA conversion:** If $|\rho| < 1$: $y_t = \frac{c}{1-\rho} + \sum_{j=0}^{\infty} \rho^j \varepsilon_{t-j}$

**Persistence comparison from class:**
- $\phi = 0.4$: shocks die out quickly (ACF: 0.4, 0.16, 0.064, ...)
- $\phi = 0.9$: shocks persist much longer (ACF: 0.9, 0.81, 0.729, ...)

### 10. ACF/PACF Identification Patterns
**This is the key diagnostic tool for model selection.**

| Model | ACF Pattern | PACF Pattern |
|-------|-------------|--------------|
| AR(p) | Decays (exponential or oscillating) | Cuts off after lag p |
| MA(q) | Cuts off after lag q | Decays (exponential or oscillating) |
| ARMA(p,q) | Decays | Decays |

**Critical distinction:** "Cuts off" means drops to zero sharply at a specific lag. "Decays" means gradually diminishes toward zero.

### 11. Unit Root and Stationarity Conditions
**AR(1) stationarity:** Requires $|\rho| < 1$. If $\rho = 1$ (unit root):
- Variance becomes infinite: $\text{Var}(Y_t) = \sigma^2 / (1 - 1) \to \infty$
- Process is a random walk — non-stationary
- All theoretical results break down

**AR(2) stationarity:** Factor $\phi(L) = (1 - \lambda_1 L)(1 - \lambda_2 L)$. Stationarity requires both roots of the characteristic polynomial to lie **outside the unit circle** (equivalently, $|\lambda_1| < 1$ and $|\lambda_2| < 1$).

**General AR(p):** All roots of $\phi(z) = 0$ must lie outside the unit circle.

### 12. ARMA(p,q) Models
**Definition:** $\phi(L) y_t = c + \theta(L) \varepsilon_t$, combining AR and MA components.
- ARMA(1,1): $y_t = c + \phi y_{t-1} + \varepsilon_t + \theta \varepsilon_{t-1}$
- Both ACF and PACF decay — neither cuts off cleanly
- Stationarity determined by the AR part; invertibility determined by the MA part

**ARMA to MA representation:** Any stationary ARMA can be written as $y_t = \mu + \psi(L)\varepsilon_t$ where $\psi(L) = \theta(L)/\phi(L)$. This connects back to the Wold theorem.

### 13. Invertibility
**Definition:** An MA process is invertible if it can be written as an AR($\infty$) process.
- MA(1) invertible if $|\theta| < 1$: $(1 + \theta L)^{-1} y_t = \varepsilon_t$
- Ensures unique mapping between ACF and model parameters
- Required for well-defined forecasting

**Why it matters:** Without invertibility, two different MA parameter values produce the same ACF — the model is not identified. Convention: always choose the invertible representation.

### 14. Estimation: Box-Jenkins Procedure
**Step-by-step approach to ARMA modeling:**
1. **Identify:** Use ACF and PACF patterns to determine candidate model orders (p, q)
2. **Estimate:** Fit candidate models using MLE or conditional least squares
3. **Diagnose:** Check if residuals are white noise (using ACF of residuals, Box-Pierce/Ljung-Box test)
4. **If residuals not WN:** Revise model order and re-estimate
5. **Forecast:** Once diagnostics pass, use the model for prediction

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| AR(1) | $y_t = c + \phi y_{t-1} + \varepsilon_t$ | Simplest cycle model |
| AR(2) | $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$ | When AR(1) is insufficient |
| MA(1) | $y_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$ | Short-memory shock process |
| MA(q) | $y_t = \mu + \theta(L) \varepsilon_t$ | ACF cuts off at lag q |
| ARMA(p,q) | $\phi(L) y_t = c + \theta(L) \varepsilon_t$ | Both ACF and PACF decay |
| AR(1) mean | $E(Y_t) = c/(1 - \rho)$ | Requires $\|\rho\| < 1$ |
| AR(1) variance | $\text{Var}(Y_t) = \sigma^2/(1 - \rho^2)$ | Requires $\|\rho\| < 1$ |
| AR(1) ACF | $\rho(s) = \rho^s$ | Geometric decay |
| MA(1) variance | $\text{Var}(Y_t) = \sigma^2(1 + \theta^2)$ | Always stationary |
| MA(1) ACF at lag 1 | $\rho(1) = \theta/(1 + \theta^2)$ | Only nonzero autocorrelation |
| AR to MA | $y_t = c/(1-\rho) + \sum \rho^j \varepsilon_{t-j}$ | Converting representations |
| Invertibility | $(1 + \theta L)^{-1}$ exists if $\|\theta\| < 1$ | MA to AR conversion |
| Exogeneity condition | $E[p \| \varepsilon] = 0$ | Required for causal interpretation |
| Autocorrelation | $\rho(s) = \gamma(s)/\gamma(0)$ | Measuring persistence/cycles |

## Examples from Class

### Example 1: Inflation Rate (Philippines)
- **Setup:** Monthly inflation rate 1955–2024
- **Key finding:** $\rho(1) = 0.983$ — extremely persistent
- **Takeaway:** Last month's inflation is highly informative about this month. Change in inflation rate is less persistent ($\rho(1) = 0.44$).

### Example 2: Log GDP vs GDP Growth
- **Setup:** Compare autocorrelation of log GDP (levels) vs first difference (growth)
- **Key finding:** Log GDP has $\rho(1) = 0.991$; GDP growth has $\rho(1) = 0.261$
- **Takeaway:** Differencing removes trend-driven persistence, but residual autocorrelation from cyclical dynamics remains significant.

### Example 3: Supply/Demand Simultaneity
- **Setup:** Price-quantity scatter plot, regress p on q
- **Key finding:** Estimated slope is neither demand nor supply, but a combination
- **Annotation:** "OLS assumes regressor is exogenous... for forecasting, it doesn't matter"
- **Takeaway:** Forecasting doesn't require causal identification; structural interpretation does.

### Example 4: AR(1) Persistence Comparison
- **Setup:** Compare AR(1) with $\phi = 0.4$ vs $\phi = 0.9$
- **Key finding:** With $\phi = 0.4$, a shock of size 1 decays to 0.016 after 10 periods. With $\phi = 0.9$, it's still 0.349 after 10 periods.
- **Takeaway:** Higher AR coefficient = longer memory. This is why distinguishing $\phi = 0.4$ from $\phi = 0.9$ matters practically for forecasting horizons.

### Example 5: MA(1) Properties Derivation
- **Setup:** Derive mean, variance, and autocovariances of MA(1): $y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}$
- **Key finding:** $\gamma(1) = \theta\sigma^2$, but $\gamma(k) = 0$ for all $k \geq 2$. The ACF has exactly one nonzero value then cuts to zero.
- **Takeaway:** This sharp cutoff in the ACF is the signature of an MA(1) — the main identification tool.

### Example 6: ACF/PACF Pattern Recognition
- **Setup:** Given ACF and PACF plots, identify the underlying model
- **Key finding:** AR models show PACF cutoff (after lag p) with decaying ACF. MA models show ACF cutoff (after lag q) with decaying PACF. ARMA shows both decaying.
- **Takeaway:** This is the Box-Jenkins identification strategy — the first step before estimation.

## Connections
- **Builds on:** Week 3 concepts of ACF, PACF, stationarity, white noise, Wold theorem
- **Related to:** Problem Set 1, Question 3 (testing for serial correlation in BTC returns)
- **Prerequisite for:** Week 5+ model estimation, information criteria, forecast evaluation

## Questions to Consider
1. Why does differencing log GDP reduce autocorrelation so dramatically (0.99 → 0.26)?
2. If a regression coefficient is biased due to endogeneity, why can it still produce good forecasts?
3. When would you choose AR(2) over AR(1)? How would you decide?
4. Why can't we forecast a structural break? What can we do instead?
5. In your own work, when do you need causal interpretation vs just forecasting?
6. Why are MA processes always stationary but AR processes are not?
7. Given an ACF that cuts off after lag 2 and a PACF that decays, what model would you fit?
8. Why does invertibility matter for MA models? What goes wrong without it?
9. For an AR(1) with $\phi = 0.95$, how many periods until a shock decays to less than 10% of its original size?
10. Why does the ARMA-to-MA conversion (Wold representation) only work for stationary ARMA models?

## Review Checklist
- [ ] Understand what "cycles" capture (dynamics beyond trend and seasonality)
- [ ] Can interpret autocorrelation tables and explain persistence
- [ ] Know why differencing reduces persistence
- [ ] Understand why stationarity is required before modeling cycles
- [ ] Can articulate the difference between structural and time series models
- [ ] Understand the supply/demand simultaneity example
- [ ] Know when endogeneity matters (causal inference) vs when it doesn't (forecasting)
- [ ] Can explain why AR terms are the "best friends" for forecasting
- [ ] Can derive mean, variance, and ACF for MA(1) and AR(1)
- [ ] Know the ACF/PACF identification patterns for AR, MA, and ARMA
- [ ] Understand stationarity conditions for AR (roots outside unit circle)
- [ ] Understand invertibility conditions for MA ($|\theta| < 1$)
- [ ] Can explain what happens at the unit root ($\phi = 1$)
- [ ] Know the Box-Jenkins estimation procedure (identify → estimate → diagnose → forecast)
- [ ] Can convert AR(1) to MA($\infty$) representation
