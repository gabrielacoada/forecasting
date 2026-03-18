# ECON 422 — FINAL (Fall 2002) — Reproduced with Solutions

**Rules**: 12 pages, 2.5 hours, closed book, calculator allowed. Explain each step for full credit.

---

## Context (for Q1)

**Q1.** As you probably know there has been a lot of discussion about electricity demand in California. In this problem we are trying to explain the electricity consumption, as measured in kilowatt-hours per residential customer in San Diego County. We are particularly interested in estimating the income and price elasticities of demand for electricity, studying whether there has been any structural change (break in the trend) and predicting the demand for 1993. The data are quarterly data from 1972:2 to 1992:4.

- **KWH** = Electricity sales per residential customers
- **PRICE** = Average price for the single-family rate tariff in real terms (i.e. adjusted by inflation)
- **Y** = San Diego County total per-capita income in current terms
- **CDD** = Cooling degree days (average number of days in the quarter when the temperature was over 65)
- **HDD** = Heating degree days (average number of days in the quarter when the temperature was less than 65)

Since we are interested in elasticities, data is transformed by taking the natural logarithm. The basic model is (LKWH is the log of KWH, LY is the log of Y, and LPRICE is the log of PRICE).

---

## Q1(a) (5 pts) — Income and Price Elasticities

**Basic regression output:**

Dependent Variable: LKWH | Sample: 1972:2 to 1992:4 | n = 83

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.435988 | 0.225173 | 1.936239 | 0.0565 |
| LY | -0.060167 | 0.158404 | -0.379830 | 0.7051 |
| LPRICE | -0.097068 | 0.029198 | -3.324449 | 0.0014 |
| CDD | 0.000262 | 3.53E-05 | 7.438805 | 0.0000 |
| HDD | 0.000360 | 3.09E-05 | 11.62252 | 0.0000 |

| Statistic | Value | | Statistic | Value |
|-----------|-------|--|-----------|-------|
| R-squared | 0.663915 | | Mean dep var | 0.327688 |
| Adj R-squared | 0.646680 | | S.D. dep var | 0.081208 |
| S.E. of regression | 0.048270 | | AIC | -3.165648 |
| Sum squared resid | 0.181742 | | Schwarz | -3.019935 |
| Log likelihood | 136.3744 | | F-statistic | 38.52102 |
| Durbin-Watson | 1.196531 | | Prob(F) | 0.000000 |

**Question**: What are the income and price elasticities of demand for electricity? Do the signs coincide with your economic intuition?

---

The graph of LKWH also suggests the presence of a linear trend. The equation was re-estimated including a trend. At the same time, during the period before 1979 the price of crude oil escalated dramatically and conservation became an important issue for reducing demand. Buildings were better insulated, more energy-efficient appliances and machinery were built and automobiles became more fuel-efficient. One may therefore expect that there is a break in trend in 1979.

- **DBROKEN** = 0 before 1979:1, 1 after
- **TDBROKEN** = TREND $\times$ DBROKEN

## Q1(b) (10 pts) — Broken Trend Test

**Two regression outputs side by side:**

**LEFT — Unrestricted (with break):**

Dep Var: LKWH | n = 83

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.460403 | 0.202617 | 2.272285 | 0.0259 |
| DBROKEN | 0.158074 | 0.036955 | 4.277478 | 0.0001 |
| TREND | 0.004933 | 0.001145 | 4.309615 | 0.0000 |
| TDBROKEN | -0.006643 | 0.001280 | -5.188350 | 0.0000 |
| LY | 0.009295 | 0.149914 | 0.062002 | 0.9507 |
| LPRICE | -0.177869 | 0.034805 | -5.110525 | 0.0000 |
| CDD | 0.000260 | 2.93E-05 | 8.859899 | 0.0000 |
| HDD | 0.000357 | 2.57E-05 | 13.87170 | 0.0000 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.776938 |
| Adj R-squared | 0.756118 |
| S.E. of regression | 0.040104 |
| Sum squared resid | 0.120624 |
| DW | 1.789111 |

**RIGHT — Restricted (no break, no DBROKEN/TDBROKEN):**

Dep Var: LKWH | n = 83

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.280999 | 0.221801 | 1.266896 | 0.2090 |
| TREND | -0.000646 | 0.000223 | -2.893065 | 0.0050 |
| LY | 0.045459 | 0.155752 | 0.291869 | 0.7712 |
| LPRICE | -0.073426 | 0.029081 | -2.524867 | 0.0136 |
| CDD | 0.000262 | 3.37E-05 | 7.781580 | 0.0000 |
| HDD | 0.000357 | 2.96E-05 | 12.07104 | 0.0000 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.696865 |
| Adj R-squared | 0.677181 |
| S.E. of regression | 0.046140 |
| Sum squared resid | 0.163924 |
| DW | 1.323347 |

**Question**: Is there a significance difference in the trend before and after 1979? Do you find evidence of a broken trend?

---

## Q1(c) (10 pts) — Economic Interpretation of Break

Explain in economic terms the difference between the trend before and after 1979. Draw a graph showing the shape of the trend suggested by the regression above.

---

## Q1(d) (10 pts) — Seasonality

The graph of the residuals from the above regression suggests we have not taken into account seasonality. Seasonal dummy variables were created and included.

**[Graph provided: Residual vs Actual vs Fitted plot showing clear seasonal oscillation in residuals]**

**Regression with seasonal dummies (D1, D2, D3; Q4 = base):**

Dep Var: LKWH | n = 83

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.569909 | 0.132071 | 4.315179 | 0.0000 |
| DBROKEN | 0.144370 | 0.024410 | 5.914400 | 0.0000 |
| TREND | 0.004153 | 0.000759 | 5.471034 | 0.0000 |
| TDBROKEN | -0.005892 | 0.000849 | -6.939062 | 0.0000 |
| LY | 0.014437 | 0.097710 | 0.147750 | 0.8830 |
| LPRICE | -0.182071 | 0.022515 | -8.086597 | 0.0000 |
| CDD | 0.000208 | 3.29E-05 | 6.311122 | 0.0000 |
| HDD | 0.000194 | 3.36E-05 | 5.773004 | 0.0000 |
| D1 | 0.035064 | 0.017212 | 2.037193 | 0.0453 |
| D2 | -0.077713 | 0.008723 | -8.909389 | 0.0000 |
| D3 | -0.064836 | 0.017090 | -3.793822 | 0.0003 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.910562 |
| Adj R-squared | 0.898140 |
| S.E. of regression | 0.025918 |
| Sum squared resid | 0.048365 |
| DW | 1.782561 |

**Question**: Is seasonality significant? Comment on the results from this new regression.

---

## Q1(e) (10 pts) — F-Test: Equal Seasonal Effects

Using the appropriate regression from the ones provided below, test whether the second and third quarters have the same effect on demand for electricity. (Note: d23 = d2+d3, and d12 = d1+d2)

**LEFT — With D12 and D3:**

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.522760 | 0.167239 | 3.125834 | 0.0025 |
| DBROKEN | 0.170321 | 0.030565 | 5.572372 | 0.0000 |
| TREND | 0.005056 | 0.000948 | 5.335962 | 0.0000 |
| TDBROKEN | -0.006890 | 0.001060 | -6.499535 | 0.0000 |
| LY | -0.016886 | 0.123762 | -0.136440 | 0.8918 |
| LPRICE | -0.176381 | 0.028531 | -6.182202 | 0.0000 |
| CDD | 0.000195 | 4.17E-05 | 4.686642 | 0.0000 |
| HDD | 0.000389 | 2.17E-05 | 17.88203 | 0.0000 |
| D12 | -0.065624 | 0.010824 | -6.062740 | 0.0000 |
| D3 | -0.003958 | 0.018393 | -0.215165 | 0.8302 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.854188 |
| Adj R-squared | 0.836211 |
| S.E. of regression | 0.032865 |
| Sum squared resid | 0.078850 |

**RIGHT — With D1 and D23:**

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.562031 | 0.131016 | 4.289776 | 0.0001 |
| DBROKEN | 0.141441 | 0.023908 | 5.916086 | 0.0000 |
| TREND | 0.004059 | 0.000743 | 5.466030 | 0.0000 |
| TDBROKEN | -0.005784 | 0.000830 | -6.969598 | 0.0000 |
| LY | 0.022691 | 0.096526 | 0.235071 | 0.8148 |
| LPRICE | -0.182601 | 0.022413 | -8.146981 | 0.0000 |
| CDD | 0.000225 | 2.09E-05 | 10.76393 | 0.0000 |
| HDD | 0.000185 | 3.08E-05 | 6.016854 | 0.0000 |
| D1 | 0.041949 | 0.013619 | 3.080221 | 0.0029 |
| D23 | -0.074910 | 0.007584 | -9.877653 | 0.0000 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.910024 |
| Adj R-squared | 0.898931 |
| S.E. of regression | 0.025817 |
| Sum squared resid | 0.048656 |

**Question**: Test whether the second and third quarters have the same effect ($\delta_2 = \delta_3$).

---

## Q1(f) (10 pts) — ACF/PACF Identification for Residual Cycles

Suppose now that we had started our problem by modeling seasonality first. Attached is the correlogram from the residuals of the model with only seasonal dummies. Only looking at the correlogram, which model for the cycles would you consider (AR, MA, ARMA)? Why?

**Seasonal-dummies-only regression:**

| Variable | Coefficient | Std. Error | t-Statistic | Prob. |
|----------|------------|-----------|------------|-------|
| C | 0.343682 | 0.010582 | 32.47851 | 0.0000 |
| D1 | 0.081656 | 0.015151 | 5.389496 | 0.0000 |
| D2 | -0.099017 | 0.014965 | -6.616558 | 0.0000 |
| D3 | -0.041967 | 0.014965 | -2.804346 | 0.0063 |

| Statistic | Value |
|-----------|-------|
| R-squared | 0.656472 |
| Sum squared resid | 0.185767 |
| DW | 0.893338 |

**Correlogram of residuals** (numerical values from the table):

| Lag | AC | PAC | Q-Stat | Prob |
|-----|------|-------|--------|------|
| 1 | 0.553 | 0.553 | 26.338 | 0.000 |
| 2 | 0.435 | 0.185 | 42.793 | 0.000 |
| 3 | 0.417 | 0.177 | 58.163 | 0.000 |
| 4 | 0.459 | 0.217 | 77.060 | 0.000 |
| 5 | 0.364 | -0.003 | 89.013 | 0.000 |
| 6 | 0.361 | 0.040 | 96.271 | 0.000 |
| 7 | 0.304 | 0.076 | 104.69 | 0.000 |
| 8 | 0.438 | 0.256 | 122.93 | 0.000 |
| 9 | 0.291 | -0.118 | 131.02 | 0.000 |
| 10 | 0.193 | -0.009 | 134.61 | 0.000 |
| 11 | 0.194 | -0.013 | 138.29 | 0.000 |
| 12 | 0.259 | 0.063 | 144.91 | 0.000 |

**Question**: Which model (AR, MA, ARMA) for the cycles? Why?

---

## Q1(g) (10 pts) — Model Selection from Multiple ARMA Outputs

I attached a few regressions that I estimated for different possible models for the cycles of this data. Of the models that I estimated which one do you think is the best model and why?

**Model comparison table (from the provided regression outputs):**

| Model | AIC | BIC (Schwarz) | DW | Sum sq resid | R-squared |
|-------|-----|------|-----|------|------|
| AR(1) + seasonal | -3.495655 | -3.348904 | 2.170212 | 0.128894 | 0.758427 |
| AR(2) + seasonal | -3.495649 | -3.318282 | 2.019048 | 0.124031 | 0.766959 |
| AR(3) + seasonal | -3.512548 | -3.304121 | 2.088123 | 0.117256 | 0.778065 |
| MA(1) + seasonal | -3.386892 | -3.241179 | 1.727906 | 0.145670 | 0.730621 |
| MA(2) + seasonal | -3.440946 | -3.266090 | 1.924393 | 0.134719 | 0.750871 |
| ARMA(1,1) + seasonal | -3.569297 | -3.393196 | 1.855379 | 0.116858 | 0.780985 |

**Question**: Which model is best? Why?

---

## Q1(h) (20 pts) — Forecasting by Hand (1-step + 2-step)

Given your answer in (g), compute your forecast for the first and second quarter of 1993. Below are some of the data you may need to compute the forecasts depending on which model you have chosen in the previous question.

**Data Table:**

| Date | LKWH | Residuals from MA(1) | Residuals from MA(2) | Residuals from ARMA(1,1) |
|------|------|---------------------|---------------------|-------------------------|
| 1991:1 | 0.392801 | -0.005694076 | -0.022133062 | -0.026877354 |
| 1991:2 | 0.205318 | -0.036940399 | -0.012792849 | -0.025993192 |
| 1991:3 | 0.242447 | -0.043961233 | -0.047096968 | -0.038930947 |
| 1991:4 | 0.349169 | 0.023702385 | 0.031645883 | 0.035213591 |
| 1992:1 | 0.373517 | -0.060759518 | -0.054551938 | -0.034587082 |
| 1992:2 | 0.229931 | 0.010488942 | 0.004106577 | 0.011495529 |
| 1992:3 | 0.408811 | 0.102749556 | 0.119780918 | 0.128869546 |
| 1992:4 | 0.338866 | -0.04739108 | -0.064279571 | -0.020704755 |

---

## Q3a (5 pts) — Compute Var(y_t)

$$y_t = \varepsilon_t + 0.8\varepsilon_{t-1} + 0.2\varepsilon_{t-2} \qquad \varepsilon_t \sim WN$$

Compute $\text{Var}(y_t)$.

---

## Q3b (10 pts) — Compute autocovariances and autocorrelations

$$y_t = \varepsilon_t + 0.8\varepsilon_{t-1} \qquad \varepsilon_t \sim WN$$

Compute $\gamma(1)$, $\gamma(2)$, $\rho(1)$, $\rho(2)$.

---

## BONUS (5 pts)

Show that a W.N. process with mean 0 and variance $\sigma^2$ is a stationary process.

---

## F-Table

Upper 5% Points of the F-Distribution provided at end of exam. Key values you might need:

- $F(2, 72)$ at 5%: approximately **3.12**
- $F(1, 72)$ at 5%: approximately **3.97**
- $F(2, 75)$ at 5%: approximately **3.12**

## t-Table

Percentage Points of the t-Distribution provided. Key values:
- df = 70-80, two-tailed 5% (0.025 each tail): approximately **1.99**
- df = 70-80, two-tailed 1%: approximately **2.64**

---
---

# SOLUTIONS

---

## Q1(a) Solution (5 pts) — Elasticities

### Exam likelihood: HIGH
Interpreting log-log regression coefficients as elasticities is a core skill. If Pesavento gives you a log-log model, this is what she'll ask.

### Step-by-step:

Since both the dependent variable (LKWH = log(KWH)) and some regressors (LY = log(Y), LPRICE = log(PRICE)) are in logs, the coefficients are **elasticities** directly.

**Income elasticity** = coefficient on LY = **-0.060**

This means: a 1% increase in income is associated with a 0.06% *decrease* in electricity demand. The sign is **negative**, which is **counterintuitive** — we'd expect higher income to increase demand (electricity is a normal good). However, the coefficient is **not statistically significant** (t = -0.38, p = 0.71), so we cannot distinguish it from zero. The negative sign is likely noise.

**Price elasticity** = coefficient on LPRICE = **-0.097**

This means: a 1% increase in price is associated with a 0.097% decrease in electricity demand. The sign is **negative**, which **does coincide with economic intuition** — higher prices reduce demand (law of demand). The coefficient IS significant (t = -3.32, p = 0.001).

The price elasticity is quite **inelastic** (|−0.097| < 1): demand doesn't respond much to price changes, which makes sense for electricity — it's a necessity with few substitutes.

---

## Q1(b) Solution (10 pts) — Broken Trend F-Test

### Exam likelihood: VERY HIGH
This is the exact same type as Exam 2 Q5 (F-test). Appeared 3/3 exams.

### Reference: `exams/study-notes/forecast-evaluation-deep-dive.md` (F-test formula)

### Step-by-step:

**Step 1: Identify restricted and unrestricted models.**
- Unrestricted (LEFT): includes DBROKEN and TDBROKEN → $SSR_U = 0.120624$, $k_U = 8$
- Restricted (RIGHT): drops DBROKEN and TDBROKEN → $SSR_R = 0.163924$, $k_R = 6$
- $q = 2$ restrictions, $n = 83$

**Step 2: Compute F.**

$$F = \frac{(SSR_R - SSR_U)/q}{SSR_U/(n - k_U)} = \frac{(0.163924 - 0.120624)/2}{0.120624/(83 - 8)} = \frac{0.04330/2}{0.120624/75} = \frac{0.02165}{0.001608} = 13.46$$

**Step 3: Compare to critical value.**

$F(2, 75)$ at 5% $\approx 3.12$. Since $13.46 \gg 3.12$, **reject $H_0$**.

**Step 4: Also check individual t-tests.**
- DBROKEN: t = 4.28, p = 0.0001 → **significant** (level shift)
- TDBROKEN: t = -5.19, p = 0.0000 → **significant** (slope change)

**Conclusion**: There is very strong evidence of a structural break at 1979. Both the joint F-test and the individual t-tests reject. The trend is significantly different before and after 1979.

---

## Q1(c) Solution (10 pts) — Economic Interpretation

### Exam likelihood: MEDIUM
Conceptual interpretation of structural breaks. Could appear as a short-answer.

### Step-by-step:

**Step 1: Compute trend slopes.**

- Trend before break: slope = TREND coefficient = **0.004933** (positive — electricity demand growing)
- Trend after break: slope = TREND + TDBROKEN = 0.004933 + (-0.006643) = **-0.001710** (negative — demand declining)

**Step 2: Interpret the level shift.**

DBROKEN = 0.158 means the intercept **jumps up** at 1979. But the slope turns negative, so after the initial jump, demand starts declining.

**Step 3: Economic story.**

Before 1979, electricity demand was growing (positive trend of ~0.5% per quarter). After the 1979 oil crisis, conservation efforts kicked in — better insulation, energy-efficient appliances, fuel-efficient cars. The trend reversed to slightly negative (-0.17% per quarter). The level shift (DBROKEN = +0.158) may reflect a temporary spike in demand or a measurement artifact at the break point.

**Graph**: The trend line goes UP before 1979, then bends DOWN after 1979 — like an inverted V with a kink at 1979.

---

## Q1(d) Solution (10 pts) — Seasonality

### Exam likelihood: HIGH
Seasonality with dummies appeared 2/3 exams. Key skill: interpret coefficients and test significance.

### Step-by-step:

**Are the seasonal dummies significant?**

| Dummy | Coef | t-stat | p-value | Significant? |
|-------|------|--------|---------|-------------|
| D1 (Q1) | 0.035 | 2.04 | 0.045 | Yes (at 5%) |
| D2 (Q2) | -0.078 | -8.91 | 0.000 | Yes (highly) |
| D3 (Q3) | -0.065 | -3.79 | 0.000 | Yes (highly) |

All three are individually significant. **Seasonality is significant.**

**Interpretation** (remember Q4 is the base):
- Q1 has ~3.5% **higher** demand than Q4 (heating season)
- Q2 has ~7.8% **lower** demand than Q4 (mild weather)
- Q3 has ~6.5% **lower** demand than Q4 (but less than Q2 — summer cooling helps)

**Impact on model quality:**
- R² jumped from 0.777 (without seasonals) to **0.911** (with seasonals) — massive improvement
- S.E. of regression dropped from 0.040 to 0.026
- DW improved from 1.79 to 1.78 (similar, but residuals are cleaner)

The seasonal pattern makes physical sense: electricity demand varies by quarter due to heating/cooling needs.

---

## Q1(e) Solution (10 pts) — F-Test for Equal Seasonal Effects

### Exam likelihood: VERY HIGH
This is the q=1 F-test (testing one restriction). Same formula, different setup.

### Step-by-step:

**What we're testing**: $H_0: \delta_2 = \delta_3$ (Q2 and Q3 have the same seasonal effect).

**Step 1: Identify the correct restricted model.**

The RIGHT table has D1 and **D23** (= D2 + D3). This forces $\delta_2 = \delta_3$ by combining them into one dummy — exactly the restriction we want. So:
- **Unrestricted**: Q1(d) output with D1, D2, D3 separately → $SSR_U = 0.048365$
- **Restricted**: RIGHT table with D1 and D23 → $SSR_R = 0.048656$

$q = 1$ (one restriction: $\delta_2 = \delta_3$), $n = 83$, $k_U = 11$ (from Q1(d)).

**Step 2: Compute F.**

$$F = \frac{(0.048656 - 0.048365)/1}{0.048365/(83 - 11)} = \frac{0.000291}{0.048365/72} = \frac{0.000291}{0.000672} = 0.433$$

**Step 3: Compare to critical value.**

$F(1, 72)$ at 5% $\approx 3.97$. Since $0.433 < 3.97$, **fail to reject**.

**Conclusion**: We cannot reject the hypothesis that Q2 and Q3 have the same effect on electricity demand. The seasonal effects are statistically indistinguishable — both quarters have similarly reduced demand relative to Q4.

---

## Q1(f) Solution (10 pts) — ACF/PACF Identification

### Exam likelihood: VERY HIGH
ACF/PACF identification appeared 3/3 exams. #2 ranked skill.

### Reference: `exams/study-notes/forecasting-by-hand-deep-dive.md` (Part 2-4 for model signatures)

### Step-by-step:

**Step 1: Examine the ACF.**

The autocorrelation values are: 0.553, 0.435, 0.417, 0.459, 0.364, 0.361, 0.304, 0.438, ...

This shows **slow, gradual decay** — the bars stay significant for many lags and decrease slowly. There's no sharp cutoff after any specific lag.

**Step 2: Examine the PACF.**

The partial autocorrelation values are: 0.553, 0.185, 0.177, 0.217, -0.003, 0.040, 0.076, 0.256, ...

The first lag is very large (0.553). Lags 2-4 are moderate (0.18-0.22). After lag 4, they drop toward zero. But there's a spike at lag 8 (0.256).

**Step 3: Identify the model.**

The slow ACF decay points to an **AR** component. The PACF doesn't cut off cleanly after lag 1 — there's still some structure at lags 2-4 and 8. This suggests either:
- **AR(1)** as the simplest option (dominant PACF spike at lag 1)
- **AR with higher order** or **ARMA** if we want to capture the additional PACF structure

Given the slow ACF decay and the PACF pattern with a dominant first spike but some residual structure, an **AR model** (possibly AR(1) or AR(2)) is the most natural starting point. The spike at lag 8 might suggest some remaining quarterly seasonality not fully captured. An ARMA(1,1) could also work if both ACF and PACF show decay.

**Answer**: The slow ACF decay suggests AR dynamics. The PACF has a dominant spike at lag 1 with some additional structure, pointing to AR(1) as the primary model, though an ARMA(1,1) may also be appropriate. I would estimate AR(1), AR(2), and ARMA(1,1) and compare using AIC/BIC (which is exactly what Q1(g) does).

---

## Q1(g) Solution (10 pts) — Model Selection

### Exam likelihood: VERY HIGH
Model selection via AIC/BIC appeared 3/3 exams.

### Step-by-step:

**Step 1: Compare AIC and BIC across all models.**

| Model | AIC | BIC |
|-------|-----|-----|
| AR(1) | -3.496 | -3.349 |
| AR(2) | -3.496 | -3.318 |
| AR(3) | -3.513 | -3.304 |
| MA(1) | -3.387 | -3.241 |
| MA(2) | -3.441 | -3.266 |
| **ARMA(1,1)** | **-3.569** | **-3.393** |

**Step 2: Select by AIC (lower = better).**

ARMA(1,1) has the lowest AIC at **-3.569**. It wins.

**Step 3: Confirm with BIC.**

ARMA(1,1) also has the lowest BIC at **-3.393**. Both criteria agree.

**Step 4: Check for issues.**

- ARMA(1,1) inverted AR root = 0.93, inverted MA root = 0.65 — both inside the unit circle. The model is stationary and invertible.
- DW = 1.86, close to 2 — residuals appear uncorrelated.
- All coefficients significant (AR(1) coef = 0.926, t = 15.49; MA(1) coef = -0.647, t = -5.28).

**Answer**: ARMA(1,1) is the best model. It has the lowest AIC and BIC, all coefficients are significant, the model is stationary and invertible, and the DW statistic is close to 2.

---

## Q1(h) Solution (20 pts) — Forecasting by Hand (Seasonal + ARMA)

### Exam likelihood: VERY HIGH
This is the hardest and highest-point question (20 pts!). Combines seasonal dummies + ARMA forecasting.

### Reference: `exams/study-notes/forecasting-by-hand-deep-dive.md` (Part 5: Seasonal Dummies + ARMA)

### Understanding the model structure

The ARMA(1,1) + seasonal dummies model (chosen in Q1(g) because it has the lowest AIC and BIC) is estimated **as one regression**. Looking at the regression output, the coefficients are:

| Variable | Coefficient |
|----------|------------|
| C | 0.340657 |
| D1 | 0.082325 |
| D2 | -0.098766 |
| D3 | -0.042208 |
| AR(1) | 0.926149 |
| MA(1) | -0.646372 |

The model can be written as two layers:

**Layer 1 (Deterministic — seasonal):** The "mean" for each quarter:
- Q4 (base): $c = 0.340657$
- Q1: $c + \delta_1 = 0.340657 + 0.082325 = 0.422982$
- Q2: $c + \delta_2 = 0.340657 - 0.098766 = 0.241891$
- Q3: $c + \delta_3 = 0.340657 - 0.042208 = 0.298449$

**Layer 2 (Stochastic — ARMA(1,1) for cycles):**
$$\hat{u}_t = \phi \hat{u}_{t-1} + \varepsilon_t + \theta \varepsilon_{t-1}$$

where $\hat{u}_t = \text{LKWH}_t - \text{seasonal mean for that quarter}$, $\phi = 0.926149$, $\theta = -0.646372$.

The "Residuals from ARMA(1,1)" column in the data table gives us the **innovations** $\varepsilon_t$.

### What we have from the data table:

| Date | LKWH | $\varepsilon_t$ (ARMA(1,1) innovation) |
|------|------|-------|
| 1992:3 (Q3) | 0.408811 | 0.128870 |
| 1992:4 (Q4) | 0.338866 | -0.020705 |

We stand at **T = 1992:4**. We want 1993:Q1 (h=1) and 1993:Q2 (h=2).

### Step 1: Compute $\hat{u}_T$ (the cycle at 1992:4)

Since 1992:4 is Q4, the seasonal mean is just $c = 0.340657$:

$$\hat{u}_T = \text{LKWH}_{1992:4} - c = 0.338866 - 0.340657 = -0.001791$$

### Step 2: Forecast the ARMA(1,1) cycle for 1993:Q1 (h=1)

Write the ARMA(1,1) forecast equation:

$$\hat{u}_{T+1,T} = \phi \hat{u}_T + \underbrace{\varepsilon_{T+1}}_{\text{future} \to 0} + \theta \varepsilon_T$$

Apply the rules:
- $\hat{u}_T = -0.001791$ → **known** (just computed)
- $\varepsilon_{T+1}$ → **future shock → 0**
- $\varepsilon_T = -0.020705$ → **known** (from the table, last ARMA(1,1) residual)

$$\hat{u}_{T+1,T} = 0.926149 \times (-0.001791) + (-0.646372) \times (-0.020705)$$

$$= -0.001659 + 0.013384 = 0.011725$$

### Step 3: Add the seasonal component for 1993:Q1

1993:Q1 is quarter 1, so the seasonal mean is $c + \delta_1 = 0.422982$:

$$\boxed{\widehat{\text{LKWH}}_{1993:Q1} = 0.422982 + 0.011725 = 0.4347}$$

### Step 4: Forecast the ARMA(1,1) cycle for 1993:Q2 (h=2)

At h=2, the MA component **dies** — $\varepsilon_{T+1}$ is future, so $\theta \varepsilon_{T+1} = 0$:

$$\hat{u}_{T+2,T} = \phi \hat{u}_{T+1,T} + \underbrace{\varepsilon_{T+2}}_{\to 0} + \theta \underbrace{\varepsilon_{T+1}}_{\to 0}$$

$$\hat{u}_{T+2,T} = \phi \hat{u}_{T+1,T} = 0.926149 \times 0.011725 = 0.010859$$

### Step 5: Add the seasonal component for 1993:Q2

1993:Q2 is quarter 2, so the seasonal mean is $c + \delta_2 = 0.241891$:

$$\boxed{\widehat{\text{LKWH}}_{1993:Q2} = 0.241891 + 0.010859 = 0.2528}$$

### Summary of what you plug in at each step

| | h=1 (1993:Q1) | h=2 (1993:Q2) |
|---|---|---|
| **Seasonal mean** | $c + \delta_1 = 0.4230$ | $c + \delta_2 = 0.2419$ |
| **AR term** ($\phi \hat{u}$) | $0.926 \times (-0.0018) = -0.0017$ | $0.926 \times 0.0117 = 0.0109$ |
| **MA term** ($\theta \varepsilon$) | $-0.646 \times (-0.0207) = +0.0134$ | **= 0** (future $\varepsilon_{T+1}$) |
| **Future $\varepsilon$** | = 0 | = 0 |
| **Cycle forecast** $\hat{u}$ | $-0.0017 + 0.0134 = 0.0117$ | $0.0109$ |
| **Total forecast** | $0.4230 + 0.0117 = \mathbf{0.4347}$ | $0.2419 + 0.0109 = \mathbf{0.2528}$ |

### What the grader wants (for full 20 points):

1. **State which model you chose** from Q1(g) and why (ARMA(1,1), lowest AIC/BIC)
2. **Show the two-layer structure**: deterministic (seasonal dummies) + stochastic (ARMA residual)
3. **Compute $\hat{u}_T$** by subtracting the seasonal mean from the last observed LKWH
4. **Write the ARMA(1,1) forecast equation** and identify which terms are zero (future $\varepsilon$) and which are known (past $\varepsilon$ from the table)
5. **Plug in $\varepsilon_T = -0.020705$** from the table — this is why the table was provided!
6. **At h=2, explicitly state the MA term dies** — both $\varepsilon_{T+2}$ and $\varepsilon_{T+1}$ are future → zero
7. **Use the correct seasonal dummy** for each target quarter ($\delta_1$ for Q1, $\delta_2$ for Q2)
8. **Show arithmetic clearly** — every multiplication, every addition

---

## Q3a Solution (5 pts) — Var(y_t) for MA(2)

### Exam likelihood: VERY HIGH
Autocovariance derivation appeared 3/3 exams. #1 ranked skill.

### Reference: `exams/study-notes/MA-autocovariance-deep-dive.md`

$$y_t = \varepsilon_t + 0.8\varepsilon_{t-1} + 0.2\varepsilon_{t-2}$$

$$\text{Var}(y_t) = (1^2 + 0.8^2 + 0.2^2)\sigma^2 = (1 + 0.64 + 0.04)\sigma^2 = \boxed{1.68\sigma^2}$$

Square each coefficient (including the implicit 1 on $\varepsilon_t$), add them up, multiply by $\sigma^2$.

---

## Q3b Solution (10 pts) — Autocovariances for MA(1)

### Exam likelihood: VERY HIGH

$$y_t = \varepsilon_t + 0.8\varepsilon_{t-1}$$

**$\gamma(0) = \text{Var}(y_t) = (1 + 0.8^2)\sigma^2 = 1.64\sigma^2$**

**$\gamma(1)$**: Multiply $y_t$ and $y_{t-1}$, keep matching $\varepsilon$ indices:

$y_t = \varepsilon_t + 0.8\varepsilon_{t-1}$
$y_{t-1} = \varepsilon_{t-1} + 0.8\varepsilon_{t-2}$

Only $\varepsilon_{t-1}$ appears in both: $\gamma(1) = 1 \times 0.8 \times \sigma^2 = \boxed{0.8\sigma^2}$

(The $0.8\varepsilon_{t-1}$ in $y_t$ times the $1 \times \varepsilon_{t-1}$ in $y_{t-1}$.)

**$\gamma(2)$**:

$y_t = \varepsilon_t + 0.8\varepsilon_{t-1}$
$y_{t-2} = \varepsilon_{t-2} + 0.8\varepsilon_{t-3}$

No common $\varepsilon$ indices → $\boxed{\gamma(2) = 0}$

MA(1) has autocovariance cutoff after lag 1.

**$\rho(1) = \gamma(1)/\gamma(0) = 0.8\sigma^2 / 1.64\sigma^2 = \boxed{0.488}$**

**$\rho(2) = \gamma(2)/\gamma(0) = 0/1.64\sigma^2 = \boxed{0}$**

---

## Bonus Solution (5 pts) — WN is Stationary

A process is weakly stationary if: (1) $E(y_t)$ is constant, (2) $\text{Var}(y_t)$ is constant, (3) $\text{Cov}(y_t, y_{t-k})$ depends only on $k$, not on $t$.

For WN with mean 0 and variance $\sigma^2$:
1. $E(\varepsilon_t) = 0$ for all $t$ → **constant** (= 0)
2. $\text{Var}(\varepsilon_t) = \sigma^2$ for all $t$ → **constant** (= $\sigma^2$)
3. $\text{Cov}(\varepsilon_t, \varepsilon_{t-k}) = 0$ for all $k \neq 0$ (by definition of WN) → depends only on $k$ (always 0)

All three conditions satisfied → WN is stationary. $\square$

---

## Summary: Exam Likelihood by Question

| Q | Topic | Points | Exam Likelihood | Priority |
|---|-------|--------|----------------|----------|
| 1a | Log-log elasticity interpretation | 5 | HIGH | Medium |
| 1b | F-test for structural break | 10 | VERY HIGH | Study this |
| 1c | Economic interpretation of break | 10 | MEDIUM | Know the concept |
| 1d | Seasonal dummies interpretation | 10 | HIGH | Know how to interpret |
| 1e | F-test q=1 (equal seasonal effects) | 10 | VERY HIGH | Study this |
| 1f | ACF/PACF identification | 10 | VERY HIGH | Study this |
| 1g | Model selection AIC/BIC | 10 | VERY HIGH | Easy points |
| 1h | Forecasting: seasonal + ARMA | 20 | VERY HIGH | Hardest — practice |
| Q3a | MA(2) variance | 5 | VERY HIGH | Quick points |
| Q3b | MA(1) autocovariances | 10 | VERY HIGH | Must-know |
| Bonus | WN stationarity proof | 5 | LOW | Only if time |
