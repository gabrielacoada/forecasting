# Answers for Exam (IMG_7507, IMG_7508, IMG_7509)

These answers correspond to the photographed exam pages (pages 2-4).

> **Note:** Pages 2-4 were photographed. Page 1 and pages beyond 4 are not shown.

---

## Question 1 (15 points) -- Dynamic Causal Effects

**Model:** ADL model for CPI inflation using monthly data (Jan 1990 - Dec 2024, T = 405 after lags):

$$\pi_t = \alpha + \beta_0 \Delta\text{oil}_t + \beta_1 \Delta\text{oil}_{t-1} + \beta_2 \Delta\text{oil}_{t-2} + \beta_3 \Delta\text{oil}_{t-3} + \delta \pi_{t-1} + \varepsilon_t$$

**Table 3 estimates:**

| Regressor       | Coefficient | Std. Error | t-statistic |
|-----------------|-------------|------------|-------------|
| Intercept       | 0.09        | 0.04       | 2.25        |
| $\Delta$oil_t   | 0.04        | 0.012      | 3.33        |
| $\Delta$oil_{t-1} | 0.03     | 0.012      | 2.50        |
| $\Delta$oil_{t-2} | 0.02     | 0.012      | 1.67        |
| $\Delta$oil_{t-3} | 0.01     | 0.011      | 0.91        |
| $\pi_{t-1}$     | 0.50        | 0.06       | 8.33        |

$R^2 = 0.36$, $DW = 2.02$, $T = 405$

---

### (i) Interpret $\hat{\beta}_0 = 0.04$

A 1 percentage point increase in the monthly log-change of WTI oil prices is associated with a **0.04 percentage point increase in monthly CPI inflation in the same month**, holding past oil price changes and lagged inflation constant.

The t-statistic (3.33) indicates this is statistically significant at the 1% level. The Durbin-Watson statistic of 2.02 is very close to 2, suggesting no significant serial correlation in the residuals.

---

### (ii) Dynamic Multipliers (Impulse Response) at h = 0, 1, 2

We want the total effect on $\pi_{t+h}$ of a one-unit shock to $\Delta\text{oil}_t$.

Let $m_h$ denote the dynamic multiplier at horizon $h$.

The key insight: the ADL model includes a lagged dependent variable ($\delta = 0.50$), so the effect of the oil shock propagates through two channels:
1. **Direct effect:** the $\beta_j$ coefficients (for $j \leq 3$)
2. **Indirect/feedback effect:** through $\delta \pi_{t-1}$

**Recursive formula:** $m_h = \beta_h + \delta \cdot m_{h-1}$, where $\beta_h = 0$ for $h > 3$.

**h = 0:**
$$m_0 = \beta_0 = 0.04$$

**h = 1:**
$$m_1 = \beta_1 + \delta \cdot m_0 = 0.03 + 0.50 \times 0.04 = 0.03 + 0.02 = \mathbf{0.05}$$

**h = 2:**
$$m_2 = \beta_2 + \delta \cdot m_1 = 0.02 + 0.50 \times 0.05 = 0.02 + 0.025 = \mathbf{0.045}$$

**Summary of dynamic multipliers:**

| Horizon h | Direct ($\beta_h$) | Feedback ($\delta \cdot m_{h-1}$) | Total ($m_h$) |
|-----------|--------------------|------------------------------------|----------------|
| 0         | 0.04               | --                                 | 0.040          |
| 1         | 0.03               | 0.020                              | 0.050          |
| 2         | 0.02               | 0.025                              | 0.045          |

The effect actually **increases** from h=0 to h=1 (the feedback from lagged inflation plus the direct lag effect exceeds the impact effect), then begins to decline at h=2. This hump-shaped pattern is typical of ADL models -- the lagged dependent variable propagates the shock beyond the direct lag effects.

**Cumulative multiplier through h=2:** $0.04 + 0.05 + 0.045 = 0.135$ percentage points total inflation from a 1 pp oil price shock over 3 months.

---

## Question 2 (15 points) -- Unit Root Testing

**Data:** Monthly log WTI crude oil price, $\text{oil}_t = \log(\text{WTI}_t)$, Jan 1990 - Dec 2024, $T = 420$.

**Table 1: ADF Tests for oil_t (log level)**

| Specification           | ADF $\tau$-stat | Lags (AIC) | 1% CV  | 5% CV  | 10% CV |
|-------------------------|-----------------|------------|--------|--------|--------|
| (A) Constant, no trend  | -1.97           | 2          | -3.45  | -2.87  | -2.57  |
| (B) Constant and trend  | -2.94           | 2          | -3.98  | -3.42  | -3.13  |

---

**Figure 1** (from page 4): Log WTI Crude Oil Price, Monthly Average (1990M1-2024M12). Source: FRED (series DCOILWTICO). The series shows large persistent swings without clear mean reversion -- consistent with a unit root.

**Table 2: ADF Test for $\Delta$oil_t (first difference of log oil, T = 419)**

| Specification           | ADF $\tau$-stat | Lags (AIC) | 1% CV  | 5% CV  | 10% CV |
|-------------------------|-----------------|------------|--------|--------|--------|
| (C) Constant, no trend  | -13.73          | 1          | -3.45  | -2.87  | -2.57  |

---

### (i) State the null and alternative hypotheses; write out the regression for Model (A)

**Hypotheses:**
- $H_0$: $\text{oil}_t$ has a unit root ($\rho = 1$, equivalently $\gamma = 0$ in the ADF regression)
- $H_1$: $\text{oil}_t$ is stationary ($|\rho| < 1$, equivalently $\gamma < 0$)

**ADF regression for Model (A) -- constant, no trend, with 2 lags (selected by AIC):**

$$\Delta\text{oil}_t = c + \gamma \cdot \text{oil}_{t-1} + \phi_1 \Delta\text{oil}_{t-1} + \phi_2 \Delta\text{oil}_{t-2} + u_t$$

where:
- $c$ is the constant (drift under $H_1$)
- $\gamma = \rho - 1$ is the coefficient of interest; under $H_0$: $\gamma = 0$
- The lagged differences ($\Delta\text{oil}_{t-1}, \Delta\text{oil}_{t-2}$) are included to absorb serial correlation in $u_t$
- The $\tau$-statistic is $\hat{\gamma}/\text{SE}(\hat{\gamma})$, tested against Dickey-Fuller critical values (not normal)

---

### ADF Test Results -- Full Interpretation

**Specification (A): Constant, no trend -- log level**
- $\tau = -1.97$, compare to CVs: $-1.97 > -2.57$ (10%)
- **Fail to reject $H_0$ at all significance levels.** Cannot reject unit root.

**Specification (B): Constant and trend -- log level**
- $\tau = -2.94$, compare to CVs: $-2.94 > -3.13$ (10%)
- **Fail to reject $H_0$ at all significance levels.** Cannot reject unit root even with a trend.

**Specification (C): Constant, no trend -- first difference**
- $\tau = -13.73$, compare to CVs: $-13.73 \ll -3.45$ (1%)
- **Strongly reject $H_0$ at the 1% level.** First differences are stationary.

### Overall Conclusion

- Tables 1A and 1B: log oil prices in **levels** have a unit root (fail to reject at all levels)
- Table 2C: **first differences** ($\Delta\text{oil}_t$) are clearly stationary ($\tau = -13.73$, massively significant)
- Therefore, $\text{oil}_t \sim I(1)$ -- log oil prices are **integrated of order 1**
- Oil price shocks have **permanent effects** on the price level
- For modeling/forecasting, use $\Delta\text{oil}_t$ (monthly log-returns), which is stationary
- This is consistent with Question 1 using $\Delta\text{oil}_t$ as the regressor rather than the log level

> **Note:** Sub-questions beyond (i) for Q2 may appear on pages not yet photographed.
