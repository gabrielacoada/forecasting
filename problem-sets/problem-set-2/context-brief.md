# Context Brief: Problem Set 2

## Source Materials
- Week 1: Metrics Review (OLS, inference, bridge to time series)
- Week 3: Univariate Time Series Introduction (ACF, PACF, stationarity, Wold theorem)
- Week 4: Cycles Modeling & ARMA Models (AR/MA properties, identification, estimation)
- Week 5: Dynamic Causal Effects (distributed lags, HAC standard errors, multipliers)

---

## Problem 1: Show y_t = x_t + e_t with AR(1) signal is ARMA(1,1)

### Relevant Lecture Concepts

**Wold Representation Theorem (Week 3):**
Any zero-mean covariance-stationary process can be written as an infinite MA: $Y_t = \sum_{j=0}^{\infty} \psi_j \varepsilon_{t-j} + k_t$. In practice we approximate with finite ARMA models.

**AR-to-MA conversion (Week 4):**
Pesavento derives this step by step: "I substitute $y_{t-1} = \rho y_{t-2} + \varepsilon_{t-1}$ and keep going forever... What is this? It's a moving average of infinite order." If $|\rho| < 1$: $(1-\rho L)^{-1} = \sum_{j=0}^{\infty} \rho^j L^j$.

**Lag operator (Week 3):**
$Ly_t = y_{t-1}$, polynomial notation $a(L)y_t$, inversion requires roots inside unit circle.

**MA autocovariance cutoff (Week 4):**
"Every time I have an expectation of a product and the two things have a different timing, that's going to be zero if this is a white noise." MA(1) has $\gamma(k) = 0$ for $k \geq 2$ — sharp cutoff is the signature of MA.

### Professor's Framework
The proof should show: (1) substitute the AR(1) equation, (2) use lag to eliminate the unobservable $x_{t-1}$, (3) verify the composite noise has MA(1) autocovariance structure, (4) invoke Wold theorem. The professor values seeing the autocovariance derivation step by step — "the math is important to understand where they come from."

---

## Problem 2: ACF vs PACF — positive ACF, negative PACF

### Relevant Lecture Concepts

**ACF vs PACF distinction (Week 3, from annotation):**
"ACF = total correlation (like simple regression coefficient); PACF = partial correlation (like multiple regression coefficient). Two different types of correlation."

**PACF definition (Week 3):**
$p(s)$ is the coefficient of $y_{t-s}$ in a population regression of $y_t$ on $y_{t-1}, y_{t-2}, \ldots, y_{t-s}$. "Measures correlation at lag $s$ after controlling for intermediate lags."

**ACF/PACF identification table (Week 4):**

| Model | ACF | PACF |
|-------|-----|------|
| AR(p) | Decays (exponential or oscillating) | Cuts off after lag p |
| MA(q) | Cuts off after lag q | Decays |
| ARMA(p,q) | Decays | Decays |

"Critical distinction: 'Cuts off' means drops to zero sharply. 'Decays' means gradually diminishes."

**AR(2) and oscillation (Week 4):**
Pesavento discusses AR(2): when $\phi_2 < 0$, ACF can oscillate. The PACF cuts off after lag 2 with $\phi_{22} = \phi_2$.

### Professor's Framework
The answer should distinguish "total" vs "partial" (or "direct") correlation. The mechanism for positive ACF with negative PACF is indirect effects through intermediate lags — exactly like omitted variable bias in OLS, where the simple regression coefficient differs from the multiple regression coefficient.

---

## Problem 3: Oil Prices and GDP Growth (Distributed Lag)

### Relevant Lecture Concepts

**Distributed Lag Model (Week 5):**
$Y_t = \beta_0 + \beta_1 X_t + \beta_2 X_{t-1} + \ldots + \beta_{r+1} X_{t-r} + u_t$

**Coefficient interpretation (Week 5, heavy annotation):**
- $\beta_1$ = **impact effect** (contemporaneous)
- $\beta_2, \beta_3, \ldots$ = **dynamic multipliers** (effect at lag 1, 2, ...)
- $\sum_{j=1}^{k+1} \beta_j$ = **cumulative dynamic multiplier** (total effect through period $k$)

**Dynamic vs cumulative multiplier (Week 5, board note page 31):**
"If your left-hand variable is the first difference, the coefficients give you the dynamic multiplier on the first difference. If you want the effect on the level, you need the cumulative multiplier." In Problem 3, $Y_t$ is quarterly GDP growth (a level, not a difference), so the coefficients are directly the dynamic multipliers on growth, and their sum is the cumulative effect on growth.

**Confidence intervals (Week 5):**
"If the confidence interval contains zero, that effect is not statistically different than zero." 95% CI: $\hat{\beta}_j \pm 1.96 \times SE(\hat{\beta}_j)$.

**HAC F-test (Week 5):**
Joint test of all coefficients. The HAC version accounts for serial correlation and heteroskedasticity. If $F > F_{critical}$, reject the null that all coefficients are zero.

**Exogeneity of oil prices (Week 5):**
Oil prices are one of the examples discussed: "Isolate price changes caused by Middle East wars (truly exogenous geopolitical events)." Hamilton's measure $O_t$ = max(0, oil price minus past-year maximum) is specifically designed to capture exogenous oil supply shocks, similar to the "creating exogenous measures" approach Pesavento describes.

**HAC standard errors (Week 5):**
Pesavento: "The cost of using HAC is very little, and it protects you against the possibility of serial correlation and also heteroskedasticity. It's a good habit, in my opinion, to always use HAC regardless." The regression uses HAC standard errors because in a distributed lag model, errors are likely serially correlated.

### Professor's Framework
For 3(a)-(b): multiply each coefficient by the shock size (25) to get dynamic multipliers; CI = effect $\pm$ 1.96 $\times$ SE(effect). For 3(c): sum the effects — this is the cumulative multiplier. For 3(d): compare the HAC F-statistic to the critical value for joint significance. The interpretation should use "impact effect," "dynamic multiplier," and "cumulative multiplier" terminology from Week 5.

---

## Problem 4: PNFIC1 ARMA Analysis

### Relevant Lecture Concepts

**Growth rate transformation (Week 3):**
$q_t = 100(\Delta y_t / y_{t-1}) \approx 100[\log(y_t) - \log(y_{t-1})]$. "Log transformations flatten exponential growth."

**Model selection — Pesavento's practical recipe (Week 4, heavy emphasis):**
1. Make data stationary (remove trend/seasonality)
2. Plot the correlogram
3. Use ACF/PACF as starting point
4. **"Start LARGE, eliminate small"** — "The ideal way to go is from large to small, rather than small to large. Always add a few extra lags if you're unsure, and then eliminate."
5. Estimate and check significance
6. Compare with information criteria — "the smaller the better"
7. **Plot correlogram of residuals** — "The most important thing"
8. Iterate

**AIC/BIC (Week 4):**
"If it's marginally significant, what do you do? Here's where the information criteria comes to help. Remember, the smaller the better." BIC penalizes more heavily than AIC, so BIC tends to select more parsimonious models.

**AR estimation (Week 4):**
"AR is estimated by simply ordinary OLS." For MA, "you need nonlinear maximization of the likelihood."

**Why AR is preferred (Week 4):**
"People don't tend to like moving average more... because AR is easy to interpret, easy to forecast with." "The three real variables I had — they were basically all AR. That's probably reality."

**Impulse response / dynamic multiplier (Week 4):**
"Suppose I have a shock today equal to 1, and $y_{t-1} = 0$. What is $y_t$? It's 1. What is $y_{t+1}$? $\rho$. What is $y_{t+2}$? $\rho^2$." For AR(1), the IRF is $\rho^j$. For AR(p), compute recursively using the AR coefficients.

**Persistence (Week 4):**
$\rho = 0.5$: "maybe in a year it's going to be irrelevant." $\rho = 0.9$: "going to be like 15-20 quarters before it's irrelevant." The sum of AR coefficients measures overall persistence.

**Stationarity conditions (Week 4):**
"All roots of the characteristic polynomial must lie outside the unit circle." For AR(2): "Now instead of having one value that needs to be less than one, I have two values... It's more complicated because the root is $1/\rho$. So you'll see 'the roots are outside the unit circle,' which is doubly confusing."

**HC vs HAC standard errors (Week 1 + Week 5):**
- HC0 (heteroscedasticity-consistent): corrects for non-constant variance only
- HAC / Newey-West: corrects for both heteroscedasticity AND serial correlation
- Week 5: "For AR models with enough lags, HAC SEs are usually unnecessary because the errors become serially uncorrelated by construction." But always compare.
- Pesavento: "If there's any doubt, use HAC."

**Coefficient interpretation (Week 1):**
"When I look at this number, 2.86, I cannot just look at it in isolation. In isolation it means nothing. Is 2.86 big, small, relevant, not relevant? I don't know — unless I know how variable it is."

### Professor's Framework
For 4(a): standard log growth transformation. For 4(b): follow the practical recipe — ACF/PACF → start large → eliminate → compare AIC/BIC → check residuals. Note that AR(1) winning is consistent with Pesavento's observation that "most things need at least AR(1), maybe not more." For 4(c)-(d): present both HC and Newey-West side by side; note that for AR models with sufficient lags, the difference should be small (if it's large, there may be remaining serial correlation). For 4(e): interpret each coefficient economically and discuss persistence via the sum. For 4(f): the IRF shows how a unit shock propagates — connect to Pesavento's dynamic multiplier interpretation.

---

## Key Terminology to Use

| Pesavento's Term | Context |
|-----------------|---------|
| "impact effect" | Contemporaneous coefficient in distributed lag |
| "dynamic multiplier" | Effect at each lag; also = impulse response |
| "cumulative multiplier" | Sum of coefficients through a given lag |
| "cuts off" vs "decays" | ACF/PACF pattern for model identification |
| "start large, eliminate small" | Model selection philosophy |
| "the smaller the better" | Information criteria comparison |
| "exploit serial correlation" | Why we use AR models — it's a feature, not a bug |
| "plot the residual correlogram" | Primary diagnostic check |
| "roots outside the unit circle" | Stationarity condition |
| HAC / Newey-West | Default robust standard errors in time series |
| "I don't care about bias, only forecasting" | Course philosophy (relevant to P4 interpretation) |
