# Week 6: Forecasting with ARMA Models & Forecast Evaluation

## Main Topics
**Lecture 1 (Tuesday):** How to construct optimal forecasts from ARMA models: the role of loss functions in defining "optimal," the mechanics of computing h-step-ahead forecasts from MA, AR, and ARMA models, properties of forecast errors, and the construction of interval and density forecasts.

**Lecture 2 (Wednesday, Feb 19):** Point forecast evaluation — how to assess whether your forecasts are any good (absolute evaluation) and how to compare two competing models (relative evaluation). Covers accuracy measures (MSE, RMSE, MAE), the Mincer-Zarnowitz regression, the Diebold-Mariano test, and market/survey-based forecast combinations.

## Recording Insights

### Lecture 1 (Tuesday) — Key Things the Professor Said

**On model complexity vs parsimony (Southern Company example):**
> "When I was consulting with Southern Company, their model was super simple — five items. They forecast electricity demand, but they have to bring that in front of the Georgia Public Commissioner, because it's semi-regulated. For them, being able to explain the model in a way that makes sense to people is very important."

This directly connects to the BofA project: BofA explicitly said they value explainable, transparent models over black-box approaches.

**On COVID and structural change:**
> "Is COVID a structural change? Is COVID just a blip? All these are decisions that you have to make."

**On out-of-sample vs pseudo out-of-sample:**
> "I could use my data between 1970 to 2024, then pretend I'm in 2024 — I use no information pertaining to 2025. I forecast, and then you can see what your model would have done. But this has to be done fair — no information past 2024."

**On why MA models are limited for forecasting:**
> "This is another reason why people don't tend to like moving average models. Because they basically tell you that you can only forecast for a couple steps ahead. After that, it doesn't tell you more than the mean."

**On the forecast variance inequality (VAR(Y) > VAR(ŷ)):**
> "Don't expect your forecast to match the actual data identically. Your forecast will always be a bit smoother, with a smaller variance."

**On the forecasting workflow:**
> "Spend first all the time you have to get the best model you can from what we've learned. Then once you have the model, write it down, and think about what happens in the future."

### Lecture 2 (Wednesday, Feb 19) — Key Things the Professor Said

**On the unforecastability principle (foundational):**
> "If I can forecast in any way my forecast error, that means that there was something in the model that I have not exploited in my forecast, and that was left as residuals in my forecast error, and therefore my forecast in the first place was not optimal."

She emphasized this holds regardless of model type — even "super complicated" models must satisfy this property.

**On estimating forecast error variance from past data (stationarity assumption):**
> "Assuming that this beta one is constant, assuming that the sigma square is constant, so that I can do this projection to the future... Only happens if this is a stationary model."

Key insight: the ability to estimate future forecast error variance from historical data depends critically on stationarity. If coefficients change over time, past information cannot reliably estimate future uncertainty.

**On MSE as the go-to accuracy measure:**
> "The mean square error is a very popular measure that is used, and you will see it a lot... is a good way between two models that produce two forecasts. You could choose the one with the smaller MSE."

**On RMSE being preferred in practice:**
> "For sure the number one would be the root mean square error" — because it preserves the same units as the forecast variable.

**On the bias-variance trade-off:**
> "Sometimes you may be willing to take a little bit of bias if it gives you a much, much smaller variance. So sometimes, even if you have a little bit of bias, you may have a smaller mean square error between two different forecasts."

This is a critical insight for model selection: a slightly biased but more stable model can beat an unbiased but high-variance model on MSE.

**On comparing models — the Diebold-Mariano test:**
> "Simply looking at the mean square error, one team did better, but when we tested the difference, there was no significant difference. At the end, they all did very well."

She told the story of last year's Southern Company project: three teams had different MSEs, but the DM test showed the difference was not statistically significant. The point: you cannot just eyeball which MSE is smaller — you must formally test whether the difference is real.

> "The DM test... some smart people have showed that scaling it by the variance is distributed like a normal, and therefore you can use the Z critical value. It should all be done in a package."

**On forecast errors being random variables (not just numbers):**
> "The forecast error is a random variable. So this is a function of a random variable — it's going to be a random variable. So when I compare the two, which way am I comparing them?"

This is why you need a formal test (DM), not just pointwise comparison of MSE values.

**On market-based forecasts — S&P 500 and financial variables as predictors:**
> "If you put something like the S&P 500 or something similar on your right hand side, it's going to turn out to be helpful for forecasting... it's not a causal relationship, but helpful in forecasting, because probably the true relationship goes the other way. It's just that the market anticipates what's going to happen."

This is directly relevant to the BofA project: financial market variables (equity indices, yield curves) can be useful RHS variables in forecasting models even without a causal story — they aggregate forward-looking information.

**On surveys for inflation expectations (directly relevant to consumer loans):**
> "If you need to think about inflation for your consumer loans, there is data — the University of Michigan and others — that ask households what their expectations for inflation are. Individual forecasts are all over the place, but on average, they do pretty well."

She explicitly connected inflation surveys to the consumer loans project. The Survey of Professional Forecasters (SPF) and Michigan Survey are potential data sources.

**On forecastability being a matter of degree:**
> "Whether a series is predictable or not should be replaced by how predictable it is. Predictability is always a matter of degree."

And more importantly: predictability depends on horizon and loss function. A series may be forecastable at short horizons but not long ones.

**On the slides she skipped (self-study):**
> "The second part of the slide is very talky, and so I'm going to let you read them through."

She explicitly told students to read the market-based and survey-based forecast combination slides on their own — this material (forward markets, Fisher equation, SPF, Livingston, Michigan) is fair game but was not lectured in detail.

## Key Concepts

### PART A: Forecasting with ARMA (Tuesday Lecture)

### 1. General Considerations for Forecasting (10 Items)
The lecture begins with 10 considerations for any forecasting task:

1. **Forecast Object** — What are we forecasting? A time series, an event, a probability?
2. **Information Set** — What data is available? For this course, mostly the time series itself.
3. **Model Uncertainty** — All models are false; they are intentional abstractions.
4. **Forecast Horizon** ($h$) — 1-step, 12-step, 120-step ahead? Different horizons may need different techniques.
5. **Structural Change** — Are our model's approximations stable over time? (COVID example)
6. **Forecast Statement** — Point forecast, interval, density, or scenarios? Who is the audience?
7. **Forecast Presentation** — Graphical methods are valuable for construction and evaluation.
8. **Decision Environment and Loss Function** — What is the cost of forecast errors? Symmetric or asymmetric?
9. **Model Complexity and Parsimony** — Bigger models are not necessarily better. (Southern Company example)
10. **Unobserved Components** — Have we handled trend, seasonality, and cycles?

### 2. Loss Functions
**Definition:** A loss function $L(e)$ maps forecast errors $e = y - \hat{y}$ to a cost. Three requirements:
1. $L(0) = 0$ — zero error means zero loss
2. $L(e)$ is continuous
3. $L(e)$ is increasing in $|e|$

**Three types:**

| Loss Function | Formula | Shape | Optimal Forecast |
|--------------|---------|-------|-----------------|
| **Quadratic** | $L(e) = e^2$ | Symmetric, penalizes big errors heavily | Conditional mean $E(y \mid x)$ |
| **Absolute** | $L(e) = \|e\|$ | Symmetric, linear penalty | Conditional median |
| **Linlin** | $L(e) = a\|e\|$ if $e > 0$; $b\|e\|$ if $e \leq 0$ | Asymmetric | Conditional $d \cdot 100\%$ quantile, where $d = \frac{b}{a+b}$ |

> **From the recording:** "OLS minimizes the quadratic loss. People like it because it's mathematically tractable — a quadratic function has a linear first derivative, so you can solve analytically." The professor also gave the bus stop / stock prediction example: if under-predicting a stock price costs more than over-predicting (you miss investment opportunities), you want an asymmetric loss function.

### 3. Optimal Forecast
**Definition:** The forecast with the smallest conditional expected loss:
$$\hat{y}(x)^* = \arg\min_{\hat{y}(x)} \iint L(y - \hat{y}(x)) f(y,x) \, dy \, dx$$

- **Quadratic loss** $\Rightarrow$ optimal forecast = **conditional mean** $E(y \mid x)$
- **Absolute loss** $\Rightarrow$ optimal forecast = **conditional median**
- **Linlin loss** $\Rightarrow$ optimal forecast = **conditional quantile** (biased by design)

**Key insight:** Under asymmetric loss, optimal forecasts are biased. The conditional mean is unbiased, but bias is optimal under asymmetric loss because we gain by pushing forecasts away from the more costly error direction.

### 4. Forecasting Deterministic Components
**Trend:** Easy — it's deterministic, so it's perfectly forecastable:
$$\hat{y}_{T+h,T} = \hat{\beta}_0 + \hat{\beta}_1 \cdot TIME_{T+h}$$

**Seasonality:** Also deterministic, also easy:
$$\hat{y}_{T+h,T} = \sum_{i=1}^{s} \hat{\gamma}_i D_{i,T+h}$$

Both produce density forecasts $N(\hat{y}_{T+h,T}, \hat{\sigma}^2)$ and interval forecasts $\hat{y}_{T+h,T} \pm 1.96\hat{\sigma}$.

> **From the recording:** "Anything deterministic, by definition, you can forecast well. Stochastic trend — that's a different thing."

### 5. Information Set
**Definition:** $\Omega_T = \{y_T, y_{T-1}, y_{T-2}, \ldots\}$ — all past and current observations.

Equivalently, for a covariance stationary process:
$$\Omega_T = \{\varepsilon_T, \varepsilon_{T-1}, \varepsilon_{T-2}, \ldots\}$$

because we can recover the shocks from the current and lagged $y$.

**Key result:** Under quadratic loss, the optimal forecast is $E(y_{T+h} \mid \Omega_T)$. For Gaussian processes, the conditional expectation is exactly linear, so **ARMA models estimated by OLS (or conditional ML) give the optimal forecast**.

### 6. Forecasting with MA(2) — Step by Step
**Model:** $y_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2}$, with $\varepsilon_t \sim WN(0, \sigma^2)$

**1-step-ahead ($h = 1$):**
- True: $y_{T+1} = \varepsilon_{T+1} + \theta_1 \varepsilon_T + \theta_2 \varepsilon_{T-1}$
- Forecast: $\hat{y}_{T+1,T} = 0 + \theta_1 \varepsilon_T + \theta_2 \varepsilon_{T-1}$ (replace future $\varepsilon_{T+1}$ with 0)
- Forecast error: $e_{T+1,T} = \varepsilon_{T+1}$ (white noise!)

**2-step-ahead ($h = 2$):**
- True: $y_{T+2} = \varepsilon_{T+2} + \theta_1 \varepsilon_{T+1} + \theta_2 \varepsilon_T$
- Forecast: $\hat{y}_{T+2,T} = 0 + 0 + \theta_2 \varepsilon_T$
- Forecast error: $e_{T+2,T} = \varepsilon_{T+2} + \theta_1 \varepsilon_{T+1}$ (MA(1)!)

**3-step-ahead and beyond ($h \geq 3$):**
- Forecast: $\hat{y}_{T+h,T} = \mu$ (just the mean)
- Forecast error: $e_{T+h,T} = \varepsilon_{T+h} + \theta_1 \varepsilon_{T+h-1} + \theta_2 \varepsilon_{T+h-2}$ (MA(2) — the process itself)

**Forecast error variances:**
| Horizon | Forecast Error | Variance |
|---------|---------------|----------|
| $h = 1$ | $\varepsilon_{T+1}$ (WN) | $\sigma^2$ |
| $h = 2$ | $\varepsilon_{T+2} + \theta_1 \varepsilon_{T+1}$ (MA(1)) | $\sigma^2(1 + \theta_1^2)$ |
| $h \geq 3$ | MA(2) | $\sigma^2(1 + \theta_1^2 + \theta_2^2) = \text{Var}(y_t)$ |

### 7. General MA(q) Forecasting
For any MA($q$) process:
- **Forecastable only $q$ steps ahead** — beyond that, forecast = unconditional mean
- Forecast error at horizon $h$: MA($h-1$) for $h \leq q$; MA($q$) for $h > q$
- Forecast error variance: $\sigma_h^2 \leq \text{Var}(y_t)$ for $h \leq q$; $\sigma_h^2 = \text{Var}(y_t)$ for $h > q$

> **From the recording:** "This is another reason why people don't tend to like moving average models — they can only forecast for a couple steps ahead."

### 8. Properties of Optimal Forecasts
For a well-specified model:
1. **Forecast errors have mean zero** — no systematic over/under-prediction
2. **Forecast errors are uncorrelated with past information** — all predictable content is used
3. **$\text{Cov}(\hat{y}_{T+h,T}, e_{T+h,T}) = 0$** — forecast and error are uncorrelated

**The variance inequality:**
$$y_{T+h} = \hat{y}_{T+h,T} + e_{T+h,T}$$

Since forecast and error are uncorrelated:
$$\text{Var}(y_{T+h}) = \text{Var}(\hat{y}_{T+h,T}) + \text{Var}(e_{T+h,T})$$

Therefore: $\text{Var}(y_{T+h}) > \text{Var}(\hat{y}_{T+h,T})$ — **the forecast is always smoother than the actual data**.

**Updating rule (MA):** $y_{T+h,T} = y_{T+h+1,T-1} + \theta_h \varepsilon_T$

### 9. Forecasting with AR(1)
**Model:** $y_t = \phi y_{t-1} + \varepsilon_t$

| Horizon | Forecast | Key |
|---------|----------|-----|
| $h = 1$ | $\hat{y}_{T+1,T} = \phi y_T$ | Plug in observed $y_T$ |
| $h = 2$ | $\hat{y}_{T+2,T} = \phi \hat{y}_{T+1,T} = \phi^2 y_T$ | Substitute previous forecast |
| $h$ | $\hat{y}_{T+h,T} = \phi^h y_T$ | Recursive or direct |

**Two equivalent formulations:**
- Direct: $\hat{y}_{T+h,T} = \hat{\phi}^h y_T$
- Recursive: $\hat{y}_{T+h,T} = \hat{\phi} \cdot \hat{y}_{T+h-1,T}$

> **From the recording:** The professor emphasized making sure Python does the recursive form correctly in pseudo out-of-sample exercises — "you have to make sure it really pretends it doesn't know anything about the future."

### 10. Forecasting with ARMA(1,1)
**Model:** $y_t = \phi y_{t-1} + \varepsilon_t + \theta \varepsilon_{t-1}$

**1-step-ahead:** $\hat{y}_{T+1,T} = \phi y_T + \theta \varepsilon_T$

**2-step-ahead:** $\hat{y}_{T+2,T} = \phi \hat{y}_{T+1,T}$ (MA component exhausted after 1 step)

**General ($h > 1$):** $\hat{y}_{T+h,T} = \phi \hat{y}_{T+h-1,T}$ — same recursive structure as AR

**2-step forecast error variance:**
First, write the MA($\infty$) representation: $y_t = \varepsilon_t + (\phi + \theta)\varepsilon_{t-1} + \ldots$

So: $\sigma_2^2 = \sigma^2(1 + (\phi + \theta)^2)$

**Interval forecast:** $\hat{y}_{T+2,T} \pm 1.96 \hat{\sigma}_2 = (\hat{\phi}^2 y_T + \hat{\phi}\hat{\theta}\varepsilon_T) \pm 1.96\hat{\sigma}\sqrt{1 + (\hat{\phi} + \hat{\theta})^2}$

### 11. Interval and Density Forecasts
If innovations are normally distributed:
- **Density forecast:** $y_{T+h} \sim N(\hat{y}_{T+h,T}, \sigma_h^2)$
- **95% interval forecast:** $\hat{y}_{T+h,T} \pm 1.96 \sigma_h$

**Practical note (slide 23):** The exact forecast error includes a parameter estimation term $(\theta_2 - \hat{\theta}_2)\varepsilon_T$. We make a convenient approximation by assuming estimated = true parameters, dropping this term. This is standard practice.

### PART B: Forecast Evaluation (Wednesday, Feb 19 Lecture)

### 12. The Unforecastability Principle
The key property of optimal forecast errors: they should be **unforecastable** based on information available at the time the forecast was made. This holds in great generality — regardless of loss function, linearity, or stationarity.

**Practical checks:**
- 1-step-ahead errors should be **white noise** with **zero mean**. Regress on a constant, check mean is zero. DW test for serial correlation.
- Multi-step-ahead errors will be serially correlated (at most MA(h-1)) but should still have zero mean.
- Forecast error variance should be **non-decreasing in h** — you're always more precise forecasting next month than 10 months out.

### 13. Testing Orthogonality of Errors (EXAM MATERIAL)
Errors should be orthogonal to available information. Test via regression:
$$e_{t+h,t} = \alpha_0 + \sum \alpha_i x_{it} + u_t$$
Do an F-test that all $\alpha$ are jointly zero.

**The Mincer-Zarnowitz Regression (EXAM):**
$$y_{t+h} = \beta_0 + \beta_1 y_{t+h,t} + u_t$$
Optimality requires $(\beta_0, \beta_1) = (0, 1)$, which means:
$$y_{t+h} = y_{t+h,t} + u_t$$
Equivalently, regress forecast error on forecast: $e_{t+h,t} = \alpha_0 + \alpha_1 y_{t+h,t} + u_t$, test $(\alpha_0, \alpha_1) = (0, 0)$.

> **Professor:** "If you regress your forecast error on your forecast, these two coefficients should all be zero... It's called the Mincer-Zarnowitz regression."

### 14. Accuracy Measures
**Forecast bias:** $\hat{\mu}_e = \frac{1}{T} \sum_{t=1}^{T} e_{t+h,t}$ — should be zero for optimal forecasts.

**Error variance:** $\hat{\sigma}^2_e = \frac{1}{T} \sum (e_{t+h,t} - \hat{\mu}_e)^2$ — should be small.

**Mean Squared Error (MSE):** $\widehat{MSE} = \frac{1}{T} \sum e_{t+h,t}^2$ — combines bias and variance: $MSE = \sigma^2_e + \mu^2_e$ (bias-variance decomposition).

**Root Mean Squared Error (RMSE):** $\widehat{RMSE} = \sqrt{\widehat{MSE}}$ — same units as the forecast. **Professor's preferred measure.**

**Mean Absolute Error (MAE):** $\widehat{MAE} = \frac{1}{T} \sum |e_{t+h,t}|$ — less popular but still used.

> **Professor:** "Most forecasting packages will give you MSE... is a good way between two models. For sure the number one would be the root mean square error."

### 15. Predictive $R^2$ and Theil's U-Statistic

**Predictive $R^2$:**
$$R^2 = 1 - \frac{\sum e^2_{t,t-1}}{\sum (y_t - \bar{y})^2}$$
Compares 1-step-ahead OOS forecast error variance to unconditional variance. If close to 1, your model is much better than the historical mean.

**Theil's U-statistic:** Same idea but benchmark is the "no-change" forecast $y_{t-1}$ instead of $\bar{y}$:
$$U = 1 - \frac{\sum e^2_{t,t-1}}{\sum (y_t - y_{t-1})^2}$$
Important caveat from slides: many economic variables are nearly random walks, so beating the no-change forecast is very hard. Theil's U may be near 0 through no fault of the forecaster.

> **Professor's board note:** "Stick to MSE or RMSE" — suggesting these are the most important for this course.

### 16. Forecastability
- It is hard to measure forecastability in general
- Predictability is always a **matter of degree**, not binary (forecastable vs. not)
- Depends on: the forecast horizon, the loss function, and the series itself
- A series may be highly predictable at short horizons but not at long horizons
- Financial data are often "not very forecastable"

> **Professor:** "Does it make sense to think about forecasting 10 years down the road?" — this is something to think carefully about for the BofA project.

### 17. Comparing Predictive Ability: Diebold-Mariano Test
When comparing Model A vs Model B:
1. Compute loss differential: $d_{12t} = L(e^a_{t+h,t}) - L(e^b_{t+h,t})$
2. Test $H_0: E(d_{12t}) = 0$ (equal predictive accuracy)
3. The DM statistic: $DM_{12} = \frac{\bar{d}_{12}}{\hat{\sigma}_{\bar{d}_{12}}} \rightarrow N(0,1)$

**Key properties:**
- DM is just a t-statistic for zero mean loss differential
- Requires covariance stationarity of the loss differential
- Standard errors should be HAC (robust to serial correlation in loss differentials)
- Simple implementation: regress loss differential on intercept, use HAC standard errors
- If you don't reject, the two models have "the same predictive ability"

> **Professor (Southern Company example):** "From a pure pointwise view, simply looking at the mean square error, one team did better, but when we tested the difference, there was no significant difference. At the end, they all did very well."

### 18. Market-Based Forecast Combinations
Financial markets aggregate forward-looking information. Useful market-based forecasts include:
- **Forward exchange rates**: $F_t(t+h) = E_t(S_{t+h})$ under risk neutrality
- **Futures markets**: exist for currencies, interest rates, commodities, energy, weather, real estate, VIX
- **Bond yields and inflation** (Fisher equation): $i_t(t+h) = r_t(t+h) + E_t(\pi_{t+h})$ — extract expected inflation from nominal-real yield spread
- **Term premium, default premium, dividend yield** — all contain forward-looking information

> **Professor:** "Imagine the financial market as an agglomeration of information... it's not a causal relationship, but helpful in forecasting, because probably the true relationship goes the other way."

**Caveats:** market inefficiencies, moral hazard, manipulation, and risk neutrality assumptions may not hold.

### 19. Survey-Based Forecast Combinations
- **Survey of Professional Forecasters (SPF)**: leading U.S. consensus macro forecast, quarterly since late 1960s, maintained by Philadelphia Fed
- **Livingston Survey**: bi-annual, maintained by Philadelphia Fed, over half a century of data
- **Michigan Consumer Survey**: household inflation expectations — useful for consumer loan modeling
- Consensus (average) of survey forecasts often performs very well relative to individual forecasts

> **Professor:** "If you need to think about inflation for your consumer loans, there is data — the University of Michigan and others that ask households what their expectations for inflation are. Individual forecasts are all over the place, but on average, they do pretty well."

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| Forecast error | $e = y - \hat{y}$ | Definition |
| Quadratic loss | $L(e) = e^2$ | Default; optimal forecast = conditional mean |
| Absolute loss | $L(e) = \|e\|$ | Optimal forecast = conditional median |
| Linlin loss | $L(e) = a\|e\|$ if $e > 0$; $b\|e\|$ if $e \leq 0$ | Asymmetric; optimal = $d \cdot 100\%$ quantile |
| Optimal forecast | $\hat{y}^* = \arg\min E[L(e)]$ | General definition |
| MA($q$) $h$-step forecast | $\hat{y}_{T+h,T} = \theta_h \varepsilon_T + \ldots + \theta_q \varepsilon_{T-q+h}$ for $h \leq q$; $= \mu$ for $h > q$ | Forecasting with MA |
| MA($q$) forecast error variance | $\sigma_h^2 = (1 + \theta_1^2 + \ldots + \theta_{h-1}^2)\sigma^2$ for $h \leq q$ | Confidence intervals |
| AR(1) $h$-step forecast | $\hat{y}_{T+h,T} = \phi^h y_T$ | Forecasting with AR |
| ARMA recursive forecast | $\hat{y}_{T+h,T} = \phi \hat{y}_{T+h-1,T}$ for $h > q$ | General ARMA forecasting |
| Variance inequality | $\text{Var}(y_{T+h}) > \text{Var}(\hat{y}_{T+h,T})$ | Interpreting forecast plots |
| 95% interval forecast | $\hat{y}_{T+h,T} \pm 1.96\sigma_h$ | Confidence bands |
| Density forecast | $N(\hat{y}_{T+h,T}, \sigma_h^2)$ | Full distributional forecast |
| Trend forecast | $\hat{y}_{T+h,T} = \hat{\beta}_0 + \hat{\beta}_1(T+h)$ | Deterministic trend |
| Seasonality forecast | $\hat{y}_{T+h,T} = \sum \hat{\gamma}_i D_{i,T+h}$ | Deterministic seasonality |

### Part B Formulas (Forecast Evaluation)

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| Forecast bias | $\hat{\mu}_e = \frac{1}{T}\sum e_{t+h,t}$ | Check unbiasedness |
| Error variance | $\hat{\sigma}^2_e = \frac{1}{T}\sum(e - \hat{\mu}_e)^2$ | Measure precision |
| MSE | $\widehat{MSE} = \frac{1}{T}\sum e^2_{t+h,t}$ | Primary accuracy measure |
| MSE decomposition | $MSE = \sigma^2_e + \mu^2_e$ | Bias-variance trade-off |
| RMSE | $\sqrt{\widehat{MSE}}$ | Same units as forecast |
| MAE | $\frac{1}{T}\sum\|e_{t+h,t}\|$ | Robust to outliers |
| Predictive $R^2$ | $1 - \frac{\sum e^2_{t,t-1}}{\sum(y_t - \bar{y})^2}$ | Compare to mean benchmark |
| Theil's U | $1 - \frac{\sum e^2_{t,t-1}}{\sum(y_t - y_{t-1})^2}$ | Compare to random walk |
| Mincer-Zarnowitz | $y_{t+h} = \beta_0 + \beta_1 y_{t+h,t} + u_t$; test $(\beta_0,\beta_1)=(0,1)$ | Test optimality (EXAM) |
| Orthogonality test | $e_{t+h,t} = \alpha_0 + \alpha_1 y_{t+h,t} + u_t$; test $(\alpha_0,\alpha_1)=(0,0)$ | Equivalent to MZ (EXAM) |
| DM test statistic | $DM_{12} = \bar{d}_{12} / \hat{\sigma}_{\bar{d}_{12}} \sim N(0,1)$ | Compare two models |
| Loss differential | $d_{12t} = L(e^a_{t+h,t}) - L(e^b_{t+h,t})$ | Input to DM test |
| Forward rate (risk neutral) | $F_t(t+h) = E_t(S_{t+h})$ | Market-based forecasts |
| Fisher equation | $i_t(t+h) = r_t(t+h) + E_t(\pi_{t+h})$ | Extract expected inflation |

## Examples from Class

### Example 1: Southern Company Electricity Forecasting
- **Setup:** Electricity demand forecasting for a semi-regulated utility
- **Key finding:** The company uses a very simple, 5-parameter model despite having access to complex methods
- **Takeaway:** Parsimony wins when you must explain your model to regulators or non-technical stakeholders. This parallels BofA's requirement for transparent, explainable models.

### Example 2: MA(2) Forecast Construction
- **Setup:** $y_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2}$, forecast from time $T$
- **Key finding:** You can only forecast 2 steps ahead; beyond that, the forecast is the unconditional mean. The forecast error grows from WN (1-step) to MA(1) (2-step) to MA(2) (3+ steps).
- **Takeaway:** MA models have a hard forecast horizon limit equal to the order $q$.

### Example 3: AR(1) Recursive Forecasting
- **Setup:** $y_t = \phi y_{t-1} + \varepsilon_t$, forecast from time $T$
- **Key finding:** The h-step forecast is $\phi^h y_T$, which decays toward zero (the mean) as $h$ grows, but never reaches a hard cutoff.
- **Takeaway:** AR models can forecast arbitrarily far ahead (though quality decays). This is why AR and ARMA are preferred over pure MA.

### Example 4: Forecast vs Actual Plots
- **Setup:** Plot actual data and forecasted values on the same graph
- **Key finding:** $\text{Var}(y_{T+h}) > \text{Var}(\hat{y}_{T+h,T})$ always holds — the forecast will always appear smoother than the actual data.
- **Takeaway:** Don't be alarmed if your forecast doesn't match the actual data's volatility. This is a mathematical property of optimal forecasts, not a deficiency.

### Example 5: Southern Company Forecast Comparison (Feb 19 lecture)
- **Setup:** Three student teams forecast electricity demand for Southern Company; actual 2025 data available for comparison
- **Key finding:** One team had a smaller MSE, but the Diebold-Mariano test showed the difference was NOT statistically significant
- **Takeaway:** You cannot just compare raw MSE numbers. Forecast errors are random variables — you must formally test whether differences are significant. The DM test is the standard tool.

### Example 6: White Noise Forecastability Paradox
- **Setup:** If the best forecast of a white noise process is zero (the mean), the forecast and actual data look completely different when plotted
- **Key finding:** A flat line (forecast) vs. a noisy series (actual) — yet this IS the optimal forecast
- **Takeaway:** Visual comparison of forecast vs. actual can be misleading. The variance inequality guarantees the forecast is smoother. Don't judge model quality from visual overlap alone.

## Connections
- **Builds on:** Week 3-4 ARMA model estimation, AR/MA process properties, AIC/BIC model selection
- **Related to:** Stock & Watson Chapter 14 (forecasting), Diebold textbook Chapters 2, 5, and 13 (market-based forecasts)
- **Prerequisite for:** VAR forecasting, and the climate-risk-loans project's scenario-conditional forecasting
- **Direct project relevance:**
  - The ARMA forecasting framework generates baseline loan growth forecasts
  - The loss function discussion matters for how BofA evaluates forecast quality
  - The pseudo out-of-sample concept is exactly what we use for model validation
  - **MSE/RMSE** are the metrics used in our OOS evaluation (scenario_forecasting.ipynb)
  - **Diebold-Mariano test** could be used to formally compare AR baseline vs. VAR model
  - **Market-based forecasts**: Professor explicitly said S&P 500 and financial variables help forecast — supports our use of DGS10 and FEDFUNDS as predictors
  - **Survey forecasts for inflation**: Michigan/SPF data could supplement our consumer loan model — professor mentioned this specifically for consumer loans
  - **Mincer-Zarnowitz regression**: we should run this on our pseudo-OOS forecasts to verify optimality

## Questions to Consider
1. Why does minimizing quadratic loss lead to the conditional mean as the optimal forecast?
2. Give an example where asymmetric (linlin) loss is more appropriate than quadratic loss.
3. Why can an MA($q$) process only be forecast $q$ steps ahead, while AR can be forecast indefinitely?
4. What is the forecast error for an AR(1) at horizon $h$? Write it as an MA process.
5. Why is $\text{Var}(y_{T+h}) > \text{Var}(\hat{y}_{T+h,T})$? What does this mean for interpreting forecast plots?
6. How do you construct a 95% interval forecast for an ARMA(1,1) at $h = 2$?
7. What is the difference between out-of-sample and pseudo out-of-sample forecasting?
8. How does the forecast error variance grow with horizon $h$ for an AR(1)? Does it converge?
9. **(EXAM)** What is the Mincer-Zarnowitz regression? What do you test and why?
10. What is the bias-variance decomposition of MSE? When would you accept a biased forecast?
11. What does the Diebold-Mariano test actually test? Why can't you just compare MSEs directly?
12. How can financial market data (e.g., forward rates, VIX) be useful for forecasting even without a causal relationship?
13. What is the Fisher equation and how can bond yields help forecast inflation?

## Review Checklist

### Part A: Forecasting with ARMA
- [ ] Understand the 10 general considerations for forecasting
- [ ] Know the three loss functions (quadratic, absolute, linlin) and their optimal forecasts
- [ ] Can explain why quadratic loss → conditional mean, absolute → median, linlin → quantile
- [ ] Know the difference between out-of-sample, pseudo out-of-sample, and nowcasting
- [ ] Can construct h-step-ahead forecasts from an MA(q) model
- [ ] Know that MA(q) forecasts collapse to the mean after q steps
- [ ] Can compute forecast errors and forecast error variances for MA(q)
- [ ] Can construct h-step-ahead forecasts from an AR(1) model: $\hat{y}_{T+h,T} = \phi^h y_T$
- [ ] Know the recursive forecast formula for ARMA: $\hat{y}_{T+h,T} = \phi \hat{y}_{T+h-1,T}$
- [ ] Understand why $\text{Var}(y) > \text{Var}(\hat{y})$ and its implications for plotting
- [ ] Can construct interval and density forecasts using the forecast error variance
- [ ] Know the forecast error structure: WN at $h=1$ for MA, growing MA for larger $h$
- [ ] Understand the parameter estimation approximation (slide 23)
- [ ] Know the practical preference for ARMA over pure MA in forecasting

### Part B: Forecast Evaluation
- [ ] Understand the unforecastability principle and why it is general (any loss, any model)
- [ ] Know how to check forecast error properties: zero mean, WN at h=1, MA(h-1) at h>1
- [ ] **(EXAM)** Can set up and interpret the Mincer-Zarnowitz regression ($\beta_0 = 0$, $\beta_1 = 1$)
- [ ] **(EXAM)** Can test orthogonality of errors via regression on available information
- [ ] Know how to compute forecast bias, error variance, MSE, RMSE, MAE
- [ ] Understand the bias-variance decomposition: $MSE = \sigma^2_e + \mu^2_e$
- [ ] Know when to accept a biased model (if it reduces MSE enough)
- [ ] Can explain Predictive $R^2$ and Theil's U-statistic (and their benchmarks)
- [ ] Understand forecastability as a matter of degree (depends on horizon, loss function)
- [ ] Know how to set up and interpret the Diebold-Mariano test for equal predictive ability
- [ ] Understand that DM is a t-test with HAC standard errors on the loss differential
- [ ] Know about market-based forecast combinations: forward rates, Fisher equation
- [ ] Know about survey-based combinations: SPF, Livingston Survey, Michigan Survey
- [ ] Can explain why financial variables help forecast (information aggregation, not causation)
