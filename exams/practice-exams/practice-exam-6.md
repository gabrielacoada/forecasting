# Practice Exam 6 — ECON 522 Midterm (Hardest)

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 55 points total**

*This exam is intentionally harder than expected — if you can do this one, you're ready.*

---

## Question 1 (10 pts) — Autocovariance: ARMA(1,1)

Consider the ARMA(1,1) process:

$$y_t = 0.8 y_{t-1} + \varepsilon_t + 0.5\varepsilon_{t-1} \qquad \varepsilon_t \sim WN(0, \sigma^2)$$

(a) (4 pts) Compute $\text{Var}(y_t) = \gamma(0)$ in terms of $\sigma^2$.

*Hint*: Use $\gamma(0) = \phi\gamma(1) + \sigma^2 + \theta\sigma^2$ and $\gamma(1) = \phi\gamma(0) + \theta\sigma^2$ to solve simultaneously.

(b) (3 pts) Compute $\gamma(1)$ in terms of $\sigma^2$.

(c) (3 pts) Compute $\rho(1)$. Is it larger or smaller than $\phi = 0.8$? Why does the MA component affect $\rho(1)$?

---

## Question 2 (8 pts) — ACF/PACF Identification

**[See figure: `figures/exam6_acf_pacf.png`]**

(a) (5 pts) What model do these correlograms suggest? Explain. (Hint: when BOTH the ACF and PACF decay gradually without a sharp cutoff, what does that indicate?)

(b) (3 pts) Would an AR(1) be a reasonable approximation for this process? Why or why not?

---

## Question 3 (12 pts) — Full Forecasting + Forecast Evaluation Combo

You estimated an AR(1) model: $y_t = 1.2 + 0.65 y_{t-1} + \varepsilon_t$ with $\hat{\sigma}^2 = 4.0$.

The last observation: $y_T = 8.0$.

**(Part A: Forecast)**

(a) (3 pts) Compute $\hat{y}_{T+1,T}$ and $\hat{y}_{T+2,T}$.

(b) (3 pts) Compute the 95% forecast interval for $\hat{y}_{T+1,T}$. (Use $\sigma = 2.0$.)

**(Part B: Evaluation)**

After collecting actual data, you find: $y_{T+1} = 7.2$, $y_{T+2} = 6.8$.

(c) (2 pts) Compute the 1-step and 2-step forecast errors.

(d) (4 pts) Suppose over 20 forecast periods you computed the Mincer-Zarnowitz regression and got:

$y_{t+1} = 0.95 + 0.82 \hat{y}_{t+1,t} + u_t$, with SE($\hat{\beta}_0$) = 0.60, SE($\hat{\beta}_1$) = 0.10

Test individually whether $\beta_0 = 0$ and $\beta_1 = 1$. What do your results suggest about the forecast?

---

## Question 4 (10 pts) — Structural Break + Seasonality

You model quarterly electricity demand (LKWH) as a function of price, income, weather, trend, and seasonal dummies:

$$\text{LKWH}_t = \beta_0 + \beta_1 \text{TREND} + \beta_2 \text{DBROKEN} + \beta_3 \text{TDBROKEN} + \delta_1 D_1 + \delta_2 D_2 + \delta_3 D_3 + u_t$$

where $D_1, D_2, D_3$ are dummies for Q1, Q2, Q3 (Q4 is the base).

**Output:**

| Variable | Coef. | Std. Err. | t | P>t |
|----------|-------|-----------|------|-------|
| TREND | 0.0042 | 0.0008 | 5.25 | 0.000 |
| DBROKEN | 0.142 | 0.024 | 5.92 | 0.000 |
| TDBROKEN | -0.0059 | 0.0008 | -7.38 | 0.000 |
| D1 | 0.041 | 0.014 | 2.93 | 0.004 |
| D2 | -0.099 | 0.011 | -9.00 | 0.000 |
| D3 | -0.042 | 0.011 | -3.82 | 0.000 |
| _cons | 0.562 | 0.132 | 4.26 | 0.000 |

(a) (3 pts) What is the trend slope before the break and after the break?

(b) (3 pts) How do you interpret $D_1 = 0.041$? What does it mean relative to Q4?

(c) (4 pts) Suppose you want to test whether Q2 and Q3 have the same seasonal effect (i.e., $\delta_2 = \delta_3$). You can't compute the F-test without the restricted output, but explain in detail: what would the restricted model look like? What would $q$ be? What would you compare?

---

## Question 5 (15 pts) — Unit Root Comprehensive

(a) (5 pts) Consider two models for real GDP:

**Model A (Trend Stationary):** $y_t = 2.0 + 0.03t + u_t$ where $u_t$ is stationary AR(1)

**Model B (Unit Root with Drift):** $\Delta y_t = 0.03 + \varepsilon_t$

Both models produce data that looks very similar (upward trend). Explain three specific ways in which they have different implications for:
(i) The effect of a recession shock (permanent vs temporary)
(ii) Your forecast 20 years from now
(iii) How you should achieve stationarity

(b) (5 pts) You run two tests on real GDP:

- ADF (H0: unit root): test stat = -2.10, 5% CV = -3.44, p = 0.54
- KPSS (H0: stationary): test stat = 0.85, 5% CV = 0.46

Both tests use the specification with trend. What does each test conclude? Do they agree? What should you do when the two tests conflict?

(c) (5 pts) Your colleague differenced GDP and now wants to fit an ARMA model to $\Delta\text{GDP}_t$. She finds the ACF of $\Delta\text{GDP}$ has a significant spike at lag 1 and nothing else. She says "it's MA(1)." Is she right? If GDP really IS a unit root process, is this consistent? If GDP is actually trend stationary and she over-differenced, what would the MA coefficient look like? (Hint: think about what over-differencing introduces.)
