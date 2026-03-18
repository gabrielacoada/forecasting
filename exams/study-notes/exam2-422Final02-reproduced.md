# ECON 422 — FINAL #2 (Reproduced)

**Rules of the game**

Count all the pages (you should have 15 pages including this) and write your name and ID number on the top of the page.

You have 2 and 1/2 hours to finish the test. The test is closed books and closed notes. You can use a calculator.

On the test you have the points assigned to each question. A correct answer with no explanation will NOT give you full credit. Make sure you explain each step. All relevant tables are at the end of the test.

---

## Context (for all questions)

**Q1.** One of the most transforming events of the 20th century was the mass production of automobiles. Besides becoming one of the most important manufacturing sectors in the United States, the automobile has spawned several industries — from highway engineering and construction, auto parts manufacturers, and automobile insurance to automobile dealerships, gasoline service stations, and auto repair shops. Today, motor vehicles play a central role within the typical American household. Motor vehicles are one of the most widely owned assets, with more than 85 percent of U.S. households owning one or more vehicles.

In this problem we will look at total expenditure on new automobiles in the United States. (Notice that this data set is different from the car sales demand we looked at in class). We have quarterly data from the first quarter of 1959 to the third quarter of 2002 for the following variables:

**CARSPEND** = total expenditure on new automobiles in billions.
**DISPOSINC** = national disposable income in the US in billions.

---

## Question 1 (10 pts)

We estimated the equation $\text{carspend}_t = c + \beta_1 \text{disposinc}_t + \varepsilon_t$. Compute the confidence interval for the effect of disposable income on total car expenditure. Using your confidence interval answer the following question: If disposable income rises by $300 billion, how much do you estimate car spending to rise (use your confidence interval for full credit)?

**Regression Output:**

| Source | SS | df | MS | | |
|--------|-----------|-----|-----------|---|---|
| Model | 147618.071 | 1 | 147618.071 | Number of obs = | 175 |
| Residual | 29406.3921 | 173 | 169.979145 | F(1, 173) = | 868.45 |
| Total | 177024.463 | 174 | 1017.38197 | Prob > F = | 0.0000 |
| | | | | R-squared = | 0.8339 |
| | | | | Adj R-squared = | 0.8329 |
| | | | | Root MSE = | 13.038 |

| carspend | Coef. | Std. Err. | t | P>t | [95% Conf. Interval] |
|----------|-------|-----------|------|-------|----------------------|
| dispinc | .01293 | .0004388 | 29.47 | 0.000 | |
| _cons | 20.17671 | 1.562143 | 12.92 | 0.000 | |

| Model | Obs | ll(null) | ll(model) | df | AIC | BIC |
|-------|-----|----------|-----------|-----|---------|---------|
| . | 175 | -853.7493 | -696.6801 | 2 | 1397.36 | 1403.69 |

---

## Question 2 (5 pts)

You are worried about the presence of autocorrelation in the error terms. What do the graphs of the actual data and residuals, and the ACF and PACF of the residuals from the above regression suggest? Which model would they suggest for the residuals? Explain your choice.

**[Four graphs provided:]**
- **Top-left**: "Total car expenditure" — time series plot of carspend from 1960q1 to 2000q1. Shows upward trend from ~10 to ~120, with a notable spike around 1986.
- **Top-right**: "Residuals" — residuals from the Q1 regression. Large positive spike around 1986 (~60), otherwise fluctuating between roughly -20 and +20.
- **Bottom-left**: "ACF" — Autocorrelation function of residuals. Bars slowly decay from ~0.8 at lag 1, remaining positive and significant through about lag 20. Very slow decay pattern.
- **Bottom-right**: "PACF" — Partial autocorrelation function of residuals. One very large spike at lag 1 (~0.8), then all subsequent lags are small and within the confidence bands.

---

## Question 3 (10 pts)

We added $\text{carspend}_{t-1}$ to correct for the serial correlation. Is this AR(1) correction a good correction for the serial correlation in the original regression? Why or why not? Explain briefly your reasoning.

**AR(1) Regression Output:**

| Source | SS | df | MS | | |
|--------|-----------|-----|-----------|---|---|
| Model | 170271.473 | 2 | 85135.7363 | Number of obs = | 174 |
| Residual | 4894.5626 | 171 | 28.6231731 | F(2, 171) = | 2974.36 |
| Total | 175166.035 | 173 | 1012.52043 | Prob > F = | 0.0000 |
| | | | | R-squared = | 0.9721 |
| | | | | Adj R-squared = | 0.9717 |
| | | | | Root MSE = | 5.3501 |

| carspend | Coef. | Std. Err. | t | P>t | [95% Conf. | Interval] |
|----------|---------|-----------|-------|-------|------------|-----------|
| dispinc | .0010708 | .0004437 | 2.41 | 0.017 | .000195 | .0019467 |
| L1. carspend | .9188597 | .0314886 | 29.18 | 0.000 | .8567032 | .9810162 |
| _cons | 2.090818 | .8982747 | 2.33 | 0.021 | .3176829 | 3.863953 |

| Model | Obs | ll(null) | ll(model) | df | AIC | BIC |
|-------|-----|----------|-----------|-----|---------|---------|
| . | 174 | -848.4511 | -537.1991 | 3 | 1080.398 | 1089.875 |

**[Two graphs provided:]**
- **ACF of AR(1) residuals**: Bars are mostly within confidence bands. Some spikes around lags 5-8 and 15-20 that appear marginally significant. No clear slow-decay pattern.
- **PACF of AR(1) residuals**: Similar pattern — some marginally significant spikes around lags 5-8 and 15-20, but no dominant single spike.

---

## Question 4 (12 pts)

We estimate the regression again, this time using a correction for an AR(2) process in the error term. Look at the confidence interval for this regression. Why do you think there is such a difference in the confidence intervals? Which confidence interval is a better estimate of the range of possible values for $\beta_1$, the one in question 1 or this one? Briefly explain why.

**AR(2) Regression Output:**

| Source | SS | df | MS | | |
|--------|-----------|-----|-----------|---|---|
| Model | 169131.767 | 3 | 56377.2556 | Number of obs = | 173 |
| Residual | 4214.1407 | 169 | 24.9357438 | F(3, 169) = | 2260.90 |
| Total | 173345.907 | 172 | 1007.82504 | Prob > F = | 0.0000 |
| | | | | R-squared = | 0.9757 |
| | | | | Adj R-squared = | 0.9753 |
| | | | | Root MSE = | 4.9936 |

| carspend | Coef. | Std. Err. | t | P>t | [95% Conf. | Interval] |
|----------|---------|-----------|------|-------|------------|-----------|
| dispinc | .0005992 | .0004241 | 1.41 | 0.160 | -.0002381 | .0014365 |
| L1. carspend | .5777969 | .0716017 | 8.07 | 0.000 | .4364479 | .7191458 |
| L2. carspend | .3774076 | .0722777 | 5.22 | 0.000 | .2347242 | .520091 |
| _cons | 1.576679 | .8513318 | 1.85 | 0.066 | -.1039355 | 3.257293 |

---

## Question 5 (10 pts)

Compute a test for the joint significance of the two lags in the regression above.

*(No additional output — use the Q1 and Q4 regression outputs.)*

---

## Question 6 (12 pts)

Compute the one step-ahead and two steps-ahead forecast of total car expenditure from the AR(2) model above.

**Data Table:**

| DATE | CARSPEND | DISPOSINC | Residuals from ARMA(2,2) | Residuals from AR(3) | Residuals from AR(2) | Residuals from MA(2) |
|--------|----------|-----------|--------------------------|----------------------|----------------------|----------------------|
| 2001:2 | 102.387 | 7340.0 | -1.51 | -4.19 | -0.09 | -5.70 |
| 2001:3 | 100.031 | 7524.2 | -3.08 | 16.12 | -4.84 | -12.03 |
| 2001:4 | 117.171 | 7391.2 | 15.64 | -7.39 | 16.61 | 14.25 |
| 2002:1 | 104.09 | 7666.7 | -5.43 | -7.30 | -7.93 | -18.01 |
| 2002:2 | 102.244 | 7786.5 | -5.67 | 2.66 | -9.02 | -13.96 |
| 2002:3 | 109.192 | 7874.4 | 3.73 | -4.19 | 4.79 | 9.32 |
| 2002:4 | | 7935.6 | | | | |
| 2003:1 | | 8039.2 | | | | |
| 2003:2 | | 8145.8 | | | | |
| 2003:3 | | 8317.8 | | | | |

---

## Question 7 (10 pts)

Explain briefly but clearly why it is important to test for a unit root in the data.

---

## Question 8 (5 pts)

Below are the test values for a Dickey-Fuller test for a unit root on Carspend. Which one of the two do you think is the correct regression to use to test for a unit root: One with a trend or without a trend? Choose one of the two and discuss what the test suggests. Do we find evidence of a unit root?

**WITHOUT TREND**

Augmented Dickey-Fuller test for unit root — Number of obs = 170

| | Test Statistic | 1% Critical Value | 5% Critical Value | 10% Critical Value |
|------|----------------|-------------------|-------------------|-------------------|
| Z(t) | **-0.309** | -3.487 | -2.885 | -2.575 |

MacKinnon approximate p-value for Z(t) = **0.9242**

**WITH TREND**

Augmented Dickey-Fuller test for unit root — Number of obs = 170

| | Test Statistic | 1% Critical Value | 5% Critical Value | 10% Critical Value |
|------|----------------|-------------------|-------------------|-------------------|
| Z(t) | **-1.989** | -4.017 | -3.441 | -3.141 |

MacKinnon approximate p-value for Z(t) = **0.6073**

---

## USEFUL REGRESSIONS (provided at end of exam)

These are additional regression outputs that may be needed for some questions.

### AR(1)

*(Same as Q3 output — reproduced above)*

### AR(2)

*(Same as Q4 output — reproduced above)*

### AR(3)

| Source | SS | df | MS | | |
|--------|-----------|-----|-----------|---|---|
| Model | 167425.953 | 4 | 41856.4882 | Number of obs = | 172 |
| Residual | 4155.22631 | 167 | 24.8815946 | F(4, 167) = | 1682.23 |
| Total | 171581.179 | 171 | 1003.39871 | Prob > F = | 0.0000 |
| | | | | R-squared = | 0.9758 |
| | | | | Adj R-squared = | 0.9752 |
| | | | | Root MSE = | 4.9881 |

| carspend | Coef. | Std. Err. | t | P>t | [95% Conf. | Interval] |
|----------|---------|-----------|------|-------|------------|-----------|
| dispinc | .0004989 | .0004288 | 1.16 | 0.246 | -.0003477 | .0013456 |
| L1. | .5335678 | .0770864 | 6.92 | 0.000 | .3813783 | .6857572 |
| L2. | .3099008 | .0844912 | 3.67 | 0.000 | .1430923 | .4767093 |
| L3. | .1196323 | .077746 | 1.54 | 0.126 | -.0338594 | .2731241 |
| _cons | 1.505381 | .858565 | 1.75 | 0.081 | -.1896585 | 3.200421 |

| Model | Obs | ll(null) | ll(model) | df | AIC | BIC |
|-------|-----|----------|-----------|-----|---------|---------|
| . | 172 | -837.9147 | -517.9354 | 5 | 1045.871 | 1061.608 |

### MA(2)

| carspend | Coef. | Std. Err. | z | P>z | [95% Conf. | Interval] |
|----------|---------|-----------|-------|-------|------------|-----------|
| _cons | 56.09762 | 3.078069 | 18.22 | 0.000 | 50.06471 | 62.13052 |
| **ARMA** | | | | | | |
| ma L1. | 1.002084 | .0539003 | 18.59 | 0.000 | .8964418 | 1.107727 |
| ma L2. | .8250592 | .0541447 | 15.24 | 0.000 | .7189375 | .9311809 |

| Model | Obs | ll(null) | ll(model) | df | AIC | BIC |
|-------|-----|----------|-----------|-----|---------|---------|
| . | 175 | . | -701.3799 | 4 | 1410.76 | 1423.419 |

### MA(4)

| carspend | Coef. | Std. Err. | z | P>z | [95% Conf. | Interval] |
|----------|---------|-----------|-------|-------|------------|-----------|
| _cons | 56.03846 | 3.874319 | 14.46 | 0.000 | 48.44493 | 63.63198 |
| **ARMA** | | | | | | |
| ma L1. | 1.264369 | .0590728 | 21.40 | 0.000 | 1.148588 | 1.380149 |
| ma L2. | 1.282615 | .0734143 | 17.47 | 0.000 | 1.138726 | 1.426504 |
| ma L3. | 1.01809 | .0811946 | 12.54 | 0.000 | .8589518 | 1.177229 |
| ma L4. | .5041441 | .0612936 | 8.23 | 0.000 | .3840109 | .6242772 |

| Model | Obs | ll(null) | ll(model) | df | AIC | BIC |
|-------|-----|----------|-----------|-----|---------|---------|
| . | 175 | . | -636.8402 | 6 | 1285.68 | 1304.669 |

---

## NOTES ON GRAPHS (for reference)

**Q2 Graphs** (ACF/PACF of Q1 residuals):
- ACF: Slow decay from ~0.8 at lag 1, bars remain significant through ~lag 20
- PACF: One large spike at lag 1 (~0.8), all others within confidence bands

**Q3 Graphs** (ACF/PACF of AR(1) residuals):
- ACF: Most bars within bands; some marginal spikes around lags 5-8 and 15-20
- PACF: Similar — some marginal spikes but no dominant pattern

---

---
---

# SOLUTIONS

---

## Question 1 Solution (10 pts) — Confidence Interval + Economic Interpretation

### Exam likelihood: HIGH

Confidence intervals from regression output appeared on 2/3 past exams. This is a bread-and-butter econometrics skill. Pesavento will almost certainly have a regression interpretation question. The twist here is that they also ask you to USE the CI to answer an economic question — not just compute it.

### Reference doc: `exams/final-study-guide.md` (Section 10: Confidence Intervals / Regression Interpretation)

### Step-by-step solution:

**Step 1: Write the CI formula.**

$$\hat{\beta}_1 \pm t_{\text{crit}} \times SE(\hat{\beta}_1)$$

For a 95% CI with large sample (n = 175, df = 173), use $t_{\text{crit}} \approx 1.96$ (or 1.974 from t-tables with df = 173, but 1.96 is fine for this sample size).

**Step 2: Read the numbers from the output.**

- $\hat{\beta}_1 = 0.01293$ (coefficient on dispinc)
- $SE(\hat{\beta}_1) = 0.0004388$

**Step 3: Compute the CI for $\beta_1$.**

$$0.01293 \pm 1.96 \times 0.0004388$$

$$0.01293 \pm 0.000860$$

$$\boxed{[0.01207, \; 0.01379]}$$

This means: we are 95% confident that the true effect of a $1 billion increase in disposable income on car spending is between $0.01207 billion and $0.01379 billion.

**Step 4: Answer the economic question — "If disposable income rises by $300 billion..."**

The model says: $\Delta \text{carspend} = \beta_1 \times \Delta \text{disposinc}$

For a $300 billion increase, multiply the ENTIRE confidence interval by 300:

- Lower bound: $0.01207 \times 300 = 3.62$ billion
- Point estimate: $0.01293 \times 300 = 3.88$ billion
- Upper bound: $0.01379 \times 300 = 4.14$ billion

$$\boxed{\text{Car spending rises by between \$3.62 and \$4.14 billion (95\% CI), point estimate \$3.88 billion.}}$$

**Why full credit requires using the CI**: The question says "use your confidence interval for full credit." If you just say "$3.88 billion" (point estimate only), you lose points. You MUST give the range.

---

## Question 2 Solution (5 pts) — ACF/PACF Identification of Residual Model

### Exam likelihood: VERY HIGH

ACF/PACF identification appeared on 3/3 past exams. This is the #2 ranked exam skill. You'll almost certainly see a correlogram and need to identify AR vs MA vs ARMA.

### Reference doc: `course-materials/lectures/week-04/summary.md` (ACF/PACF identification rules)

### Step-by-step solution:

**Step 1: Look at the ACF.**

The ACF of the residuals shows **slow, gradual decay** — bars slowly get smaller from lag 1 (~0.8) through lag 20+. They don't cut off sharply.

**Step 2: Look at the PACF.**

The PACF shows **one large spike at lag 1** (~0.8), then all other lags are within the confidence bands (essentially zero).

**Step 3: Apply the identification rules.**

| Pattern | ACF | PACF | Model |
|---------|-----|------|-------|
| Slow decay + sharp PACF cutoff after p | Decays | Cuts off at p | **AR(p)** |
| Sharp cutoff after q + slow decay | Cuts off at q | Decays | MA(q) |
| Both decay | Decays | Decays | ARMA(p,q) |

Here: ACF decays slowly, PACF cuts off after lag 1 → this is the **AR(1)** signature.

**Step 4: Write the answer.**

The ACF of the residuals decays slowly (geometrically), which is characteristic of an autoregressive process. The PACF has a single significant spike at lag 1 and is insignificant at all higher lags, which indicates exactly one autoregressive lag. This suggests the residuals follow an **AR(1) process**. We should add $\text{carspend}_{t-1}$ (the first lag of the dependent variable) to the regression to correct for this serial correlation.

---

## Question 3 Solution (10 pts) — Is the AR(1) Correction Adequate?

### Exam likelihood: MEDIUM-HIGH

Serial correlation correction appeared on 1/3 past exams directly, but interpreting residual diagnostics after adding lags is a core skill tested implicitly in many questions. If Pesavento gives you a model and then asks "is this a good fit?", this is how you check.

### Reference doc: `exams/study-notes/forecast-evaluation-deep-dive.md` (Part 2: Properties of optimal forecasts — check residuals are WN)

### Step-by-step solution:

**Step 1: Understand what "good correction" means.**

If the AR(1) correction fully accounts for the serial correlation, the **residuals from the AR(1) model should be white noise** — no remaining autocorrelation pattern. Check the ACF and PACF of the NEW residuals.

**Step 2: Examine the AR(1) residual ACF/PACF.**

From the graphs: the ACF and PACF of the AR(1) residuals show some marginally significant spikes around lags 5-8 and 15-20, but no dominant single spike and no slow decay pattern. Most bars are within the confidence bands.

**Step 3: Check other indicators.**

- **Durbin-Watson**: Not given directly, but we can assess from the ACF. Since most bars are within bands, the serial correlation is mostly cleaned up.
- **R-squared jumped**: From 0.8339 (Q1) to 0.9721 (AR(1)) — a massive improvement.
- **Root MSE dropped**: From 13.038 to 5.3501 — the model fits much better.
- **L1 coefficient**: 0.919, highly significant (t = 29.18) — the lag is clearly needed.

**Step 4: Assess whether AR(1) is sufficient.**

The AR(1) correction is a **substantial improvement** — it removes the dominant serial correlation pattern (the slow-decaying ACF from Q2 is gone). However, the remaining ACF/PACF show some marginally significant spikes at higher lags (5-8), which suggest the AR(1) may not have fully captured all the dynamics. An AR(2) might be worth trying.

**Answer:**

The AR(1) correction is a good first step but may not be fully adequate. The original residuals had a clear AR(1) pattern (slow ACF decay, one PACF spike), and adding L1 largely removes this — the new residual ACF/PACF are mostly within the confidence bands. However, there are some marginally significant spikes remaining at lags around 5-8, suggesting additional autocorrelation structure that the AR(1) doesn't capture. An AR(2) specification (as in Q4) would be worth testing. The dramatic improvement in R-squared (0.83 → 0.97) and Root MSE (13.0 → 5.4) confirms the lag is important, but the residual patterns suggest the correction is incomplete.

---

## Question 4 Solution (12 pts) — AR(2) Confidence Intervals Comparison

### Exam likelihood: MEDIUM

Comparing confidence intervals across model specifications appeared on this exam specifically. The general skill — understanding why CIs change when you fix serial correlation — is conceptually important and could appear as a short-answer question.

### Reference doc: `exams/final-study-guide.md` (Section 10: Confidence Intervals)

### Step-by-step solution:

**Step 1: Read the CI for $\beta_1$ (dispinc) from each model.**

| Model | $\hat{\beta}_1$ | 95% CI | Width |
|-------|-----------------|--------|-------|
| Q1 (no lags) | .01293 | [.01207, .01379] | 0.00172 |
| Q4 (AR(2)) | .0005992 | [-.0002381, .0014365] | 0.00168 |

**Step 2: Identify the key differences.**

1. **The point estimate changed dramatically**: from .01293 to .0005992 — more than 20x smaller!
2. **The CI width is similar**, but the AR(2) CI now **includes zero** (the lower bound is negative: -.0002381). In Q1, the CI was entirely positive.
3. **dispinc is no longer significant** in the AR(2) model (p = 0.160), while it was highly significant in Q1 (p = 0.000).

**Step 3: Explain WHY this happened.**

The original regression (Q1) suffered from severe serial correlation (we saw the AR(1) pattern in Q2). When you have serial correlation and don't correct for it:

- **OLS estimates are still unbiased** (the point estimate isn't wrong per se)
- **BUT the standard errors are WRONG** — they are too small (understated)
- This means the confidence interval is **too narrow** — it gives you false precision
- The t-statistics are inflated, making things look significant when they might not be

When we add the AR lags (Q4), we're properly accounting for the serial correlation. Now:
- The standard errors are **correct** (properly estimated)
- The CI is a **more honest** representation of our uncertainty about $\beta_1$
- It turns out the effect of disposable income is much less certain than Q1 suggested

**Step 4: Which CI is better?**

The AR(2) confidence interval is the **better estimate**. The Q1 confidence interval is artificially narrow because it ignores serial correlation, which biases the standard errors downward. The AR(2) model corrects for the autocorrelation in the error term, producing valid standard errors and a CI that honestly reflects our uncertainty about $\beta_1$.

The fact that dispinc becomes insignificant (p = 0.160) once we account for dynamics is itself a finding: most of the variation in car spending is explained by its own past (persistence through L1 and L2), and the additional effect of current disposable income is small and uncertain once you control for that persistence.

---

## Question 5 Solution (10 pts) — F-Test for Joint Significance of Lags

### Exam likelihood: VERY HIGH

The F-test appeared on 3/3 past exams. This is the #6 ranked skill and the exam always provides the regression outputs you need. You MUST know the formula.

### Reference doc: `exams/study-notes/forecast-evaluation-deep-dive.md` (Section 3.7: F-test formula); `exams/final-study-guide.md` (Worked Example 3)

### Step-by-step solution:

**Step 1: Identify the restricted and unrestricted models.**

We're testing whether L1 and L2 are jointly significant. That means:
- **Unrestricted model**: AR(2) from Q4 (includes dispinc, L1, L2, _cons) → $SSR_U$, $k_U$
- **Restricted model**: Q1 (only dispinc and _cons — no lags) → $SSR_R$, $k_R$

**Step 2: Read SSR from the regression outputs.**

- $SSR_R$ = "Residual SS" from Q1 = **29406.3921**
- $SSR_U$ = "Residual SS" from Q4 = **4214.1407**
- $q$ = number of restrictions = 2 (we dropped L1 and L2)
- $n$ = 173 (from Q4 output)
- $k_U$ = 4 (constant, dispinc, L1, L2)

**Step 3: Plug into the F formula.**

$$F = \frac{(SSR_R - SSR_U) / q}{SSR_U / (n - k_U)}$$

$$F = \frac{(29406.3921 - 4214.1407) / 2}{4214.1407 / (173 - 4)}$$

$$F = \frac{25192.2514 / 2}{4214.1407 / 169}$$

$$F = \frac{12596.13}{24.94}$$

$$\boxed{F = 505.1}$$

**Step 4: Compare to the critical value.**

$F(2, 169)$ at 5% $\approx 3.05$ (from F-tables). Since $505.1 \gg 3.05$, we **overwhelmingly reject** $H_0$.

**Step 5: Conclude.**

The two lags (L1 and L2) are **jointly highly significant**. Adding the autoregressive terms dramatically improves the model — the SSR drops from 29,406 to 4,214 (an 86% reduction). Even though dispinc becomes individually insignificant in the AR(2) model, the lagged carspend terms are essential for explaining the dynamics of car expenditure.

---

## Question 6 Solution (12 pts) — Forecasting by Hand from AR(2)

### Exam likelihood: VERY HIGH

Forecasting by hand appeared on 3/3 past exams. This is the #3 ranked skill. This exact question type — AR(2) with exogenous variable and a data table — is the most common format.

### Reference doc: `exams/study-notes/forecasting-by-hand-deep-dive.md` (Section 2.4: Worked Example — this exact question!)

### Step-by-step solution:

**The model** (from Q4):

$$\text{carspend}_t = 1.576679 + 0.0005992 \cdot \text{disposinc}_t + 0.5777969 \cdot \text{carspend}_{t-1} + 0.3774076 \cdot \text{carspend}_{t-2} + \varepsilon_t$$

**We stand at T = 2002:3** (last observed carspend = 109.192). We want 2002:4 (h=1) and 2003:1 (h=2).

### h = 1: Forecasting 2002:4

**Step 1 — Write the equation at T+1 with variable names:**

$$\text{carspend}_{T+1} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+1} + \hat{\phi}_1 \cdot \text{carspend}_{T} + \hat{\phi}_2 \cdot \text{carspend}_{T-1} + \varepsilon_{T+1}$$

**Step 2 — Apply the rules:**

| Term | Value | Known or future? | Action |
|------|-------|-----------------|--------|
| $\hat{c}$ | 1.576679 | Parameter | Keep |
| $\text{disposinc}_{T+1}$ | 7935.6 (2002:4) | Exogenous, given | Keep |
| $\text{carspend}_T$ | 109.192 (2002:3) | Last observed | Keep |
| $\text{carspend}_{T-1}$ | 102.244 (2002:2) | In the past | Keep |
| $\varepsilon_{T+1}$ | Future shock | Unknown | **= 0** |

**Step 3 — Forecast equation:**

$$\hat{y}_{T+1,T} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+1} + \hat{\phi}_1 \cdot \text{carspend}_{T} + \hat{\phi}_2 \cdot \text{carspend}_{T-1}$$

**Step 4 — Plug in:**

$$\hat{y}_{2002:4} = 1.576679 + 0.0005992 \times 7935.6 + 0.5777969 \times 109.192 + 0.3774076 \times 102.244$$

| Term | Calculation | Result |
|------|------------|--------|
| Constant | | 1.577 |
| disposinc | $0.0005992 \times 7935.6$ | 4.754 |
| L1 (carspend_T) | $0.5777969 \times 109.192$ | 63.10 |
| L2 (carspend_{T-1}) | $0.3774076 \times 102.244$ | 38.59 |
| **Total** | | **108.02** |

$$\boxed{\hat{y}_{2002:4} \approx 108.02}$$

### h = 2: Forecasting 2003:1

**Step 1 — Write the equation at T+2:**

$$\text{carspend}_{T+2} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+2} + \hat{\phi}_1 \cdot \text{carspend}_{T+1} + \hat{\phi}_2 \cdot \text{carspend}_{T} + \varepsilon_{T+2}$$

**Step 2 — Apply the rules:**

| Term | Value | Known or future? | Action |
|------|-------|-----------------|--------|
| $\hat{c}$ | 1.576679 | Parameter | Keep |
| $\text{disposinc}_{T+2}$ | 8039.2 (2003:1) | Exogenous, given | Keep |
| $\text{carspend}_{T+1}$ | 2002:4 | **UNKNOWN — future!** | **Use forecast = 108.02** |
| $\text{carspend}_T$ | 109.192 (2002:3) | Observed (still in past from T+2's perspective) | Keep |
| $\varepsilon_{T+2}$ | Future shock | Unknown | **= 0** |

**Step 3 — Forecast equation:**

$$\hat{y}_{T+2,T} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+2} + \hat{\phi}_1 \cdot \boxed{\hat{y}_{T+1,T}} + \hat{\phi}_2 \cdot \text{carspend}_{T}$$

**Step 4 — Plug in:**

$$\hat{y}_{2003:1} = 1.576679 + 0.0005992 \times 8039.2 + 0.5777969 \times 108.02 + 0.3774076 \times 109.192$$

| Term | Calculation | Result |
|------|------------|--------|
| Constant | | 1.577 |
| disposinc | $0.0005992 \times 8039.2$ | 4.816 |
| L1 (**forecast**) | $0.5777969 \times 108.02$ | 62.42 |
| L2 (carspend_T) | $0.3774076 \times 109.192$ | 41.21 |
| **Total** | | **110.02** |

$$\boxed{\hat{y}_{2003:1} \approx 110.02}$$

**For full credit**: Explicitly state that you replaced carspend at 2002:4 with your FORECAST (108.02), not an actual value. This is the key step the grader looks for.

---

## Question 7 Solution (10 pts) — Why Test for a Unit Root?

### Exam likelihood: HIGH

Pesavento confirmed unit roots will be on the exam. This exact conceptual question appeared on this past exam. Even if she doesn't ask it identically, you need this understanding for any unit root question.

### Reference doc: `exams/study-notes/unit-root-deep-dive.md` (Part 1: Why it matters; Section 8.2: Exam 2 Q7 model answer)

### Step-by-step solution:

This is a short-answer/essay question. Hit these four points:

**Point 1: It determines the correct transformation.**

If the data has a unit root (stochastic trend), we must take first differences to achieve stationarity. If the data is trend stationary, we should detrend instead (include a time trend in the regression). Using the wrong transformation makes things worse:
- Differencing a trend stationary series introduces an MA unit root (non-invertible)
- Detrending a unit root series leaves the variance growing over time (still non-stationary)

**Point 2: It determines how we forecast.**

With a deterministic trend, the forecast converges to the trend line regardless of today's value — the starting point doesn't matter. With a unit root, the forecast depends entirely on today's value — every new data point shifts the entire forecast path. The forecast MSE is finite for trend stationary but grows without bound for a unit root.

**Point 3: It determines whether shocks are permanent or temporary.**

Under trend stationarity, the effect of a shock eventually dies out — the dynamic multiplier goes to zero. Under a unit root, shocks have a permanent effect — the dynamic multiplier converges to $\Psi(1) \neq 0$. This has major policy implications: a policymaker needs to know whether a policy intervention will have a lasting effect or fade away.

**Point 4: Standard inference breaks down.**

Under a unit root, the OLS estimator of $\rho$ does not have a normal distribution. The usual t-statistics and critical values (-1.96) are invalid. Special critical values from the Dickey-Fuller distribution are required, which are more negative than the standard normal values.

---

## Question 8 Solution (5 pts) — Dickey-Fuller Test Interpretation

### Exam likelihood: HIGH

Pesavento said unit roots will be on the exam. DF test interpretation is the practical application. She may give you output like this and ask you to interpret it.

### Reference doc: `exams/study-notes/unit-root-deep-dive.md` (Part 6: Dickey-Fuller test; Section 8.3: This exact question)

### Step-by-step solution:

**Step 1: Choose the correct specification.**

Carspend (car expenditure) is an economic variable that shows an **upward drift over time** — it grows from ~$10 billion in 1959 to ~$120 billion in 2002. This looks like it could be either a deterministic trend or a stochastic trend (random walk with drift). Since there's a visible upward trajectory, we should use the specification **with trend** (intercept and time trend).

**Step 2: Read the test output for the WITH TREND specification.**

- Test statistic: **-1.989**
- 1% Critical Value: -4.017
- 5% Critical Value: **-3.441**
- 10% Critical Value: -3.141
- p-value: **0.6073**

**Step 3: Apply the decision rule.**

Reject the null of a unit root if the test statistic is **more negative** than the critical value.

Is -1.989 more negative than -3.441? **No.** $-1.989 > -3.441$.

We **fail to reject** the null hypothesis of a unit root at the 5% level. (Also fail at 10%: $-1.989 > -3.141$.)

The p-value of 0.6073 confirms — it's nowhere near conventional significance levels.

**Step 4: Conclude.**

The Dickey-Fuller test does not reject the presence of a unit root in carspend. The data appears to have a stochastic trend (unit root with drift). This means:
- We should work with **first differences** ($\Delta$carspend) when modeling
- Shocks to car expenditure have **permanent effects**
- The AR(2) model from Q4 is estimated on levels, which is common in practice but the inference should be interpreted with caution given the unit root evidence
- This is consistent with Q2's finding that the residuals have very persistent serial correlation (the slow ACF decay could partly reflect unit root behavior in the dependent variable)

**Note**: Even the "without trend" specification fails to reject (test stat = -0.309, p = 0.9242). Both specifications point to a unit root.

---

## Summary: What to Prioritize for Tomorrow

| Q | Topic | Exam Likelihood | Points | Your Confidence? |
|---|-------|----------------|--------|-----------------|
| 1 | CI from regression output + economic interpretation | HIGH | 10 | |
| 2 | ACF/PACF identification | VERY HIGH | 5 | |
| 3 | Serial correlation correction (residual diagnostics) | MEDIUM-HIGH | 10 | |
| 4 | CI comparison across models (serial correlation effect) | MEDIUM | 12 | |
| 5 | F-test by hand from regression output | VERY HIGH | 10 | |
| 6 | Forecasting by hand (AR(2), 1-step + 2-step) | VERY HIGH | 12 | |
| 7 | Why test for unit root (conceptual) | HIGH | 10 | |
| 8 | Dickey-Fuller test interpretation | HIGH | 5 | |

**The three highest-value skills for tomorrow**: Forecasting by hand (Q6), F-test (Q5), ACF/PACF identification (Q2). If you nail these three, you're covering ~27 points of almost-certain exam content.
