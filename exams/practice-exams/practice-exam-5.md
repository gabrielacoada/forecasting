# Practice Exam 5 — ECON 522 Midterm

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 50 points total**

---

## Question 1 (10 pts) — Unit Root: ACF/PACF + DF Test

You observe a quarterly time series $y_t$ (200 observations). The time series plot and ACF/PACF are shown below.

**[See figure: `figures/exam5_series.png`]** — time series plot of $y_t$
**[See figure: `figures/exam5_acf_pacf.png`]** — ACF and PACF of $y_t$

(a) (3 pts) Describe what you see in the time series plot and the ACF. Does this look stationary? Why or why not?

(b) (3 pts) You run an ADF test (intercept only, since no obvious trend):

Test statistic = -1.78, 5% CV = -2.88, p-value = 0.39

Does the data have a unit root? Explain.

(c) (4 pts) If the series has a unit root, what transformation should you apply? After applying it, what kind of model (AR, MA, ARMA) would you fit to the transformed data? Would you expect the ACF of $\Delta y_t$ to look different from the ACF of $y_t$?

---

## Question 2 (12 pts) — Autocovariance: MA(2)

Given the process:

$$y_t = 3 + \varepsilon_t - 0.5\varepsilon_{t-1} + 0.4\varepsilon_{t-2} \qquad \varepsilon_t \sim WN(0, 9)$$

Note: $\sigma^2 = 9$.

(a) (2 pts) What is $E(y_t)$?

(b) (4 pts) Compute $\text{Var}(y_t)$. Plug in $\sigma^2 = 9$ to get a number.

(c) (4 pts) Compute $\gamma(1)$ and $\gamma(2)$. Plug in $\sigma^2 = 9$.

(d) (2 pts) Compute $\rho(1)$.

---

## Question 3 (8 pts) — Loss Functions and Forecast Properties

(a) (4 pts) Name the three loss functions covered in class. For each one, state what the optimal forecast is (conditional mean, median, or quantile).

(b) (4 pts) You are forecasting demand for a perishable product. Under-predicting means you run out of stock and lose sales (very costly). Over-predicting means you have unsold inventory (less costly). Which loss function is most appropriate? Should your forecast be biased? If so, in which direction?

---

## Question 4 (10 pts) — Comparing Two Models: RMSE and Diebold-Mariano

You compared two models for forecasting monthly unemployment:

| Model | RMSE | MAE |
|-------|------|-----|
| AR(2) | 0.342 | 0.271 |
| AR(4) | 0.318 | 0.258 |

The Diebold-Mariano test gives: DM = 1.45, p-value = 0.153.

(a) (3 pts) Based on RMSE and MAE alone, which model appears better?

(b) (4 pts) Based on the DM test, can you conclude that AR(4) is significantly better? Explain what the DM test is testing and why you can't just compare raw RMSEs.

(c) (3 pts) Given the DM result, which model would you choose for forecasting? Consider the trade-off between accuracy and parsimony (number of parameters).

---

## Question 5 (10 pts) — Forecasting from MA(2) + Residual Table

You estimated an MA(2) model for detrended quarterly housing starts:

$$y_t = 2.1 + \varepsilon_t + 0.7\varepsilon_{t-1} - 0.3\varepsilon_{t-2}$$

From the residual table, the last three residuals are:
- $\hat{\varepsilon}_T = 1.5$
- $\hat{\varepsilon}_{T-1} = -0.8$

(a) (4 pts) Compute $\hat{y}_{T+1,T}$ (1-step ahead). Show the equation first.

(b) (3 pts) Compute $\hat{y}_{T+2,T}$ (2-step ahead).

(c) (3 pts) Compute $\hat{y}_{T+3,T}$ (3-step ahead). Why does the forecast take this value?
