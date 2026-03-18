# Forecast Evaluation: The Complete Guide

**What this is**: A from-scratch explanation of how to evaluate forecasts — testing whether your forecast is any good (absolute evaluation) and comparing two models (relative evaluation). This covers the Mincer-Zarnowitz regression (EXAM), accuracy measures (MSE/RMSE/MAE), the bias-variance trade-off, and the Diebold-Mariano test.

**How to use this**: Read Parts 1-7 for understanding (45-60 min). On exam morning, skip to the Cheat Sheet at the end.

---

## Lecture Reference Guide

| Topic | File Path | What's There |
|-------|-----------|-------------|
| **Unforecastability principle** | `week-06/Forecasting-evaluation-transcript-feb-19.txt` | "If I can forecast my error, my forecast was not optimal" |
| **Mincer-Zarnowitz regression (EXAM)** | `week-06/Forecasting-evaluation-transcript-feb-19.txt` | Two formulations + naming; `week-06/Forecasts+Evaluation.pdf` slide 5 |
| **Orthogonality test (EXAM)** | `week-06/Forecasts+Evaluation.pdf` slide 5 | General regression test + MZ equivalence |
| **MSE / RMSE / MAE** | `week-06/Forecasts+Evaluation.pdf` slides 6-9 | Formulas + bias-variance decomposition |
| **RMSE is #1 choice** | `week-06/Forecasting-evaluation-transcript-feb-19.txt` | "For sure the number one would be the root mean square error" |
| **Bias-variance trade-off** | `week-06/Forecasts+Evaluation.pdf` slide 9 | MSE = variance + bias²; "sometimes take a little bias" |
| **Predictive R² and Theil U** | `week-06/Forecasts+Evaluation.pdf` slides 10-11 | Benchmarks: historical mean vs random walk |
| **Forecastability** | `week-06/Forecasts+Evaluation.pdf` slide 12 | "Matter of degree, not binary" |
| **Diebold-Mariano test** | `week-06/Forecasts+Evaluation.pdf` slides 13-15 | Full setup + HAC requirement |
| **Southern Company example** | `week-06/Forecasting-evaluation-transcript-feb-19.txt` | "One team did better, but DM test... no significant difference" |
| **Forecast error properties** | `week-06/Forecasts+Evaluation.pdf` slides 1-4 | Review: unbiased, WN at h=1, MA(h-1) at h>1 |
| **Variance inequality** | `week-06/lecture-transcrip.txt` | "Forecast always smoother than actual data" |
| **Market-based forecasts** | `week-06/Forecasts+Evaluation.pdf` slide 16 | Forwards, Fisher equation, VIX |
| **Survey-based forecasts** | `week-06/Forecasting-evaluation-transcript-feb-19.txt` | SPF, Michigan, Livingston |
| **RMSE/MAE exam question** | `exams/past-exams/422oldfinal2.pdf` Q3d | Compare DLDM vs LDM forecast accuracy |

---

## Part 1: The Two Questions of Forecast Evaluation

There are two fundamentally different questions you can ask about a forecast:

### 1.1 Absolute Evaluation: "Is my forecast any good?"

This is about your forecast in isolation. Even if you only have one model, you want to know: are my forecast errors well-behaved? Am I making systematic mistakes? Is the forecast optimal?

**Tools**: Properties of optimal forecasts, Mincer-Zarnowitz regression, orthogonality tests.

### 1.2 Relative Evaluation: "Is Model A better than Model B?"

This is about comparing two (or more) forecasts. Both might be "good" in absolute terms, but you want to know which one is more accurate.

**Tools**: MSE/RMSE/MAE comparison, Diebold-Mariano test.

Pesavento's slides make this distinction explicit (slide 1):
> "We discuss both absolute aspects of forecast evaluation, focusing on methods for checking forecast optimality, and relative aspects, focusing on methods for ranking forecast accuracy, quite apart from optimality."

---

## Part 2: Properties of Optimal Forecasts (What "Good" Means)

Before you can evaluate a forecast, you need to know what an optimal forecast looks like. These properties come from the forecasting theory in the first half of Week 6 — they're the **standards** you check against.

### 2.1 The Four Properties (from slide 3 — Pesavento annotated "EXAM")

**Property 1: Optimal forecasts are unbiased**

$$E[e_{t+h,t}] = 0$$

The forecast error should have mean zero. You shouldn't systematically over-predict or under-predict. If your average error is positive, your forecasts are too low. If negative, too high.

**How to check**: Regress the forecast errors on a constant. The constant should not be significantly different from zero. Pesavento (transcript): *"You take your forecast error, you regress on a constant, and that constant coefficient should be zero."*

**Property 2: 1-step-ahead errors are white noise**

For h=1 forecasts, the errors should be completely random — no serial correlation, no predictable pattern. If you see patterns in 1-step errors, your model missed something.

**How to check**: Durbin-Watson test on errors, or check the ACF of the errors. DW near 2 = good. Pesavento highlights on slide 4: "DW test is an option."

**Property 3: h-step-ahead errors are at most MA(h-1)**

For multi-step forecasts, errors WILL be serially correlated — but at most MA(h-1). This is NOT a sign of a bad model. It's the natural structure we derived in the forecasting deep dive. At h=2, the error is $\varepsilon_{T+2} + b_1\varepsilon_{T+1}$, which is MA(1). At h=3, it's MA(2). And so on.

They should still have zero mean.

**Property 4: Error variance is non-decreasing in h**

$$\sigma_1^2 \leq \sigma_2^2 \leq \sigma_3^2 \leq \cdots \to \text{Var}(y_t)$$

You're always more precise forecasting next period than 10 periods out. The error variance converges to the unconditional variance of the process.

Pesavento's annotation on slide 3: *"you are always more precise in forecasting next month than 10 months from now."*

### 2.2 The Master Property: Unforecastability

All four properties follow from one master principle: **optimal forecast errors should be unforecastable based on information available at the time the forecast was made**.

Pesavento (transcript): *"If I can forecast in any way my forecast error, that means that there was something in the model that I have not exploited in my forecast, and that was left as residuals in my forecast error, and therefore my forecast in the first place was not optimal."*

This holds in **great generality** (slide 2):
- Regardless of whether you use linear projection or conditional mean
- Regardless of whether the loss function is quadratic
- Regardless of whether the series is stationary

If there's ANY predictable pattern in your forecast errors, you should have used that information to make a better forecast.

---

## Part 3: Testing Forecast Optimality — The Mincer-Zarnowitz Regression (EXAM)

This is the formal test for whether your forecast is optimal. Pesavento flagged it with a double star and "Exam" annotation on slide 5.

### 3.1 The General Orthogonality Test

Errors should be orthogonal (uncorrelated) to all available information. Test this by regressing the forecast error on any information you had:

$$e_{t+h,t} = \alpha_0 + \sum_i \alpha_i x_{it} + u_t$$

Do an F-test that all $\alpha$ are jointly zero. If any information variable $x_i$ is significantly related to the forecast error, your model left predictable content on the table.

### 3.2 The MZ Regression — Form 1 (Orthogonality Version)

A special case of the general test: use the forecast itself as the information variable:

$$e_{t+h,t} = \alpha_0 + \alpha_1 \hat{y}_{t+h,t} + u_t$$

**Test**: $H_0: (\alpha_0, \alpha_1) = (0, 0)$ jointly, using an F-test.

Pesavento's annotation on slide 5: *"why should this be zero?"* — because if $\alpha_1 \neq 0$, then your forecast error is correlated with your forecast, meaning you could predict part of your error from your own forecast. That's not optimal.

### 3.3 The MZ Regression — Form 2 (The "Classic" Version)

Equivalent formulation — regress actual values on the forecast:

$$y_{t+h} = \beta_0 + \beta_1 \hat{y}_{t+h,t} + u_t$$

**Test**: $H_0: (\beta_0, \beta_1) = (0, 1)$ jointly, using an F-test.

If $\beta_0 = 0$ and $\beta_1 = 1$, then $y_{t+h} = \hat{y}_{t+h,t} + u_t$, which says the actual value differs from the forecast only by unpredictable noise — exactly the optimality condition.

Pesavento (transcript): *"If you regress your forecast error on your forecast, these two coefficients should all be zero... It's called the Mincer-Zarnowitz regression."*

### 3.4 How the Two Forms are Equivalent

Start from Form 2: $y_{t+h} = \beta_0 + \beta_1 \hat{y}_{t+h,t} + u_t$

Subtract $\hat{y}_{t+h,t}$ from both sides:

$$y_{t+h} - \hat{y}_{t+h,t} = \beta_0 + (\beta_1 - 1)\hat{y}_{t+h,t} + u_t$$

$$e_{t+h,t} = \beta_0 + (\beta_1 - 1)\hat{y}_{t+h,t} + u_t$$

Set $\alpha_0 = \beta_0$ and $\alpha_1 = \beta_1 - 1$. Then $(\beta_0, \beta_1) = (0, 1)$ is the same as $(\alpha_0, \alpha_1) = (0, 0)$.

This is what the slide means by *"To get from one to the other, subtract $\hat{y}_{t+h,t}$ from each side of the MZ regression."*

### 3.5 How to Interpret the Results

| Result | What It Means |
|--------|---------------|
| $\beta_0 \neq 0$, $\beta_1 = 1$ | Forecast has a **constant bias** — it's systematically too high or too low by a fixed amount |
| $\beta_0 = 0$, $\beta_1 \neq 1$ | Forecast has a **scaling problem** — it moves in the right direction but by the wrong amount |
| $\beta_1 < 1$ | Forecast is **too smooth** — it doesn't swing enough relative to actuals (this is common and mild) |
| $\beta_1 > 1$ | Forecast is **too volatile** — it overreacts (less common, more concerning) |
| $\beta_0 = 0$, $\beta_1 = 1$ | Forecast is **optimal** — errors are just unpredictable noise |

**Why $\beta_1 < 1$ means "too smooth"**: Think about it concretely. If $\beta_1 = 0.8$, the regression says $y_{t+h} = 0.8 \hat{y}_{t+h,t} + \text{noise}$. When the forecast moves by 10, the actual only moves by 8 on average. But wait — that means the forecast is moving MORE than the actual. The forecast swings by 10, but reality only swings by 8. So the forecast is... too volatile? No! Flip it: the forecast predicts a movement of 10, but the coefficient says reality is 0.8 times the forecast. This means the forecast overshoots — for every unit the forecast moves, reality moves less. The forecast thinks the data is swinging more than it actually is.

Actually, let's think about it the more intuitive way. $\beta_1 < 1$ means: when actuals go up by 1, the forecast only went up by less than 1. The forecast **under-reacted** — it didn't swing enough. The forecast was too flat, too smooth.

### 3.6 The F-Test for MZ: Why You Need It (Not Just Individual t-tests)

You might think: "I'll just check if $\beta_0$ is significantly different from 0 (t-test) and if $\beta_1$ is significantly different from 1 (t-test). If both pass, the forecast is optimal."

**This is not enough.** Pesavento's slides show the **joint** test — both conditions must hold **simultaneously**. It's possible that neither coefficient is individually significant, but they're jointly significant (or vice versa). The F-test captures the joint restriction.

**The analogy**: An F-test is like checking whether two suspects together could have committed the crime, even if neither one alone has enough evidence.

### 3.7 How to Compute the F-Test by Hand

The F-test for the MZ regression tests $q = 2$ restrictions: $\beta_0 = 0$ AND $\beta_1 = 1$.

**The general F-test formula** (this is the same formula from Exam 2 Q5 and Exam 3 Q1b/Q1e — it appears on every past exam):

$$F = \frac{(SSR_R - SSR_U) / q}{SSR_U / (n - k_U)}$$

where:
- $SSR_R$ = Sum of Squared Residuals from the **restricted** model (imposing $H_0$)
- $SSR_U$ = Sum of Squared Residuals from the **unrestricted** model (estimated freely)
- $q$ = number of restrictions (for MZ: $q = 2$)
- $n$ = number of observations
- $k_U$ = number of parameters in the unrestricted model (for MZ: $k_U = 2$, which is $\beta_0$ and $\beta_1$)

Under $H_0$: $F \sim F(q, n - k_U)$. Reject if $F > F_{\text{critical}}$.

#### What is the "restricted model" for MZ?

Under $H_0: (\beta_0, \beta_1) = (0, 1)$, the MZ regression becomes:

$$y_{t+h} = 0 + 1 \cdot \hat{y}_{t+h,t} + u_t \quad \Rightarrow \quad y_{t+h} - \hat{y}_{t+h,t} = u_t \quad \Rightarrow \quad e_{t+h,t} = u_t$$

The restricted model says: the forecast error is just pure noise — no constant, no slope. The restricted $SSR_R$ is simply:

$$SSR_R = \sum_{t=1}^{n} e_{t+h,t}^2 = \sum_{t=1}^{n} (y_{t+h} - \hat{y}_{t+h,t})^2$$

That's just the **sum of squared forecast errors**! You don't even need to run a regression — it's the forecast errors you already have, squared and summed.

The unrestricted $SSR_U$ comes from running the MZ regression $y_{t+h} = \beta_0 + \beta_1 \hat{y}_{t+h,t} + u_t$ and reading $SSR_U$ = "Sum squared resid" from the output.

### 3.8 Full Worked Example #1: MZ from Regression Output

**Scenario**: You forecast quarterly GDP growth and want to test if your forecasts are optimal. You have $n = 40$ forecast-actual pairs. You run the MZ regression and get this output:

```
Dependent Variable: ACTUAL_GDP_GROWTH
Method: Least Squares
Included observations: 40

Variable     Coefficient   Std. Error    t-Statistic    Prob.
C              0.320        0.155         2.065         0.0460
FORECAST       0.850        0.072         11.806        0.0000

R-squared        0.786
Sum squared resid  12.450    ← This is SSR_U
```

**Step 1: Read off the coefficients and their individual t-tests.**

- $\hat{\beta}_0 = 0.320$ (SE = 0.155)
- $\hat{\beta}_1 = 0.850$ (SE = 0.072)

**Step 2: Individual tests (informative but not sufficient)**

Test $\beta_0 = 0$: $t = 0.320 / 0.155 = 2.065$, p = 0.046. **Significant at 5%.** There's evidence of constant bias — the forecast is systematically about 0.32 percentage points too low.

Test $\beta_1 = 1$: $t = (0.850 - 1) / 0.072 = -0.150 / 0.072 = -2.083$. Compare to $\pm 1.96$ (or $\pm 2.02$ for df = 38). **Significant at 5%.** The coefficient is significantly below 1 — the forecast is too smooth (under-reacts).

**Step 3: Compute the F-test for the joint hypothesis $(\beta_0, \beta_1) = (0, 1)$.**

First, I need $SSR_R$. Under $H_0$, the restricted model is $y_{t+h} = \hat{y}_{t+h,t} + u_t$, so $SSR_R = \sum e_{t+h,t}^2 = \sum(y_{t+h} - \hat{y}_{t+h,t})^2$.

Suppose you're told (or can compute from the forecast errors) that $SSR_R = 18.200$.

Now plug into the F formula:

$$F = \frac{(SSR_R - SSR_U) / q}{SSR_U / (n - k_U)} = \frac{(18.200 - 12.450) / 2}{12.450 / (40 - 2)} = \frac{5.750 / 2}{12.450 / 38} = \frac{2.875}{0.3276} = 8.78$$

**Step 4: Compare to critical value.**

$F(2, 38)$ at 5%: approximately 3.24 (from F-table). Since 8.78 > 3.24, we **reject $H_0$**.

**Step 5: Conclude.**

The forecast is NOT optimal. There is a combination of constant bias ($\beta_0 = 0.32$, forecasts too low) and under-reaction ($\beta_1 = 0.85$, forecasts too smooth). The forecaster could improve by: (a) adding 0.32 to all forecasts, and (b) scaling forecasts to be more responsive to changes.

### 3.9 Full Worked Example #2: MZ When the Forecast IS Optimal

**Scenario**: Same setup, but different output:

```
Dependent Variable: ACTUAL_GDP_GROWTH
Included observations: 40

Variable     Coefficient   Std. Error    t-Statistic    Prob.
C              0.085        0.180         0.472         0.6395
FORECAST       0.965        0.080         12.063        0.0000

Sum squared resid  15.800    ← SSR_U
```

$SSR_R = 16.500$ (from the raw forecast errors).

**Individual tests:**

Test $\beta_0 = 0$: $t = 0.085/0.180 = 0.472$, p = 0.64. **Not significant.** No evidence of constant bias.

Test $\beta_1 = 1$: $t = (0.965 - 1)/0.080 = -0.035/0.080 = -0.438$. **Not significant.** No evidence of under/over-reaction.

**F-test:**

$$F = \frac{(16.500 - 15.800) / 2}{15.800 / 38} = \frac{0.700 / 2}{0.4158} = \frac{0.350}{0.4158} = 0.84$$

$F(2, 38)$ at 5% = 3.24. Since 0.84 < 3.24, we **fail to reject $H_0$**.

**Conclusion**: The forecast passes the MZ optimality test. There is no evidence of systematic bias or inefficiency. The forecast errors appear to be unpredictable noise — exactly what we want.

### 3.10 Full Worked Example #3: Using the Orthogonality Form

Sometimes the exam uses Form 1 instead. Same data, but now:

$$e_{t+h,t} = \alpha_0 + \alpha_1 \hat{y}_{t+h,t} + u_t$$

**Test**: $H_0: (\alpha_0, \alpha_1) = (0, 0)$.

This is actually **easier** to test because the null is that all coefficients are zero — and the standard regression F-statistic from the output directly tests this!

```
Dependent Variable: FORECAST_ERROR
Included observations: 40

Variable     Coefficient   Std. Error    t-Statistic    Prob.
C              0.320        0.155         2.065         0.0460
FORECAST      -0.150        0.072        -2.083         0.0441

R-squared        0.103
F-statistic      4.35
Prob(F-stat)     0.0200
```

The F-statistic from the output (4.35, p = 0.020) **directly tests** $H_0: \alpha_0 = \alpha_1 = 0$. Since p = 0.020 < 0.05, we **reject** — the forecast is not optimal.

Notice: $\alpha_0 = 0.320 = \beta_0$ (same bias), and $\alpha_1 = -0.150 = \beta_1 - 1 = 0.850 - 1$ (the under-reaction, reframed as the error being predictable from the forecast). Same answer, different framing.

**Exam tip**: If you're given the orthogonality form ($e$ on $\hat{y}$), the F-statistic in the output IS the MZ test — you don't need to compute anything. If you're given the classic form ($y$ on $\hat{y}$), you need to do the restricted-unrestricted SSR computation because the null is $(\beta_0, \beta_1) = (0, 1)$, not $(0, 0)$.

### 3.11 Quick Reference: What Exam Questions Look Like

**Format A (most likely)**: "Here is regression output from the MZ regression. Test whether the forecast is optimal."

→ Read $\hat{\beta}_0$, $\hat{\beta}_1$ and their SEs. Do individual t-tests ($\beta_0 = 0$? $\beta_1 = 1$?). If asked for joint test, compute F from SSR values.

**Format B**: "Here are forecast errors and forecasts. Run the orthogonality regression."

→ Set up $e_{t+h,t} = \alpha_0 + \alpha_1 \hat{y}_{t+h,t} + u_t$. The output's built-in F-stat tests $H_0: \alpha_0 = \alpha_1 = 0$ directly.

**Format C**: "Is this forecast optimal? Explain what you would test and how."

→ Write the MZ regression, state the null, explain the F-test, interpret $\beta_0$ and $\beta_1$.

### 3.12 Step-by-Step Exam Procedure for MZ

```
MINCER-ZARNOWITZ ON THE EXAM — STEP BY STEP

1. WRITE the regression:
   y_{t+h} = β₀ + β₁·ŷ_{t+h|t} + u_t

2. STATE the null:
   H₀: (β₀, β₁) = (0, 1)    "forecast is optimal"

3. INDIVIDUAL t-tests (from output):
   β₀ = 0?  →  t = β̂₀ / SE(β̂₀)  →  compare to ±1.96
   β₁ = 1?  →  t = (β̂₁ - 1) / SE(β̂₁)  →  compare to ±1.96

4. INTERPRET each:
   β̂₀ > 0 significant → forecast is too LOW (positive bias)
   β̂₀ < 0 significant → forecast is too HIGH (negative bias)
   β̂₁ < 1 significant → forecast too SMOOTH (under-reacts)
   β̂₁ > 1 significant → forecast too VOLATILE (over-reacts)

5. JOINT F-test (if asked):
   SSR_R = Σ(y_{t+h} - ŷ_{t+h|t})² = Σe²  (sum of squared forecast errors)
   SSR_U = "Sum squared resid" from MZ regression output

   F = [(SSR_R - SSR_U) / 2] / [SSR_U / (n - 2)]

   Compare to F(2, n-2) critical value.

6. CONCLUDE:
   Reject → forecast NOT optimal, there's systematic bias/inefficiency
   Fail to reject → forecast appears optimal, errors are unpredictable
```

### 3.13 Common MZ Mistakes

**Mistake 1**: Testing $\beta_1 = 0$ instead of $\beta_1 = 1$.

The null for the slope is NOT that it equals zero. The null is $\beta_1 = 1$. To test this, compute $t = (\hat{\beta}_1 - 1) / SE(\hat{\beta}_1)$. Don't use the p-value from the regression output — that p-value tests $\beta_1 = 0$, which is a different (and irrelevant) hypothesis.

**Mistake 2**: Using only individual t-tests and ignoring the joint F-test.

Each coefficient might look fine individually, but the joint test can reject (or vice versa). The F-test is the proper test. If the exam asks "is this forecast optimal?" you need the joint test.

**Mistake 3**: Confusing the two forms of MZ.

If the exam sets up $e = \alpha_0 + \alpha_1 \hat{y} + u$, then $H_0: (\alpha_0, \alpha_1) = (0, 0)$, and the output's F-stat tests this directly. If it sets up $y = \beta_0 + \beta_1 \hat{y} + u$, then $H_0: (\beta_0, \beta_1) = (0, 1)$, and the output's F-stat does NOT test this — you need the restricted SSR.

**Mistake 4**: Forgetting what $SSR_R$ is for MZ.

The restricted model under $H_0$ forces $y_{t+h} = \hat{y}_{t+h,t} + u_t$. That means $SSR_R = \sum(y_{t+h} - \hat{y}_{t+h,t})^2$ — the sum of squared raw forecast errors. You don't run a separate regression; you just square the forecast errors and add them up.

---

## Part 4: Accuracy Measures — How to Score a Forecast

Once you've checked whether your forecast is optimal (absolute evaluation), you need measures to **quantify** how good it is and **compare** it to alternatives.

### 4.1 Forecast Bias

$$\hat{\mu}_e = \frac{1}{T}\sum_{t=1}^{T} e_{t+h,t}$$

The average forecast error. Should be zero for an optimal forecast. If positive, you're under-predicting on average. If negative, over-predicting.

### 4.2 Error Variance

$$\hat{\sigma}^2_e = \frac{1}{T}\sum_{t=1}^{T} (e_{t+h,t} - \hat{\mu}_e)^2$$

How spread out your errors are around their mean. Even if your forecast is unbiased (mean error = 0), the errors could still be large and variable.

### 4.3 Mean Squared Error (MSE)

The key measure. Pesavento's annotation on slide 8: "measure of accuracy."

$$\widehat{MSE} = \frac{1}{T}\sum_{t=1}^{T} e_{t+h,t}^2$$

MSE captures both bias and variance in a single number. Lower MSE = better forecast.

### 4.4 The Bias-Variance Decomposition (IMPORTANT)

$$MSE = \sigma^2_e + \mu^2_e$$

In words: **MSE = Error Variance + Bias Squared**

Pesavento's annotations on slide 9: "bias" (pointing to $\mu^2_e$), "variance" (pointing to $\sigma^2_e$), "small MSE is good."

**Why this matters**: A forecast can have low MSE in two ways:
- Small bias AND small variance (ideal)
- Small variance but some bias (acceptable if variance reduction is large enough)

Pesavento (transcript): *"Sometimes you may be willing to take a little bit of bias if it gives you a much, much smaller variance. So sometimes, even if you have a little bit of bias, you may have a smaller mean square error between two different forecasts."*

**Example**: Suppose Model A is unbiased ($\mu = 0$, $\sigma^2 = 10$) → MSE = 10. Model B has small bias ($\mu = 0.5$, $\sigma^2 = 7$) → MSE = 7.25. **Model B is better on MSE** despite being biased, because the variance reduction more than compensates.

### 4.5 Root Mean Squared Error (RMSE)

$$\widehat{RMSE} = \sqrt{\widehat{MSE}} = \sqrt{\frac{1}{T}\sum_{t=1}^{T} e_{t+h,t}^2}

Pesavento's annotation on slide 8: "same unit of forecast."

This is just the square root of MSE. The advantage: it's in the **same units as the variable you're forecasting**. If you're forecasting GDP growth in percent, RMSE is also in percent — easier to interpret.

Pesavento (transcript): *"For sure the number one would be the root mean square error."* This is the go-to measure for this course.

### 4.6 Mean Absolute Error (MAE)

$$\widehat{MAE} = \frac{1}{T}\sum_{t=1}^{T} |e_{t+h,t}|$$

Pesavento's annotation on slide 9: "sum of absolute value of errors."

Less popular than RMSE. The key difference: MAE does not penalize large errors as heavily as MSE/RMSE (because it doesn't square them). This makes MAE more robust to outliers.

**When to use MAE over RMSE**: If you have a few extreme forecast errors (like COVID quarters) that dominate the MSE, MAE gives a more representative picture of typical forecast performance.

### 4.7 Summary of Measures

| Measure | Formula | Units | Penalizes big errors? | Professor's take |
|---------|---------|-------|-----------------------|-----------------|
| MSE | $(1/T)\sum e^2$ | Squared units | Yes (heavily) | "Very popular" |
| RMSE | $\sqrt{MSE}$ | Same as forecast | Yes (heavily) | "Number one" |
| MAE | $(1/T)\sum |e|$ | Same as forecast | No (linear penalty) | "Less popular but still used" |
| Bias | $(1/T)\sum e$ | Same as forecast | N/A | Check first |

---

## Part 5: Benchmarking — Predictive R² and Theil's U

These measures answer: "Is my model better than a **naive** benchmark?"

### 5.1 Predictive R²

$$R^2 = 1 - \frac{\sum_{t=1}^{T} e^2_{t,t-1}}{\sum_{t=1}^{T} (y_t - \bar{y})^2}$$

**Benchmark**: the historical mean $\bar{y}$ (always guess the average).

**Numerator**: your model's 1-step-ahead forecast errors (OOS).
**Denominator**: how far the actual data is from the mean (variance of $y$).

Pesavento's annotation on slide 10: denominator is "variance of y's."

**Interpretation**: If Predictive $R^2$ is near 1, your model is much better than just guessing the mean. If near 0, your model adds little forecasting value beyond the mean.

### 5.2 Theil's U-Statistic

$$U = 1 - \frac{\sum_{t=1}^{T} e^2_{t,t-1}}{\sum_{t=1}^{T} (y_t - y_{t-1})^2}$$

**Benchmark**: the "no-change" forecast $y_{t-1}$ (random walk — always guess yesterday's value).

Pesavento's annotation on slide 11: "stick to MSE or RMSE" — suggesting Theil U is less important for this course.

**Critical caveat** from the slides: *"It is important to note that allegedly-naive benchmarks may not be so naive. For example, many economic variables may in fact be nearly random walks, in which case forecasters will have great difficulty beating the random walk through no fault of their own."*

In other words: if Theil's U is near 0, it might just mean the variable is close to a random walk, not that your model is bad. Don't panic.

---

## Part 6: Comparing Two Models — The Diebold-Mariano Test

This is the most important concept in relative forecast evaluation. It appeared on Pesavento's annotated slides and she spent significant lecture time on it.

### 6.1 The Problem

You have Model A and Model B. Model A has RMSE = 1.32, Model B has RMSE = 1.71. Model A looks better. But is the difference **statistically significant**, or just noise?

Pesavento (transcript): *"Simply looking at the mean square error, one team did better, but when we tested the difference, there was no significant difference."*

**The key insight**: Forecast errors are **random variables**. The MSE is a function of random variables. So the difference in MSEs between two models is **also a random variable**. It will never be exactly zero, even if both models are equally good. You need a formal test.

### 6.2 Setup

**Step 1**: Compute the loss for each model at each time point.

Under quadratic loss: $L(e^a_{t+h,t}) = (e^a_{t+h,t})^2$ and $L(e^b_{t+h,t}) = (e^b_{t+h,t})^2$

**Step 2**: Compute the loss differential.

$$d_{12t} = L(e^a_{t+h,t}) - L(e^b_{t+h,t}) = (e^a_{t+h,t})^2 - (e^b_{t+h,t})^2$$

This is the difference in squared errors at each time point. Sometimes $d_t$ is positive (Model B was better that period), sometimes negative (Model A was better).

**Step 3**: Test whether the average loss differential is zero.

$$H_0: E(d_{12t}) = 0 \quad \text{(equal predictive accuracy)}$$
$$H_1: E(d_{12t}) \neq 0 \quad \text{(one model is better)}$$

### 6.3 The DM Statistic

$$DM_{12} = \frac{\bar{d}_{12}}{\hat{\sigma}_{\bar{d}_{12}}} \rightarrow N(0, 1)$$

where $\bar{d}_{12} = \frac{1}{T}\sum_{t=1}^{T} d_{12t}$ is the sample mean loss differential.

Pesavento's annotation on slide 14: "distributed normally."

**This is just a t-test**. The DM test is nothing more than a t-test for whether the mean of a series ($d_t$) is zero. Pesavento says so explicitly (transcript): *"DM is simply an asymptotic z-test of the hypothesis that the mean of a constructed but observed series (the loss differential) is zero."*

### 6.4 Why You Need HAC Standard Errors

The denominator $\hat{\sigma}_{\bar{d}_{12}}$ is the standard error of $\bar{d}_{12}$. But there's a subtlety: if you're doing multi-step forecasts (h > 1), the forecast errors are serially correlated (they're MA(h-1)). That means the loss differentials $d_t$ may also be serially correlated.

From slide 15: *"Since the forecast errors, and hence loss differentials, may be serially correlated, the standard error in the denominator of the DM statistic should be calculated robustly."*

**Two approaches** (from slide 15):
1. Recognize DM is a t-statistic and use **HAC standard errors** (Newey-West)
2. Regress $d_t$ on a constant, allow for AR(p) disturbances, select p by AIC

### 6.5 Interpreting the Result

| Result | Interpretation |
|--------|---------------|
| Reject $H_0$ ($|DM| > 1.96$) | One model is **significantly** better than the other |
| Fail to reject ($|DM| < 1.96$) | Models have **equal predictive ability** — cannot distinguish them |
| $DM > 0$ and significant | Model A has larger losses → **Model B wins** |
| $DM < 0$ and significant | Model B has larger losses → **Model A wins** |

### 6.6 The Southern Company Story

Pesavento's motivating example (transcript):

Three student teams forecast electricity demand for Southern Company. Each team had a different MSE. One team appeared to win.

But when they ran the DM test: *"From a pure pointwise view, simply looking at the mean square error, one team did better, but when we tested the difference, there was no significant difference. At the end, they all did very well."*

**The lesson**: You cannot eyeball MSE differences. The DM test is the proper way to compare. A 10% RMSE improvement might be significant or might be noise — only the DM test can tell you.

### 6.7 Simple Implementation

The simplest way to compute DM in practice:

1. Compute $d_t = e^2_{A,t} - e^2_{B,t}$ for each period
2. Run the regression: $d_t = \alpha + u_t$, using HAC standard errors
3. The t-statistic on $\alpha$ IS the DM test statistic
4. If $|t| > 1.96$ (or check p-value < 0.05), reject equal predictive ability

---

## Part 7: Market and Survey Forecasts (Self-Study Material)

Pesavento told the class to read these slides on their own: *"The second part of the slide is very talky, and so I'm going to let you read them through."*

### 7.1 Market-Based Forecasts

Financial markets aggregate forward-looking information from participants with "real money on the line." Useful sources:

| Source | What It Forecasts | Formula |
|--------|-------------------|---------|
| Forward exchange rates | Future spot rate | $F_t(t+h) = E_t(S_{t+h})$ (under risk neutrality) |
| Bond yield spread | Expected inflation | $i_t = r_t + E_t(\pi_{t+h})$ (Fisher equation) |
| VIX | Market volatility | — |
| Futures markets | Commodities, rates, energy | — |

Pesavento (transcript): *"If you put something like the S&P 500 on your right hand side, it's going to turn out to be helpful for forecasting... it's not a causal relationship, but helpful in forecasting, because the market anticipates what's going to happen."*

**Key principle**: Markets don't CAUSE outcomes — they ANTICIPATE them. The predictive relationship is through information aggregation, not causation.

### 7.2 Survey-Based Forecasts

| Survey | Maintained By | Frequency | Key Use |
|--------|---------------|-----------|---------|
| Survey of Professional Forecasters (SPF) | Philadelphia Fed | Quarterly | Macro consensus |
| Livingston Survey | Philadelphia Fed | Semi-annual | Long history (50+ years) |
| Michigan Consumer Survey | Univ. of Michigan | Monthly | Household inflation expectations |

Pesavento specifically connected Michigan to the BofA project: *"If you need to think about inflation for your consumer loans, there is data — University of Michigan — individual forecasts are all over the place, but on average, they do pretty well."*

**Key principle**: Individual survey responses are noisy, but the **consensus** (average) often performs surprisingly well.

---

## Worked Examples from Past Exams

### Exam 1 Q3d: RMSE/MAE Comparison (10 pts)

**Given**: Forecast output for two models of the DM/Dollar exchange rate:
- DLDM (first differences): RMSE = 0.028, MAE = 0.022
- LDM (levels): RMSE = 0.144, MAE = 0.107

**Question**: Which model gives the best forecasts?

**Answer**: DLDM wins on both metrics — dramatically lower RMSE and MAE. The level model (LDM) has near-unit-root behavior, so forecasting in levels accumulates errors over time. Differencing removes the unit root, making the series much more forecastable.

**On the exam**: When both RMSE and MAE agree, just state the winner. If they disagree, discuss the trade-off: RMSE penalizes large errors more (quadratic loss); MAE treats all errors equally (absolute loss).

### Hypothetical Exam Question: Mincer-Zarnowitz

**Given**: You ran the regression $y_{t+1} = \beta_0 + \beta_1 \hat{y}_{t+1,t} + u_t$ and got:
- $\hat{\beta}_0 = 0.52$ (SE = 0.31, p = 0.10)
- $\hat{\beta}_1 = 0.85$ (SE = 0.12, p = 0.00)
- Joint F-test: F = 3.42, p = 0.04

**Answer**:
1. $\beta_0 = 0.52$ is marginally significant — slight evidence of constant bias (forecast systematically too low by ~0.52 units)
2. $\beta_1 = 0.85 < 1$ — the forecast is too smooth. When actuals move by 1 unit, the forecast only moves by 0.85. This is common and mild.
3. Joint test: F = 3.42 with p = 0.04 → **reject** forecast optimality at 5%. The forecast is not fully optimal — there's a combination of mild bias and under-reaction.
4. However, this doesn't mean the forecast is useless. It means there's room for improvement, perhaps by adjusting the model to be more responsive.

---

## Common Exam Traps

### Trap 1: Comparing MSEs without the DM test

**Wrong**: "Model A has RMSE = 1.32 and Model B has RMSE = 1.71, so Model A is better."

**Right**: "Model A has a lower RMSE, but we need the Diebold-Mariano test to determine if this difference is statistically significant. The DM test accounts for the fact that forecast errors are random variables."

Pesavento made this point repeatedly with the Southern Company example.

### Trap 2: Thinking bias is always bad

**Wrong**: "Model B has a nonzero bias, so it's worse."

**Right**: Check the MSE. $MSE = \text{bias}^2 + \text{variance}$. A biased model with much lower variance can have lower MSE than an unbiased model with high variance.

### Trap 3: Confusing the two MZ forms

**Form 1** (orthogonality): $e_{t+h,t} = \alpha_0 + \alpha_1 \hat{y}_{t+h,t} + u_t$ → test $(\alpha_0, \alpha_1) = (0, 0)$

**Form 2** (classic MZ): $y_{t+h} = \beta_0 + \beta_1 \hat{y}_{t+h,t} + u_t$ → test $(\beta_0, \beta_1) = (0, 1)$

These are equivalent — you get from one to the other by subtracting $\hat{y}_{t+h,t}$ from both sides. On the exam, use whichever form the question sets up.

### Trap 4: Expecting forecast to match actual data

The variance inequality guarantees $\text{Var}(\hat{y}) < \text{Var}(y)$. Forecasts are ALWAYS smoother than reality. When you plot them together, the forecast line won't swing as much. This is mathematically correct, not a model failure.

### Trap 5: Forgetting HAC standard errors in DM

Multi-step forecast errors are MA(h-1) → loss differentials may be serially correlated → standard errors must be HAC (robust). Using regular OLS standard errors in the DM test overstates significance.

### Trap 6: Misinterpreting Theil's U near zero

Theil's U benchmarks against the random walk ($y_{t-1}$). Many economic variables are near-random-walks, so U near 0 might mean the variable is inherently hard to beat, not that your model is bad. Pesavento on slide 11: *"the predictive R² relative to a random walk 'no-change' forecast given by Theil's U may be near 0!"*

### Trap 7: Thinking h-step errors should be white noise

Only 1-step-ahead errors should be white noise. Multi-step errors are MA(h-1) by construction — this serial correlation is expected. Check that errors have zero mean, not that they're uncorrelated at all lags.

---

## How Everything Connects

```
FORECAST EVALUATION FRAMEWORK

                    ┌─────────────────────────────────┐
                    │  ABSOLUTE: Is my forecast good?  │
                    └────────────┬────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
  Properties of           Mincer-Zarnowitz        Accuracy
  Optimal Errors          Regression (EXAM)       Measures
  ──────────────          ─────────────────       ────────
  • Mean zero             Form 1: e = α₀+α₁ŷ+u  • Bias
  • WN at h=1             Test: (α₀,α₁)=(0,0)    • Variance
  • MA(h-1) at h>1                                • MSE = σ²+μ²
  • Var grows with h      Form 2: y = β₀+β₁ŷ+u   • RMSE (⭐#1)
                          Test: (β₀,β₁)=(0,1)    • MAE

                    ┌─────────────────────────────────┐
                    │  RELATIVE: Which model is better?│
                    └────────────┬────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
  Compare RMSE/MAE       Diebold-Mariano         Benchmarking
  (not sufficient         Test                    ────────────
   by itself!)            ──────────────          • Pred R² (vs mean)
                          d_t = e²_A - e²_B      • Theil U (vs RW)
  "One team did           DM = d̄/σ̂_d̄ → N(0,1)
   better, but            Use HAC standard errors!
   DM test showed         Reject → one is better
   no significant         Fail to reject → equal
   difference"
```

---

## Cheat Sheet (Exam Morning Review)

```
================================================================
        FORECAST EVALUATION — EVERYTHING ON ONE PAGE
================================================================

PROPERTIES OF OPTIMAL FORECASTS
  1. Unbiased: E[error] = 0
  2. 1-step errors = white noise (check DW, ACF)
  3. h-step errors ≤ MA(h-1) (serial corr is EXPECTED)
  4. Error variance non-decreasing in h
  Master: errors should be UNFORECASTABLE

================================================================
MINCER-ZARNOWITZ (EXAM — know both forms!)

  Form 1:  e_{t+h} = α₀ + α₁ŷ_{t+h|t} + u
           Test: (α₀, α₁) = (0, 0)
           → Output F-stat tests this DIRECTLY

  Form 2:  y_{t+h} = β₀ + β₁ŷ_{t+h|t} + u
           Test: (β₀, β₁) = (0, 1)
           → Must compute F by hand (restricted SSR method)

  Equivalent: subtract ŷ from both sides of Form 2

  Individual t-tests:
    β₀ = 0?  t = β̂₀ / SE(β̂₀)
    β₁ = 1?  t = (β̂₁ - 1) / SE(β̂₁)    ⚠ NOT β₁ = 0!

  β₀ ≠ 0 → constant bias
  β₁ < 1 → forecast too smooth (under-reacts)
  β₁ > 1 → forecast too volatile (over-reacts)

  Joint F-test (Form 2):
    SSR_R = Σ(actual - forecast)² = Σe²  (just the forecast errors!)
    SSR_U = "Sum squared resid" from MZ regression output
    F = [(SSR_R - SSR_U) / 2] / [SSR_U / (n - 2)]
    Compare to F(2, n-2) critical value

  Reject → forecast NOT optimal
  Fail to reject → forecast appears optimal

================================================================
ACCURACY MEASURES

  Bias  = (1/T)Σe                    (should be ≈ 0)
  MSE   = (1/T)Σe²                  (lower = better)
  MSE   = σ² + μ²                   (variance + bias²)
  RMSE  = √MSE                      (⭐ Professor's #1)
  MAE   = (1/T)Σ|e|                 (robust to outliers)

  Bias-variance trade-off:
    "Sometimes willing to take a little bias
     if it gives much smaller variance" — Pesavento

================================================================
BENCHMARKS

  Pred R² = 1 - Σe²/Σ(y-ȳ)²        (vs historical mean)
  Theil U = 1 - Σe²/Σ(y-y_{t-1})²  (vs random walk)
  ⚠ Theil U ≈ 0 may just mean variable ≈ random walk

  Professor: "Stick to MSE or RMSE"

================================================================
DIEBOLD-MARIANO TEST (comparing Model A vs Model B)

  1. d_t = e²_A,t - e²_B,t          (loss differential)
  2. DM = d̄ / σ̂_d̄ → N(0,1)         (t-test on d̄)
  3. Use HAC standard errors!
  4. |DM| > 1.96 → reject equal predictive ability
  5. Cannot just compare raw MSEs!

  Southern Company lesson:
    "One team did better on MSE, but DM showed
     no significant difference"

================================================================
MARKET & SURVEY FORECASTS (self-study)

  Markets: forwards, Fisher eq (i = r + E[π]), VIX
    "Not causal — market anticipates"
  Surveys: SPF, Michigan (inflation expectations)
    "Individual forecasts all over, but average does well"

================================================================
EXAM PROCEDURE

  If asked "evaluate this forecast":
    1. Check bias (mean error ≈ 0?)
    2. Run MZ regression, test (β₀,β₁) = (0,1)
    3. Report RMSE

  If asked "compare Model A vs Model B":
    1. Report both RMSEs
    2. Compute % improvement
    3. Run DM test
    4. State whether difference is significant
================================================================
```

---

## Practice Problems

### Practice 1: Identify the Better Forecast
Model A: errors = {2, -1, 3, -2, 1, -3}
Model B: errors = {1, -1, 2, -1, 0, -2}

Compute MSE, RMSE, and MAE for both. Which is better?

<details>
<summary>Solution</summary>

**Model A:**
- MSE = (4+1+9+4+1+9)/6 = 28/6 = 4.667
- RMSE = √4.667 = 2.160
- MAE = (2+1+3+2+1+3)/6 = 12/6 = 2.000

**Model B:**
- MSE = (1+1+4+1+0+4)/6 = 11/6 = 1.833
- RMSE = √1.833 = 1.354
- MAE = (1+1+2+1+0+2)/6 = 7/6 = 1.167

Model B wins on all three measures. RMSE improvement: (2.160-1.354)/2.160 = 37.3%.

(But remember — to formally claim B is better, you'd need the DM test!)
</details>

### Practice 2: Bias-Variance Trade-off
Model A: unbiased, error variance = 16 → MSE = ?
Model B: bias = 1.5, error variance = 10 → MSE = ?

<details>
<summary>Solution</summary>

**Model A:** MSE = 0² + 16 = 16
**Model B:** MSE = 1.5² + 10 = 2.25 + 10 = 12.25

Model B has **lower MSE** despite being biased! The variance reduction (16 → 10) more than compensates for the bias penalty (0 → 2.25). This is Pesavento's point: "sometimes willing to take a little bias if it gives much smaller variance."
</details>

### Practice 3: MZ Individual t-tests
You run: $y_{t+1} = 0.3 + 0.92 \hat{y}_{t+1,t} + u_t$

SE($\hat{\beta}_0$) = 0.18, SE($\hat{\beta}_1$) = 0.06

Are the individual coefficients consistent with optimality?

<details>
<summary>Solution</summary>

**Test $\beta_0 = 0$**: $t = 0.3/0.18 = 1.67$. Not significant at 5% ($|t| < 1.96$). No strong evidence of constant bias.

**Test $\beta_1 = 1$**: $t = (0.92 - 1)/0.06 = -0.08/0.06 = -1.33$. Not significant at 5%. No strong evidence the forecast is too smooth or too volatile.

**Individually, neither coefficient is significantly different from the optimal value.** $\beta_1 = 0.92$ suggests very mild under-reaction (forecast slightly too smooth), but not statistically significant. You'd still want the joint F-test for a definitive answer.
</details>

### Practice 3b: MZ Full F-Test Computation (EXAM-STYLE)
Continuing from Practice 3. You have $n = 30$ forecast-actual pairs.
- MZ regression output: SSR_U = 24.50 ("Sum squared resid")
- Sum of squared raw forecast errors: $\sum e^2_{t+1,t} = \sum(y_{t+1} - \hat{y}_{t+1,t})^2 = 26.80$

Test jointly whether $(\beta_0, \beta_1) = (0, 1)$.

<details>
<summary>Solution</summary>

**Step 1: Identify the pieces.**
- $SSR_R = 26.80$ (the restricted model: $y = \hat{y} + u$, so residuals are just the raw forecast errors)
- $SSR_U = 24.50$ (from the unrestricted MZ regression output)
- $q = 2$ (two restrictions: $\beta_0 = 0$ and $\beta_1 = 1$)
- $n = 30$, $k_U = 2$ (two parameters: $\beta_0$ and $\beta_1$)

**Step 2: Compute F.**

$$F = \frac{(SSR_R - SSR_U)/q}{SSR_U/(n - k_U)} = \frac{(26.80 - 24.50)/2}{24.50/(30 - 2)} = \frac{2.30/2}{24.50/28} = \frac{1.15}{0.875} = 1.31$$

**Step 3: Compare to critical value.**

$F(2, 28)$ at 5% $\approx 3.34$ (from F-table). Since $1.31 < 3.34$, we **fail to reject** $H_0$.

**Step 4: Conclude.**

The forecast passes the MZ joint test. We cannot reject forecast optimality at the 5% level. The mild under-reaction ($\beta_1 = 0.92$) and small bias ($\beta_0 = 0.30$) are not jointly significant — they could be sampling noise.

**Key point**: The individual t-tests said "not significant" and the joint F-test confirms. But that won't always be the case — sometimes the joint test rejects even when neither individual test does (or vice versa). Always do the joint test if the exam asks for it.
</details>

### Practice 3c: MZ Using the Orthogonality Form
You run the alternative form: $e_{t+1,t} = \alpha_0 + \alpha_1 \hat{y}_{t+1,t} + u_t$ and get:

```
Variable     Coefficient   Std. Error    t-Stat    Prob.
C              0.520        0.200         2.60     0.014
FORECAST      -0.230        0.090        -2.56     0.016

F-statistic    4.82
Prob(F-stat)   0.015
```

Is the forecast optimal?

<details>
<summary>Solution</summary>

With the orthogonality form, $H_0: (\alpha_0, \alpha_1) = (0, 0)$ — and the **F-statistic in the output directly tests this**. No hand computation needed.

$F = 4.82$, $p = 0.015$. Since $p < 0.05$, we **reject** $H_0$.

**Interpretation:**
- $\alpha_0 = 0.520$ (p = 0.014): The forecast error has a significant positive mean → the forecast is **biased low** (systematically under-predicts by about 0.52 units)
- $\alpha_1 = -0.230$ (p = 0.016): The forecast error is negatively correlated with the forecast → when the forecast is high, the error tends to be negative (actual < forecast) → the forecast **over-reacts** at high values. Equivalently, in the classic MZ form, $\beta_1 = 1 + \alpha_1 = 1 + (-0.230) = 0.77$ — the forecast is too smooth.

**Conclusion**: The forecast is NOT optimal. It has both constant bias and inefficient scaling. The forecaster should add ~0.52 to all forecasts and dampen the forecast's responsiveness.

**Note the shortcut**: With this form, you just read the F-stat and p-value from the output. That's it. No SSR computation needed.
</details>

### Practice 4: DM Test Logic
Model A: RMSE = 2.45. Model B: RMSE = 2.38. DM test: t = 0.73, p = 0.47.

What do you conclude?

<details>
<summary>Solution</summary>

Model B has a numerically lower RMSE (2.38 vs 2.45), suggesting ~2.9% improvement. However, the DM test gives p = 0.47 → **cannot reject** the null of equal predictive ability.

**Conclusion**: The difference in forecast accuracy is **not statistically significant**. We cannot say Model B is better than Model A. Both models have essentially the same predictive ability.

This is exactly the Southern Company lesson — you can't just eyeball the MSEs.
</details>
