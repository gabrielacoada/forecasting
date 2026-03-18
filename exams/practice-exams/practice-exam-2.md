# Practice Exam 2 — ECON 522 Midterm

**Time: 1 hour 15 minutes | Closed book, calculator allowed | 50 points total**

---

## Question 1 (10 pts) — Autocovariance Derivation

You know that $y_t$ is given by the MA(2) process:

$$y_t = \varepsilon_t + 0.8\varepsilon_{t-1} + 0.2\varepsilon_{t-2} \qquad \varepsilon_t \sim WN(0, \sigma^2)$$

(a) (3 pts) Compute $\text{Var}(y_t)$.

(b) (3 pts) Compute $\gamma(1)$ and $\gamma(2)$.

(c) (2 pts) Compute $\gamma(3)$. Explain why it takes this value.

(d) (2 pts) Compute $\rho(1)$ and $\rho(2)$.

---

## Question 2 (8 pts) — ACF/PACF Identification

Examine the ACF and PACF of the residuals below.

**[See figure: `figures/exam2_acf_pacf.png`]**

(a) (5 pts) What model do these correlograms suggest? Explain by describing what you see in each plot and how this matches the theoretical ACF/PACF signatures.

(b) (3 pts) How many steps ahead can you forecast with this model beyond the unconditional mean? Why?

---

## Question 3 (10 pts) — Confidence Interval + Forecast Evaluation

You estimated a model to forecast quarterly GDP growth. You ran the Mincer-Zarnowitz regression on your out-of-sample forecast errors and got:

$$y_{t+1} = \beta_0 + \beta_1 \hat{y}_{t+1,t} + u_t$$

**Output** (n = 36 forecast periods):

| Variable | Coef. | Std. Err. | t | P>t |
|----------|-------|-----------|------|-------|
| forecast | 0.78 | 0.11 | 7.09 | 0.000 |
| _cons | 0.45 | 0.20 | 2.25 | 0.031 |

Sum squared resid (unrestricted): SSR_U = 8.42

Sum of squared raw forecast errors: $\sum(y_{t+1} - \hat{y}_{t+1,t})^2$ = SSR_R = 10.85

(a) (3 pts) Is there evidence that the forecast is biased? Test $\beta_0 = 0$.

(b) (3 pts) Is the forecast "too smooth"? Test $\beta_1 = 1$.

(c) (4 pts) Perform the joint F-test for forecast optimality. Show all steps. Is the forecast optimal?

---

## Question 4 (12 pts) — Forecasting from ARMA(1,1)

You estimated the following model for monthly inflation:

$$\pi_t = 0.15 + 0.72 \pi_{t-1} + \varepsilon_t + 0.35 \varepsilon_{t-1}$$

The last observation is at time T: $\pi_T = 2.8$, $\hat{\varepsilon}_T = 0.42$.

(a) (4 pts) Compute the 1-step ahead forecast $\hat{\pi}_{T+1,T}$. Write out the equation with variable names first.

(b) (4 pts) Compute the 2-step ahead forecast $\hat{\pi}_{T+2,T}$. Explain what happens to the MA component.

(c) (4 pts) Which forecast has a larger forecast error variance — 1-step or 2-step? Write down the formula for the 2-step error variance in terms of $\sigma^2$, $\phi$, and $\theta$. (You do not need to compute a number.)

---

## Question 5 (10 pts) — Unit Roots

(a) (5 pts) Explain briefly but clearly the difference between a deterministic trend and a stochastic trend in terms of:
   - (i) the effect of a shock (permanent or temporary?)
   - (ii) the forecast at long horizons
   - (iii) the correct transformation to achieve stationarity

(b) (5 pts) You run an ADF test on a series that fluctuates around a constant level (no visible trend). The output gives:

**Intercept only**: Test statistic = -3.15, 5% CV = -2.89, p-value = 0.023

Does the series have a unit root? Explain your reasoning. What would you do next — model in levels or take first differences?
