# Week 6: Forecasting with ARMA Models

## Main Topic
How to construct optimal forecasts from ARMA models: the role of loss functions in defining "optimal," the mechanics of computing h-step-ahead forecasts from MA, AR, and ARMA models, properties of forecast errors, and the construction of interval and density forecasts. This lecture is the bridge between model estimation (Weeks 3-4) and forecast evaluation (coming in Week 6 Thursday / Week 7).

## Recording Insights

### Key Things the Professor Said (not on slides)

**On model complexity vs parsimony (Southern Company example):**
> "When I was consulting with Southern Company, their model was super simple — five items. They forecast electricity demand, but they have to bring that in front of the Georgia Public Commissioner, because it's semi-regulated. For them, being able to explain the model in a way that makes sense to people is very important."

This directly connects to the BofA project: BofA explicitly said they value explainable, transparent models over black-box approaches. Parsimony is not just theoretical — it's what practitioners need.

**On COVID and structural change:**
> "Is COVID a structural change? Is COVID just a blip? All these are decisions that you have to make."

The professor flagged this as a key forecasting decision, exactly matching what BofA said in the kickoff about COVID treatment being a major question.

**On out-of-sample vs pseudo out-of-sample:**
> "I could use my data between 1970 to 2024, then pretend I'm in 2024 — I use no information pertaining to 2025. I forecast, and then you can see what your model would have done. But this has to be done fair — no information past 2024."

The professor stressed the importance of "fair" pseudo out-of-sample testing: you cannot use any future information, including for data transformations or variable selection.

**On nowcasting:**
> "Nowcasting is when you want to forecast now. For example, you may want to forecast GDP now, but GDP doesn't come out until the end of the quarter. You're trying to forecast what's happening right now before the actual release."

She distinguished nowcasting (filling current gaps) from forecasting (predicting future) and backcasting (filling past gaps).

**On why MA models are limited for forecasting:**
> "This is another reason why people don't tend to like moving average models. Because they basically tell you that you can only forecast for a couple steps ahead. After that, it doesn't tell you more than the mean."

This is the practical motivation for preferring AR and ARMA specifications — they can forecast arbitrarily far ahead.

**On the forecast variance inequality (VAR(Y) > VAR(ŷ)):**
> "Don't expect your forecast to match the actual data identically. Your forecast will always be a bit smoother, with a smaller variance. Plotting the two together, you have to be very careful how you interpret this graph."

This is a critical practical point: when you overlay actual vs. forecast on the same plot, the forecast will always appear smoother. This is mathematically guaranteed, not a sign of a bad model.

**On the forecasting workflow:**
> "Spend first all the time you have to get the best model you can from what we've learned. Then once you have the model, write it down, and think about what happens in the future."

**On ARMA preference:**
> "ARMA preferred because you can forecast far into the future."

## Key Concepts

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

## Connections
- **Builds on:** Week 3-4 ARMA model estimation, AR/MA process properties, AIC/BIC model selection
- **Related to:** Stock & Watson Chapter 14 (forecasting), Diebold textbook Chapters 2 and 5
- **Prerequisite for:** Forecast evaluation (Thursday / Week 7), VAR forecasting, and the climate-risk-loans project's scenario-conditional forecasting
- **Direct project relevance:** The ARMA forecasting framework is how we'll generate baseline loan growth forecasts; the loss function discussion matters for how BofA evaluates forecast quality; the pseudo out-of-sample concept is exactly what we need for model validation.

## Questions to Consider
1. Why does minimizing quadratic loss lead to the conditional mean as the optimal forecast?
2. Give an example where asymmetric (linlin) loss is more appropriate than quadratic loss.
3. Why can an MA($q$) process only be forecast $q$ steps ahead, while AR can be forecast indefinitely?
4. What is the forecast error for an AR(1) at horizon $h$? Write it as an MA process.
5. Why is $\text{Var}(y_{T+h}) > \text{Var}(\hat{y}_{T+h,T})$? What does this mean for interpreting forecast plots?
6. How do you construct a 95% interval forecast for an ARMA(1,1) at $h = 2$?
7. What is the difference between out-of-sample and pseudo out-of-sample forecasting?
8. Why do we approximate by assuming estimated parameters equal true parameters when computing forecast error variance?
9. How does the forecast error variance grow with horizon $h$ for an AR(1)? Does it converge?
10. In what sense is the forecast "smoother" than the actual data?

## Review Checklist
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
