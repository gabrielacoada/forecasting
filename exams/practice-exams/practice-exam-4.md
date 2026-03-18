# Practice Exam 4 — ECON 522 Midterm

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 50 points total**

---

## Question 1 (12 pts) — Autocovariance: AR(1)

Consider the AR(1) process:

$$y_t = 0.7 y_{t-1} + \varepsilon_t \qquad \varepsilon_t \sim WN(0, \sigma^2)$$

(a) (3 pts) Compute $\text{Var}(y_t) = \gamma(0)$ in terms of $\sigma^2$.

(b) (3 pts) Compute $\gamma(1)$ and $\gamma(2)$ in terms of $\sigma^2$.

(c) (3 pts) Compute $\rho(1)$ and $\rho(2)$. What pattern do you see?

(d) (3 pts) A shock of size 1 hits at time $t$. What is the effect on $y_{t+1}$, $y_{t+2}$, and $y_{t+5}$? Does the shock ever fully disappear? What is this called?

---

## Question 2 (8 pts) — ACF/PACF + Model Selection

**[See figure: `figures/exam4_acf_pacf.png`]**

(a) (5 pts) What model do these correlograms suggest? Explain by describing what you see in the ACF and PACF separately.

(b) (3 pts) If you were to forecast from this model, how many steps ahead could you forecast beyond the unconditional mean? After that, what is the forecast?

---

## Question 3 (10 pts) — Confidence Interval + Serial Correlation

You estimate a regression of WAGE on EDUCATION and EXPERIENCE. The output shows:

| WAGE | Coef. | Std. Err. | t | P>t | [95% CI] |
|------|-------|-----------|------|-------|----------|
| EDUC | 2.45 | 0.38 | 6.45 | 0.000 | [1.70, 3.20] |
| EXPER | 0.52 | 0.12 | 4.33 | 0.000 | [0.28, 0.76] |
| _cons | 8.30 | 1.95 | 4.26 | 0.000 | [4.44, 12.16] |

$n = 120$, $R^2 = 0.45$, Root MSE = 4.82, DW = 0.85

(a) (3 pts) A worker has 4 more years of education than another, holding experience constant. Construct a 95% CI for the wage difference.

(b) (4 pts) The Durbin-Watson statistic is 0.85. What does this suggest? How does this affect your confidence in the CI from part (a)?

(c) (3 pts) If DW indicates serial correlation, what would you do to fix it? Name one specific approach.

---

## Question 4 (10 pts) — Forecasting by Hand: AR(2) with Exogenous Variable

You estimated:

$$\text{RENT}_t = 85.2 + 0.42 \cdot \text{INCOME}_t + 0.55 \cdot \text{RENT}_{t-1} + 0.20 \cdot \text{RENT}_{t-2} + \varepsilon_t$$

| Quarter | RENT | INCOME |
|---------|------|--------|
| 2024:Q3 | 1420 | 3200 |
| 2024:Q4 | 1480 | 3350 |
| 2025:Q1 | — | 3400 |
| 2025:Q2 | — | 3500 |

(a) (5 pts) Compute the 1-step ahead forecast for 2025:Q1. Write the equation with variable names before plugging in.

(b) (5 pts) Compute the 2-step ahead forecast for 2025:Q2. Clearly label which values are observed vs forecasted.

---

## Question 5 (10 pts) — Dickey-Fuller Interpretation

You have two variables: CPI (price level) and INFLATION (percentage change in CPI).

(a) (3 pts) Without running any test, which variable do you expect to have a unit root? Why?

(b) (4 pts) You run an ADF test on CPI (with trend):
- Test statistic: -1.12
- 5% Critical Value: -3.44
- p-value: 0.72

And on INFLATION (intercept only):
- Test statistic: -3.85
- 5% Critical Value: -2.88
- p-value: 0.002

Interpret both results.

(c) (3 pts) Based on these results, if you wanted to build a forecasting model, should you use CPI in levels or first differences? What about INFLATION?
