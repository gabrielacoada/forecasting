# Practice Exam 1 — ECON 522 Midterm

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 50 points total**

---

## Question 1 (12 pts) — Autocovariance Derivation

You know that $y_t$ is given by the MA(1) process:

$$y_t = \varepsilon_t + 0.6\varepsilon_{t-1} \qquad \varepsilon_t \sim WN(0, \sigma^2)$$

Compute the following:

(a) (4 pts) $\text{Var}(y_t)$

(b) (4 pts) $\gamma(1)$

(c) (2 pts) $\gamma(2)$

(d) (2 pts) $\rho(1)$

---

## Question 2 (8 pts) — ACF/PACF Identification

Look at the ACF and PACF of the residuals from a regression below.

**[See figure: `figures/exam1_acf_pacf.png`]**

(a) (5 pts) Based on the ACF and PACF, which model (AR, MA, or ARMA) would you suggest for these residuals? What order? Explain your reasoning by referencing specific features of both plots.

(b) (3 pts) If you chose an AR(p) model, what is the value of p? If MA(q), what is q? Justify.

---

## Question 3 (10 pts) — F-Test for Joint Significance

You are studying the effect of advertising spending (ADSPEND) on quarterly sales (SALES). You estimated two models:

**Restricted Model** (no lags):

| Source | SS | df | MS |
|--------|-----|-----|-----|
| Model | 2450.3 | 1 | 2450.3 |
| Residual | 1820.6 | 78 | 23.34 |
| Total | 4270.9 | 79 | |

| SALES | Coef. | Std. Err. | t | P>t |
|-------|-------|-----------|------|-------|
| ADSPEND | 0.342 | 0.048 | 7.13 | 0.000 |
| _cons | 15.20 | 2.31 | 6.58 | 0.000 |

**Unrestricted Model** (with 2 lags of SALES):

| Source | SS | df | MS |
|--------|-----|-----|-----|
| Model | 3680.1 | 3 | 1226.7 |
| Residual | 590.8 | 76 | 7.77 |
| Total | 4270.9 | 79 | |

| SALES | Coef. | Std. Err. | t | P>t |
|-------|-------|-----------|------|-------|
| ADSPEND | 0.085 | 0.052 | 1.63 | 0.107 |
| L1. SALES | 0.612 | 0.098 | 6.24 | 0.000 |
| L2. SALES | 0.245 | 0.101 | 2.43 | 0.018 |
| _cons | 3.45 | 1.85 | 1.86 | 0.066 |

(a) (7 pts) Test the joint significance of the two lags (L1 and L2). Show all steps.

(b) (3 pts) What happened to the coefficient on ADSPEND when you added the lags? Explain economically why this makes sense.

---

## Question 4 (12 pts) — Forecasting by Hand

Using the unrestricted model from Q3, compute the 1-step and 2-step ahead forecast.

**The model**: $\text{SALES}_t = 3.45 + 0.085 \cdot \text{ADSPEND}_t + 0.612 \cdot \text{SALES}_{t-1} + 0.245 \cdot \text{SALES}_{t-2} + \varepsilon_t$

**Data:**

| Quarter | SALES | ADSPEND |
|---------|-------|---------|
| 2024:Q3 | 48.2 | 12.5 |
| 2024:Q4 | 51.7 | 13.1 |
| 2025:Q1 | — | 14.0 |
| 2025:Q2 | — | 13.5 |

(a) (6 pts) Compute $\hat{y}_{2025:Q1}$ (1-step ahead). Show the equation with variable names before plugging in numbers.

(b) (6 pts) Compute $\hat{y}_{2025:Q2}$ (2-step ahead). Clearly indicate which values are actual and which are forecasts.

---

## Question 5 (8 pts) — Unit Root Concepts

(a) (4 pts) You are given the following Dickey-Fuller test output for a variable that shows an upward trend:

**With trend**: Test statistic = -2.45, 5% Critical Value = -3.44, p-value = 0.35

Interpret this result. Does the data have a unit root? What should you do next?

(b) (4 pts) Your colleague says: "The data has a trend, so I'll just detrend it by regressing on TIME and using the residuals." Under what condition is this correct? Under what condition would this be wrong?
