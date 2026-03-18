# Week 7: Unit Root Tests — Synced Lecture Notes

> Transcript from Professor Pesavento's lecture matched to slide content. Includes her explanations, analogies, student Q&A, and practical advice that goes beyond the slides.

---

## Slides 1-2: Non-Stationarity Introduction

**Slide content:** Various reasons for non-stationarity. Deterministic trend = trend stationary. Breaks and time-varying variance. Most common in macro data: stochastic trend (unit root / random walk). Wold decomposition and CLT require stationarity. Hard to differentiate trend stationary from unit root.

**Professor Pesavento's explanation:**

> Remember, to do anything that we've done about constructing and finding the best ARMA model, you need the data to be stationary. If you have deterministic trend and seasonality, first you have to detrend the data and deseasonalize the data, and then you proceed.

She lays out the hierarchy of non-stationarity:
- Breaks -> non-stationary
- Time-varying parameters -> non-stationary
- **Stochastic trend (unit root)** -> the most common cause in macro data

> If you have what's called a unit root, or if your data is a random walk, then the Wold theory that we just saw, and all the ARMA models, do not apply. And also the CLT does not apply.

The key difficulty she emphasizes early:

> It's very difficult to differentiate between a stationary model — or a trend stationary, which we're going to call it from now — and the unit root.

---

## Slide 3: The Trend Model

**Slide content:** Many time series have trends. OLS estimation with a deterministic trend is equivalent to estimation after linear detrending (FWL theorem). Including a linear/quadratic time trend is the easiest method. But deterministic trend is not the only possibility — stochastic trend has very different implications and is hard to distinguish.

**Professor Pesavento adds:** This slide sets up the contrast. Deterministic trends are conceptually simple — include `t` in your regression and you're done. The rest of the lecture is about what happens when the trend isn't deterministic.

---

## Slide 4: Stochastic Trends — Definitions

**Slide content:**
- **Random Walk:** y_t = y_{t-1} + epsilon_t
- **Random Walk with Drift:** y_t = c + y_{t-1} + epsilon_t
- First difference of both is epsilon_t (stationary)
- y_t is I(d) if the d-th difference is stationary
- AR coefficient > 1 means explosive process

**Professor Pesavento's explanation:**

> What is a random walk? It's exactly an autoregressive model of order one when that coefficient is equal to one. So AR(1) is y_t = rho * y_{t-1} + white noise. So that's why it's also called a unit root — because it's an autoregressive with the root equal to one.

She connects back to earlier lectures:

> Remember that when we talked about AR(1)... we had the assumption that rho had to be strictly less than one. So that infinite sum that we had there had to converge. Now we're saying, what happens when rho equals one?

On the first difference and integration order:

> If I take the first difference of a random walk, I get white noise — something that is stationary. This is what we say: y_t is integrated of order d if the d-th difference is stationary. So a random walk is integrated of order one.

**Connection to Python's ARIMA command:**

> In Python, when you do the ARIMA command, you have three choices: ARIMA(p, d, q). The `d` in the middle is the same `d` I have here. If `d=1`, it says I have a model that is integrated order one, and I want to fit ARMA on the first difference. You can also do it by steps — take the first difference yourself and then tell it to do ARIMA(p, 0, q).

---

## Slide 5: Stochastic Trends — Plots

**Slide content:** Two plots showing simulated data — Random Walk (left) and Random Walk with Drift (right). The RW shows long swings up and down with no clear trend; the RW with drift shows an upward trajectory that looks like a deterministic trend.

**Professor Pesavento's key point — this is the heart of the problem:**

> If you knew nothing about random walks, what would you tell me about this data? You'd say you see a trend. And the one with drift — maybe quadratic. The key thing I want to tell you is that I generated this as a random walk. With 300 observations, it's going to be really hard for you to detect with the naked eye whether this is a deterministic trend or a stochastic trend.

(Handwritten annotations on slide: "deterministic or stochastic trend" with arrow pointing to the plots)

> We're going to see next what are the implications of having a stochastic trend, and you will see that the implications are quite important. Yet you won't be able to see it with the naked eye. You're going to have to test with good statistical tests.

She provides historical context:

> This problem was discovered in the late 80s, early 90s, and there were so many papers written about what is the best test — how can we detect if macro data has a unit root or not — because it's a very, very important question.

---

## Slides 6-8: Random Walk Properties

**Slide 6 content:** By back-substitution: y_t = y_0 + SUM(epsilon_j). Initial condition doesn't disappear. AR polynomial alpha(z) = 1 - z is not invertible.

**Slide 7 content (Random Walk):**
- E(y_t) = 0
- Var(y_t) = t * sigma^2
- gamma_k = (t-k) * sigma^2
- rho_k = sqrt((t-k)/t) -> 1

**Slide 8 content (Random Walk with Drift):**
- E(y_t) = ct (linear trend in the mean)
- Same variance and autocovariance structure
- Both clearly not weakly stationary

**Professor Pesavento's explanation:**

> For a random walk, if you substitute backwards, you can write it as an infinite sum of the epsilons. The variance is t times sigma squared. So the variance today is going to be different than the variance tomorrow, different than next week. The variance changes over time — so it's not stationary.

> As t gets very large, the variance gets very large. So if GDP is a unit root and I want to predict what GDP is going to be in 20 years, the variance is so big that I would not be able to say where it goes.

On the autocorrelation converging to 1:

> The autocorrelation, as t gets large, converges to one. This is saying that if I try to predict in the future where y_t is going to be, my best guess is where it is today, because everything else is noise.

**The drunk person analogy:**

> The image that people use all the time for a random walk: imagine a drunk person walking down the street. The person stumbles around — you cannot predict where they go. They don't walk in a rational way. Occasionally they hit a curb, and they go one way for a very long time, until they hit a pebble, and then they go this way. But you cannot predict where they're going. So if this random drunk person is here and you have to guess which way they're going — you have no guess. You may as well say that your best prediction is going to be where they are right now.

---

## Slides 9-10: Forecasts — Trend vs. Stochastic Trend

**Slide content:**

Deterministic trend: y_t = alpha + ct + Psi(L)*epsilon_t
- Forecast converges to alpha + c(t+s) as s -> infinity

Stochastic trend: Delta_y_t = c + Psi(L)*epsilon_t
- Forecast converges to sc + y_t as s -> infinity

Two very different implications for forecasting.

**Professor Pesavento's extended explanation with class interaction:**

She walks through the deterministic trend case first:

> Suppose I want to forecast GDP. I have 100 observations and want to forecast 10 months ahead. If it's a deterministic trend, my best forecast is the mean of the data plus the slope times 110. It doesn't matter when I start — it's always going to project forward on the trend.

Then the stochastic trend:

> If this is a stochastic trend instead, it's going to look different. My forecast is still going to have slope c, but I'm going to start from where I am today. If I wait a little longer, maybe the data goes down, and now I forecast again — the slope is still c, but now I end up somewhere different.

> So in one case, no matter where I start, I end up in the same place. In the second case, the starting point matters, and every time you have new data, you may change your forecast.

**Student question:** "Is there one that is better or worse for forecasting?"

**Professor Pesavento's answer:**

> No, that's a good question. Neither is inherently better. With a deterministic trend, you can forecast y_t itself. With a stochastic trend, y_t is much harder to forecast, but you can forecast the first difference very well. So it tells you: in one case forecast y_t, in the other forecast Delta_y_t. They're two different implications of two different models. Therefore we should know which model is behind our data.

---

## Slide 11: MSE — Trend vs. Stochastic Trend

**Slide content:**
- Deterministic trend: MSE = (1 + psi_1^2 + psi_2^2 + ... + psi_{s-1}^2) * sigma^2 — converges to unconditional variance
- Stochastic trend: MSE = {1 + (1+psi_1)^2 + (1+psi_1+psi_2)^2 + ... } — does NOT converge

**Professor Pesavento notes:** The mean square error being potentially infinite for the stochastic trend case is another way of saying the variance of your forecast error keeps growing. This is why "we cannot forecast" a unit root process at long horizons.

She illustrates the accumulation of forecast errors:

> One step ahead: I'm missing epsilon_{t+1}. Two steps ahead: I'm missing epsilon_{t+1} plus epsilon_{t+2}. They add up! The further you go, the more you're missing, and the bigger and bigger the forecast error becomes.

---

## Slide 12: Dynamic Multipliers — Trend vs. Stochastic Trend

**Slide content:**
- Deterministic trend: dy_{t+s}/d(epsilon_t) = psi_s -> 0 (shock vanishes)
- Stochastic trend: dy_{t+s}/d(epsilon_t) = 1 + psi_1 + ... + psi_s -> Psi(1) (shock is permanent)

**Professor Pesavento on policy implications:**

> This is all to say what we already know: if I have a shock today and the coefficient is less than one, the shock eventually disappears. If rho equals one, any shock today will never disappear — it has a permanent effect. These are two very different implications. Suppose I'm a policymaker and I want to surprise the economy with a policy shock. I need to know if the effect is going to be permanent or temporary.

**Student Q&A:**

> **Student:** "When you say the effect is permanent, does it just mean to some degree, or is it constantly at that same magnitude?"
>
> **Pesavento:** "If rho is exactly equal to one, it stays forever at that same magnitude. Yes."

---

## Slides 13-15: Transformations to Achieve Stationarity

**Slide 13:** Detrending works for trend stationary (y_t - ct = mu + epsilon_t is stationary). But for unit root with drift, detrending gives y_t - ct = y_0 + SUM(epsilon_j), which still has variance t*sigma^2. Detrending is not enough.

**Slide 14:** First differencing works for unit root (Delta_y_t = c + epsilon_t). But for trend stationary, Delta_y_t = c + epsilon_t + epsilon_{t-1} — introduces a unit root in the MA part (non-invertible).

**Slide 15:** There is no single solution. Nelson and Plosser (1982) argued many series have unit roots. Distinguishing the two models in finite sample is very hard. Testing has become a crucial step.

**Professor Pesavento's explanation:**

> If I have a deterministic trend, I can detrend. If I have a stochastic trend, I need to take the difference. You tell me, "Can we just take the difference of everything?" The problem is, if I take the difference of trend stationary data, I end up with something that's not good either — I introduce a unit root in the MA part and lose invertibility.

> So the truth is: you need to make sure whether your data has a deterministic or stochastic trend, because what you need to do to make it stationary is very different, and there is not a solution that works for both.

She gives the historical narrative:

> In the 80s, Nelson and Plosser argued that many data had unit roots and you need to difference. Then people said "hold on, let's test." They realized many early tests performed poorly — concluding unit roots when there weren't any. Then in the 90s, much better testing came along (this was my dissertation). We realized that a lot of the macro data probably does not have a unit root. What is true is most macro data is probably not exactly a unit root, but still very persistent — around 0.9-0.95.

> What does that mean in practice? The shock will have an effect that lasts for a very long time, but eventually dies out. And in practice, when you have only 20 years of data, is 0.95 really different from 1? That's a very nuanced argument.

---

## Slides 16-19: Unit Root Tests — Dickey-Fuller

**Slide 16:** Benchmark case — reparameterize AR(1) as Delta_y_t = alpha * y_{t-1} + epsilon_t where alpha = rho - 1. H0: alpha = 0 (unit root) vs H1: alpha < 0 (stationary). Use t-test.

**Slide 17:** Under the null, the t-test does NOT have the standard normal distribution. Random walks behave differently (Brownian motions). You must use the Dickey-Fuller critical values, not the normal ones.

**Slide 18:** Two specifications: intercept only vs. intercept + trend. Critical values differ between the two (the test is non-pivotal).

**Slide 19:** Table of DF critical values.

**Professor Pesavento's explanation of the test mechanics:**

> So this is a regression I can do, and my hypothesis is: if rho = 1, then alpha = 0 (unit root). If rho < 1, then alpha < 0 (stationary). One option that people realized is, OK, I can just run this by OLS — regress the first difference on the lagged level and do a regular t-test. Seems very easy. And that's what Nelson and Plosser did. The problem is that later on, somebody figured out that unfortunately it's more complicated than that.

On why the distribution is non-standard:

> Under the null — which is the case where the data has a unit root — things behave very differently than normal. The test does not have the usual distribution. It has a distribution much more shifted to the left. It's called the Dickey-Fuller distribution. If you're a big finance person, this relates to continuous processes and Brownian motions.

On the non-pivotal nature:

> In a standard regression, no matter what other variables you have, the t-statistic is still normally distributed and you look at the same critical values. When you have a unit root, whether you have a constant or a trend in the regression matters — the critical values are different. So you have to make that decision ahead of time.

**Her practical guidance on choosing the specification:**

> Look at the data. If something looks like it might be stationary around a constant, use intercept only. If it looks like there might be a trend — either drift or deterministic — then include the trend in the regression.

---

## Slide 20: Augmented Dickey-Fuller (ADF) Test

**Slide content:** In most cases, AR(1) is too simple. Include lags of the first difference:

Delta_Y_t = mu + alpha*Y_{t-1} + gamma_1*Delta_Y_{t-1} + ... + gamma_{p-1}*Delta_Y_{t-p+1} + u_t

Same t-test on alpha = 0, same DF critical values. Decide trend or no trend. Reject if t-stat < DF critical value.

**Professor Pesavento:**

> In most cases, models are more complicated than AR(1). You have more dynamics. So you have the augmented Dickey-Fuller test — regress the difference on the lagged level plus lags on the first difference. You tell Python you want an ADF test, tell it how many lags. Choosing the number of lags is not an easy task.

---

## Slide 21: Trend or No Trend?

**Slide content:** The choice depends on what the alternative is and what the data looks like.
- Intercept only: alternative is Y stationary around a constant
- Intercept + trend: alternative is Y stationary around a linear time trend

---

## Slides 22-23: Example — US Inflation Rate

**Slide 22:** Plot of US inflation rate (1960-present), showing no obvious trend, fluctuations around zero.

**Slide 23:** ADF test results — Constant only, AIC selects 8 lags. Test statistic: -3.94, p-value: 0.0018. Critical values: 1% = -3.44, 5% = -2.87, 10% = -2.57. Reject at all levels but close at 1%.

**Professor Pesavento's discussion:**

> First thing: would you include the trend or constant only? [Class responds: constant only — no obvious trend in inflation.]

> The test statistic is -3.94 with a p-value of 0.0018. This is more negative than any of the critical values, so at all levels I reject. Rejecting means: I reject the null of a unit root. So the data does not have a unit root.

But she immediately adds nuance:

> I would say that -3.94 with a critical value of -3.43 is actually very close. You reject, yes, but you barely reject. And in a situation like this, where it's so difficult to detect, you may want to think about what you believe is happening. You may add more data, take more data off, and the result could change. People argue forever about what has a unit root and what doesn't.

**Student question about breaks:**

> **Student:** "Could structural breaks show up as a unit root if we didn't account for them?"
>
> **Pesavento:** "That's very good — exactly correct. You pinpoint years of research. If there is an obvious break and you ignore it, then you do a unit root test, you may conclude there is a unit root when there isn't one. People came up with unit root tests that allow for breaks, or you can include break dummies."

---

## Slide 24: Stationarity Tests

**Slide content:** Why test the null of non-stationarity? We usually prefer a null we'd like to not reject. Stationarity tests (H0: stationary, H1: unit root) exist as complements. Don't expect the two test types to agree — they can reject for different reasons.

---

## Slide 25: Summary

**Slide content:**
1. Random walk is the workhorse model for trends in economic time series
2. First plot, then test (choose intercept or intercept+trend)
3. Detection is not easy: use multiple tests
4. Fail to reject -> unit root; reject -> no unit root
5. If unit root: use Delta_y_t for regression and forecasting

---

## Slides 26-27: Which Test & Final Notes

**Slide 26:**
- Any test struggles to distinguish rho = 0.95 from rho = 1 in finite samples
- Use the most powerful tests available (DF-GLS, ERS)
- Present a battery of tests
- Consider stationarity tests too
- Lag selection matters (AIC, BIC, MAIC)
- Watch for confounders (breaks, heteroskedasticity, seasonality)

**Slide 27:**
- Not an easy question — don't expect an easy answer
- Beliefs have shifted: "everything is a unit root" -> "most things are persistent but not exactly unit root" (near unit root / fractional integration)
- Make a good case and move on
- Don't apply filters (HP, BK) to non-stationary data
- When in doubt, don't impose potentially wrong restrictions
- Recent consensus: use robust methods, leave things in levels in VARs

**Professor Pesavento's practical framework:**

> First, plot the data — always a good habit. Then if a trend looks possible, test with the trend included. If you don't see a trend but suspect a unit root, test with just a constant. Use a package. If your package gives you different tests, look at all of them.

> If you reject clearly with all tests: no unit root. If you fail to reject: unit root. If you're somewhere in between — some tests reject, some don't, you barely reject or barely don't — then stop and spend some time thinking. Make a decision and go with it, but be ready to justify your decision.

> If you find a unit root and you're very convinced, then the best course of action is to work on forecasting and modeling the first difference. Take the first difference, and then treat that as your variable.

Her final word of caution:

> There is some reason to believe nowadays that not differencing may be better for some things. This is not an easy question. Make a good case for what you want to do and move on.

---

## ACF/PACF Behavior for Unit Root Processes

**From class discussion (not on slides):**

> **Student:** "What does the ACF/PACF look like for a unit root?"
>
> **Pesavento:** "If this is a unit root, the ACF is going to be 1, 1, 1, 1, 1, 1..."
>
> **Student:** "So the PACF would just drop down after the first one?"
>
> **Pesavento:** "Yes, go down."

This is a practical diagnostic: if the ACF decays extremely slowly (stays near 1 for many lags) and the PACF cuts off after lag 1 with a value near 1, suspect a unit root.

---

## Professor Pesavento's Key Practical Takeaways

1. **You cannot eyeball the difference** between deterministic and stochastic trends with 300 observations
2. **The wrong transformation is worse than no transformation** — detrending a unit root or differencing a trend stationary process both create problems
3. **Shocks are permanent under unit root** — this matters enormously for policy analysis
4. **Inflation is the classic ambiguous case** — persistent but probably not exactly I(1)
5. **Structural breaks can masquerade as unit roots** — always consider this
6. **Most macro data is "near unit root"** (rho ~ 0.9-0.95) — the effect dies out eventually but very slowly
7. **When in doubt, don't impose** — robust methods that work regardless of unit root status are increasingly preferred
8. **Make a defensible decision and move on** — this is a pragmatic field, not a philosophical one
