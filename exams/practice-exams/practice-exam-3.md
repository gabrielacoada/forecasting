# Practice Exam 3 — ECON 522 Midterm

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 50 points total**

---

## Question 1 (10 pts) — Regression Interpretation + Structural Break

You are studying quarterly retail SALES (in millions) from 1990:Q1 to 2024:Q4 (n = 140). You suspect a structural break at 2008:Q1 (the financial crisis). You construct:
- TREND = 1, 2, 3, ..., 140
- DBROKEN = 0 before 2008:Q1, 1 after
- TDBROKEN = TREND $\times$ DBROKEN

**Unrestricted Model** (with break):

| Source | SS | df | MS |
|--------|------|-----|------|
| Residual | 3245.8 | 136 | 23.87 |

| SALES | Coef. | Std. Err. | t | P>t |
|-------|-------|-----------|------|-------|
| TREND | 1.85 | 0.22 | 8.41 | 0.000 |
| DBROKEN | -12.40 | 5.60 | -2.21 | 0.029 |
| TDBROKEN | -0.45 | 0.28 | -1.61 | 0.110 |
| _cons | 42.30 | 3.10 | 13.65 | 0.000 |

**Restricted Model** (no break — drops DBROKEN and TDBROKEN):

| Source | SS | df | MS |
|--------|------|-----|------|
| Residual | 4180.2 | 138 | 30.29 |

| SALES | Coef. | Std. Err. | t | P>t |
|-------|-------|-----------|------|-------|
| TREND | 1.42 | 0.18 | 7.89 | 0.000 |
| _cons | 48.50 | 2.80 | 17.32 | 0.000 |

(a) (3 pts) What is the estimated trend slope BEFORE the break? What is it AFTER? Show how you get the "after" slope.

(b) (4 pts) Test the joint significance of DBROKEN and TDBROKEN using an F-test. Is there evidence of a structural break?

(c) (3 pts) DBROKEN is individually significant but TDBROKEN is not. What does this tell you about the nature of the break — is it a level shift, a slope change, or both?

---

## Question 2 (8 pts) — ACF/PACF Identification

**[See figure: `figures/exam3_acf_pacf.png`]**

(a) (5 pts) What ARMA model do these correlograms suggest for the residuals? Justify.

(b) (3 pts) You also have an AIC/BIC table from several candidate models:

| Model | AIC | BIC |
|-------|-----|-----|
| AR(1) | 245.3 | 249.1 |
| AR(2) | 238.7 | 245.2 |
| AR(3) | 239.1 | 248.4 |
| MA(1) | 262.1 | 265.9 |
| ARMA(1,1) | 240.2 | 246.8 |

Which model do you select? Does it agree with your answer in (a)?

---

## Question 3 (12 pts) — Forecasting by Hand from AR(1)

You estimated the following model for detrended log GDP:

$$y_t = 0.35 + 0.82 y_{t-1} + \varepsilon_t$$

The last two observations are: $y_T = 3.60$, $y_{T-1} = 3.45$.

(a) (4 pts) Compute $\hat{y}_{T+1,T}$ (1-step ahead).

(b) (4 pts) Compute $\hat{y}_{T+2,T}$ (2-step ahead).

(c) (4 pts) What is the unconditional mean $\mu$ of this process? As $h \to \infty$, what does the forecast converge to? Show the formula.

---

## Question 4 (10 pts) — Forecast Error Properties

(a) (3 pts) List three properties that optimal forecast errors should satisfy.

(b) (3 pts) Your 1-step ahead forecast errors from an AR(1) model are: {0.8, -1.2, 0.5, 1.4, -0.3, -0.9, 0.7, -0.5}. Compute the forecast bias and MSE.

(c) (4 pts) You want to test whether your forecast is optimal using the Mincer-Zarnowitz regression. Write down the regression equation, state the null hypothesis, and explain what it means if you reject.

---

## Question 5 (10 pts) — Unit Root: Random Walk Properties

Consider the random walk: $y_t = y_{t-1} + \varepsilon_t$, with $\varepsilon_t \sim WN(0, 4)$ and $y_0 = 0$.

(a) (3 pts) Write $y_t$ using back-substitution. What is $E(y_t)$ and $\text{Var}(y_t)$?

(b) (3 pts) Compute $\text{Var}(y_{50})$ and $\text{Var}(y_{200})$. Why does the variance changing over time violate stationarity?

(c) (4 pts) You want to forecast $y_{T+h}$ where $T = 100$, $y_{100} = 15$. What is your best forecast for any horizon $h$? What is the forecast error variance at $h = 10$? Compare this to a stationary AR(1) with $\rho = 0.8$ — which has larger forecast uncertainty at $h = 10$?
