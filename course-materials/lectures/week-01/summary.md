# Week 1: Metrics Review — OLS, Inference, and the Bridge to Time Series

## Main Topic
A comprehensive review of OLS regression fundamentals — estimation, assumptions, goodness of fit, hypothesis testing, dummy variables, and interactions — with a deliberate emphasis on what carries over to time series forecasting and what changes.

## Key Concepts

### 1. The Linear Regression Model
**Definition:** $Y_i = \omega_0 + \omega_1 X_{1i} + \cdots + \omega_k X_{ki} + u_i$

**From lecture:** "Why do we pick linear models? Because it's easier to interpret... but there's more technical reasons. This is actually a very good approximation for most nonlinearity. Unless it's very complex, a linear model can get along."

**Key points:**
- $\omega_0$ (intercept): "You always want an intercept. In an autoregressive model, the intercept is going to have sometimes very specific results."
- $\omega_j$ (slope): change in $Y$ for a one-unit change in $X_j$, holding everything else constant
- $u_i$ (error): everything unobserved or not included — "if I know that the distance from the ocean or the number of bathrooms will matter for the price, and I don't include that, they're all going to get sucked into this"
- We never observe $\omega_0, \omega_1$ or $u_i$ — we estimate them from data

### 2. OLS Estimation
**Definition:** Choose $\hat{\omega}_0, \hat{\omega}_1, \ldots, \hat{\omega}_k$ to minimize $\sum_{i=1}^n \hat{u}_i^2 = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2$

**Why squared residuals (from lecture):**
1. "Treats positive and negative, overshooting or underfitting, equally"
2. "Squaring errors — I really don't like big mistakes" (penalizes large errors more)
3. "When I take the first derivative of a square, it becomes a linear function. It's easy to solve." (Absolute value is not differentiable everywhere)

**OLS formula (simple regression):**
$$\hat{\omega}_1 = \frac{\sum(X_i - \bar{X})(Y_i - \bar{Y})}{\sum(X_i - \bar{X})^2} = \frac{\text{Cov}(X,Y)}{\text{Var}(X)}$$

**From lecture:** "You only make sense if you have some variation in your X. If I want to really know how the price of a house relates to the size, it's not helpful if I only measure houses that have the same size — I learn nothing."

### 3. Loss Functions: A Preview of Forecasting
**This is a major theme that Pesavento introduces early.**

**From lecture:** "This is very similar to when we're going to talk about loss function for forecasting. Does it make sense to have a square loss function? You're making an investment, investing in some stocks. Are you equally happy if you under-predict your stock or over-predict your stock? Not equally happy!"

**Examples from lecture:**
- **Stock investing:** You're happy about upside surprises, unhappy about downside. Asymmetric loss makes more sense than symmetric squared loss.
- **Bus stop timing:** "If you get there two minutes too early vs two minutes too late — the cost of being two minutes late is very costly." Asymmetric again.
- **Takeaway:** Squared loss is convenient and mathematically tractable, but "these are things you need to keep in mind when you think about this type of question."

### 4. Gauss-Markov Assumptions
**The six classical assumptions:**
1. **Linearity:** $Y_i = \omega_0 + \omega_1 X_{1i} + \cdots + \omega_k X_{ki} + u_i$
2. **Random sampling:** $(Y_i, X_{1i}, \ldots, X_{ki})$ are i.i.d.
3. **No perfect collinearity:** No $X_j$ is a perfect linear combination of others
4. **Zero conditional mean (exogeneity):** $E[u_i | X_{1i}, \ldots, X_{ki}] = 0$
5. **Homoskedasticity:** $\text{Var}(u_i | X) = \sigma^2$
6. **Normality:** $u_i | X \sim N(0, \sigma^2)$ (for exact inference)

**Under 1–4:** OLS is unbiased and consistent
**Under 1–5:** OLS is BLUE (Best Linear Unbiased Estimator)

**From lecture on time series implications:** "IID — this is the first assumption. What happens? Is time series independent? No. There you go. First problem we are facing."

### 5. Exogeneity and Omitted Variable Bias — The Forecasting Perspective
**This is the most important conceptual insight of the lecture for the course.**

**Omitted variable bias formula:** $E[\hat{\omega}_1] = \omega_1 + \omega_2 \frac{\text{Cov}(X_1, X_2)}{\text{Var}(X_1)}$

**From lecture (key quote, repeated emphasis):** "I need this number to be unbiased if I really want to know the **causal effect** of adding 100 square feet to the price. But suppose I only care about **predicting** the price — where it is going to go next. In that case, I don't care. And I'm going to repeat this a million times: I don't care about the parameter being unbiased, because I don't care about the causal relationship. I only care about forecasting."

**Specific examples from lecture:**
- **GDP forecasting:** "Instead of including variables that may explain what GDP is going to do in the future, we're just going to put where GDP was last quarter, and that's going to be enough to explain 90%."
- **Exchange rates:** "If I want to predict exchange rates and I put the S&P 500 as an explanatory variable, it's very likely that both have the same driver behind them. So I do have simultaneity, but I don't care about finding the true relationship — I only care about predicting exchange rate."

### 6. Heteroskedasticity
**Definition:** $\text{Var}(u_i | X_i) = \sigma_i^2$ (variance depends on $X$)

**From lecture:** "Remember the stock data — how the variance was smaller at the beginning than at the end. That is heteroskedasticity."

**Consequence:** OLS still unbiased, but standard errors are wrong.
**Solution:** Robust (Huber-White) standard errors. "When you write robust in R or Python, it does what we call HAC — heteroskedasticity and autocorrelation consistent. It's robust to both."

### 7. Serial Correlation — The Bridge to Time Series
**Definition:** $\text{Cov}(u_i, u_j) \neq 0$ for $i \neq j$

**From lecture:** "Signal correlation is something you don't discuss so much in [cross-section] because it's not easy to find, but in time series, it's there all the time, because data over time is correlated with each other."

**Key insight from lecture:** "Rather than say, 'I want to correct for the standard errors,' we're actually going to say we're going to **exploit this** from the very beginning... If things are correlated over time, I'm actually going to use that to my advantage, and I'm going to use that to forecast better. That's what autoregressive models are all about — exploiting serial correlation in the data."

**Consequence:** OLS still unbiased, standard errors wrong (usually too small). Use Newey-West HAC standard errors.

### 8. Goodness of Fit: R² and Adjusted R²
**R²:** $R^2 = 1 - \frac{\text{RSS}}{\text{TSS}} = 1 - \frac{\sum \hat{u}_i^2}{\sum(Y_i - \bar{Y})^2}$

**Adjusted R²:** $\bar{R}^2 = 1 - \frac{\text{RSS}/(n-k-1)}{\text{TSS}/(n-1)}$

**From lecture — R² is relative to the problem:**
- Housing prices: $R^2 = 0.62$ — "Not bad, but I would not be that happy. I only explain 62%."
- Finance: "When we start doing work with finance data, we're going to find R-squared equal to like 0.2, and you will be happy. It's very hard to predict stock."
- Macro: "When I run a trend on GDP data, the R-squared will be 90% already. So for us in time series, sometimes in macro data, we're going to spend a lot of time going from 0.90 to 0.93, and that's going to buy us a lot."

**On spurious regression (from lecture):** "If I find two variables that both go up like this, and I regress one on the other, I probably get a very high R-squared simply due to the fact that they're both going up. But are they even related to each other? Sometimes not."

**Why Adjusted R²:** "If I add junk — something that has zero significance — the R-squared is always going to go up. But we have a cost: every time we add a variable, we're losing degrees of freedom."

**On macro data constraints:** "Most data we have are maybe from the 50s to now. Oftentimes quarterly data. You may have 300 observations. So we're going to want to be parsimonious."

### 9. Hypothesis Testing and the Sampling Distribution
**The t-statistic:** $t = \frac{\hat{\omega}_j}{SE(\hat{\omega}_j)} \sim t_{n-k-1}$

**From lecture on why we can't look at coefficients alone:** "When I look at this number, 2.86, I cannot just look at it in isolation. In isolation it means nothing. Is 2.86 big, small, relevant, not relevant? I don't know — unless I know how variable it is. Because if my distribution has huge variance, a number of 2.86 probably contains no information."

**Confidence intervals:** $\hat{\omega}_j \pm 1.96 \times SE(\hat{\omega}_j)$

**Interpretation (from lecture):** "The standard error will determine whether this confidence interval is wide or not."

**F-test for overall significance:** $F = \frac{R^2/k}{(1-R^2)/(n-k-1)} \sim F_{k, n-k-1}$

### 10. Small Sample vs. Asymptotic Properties
**Small sample (exact):** Under Gauss-Markov + normality, t-statistics follow $t_{n-k-1}$ exactly.

**Asymptotic (large sample):**
- Consistency: $\hat{\omega}_j \xrightarrow{p} \omega_j$ as $n \to \infty$ (only needs assumptions 1–4)
- Asymptotic normality: $\sqrt{n}(\hat{\omega}_j - \omega_j) \xrightarrow{d} N(0, V)$ (don't need normality assumption)

**From lecture:** "The assumption of normality is actually very rare. Data are not very much normal. When data are not normal, then we can rely on asymptotic properties."

**Practical guidelines from lecture:**
- $n < 30$: "You got to be careful"
- $n > 100$: Asymptotic approximations work well
- "How large depends on how the data looks. If it looks like a normal, you may not need many observations. If the data has fat tails, like finance data, then you need a lot more data points."

### 11. Dummy Variables
**Definition:** Binary indicator (0 or 1) capturing qualitative group differences.

**From lecture — main time series application:** "For us, one of the biggest ways to use dummy variables is going to be for seasonality — one for each month, to indicate that some things happen that are specific to each month."

**Single dummy:** $\text{Price}_i = \omega_0 + \omega_1 \text{SqFt}_i + \omega_2 \text{Waterfront}_i + u_i$
- $\omega_2$ = difference in average price between groups (holding other variables constant)
- Creates two parallel regression lines (same slope, different intercepts)

**Multiple categories:** For $m$ categories, use $m - 1$ dummies.

**Dummy variable trap (from lecture):** "If I add square feet, and then I have D1, D2, D3, plus a constant — Python is going to say, 'I cannot do anything.' Why? Because $D_1 + D_2 + D_3 = 1$ always, which is exactly the constant. Perfect multicollinearity."

### 12. Interaction Terms
**Model:** $\text{Price}_i = \omega_0 + \omega_1 \text{SqFt}_i + \omega_2 \text{Waterfront}_i + \omega_3 (\text{SqFt}_i \times \text{Waterfront}_i) + u_i$

**Interpretation (from lecture):** "This [$\omega_3$] is the incremental effect of square feet for being on the waterfront, incremental over whatever the non-waterfront effect is."

- Non-waterfront: $\text{Price} = \omega_0 + \omega_1 \text{SqFt}$
- Waterfront: $\text{Price} = (\omega_0 + \omega_2) + (\omega_1 + \omega_3) \text{SqFt}$

**From lecture:** "What is the effect of square feet on waterfront? It's not $\omega_1$ — it's $\omega_1 + \omega_3$."

**Test for interaction:** $H_0: \omega_3 = 0$ via t-test. If rejected, slopes differ; keep the interaction.

### 13. Functional Forms
Common transformations (important for time series):
- **Log-log:** $\log(Y) = \omega_0 + \omega_1 \log(X) + u$ — $\omega_1$ is an elasticity
- **Log-level:** $\log(Y) = \omega_0 + \omega_1 X + u$ — $\omega_1 \times 100$ is a semi-elasticity
- **Quadratic:** $Y = \omega_0 + \omega_1 X + \omega_2 X^2 + u$ — allows non-monotonic relationships

### 14. Connection to Time Series (The Punchline)
**From lecture and slides:** "Everything we covered applies to time series, but with important caveats."

**Why OLS matters for AR models:**
- AR(1): $Y_t = \omega_0 + \omega_1 Y_{t-1} + u_t$ looks like an OLS regression
- Same estimation principle (minimize squared residuals)

**Key differences in time series:**
- Serial correlation: errors are correlated over time (violates i.i.d.)
- Non-stationarity: mean/variance may change
- Dynamics: lagged dependent variables common
- Standard errors: need HAC correction

**The course's central philosophy (from lecture):** We don't care about unbiasedness for causal interpretation — we care about **forecasting**. This relaxes many of the assumptions we'd normally worry about (omitted variables, simultaneity, endogeneity).

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| OLS slope (simple) | $\hat{\omega}_1 = \text{Cov}(X,Y) / \text{Var}(X)$ | Understanding what OLS estimates |
| OLS intercept | $\hat{\omega}_0 = \bar{Y} - \hat{\omega}_1 \bar{X}$ | Regression line passes through $(\bar{X}, \bar{Y})$ |
| R² | $R^2 = 1 - \text{RSS}/\text{TSS}$ | Fraction of variation explained |
| Adjusted R² | $\bar{R}^2 = 1 - (1-R^2)\frac{n-1}{n-k-1}$ | Model comparison (penalizes extra variables) |
| t-statistic | $t = \hat{\omega}_j / SE(\hat{\omega}_j)$ | Testing significance |
| F-statistic | $F = \frac{R^2/k}{(1-R^2)/(n-k-1)}$ | Joint significance |
| Confidence interval | $\hat{\omega}_j \pm 1.96 \times SE(\hat{\omega}_j)$ | 95% CI for coefficient |
| OVB formula | $E[\hat{\omega}_1] = \omega_1 + \omega_2 \frac{\text{Cov}(X_1,X_2)}{\text{Var}(X_1)}$ | Direction of bias from omitted variable |
| Variance of $\hat{\omega}_1$ | $\text{Var}(\hat{\omega}_1) = \sigma^2 / \text{SST}_X$ | Precision depends on variation in X |

## Examples from Class

### Example 1: Housing Price Regression
- **Setup:** 200 observations, predict house price from square footage
- **Results:** $\hat{\omega}_1 = 2.865$, $R^2 = 0.623$, $t = 18.09$
- **Annotation:** "Each 100 sq ft increases price by $2,865 on average"
- **Takeaway:** High significance, moderate fit. Pesavento: "I would not be that happy with 0.62"

### Example 2: Waterfront Dummy
- **Setup:** Add waterfront dummy to housing regression
- **Results:** Waterfront premium = $87,342, $R^2$ jumps from 0.623 to 0.741
- **From lecture:** "Does it make sense that the effect of square feet is the same whether waterfront or not? No." — Motivates adding interaction term.

### Example 3: Spurious Regression
- **From lecture:** "Ice cream sales and homicides — if you regress one on the other, R-squared is like 80%. Is that because ice cream causes homicides? No. They're both driven by temperature."
- **Also:** "Number of churches vs number of bars across cities. High R²! Both driven by population."
- **Takeaway:** High R² doesn't mean a meaningful relationship. Critical for time series where trending variables produce spurious correlations.

### Example 4: Loss Function Asymmetry
- **From lecture:** Stock investment — you're not equally happy about under-prediction vs over-prediction. Bus stop — getting there 2 minutes late is much costlier than 2 minutes early.
- **Takeaway:** Squared loss is convenient but not always appropriate. Forecasting will revisit this.

## Connections
- **Prerequisite for:** All subsequent weeks — OLS is the foundation for AR/MA/ARMA estimation
- **Directly leads to:** Week 2 (trend estimation via OLS), Week 3 (serial correlation, stationarity), Week 4 (AR models = OLS with lagged dependent variables)
- **Key thread:** The forecasting vs causality distinction introduced here runs through the entire course

## Questions to Consider
1. Why does Pesavento say "I don't care about omitted variable bias" for forecasting? Under what conditions would bias actually hurt forecasts?
2. If serial correlation makes standard errors wrong, why does Pesavento say we should "exploit" it rather than just correct for it?
3. In what situations would you prefer absolute value loss over squared loss? What about asymmetric loss?
4. Why is $R^2 = 0.20$ acceptable in finance but $R^2 = 0.62$ is only "okay" for housing prices?
5. How does the dummy variable trap relate to the multicollinearity assumption?

## Review Checklist
- [ ] Can write down and interpret the OLS regression model
- [ ] Understand why OLS minimizes squared residuals (3 reasons from lecture)
- [ ] Know all 6 Gauss-Markov assumptions and which properties they guarantee
- [ ] Understand omitted variable bias formula and its direction
- [ ] **Key:** Know why OVB doesn't matter for forecasting (Pesavento's central point)
- [ ] Can interpret R², Adjusted R², and know when each is appropriate
- [ ] Understand that R² benchmarks differ by field (macro vs finance)
- [ ] Know why we can't interpret coefficients in isolation (need standard errors)
- [ ] Understand small sample vs asymptotic properties
- [ ] Can set up and interpret dummy variable models
- [ ] Can set up and interpret interaction models (both dummy×continuous and continuous×continuous)
- [ ] Know the dummy variable trap and how to avoid it
- [ ] Understand heteroskedasticity and serial correlation: effects on OLS + solutions
- [ ] **Key:** Understand that serial correlation will be *exploited* in time series, not just corrected
- [ ] Know the connection: AR(1) = OLS regression with lagged dependent variable
