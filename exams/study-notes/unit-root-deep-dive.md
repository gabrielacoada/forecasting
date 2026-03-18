# Unit Roots: The Complete Guide

**What this is**: A from-scratch explanation of unit roots, random walks, why they matter, how to test for them (Dickey-Fuller / ADF), and what to do when you find one. Professor Pesavento confirmed unit roots will be on the exam.

**How to use this**: Read Parts 1-8 for understanding (60-75 min). On exam morning, skip to the Cheat Sheet at the end.

---

## Lecture Reference Guide

| Topic | File Path | What's There |
|-------|-----------|-------------|
| **Random walk definition** | `week-07/Unit+Root+Tests.pdf` slide 4 | y_t = y_{t-1} + epsilon_t; annotations: "AR(1) → rho = 1" |
| **RW properties (variance, ACF)** | `week-07/Unit+Root+Tests.pdf` slides 7-8 | Var = t*sigma², rho_k → 1; annotations: "ON" (clearly not stationary) |
| **Drunk person analogy** | `week-07/transcripts/Forecasting.txt` | "Your best prediction is where he is right now" |
| **Det. vs stochastic trend forecasts** | `week-07/Unit+Root+Tests.pdf` slides 9-10 | Det: converges to trend line; Stoch: depends on y_t |
| **MSE comparison** | `week-07/Unit+Root+Tests.pdf` slide 11 | Det: converges; Stoch: grows without bound |
| **Dynamic multipliers** | `week-07/Unit+Root+Tests.pdf` slide 12 | Det: shock → 0; Stoch: shock → Psi(1) permanent |
| **Wrong transformation danger** | `week-07/Unit+Root+Tests.pdf` slides 13-14 | Detrend a UR → still non-stationary; Difference a trend → MA unit root |
| **DF test setup** | `week-07/Unit+Root+Tests.pdf` slide 16 | Delta_y = alpha*y_{t-1} + eps; alpha = rho-1 |
| **DF critical values** | `week-07/Unit+Root+Tests.pdf` slide 19 | Table: intercept only vs intercept+trend |
| **Non-normal distribution** | `week-07/Unit+Root+Tests.pdf` slide 17 | "You cannot use the tables for the Normal" |
| **Non-pivotal property** | `week-07/Unit+Root+Tests.pdf` slide 18 | Different specs → different critical values |
| **ADF test** | `week-07/unit-roots-summary.md` section 8 | Add lagged differences; same DF critical values |
| **Inflation worked example** | `week-07/unit-roots-summary.md` section 9 | ADF = -3.94 > 1% CV; reject unit root |
| **Near-unit-root consensus** | `week-07/transcripts/Forecasting.txt` | "Most macro data around 0.9-0.95" |
| **Structural breaks masquerade** | `week-07/unit-roots-summary.md` section 9 | Ignored breaks → false unit root conclusion |
| **KPSS (reverse test)** | `week-07/unit-roots-summary.md` section 10 | H0: stationary; H1: unit root |
| **Practical framework** | `week-07/unit-roots-summary.md` section 11 | Pesavento's 8-step decision process |
| **Past exam: Q7 why test for UR** | `exams/past-exams/422Final02.pdf` Q7 | 10 pts conceptual |
| **Past exam: Q8 DF interpretation** | `exams/past-exams/422Final02.pdf` Q8 | 5 pts — interpret DF output with/without trend |

---

## Part 1: What Is a Unit Root and Why Should You Care?

### 1.1 The Core Problem

Everything in this course — ARMA models, Wold decomposition, CLT, OLS inference — **requires stationarity**. If your data is non-stationary, none of those tools work properly.

Pesavento (transcript): *"To do anything that we've done about constructing and finding the best ARMA model, you need the data to be stationary. If you have a unit root, the Wold theory and all the ARMA models do not apply. And also the CLT does not apply."*

There are several causes of non-stationarity (deterministic trends, structural breaks, time-varying variance), but the most common one in macro data is a **stochastic trend** — also known as a **unit root** or **random walk**.

### 1.2 Why It Matters for the Exam

The answer to "why test for a unit root?" (Exam 2 Q7, 10 pts) is:

1. **It determines your transformation.** Trend stationary → detrend. Unit root → difference. Using the wrong one makes things worse.
2. **It determines your forecasting method.** Deterministic trend → forecast converges to the trend line regardless of today's value. Unit root → forecast depends entirely on today's value.
3. **It determines whether shocks are permanent or temporary.** This has policy implications.
4. **Standard inference (t-tests, F-tests) breaks down** under a unit root — the usual critical values are wrong.

---

## Part 2: Definitions

### 2.1 Random Walk (No Drift)

$$y_t = y_{t-1} + \varepsilon_t \qquad \varepsilon_t \sim WN(0, \sigma^2)$$

This is just an AR(1) with $\rho = 1$. Pesavento's annotation on slide 4: "AR(1) → rho = 1."

Other names for the same thing: **unit root process**, **integrated process**, **martingale**.

### 2.2 Random Walk with Drift

$$y_t = c + y_{t-1} + \varepsilon_t$$

Same thing but with a constant $c$. The drift creates a linear trend in the mean (the data drifts upward or downward on average), but the variance still grows with time.

### 2.3 Integration Order

$y_t$ is **integrated of order $d$**, written $I(d)$, if the $d$-th difference is stationary.

- Random walk: $\Delta y_t = \varepsilon_t$ → stationary after one difference → $y_t$ is **I(1)**
- Stationary process: already stationary without differencing → **I(0)**
- If you had to difference twice → I(2) (rare in practice)

Pesavento (transcript): *"A random walk, a stochastic trend, a unit root, integrated order one — you can think that in a broad sense, they all mean the same thing."*

### 2.4 Connection to Python

In `ARIMA(p, d, q)`, the middle parameter $d$ is the integration order:
- `ARIMA(2, 0, 1)` = ARMA(2,1) on the levels (data is stationary)
- `ARIMA(2, 1, 1)` = take first difference, then fit ARMA(2,1) on $\Delta y_t$

---

## Part 3: Properties of a Random Walk (Why It's Not Stationary)

### 3.1 Back-Substitution

Start from $y_t = y_{t-1} + \varepsilon_t$ and substitute repeatedly:

$$y_t = y_{t-1} + \varepsilon_t = y_{t-2} + \varepsilon_{t-1} + \varepsilon_t = \cdots = y_0 + \sum_{j=1}^{t} \varepsilon_j$$

The random walk is a **cumulative sum of all past shocks**. Every shock ever received stays in the process forever. The initial condition $y_0$ never disappears.

### 3.2 Properties (from slides 7-8)

| Property | Random Walk | Random Walk with Drift |
|----------|-------------|----------------------|
| **Mean** | $E(y_t) = 0$ | $E(y_t) = ct$ |
| **Variance** | $\text{Var}(y_t) = t\sigma^2$ | $\text{Var}(y_t) = t\sigma^2$ |
| **Autocovariance** | $\gamma_k = (t-k)\sigma^2$ | $\gamma_k = (t-k)\sigma^2$ |
| **Autocorrelation** | $\rho_k = \sqrt{(t-k)/t} \to 1$ | $\rho_k \to 1$ |

### 3.3 Why Each Property Breaks Stationarity

**Variance depends on $t$**: At $t = 10$, $\text{Var} = 10\sigma^2$. At $t = 100$, $\text{Var} = 100\sigma^2$. The process gets more and more spread out over time. Stationarity requires constant variance.

**Autocovariance depends on $t$, not just on $k$**: $\gamma_k = (t-k)\sigma^2$ depends on when you are ($t$), not just on the lag ($k$). Stationarity requires $\gamma_k$ to depend only on $k$.

**Autocorrelation converges to 1**: As $t$ grows, $\rho_k \to 1$ for any fixed $k$. This means the series is almost perfectly correlated with its own past. In the ACF, you'll see bars that decline very slowly — they barely decay.

Pesavento (transcript): *"If I try to predict in the future where y_t is going to be, my best guess is where it is today, because everything else is noise."*

### 3.4 The Drunk Person Analogy

Pesavento (transcript): *"Imagine a drunk person walking down the street. They stumble around randomly. They hit a curb and drift one way for a very long time, until they hit a pebble and go the other way. You cannot predict where they're going. Your best prediction is where they are right now."*

This captures two key intuitions:
1. **The best forecast is today's value** (because you can't predict the random stumbles)
2. **Long swings look like trends** (the person drifts in one direction for a while — mimicking a trend — but it's just random accumulation)

---

## Part 4: Deterministic Trend vs. Stochastic Trend — The Central Comparison

This is the most important section of the lecture. The two models **look similar** but have **completely different implications**.

### 4.1 The Two Models Side by Side

**Deterministic trend (trend stationary):**
$$y_t = \alpha + ct + \Psi(L)\varepsilon_t$$

The trend is a fixed rail. The data wiggles around it but always returns.

**Stochastic trend (unit root):**
$$\Delta y_t = c + \Psi(L)\varepsilon_t \qquad \Leftrightarrow \qquad y_t = y_{t-1} + c + \text{ARMA stuff}$$

The trend is itself random. The data wanders and never returns to a fixed path.

### 4.2 Forecasting (slides 9-10)

| | Deterministic Trend | Stochastic Trend |
|---|---|---|
| **Long-run forecast** | Converges to $\alpha + c(t+s)$ | Converges to $sc + y_t$ |
| **Depends on $y_t$?** | **No** — forecast is the same regardless of where you are today | **Yes** — forecast starts from today's value |
| **Starting point matters?** | No | Yes, completely |
| **New data changes forecast?** | No | Yes, every new observation shifts the whole path |

Pesavento's GDP example (transcript): *"With a deterministic trend, it doesn't matter when I start my forecast — I always end up at the same projected trend value. With a stochastic trend, your forecast made from a different starting point gives a different answer every time."*

**Student question:** "Is one better for forecasting?"

**Pesavento:** *"No. With a deterministic trend, you can forecast y_t itself. With a stochastic trend, y_t is much harder to forecast, but you can forecast the first difference very well. They're two different implications of two different models. Therefore we should know which model is behind our data."*

### 4.3 MSE (slide 11)

| | Deterministic Trend | Stochastic Trend |
|---|---|---|
| **MSE** | $(1 + \psi_1^2 + \psi_2^2 + \cdots + \psi_{s-1}^2)\sigma^2$ | Does **not** converge |
| **As $s \to \infty$** | Converges to $\text{Var}(y_t)$ (finite) | **Grows without bound** |

With a unit root, your forecast error MSE explodes as the horizon increases. You literally cannot forecast far ahead with any precision.

### 4.4 Dynamic Multipliers — Permanent vs. Temporary Shocks (slide 12)

| | Deterministic Trend | Stochastic Trend |
|---|---|---|
| **Effect of shock at $t$** | $\partial y_{t+s}/\partial\varepsilon_t = \psi_s$ | $\partial y_{t+s}/\partial\varepsilon_t = 1 + \psi_1 + \cdots + \psi_s$ |
| **As $s \to \infty$** | $\to 0$ (temporary) | $\to \Psi(1)$ (permanent) |

**Deterministic trend**: Shocks die out. A recession is temporary — the economy returns to trend.

**Stochastic trend**: Shocks are **permanent**. A recession permanently shifts the level of GDP. The economy never fully recovers to where it would have been.

Pesavento (transcript): *"Suppose I'm a policymaker and I want to surprise the economy with a policy shock. I need to know if the effect is going to be permanent or temporary. And even if temporary, how quickly it disappears."*

**Student Q:** "When you say permanent, is it at the same magnitude forever?"

**Pesavento:** *"If rho is exactly equal to one, yes. It stays forever at the same magnitude."*

---

## Part 5: Transformations — Why You Can't Just Pick One

### 5.1 The Trap (slides 13-14)

You might think: "just difference everything to be safe." **Wrong.** Each transformation works for one model and breaks the other.

**Option 1: Detrend** (subtract the trend)

- If data is **trend stationary**: $y_t - ct = \mu + \varepsilon_t$ → stationary. Works!
- If data has a **unit root with drift**: $y_t - ct = y_0 + \sum \varepsilon_j$ → still has variance $t\sigma^2$. **Fails.** Detrending removes the trend in the mean but NOT in the variance.

**Option 2: Take the first difference**

- If data has a **unit root**: $\Delta y_t = c + \varepsilon_t$ → stationary. Works!
- If data is **trend stationary**: $\Delta y_t = c + \varepsilon_t + \varepsilon_{t-1}$ → introduces a **unit root in the MA part** (non-invertible). **Fails.** You've over-differenced.

Pesavento (transcript): *"The truth is: you need to make sure whether your data has a deterministic or stochastic trend, because what you need to do to make it stationary is very different, and there is not a solution that works for both."*

### 5.2 Summary Decision Rule

| Data Type | Correct Action | Wrong Action |
|-----------|---------------|--------------|
| **Trend stationary** | Detrend (include trend in regression) | Differencing (introduces MA unit root) |
| **Unit root** | Difference ($\Delta y_t$) | Detrending (variance still explodes) |

**This is exactly why you need to test for a unit root before choosing your transformation.**

---

## Part 6: The Dickey-Fuller Test

### 6.1 Setup (slide 16)

Start from the AR(1): $y_t = \rho y_{t-1} + \varepsilon_t$

Reparameterize by subtracting $y_{t-1}$ from both sides:

$$\Delta y_t = \alpha \cdot y_{t-1} + \varepsilon_t \qquad \text{where } \alpha = \rho - 1$$

Now the hypotheses are clean:

$$H_0: \rho = 1 \;\Leftrightarrow\; \alpha = 0 \quad \text{(unit root)}$$
$$H_1: \rho < 1 \;\Leftrightarrow\; \alpha < 0 \quad \text{(stationary)}$$

The test statistic looks like a t-test:

$$t = \frac{\hat{\alpha}}{SE(\hat{\alpha})}$$

### 6.2 Why You Can't Use Normal Critical Values (slide 17)

This is the key subtlety. The test statistic $t$ **does NOT follow a normal or t-distribution** under the null. It follows the **Dickey-Fuller distribution**, which is shifted to the left.

Pesavento (slides): *"Under the null hypothesis, the t-test does not have the standard distribution. Why? Random walks behave differently and have very different statistical properties. A normal is not a good approximation. (Brownian Motions.) You can still use the t-statistic but you have to look at a different table of critical values."*

If you used the standard t-table (critical value -1.96 at 5%), you would **reject the null too often** — falsely concluding there's no unit root when there actually is one. The DF critical values are more negative (harder to reject), accounting for the non-standard distribution.

### 6.3 Critical Values (slide 19)

| Specification | 10% | 5% | 1% |
|---|---|---|---|
| **Intercept only**: $\Delta y_t = \mu + \alpha y_{t-1} + u_t$ | -2.57 | **-2.86** | -3.43 |
| **Intercept + trend**: $\Delta y_t = \mu + ct + \alpha y_{t-1} + u_t$ | -3.12 | **-3.41** | -3.96 |

**Decision rule**: Reject $H_0$ (reject unit root) if the test statistic is **more negative** than the critical value. This is a **one-sided test** — you only look at the left tail.

**Example**: Test statistic = -3.12. With intercept only: -3.12 < -2.86 → **reject at 5%** (no unit root). With intercept + trend: -3.12 is NOT < -3.41 → **fail to reject at 5%** (can't rule out unit root).

### 6.4 The Test Is "Non-Pivotal" (slide 18)

Unlike normal t-tests, what you include in the regression **changes the critical values**. Adding a trend term makes the critical values more negative (harder to reject).

This means: **you must decide the specification (intercept only vs. intercept + trend) BEFORE running the test.**

**How to choose:**
- **Intercept only**: when data fluctuates around a constant (no obvious trend) — e.g., inflation rate, interest rate spreads
- **Intercept + trend**: when data has a visible upward/downward drift that could be either deterministic or stochastic — e.g., GDP, stock prices, population

### 6.5 Augmented Dickey-Fuller (ADF)

Real data is more complex than AR(1). The ADF test adds lagged differences to capture richer dynamics:

$$\Delta y_t = \mu + \alpha y_{t-1} + \gamma_1 \Delta y_{t-1} + \gamma_2 \Delta y_{t-2} + \cdots + \gamma_{p-1} \Delta y_{t-p+1} + u_t$$

- Still testing $\alpha = 0$ using the **same DF critical values**
- The lagged differences clean up the residual serial correlation
- **Choosing lags**: Use AIC or BIC. Reasonable max: 12 for monthly, 4 for quarterly.
- Most software (Python, Stata, R) auto-selects the lags

---

## Part 7: Practical Decision Framework (Pesavento's Steps)

This is the real-world workflow Pesavento recommends:

**Step 1: Plot your data.** Always look at it first.

**Step 2: Does a trend look plausible?** If yes → include trend in the test regression. If no obvious trend → intercept only.

**Step 3: Run the ADF test.** Use a software package. Let it auto-select lags (or use AIC/BIC).

**Step 4: Interpret the result.**

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| **Clearly reject** (statistic << critical value, small p-value) | No unit root. Data is stationary (possibly trend stationary). | Model in levels. Include trend if visible. |
| **Clearly fail to reject** (statistic close to 0, large p-value) | Unit root. | Take first difference, then model $\Delta y_t$ with ARMA. |
| **Borderline** (close to critical value) | Ambiguous. | Think. Run multiple tests. Consider structural breaks. Justify your decision. |

**Step 5: If unit root → work with first differences.** Take $\Delta y_t = y_t - y_{t-1}$, then fit ARMA to the differenced series.

### 7.1 The Near-Unit-Root Reality

Pesavento (transcript): *"Most macro data is probably not exactly a unit root, but still very persistent — around 0.9-0.95. The shock will last for a very long time, but eventually dies out. In practice, with only 20 years of data, is 0.95 really different from 1?"*

This is why unit root testing is genuinely hard. The current consensus:
- Early tests (1980s) had low power → falsely concluded unit roots everywhere
- Better tests (1990s, Pesavento's own work) revealed many series are persistent but stationary
- In finite samples, $\rho = 0.95$ is nearly indistinguishable from $\rho = 1$
- When in doubt, use robust methods that work regardless

### 7.2 Structural Breaks Can Fool the Test

If data has a structural break and you ignore it, the ADF test can falsely conclude there's a unit root. The break creates a persistent shift that mimics unit root behavior.

**Solution**: Include break dummies in the test regression, or use unit root tests that allow for breaks.

---

## Part 8: Worked Examples

### 8.1 Worked Example: US Inflation Rate

From the lecture:

1. **Visual inspection**: No obvious trend — fluctuates around a level → use **intercept only**
2. **ADF test**: Auto-selected 8 lags (AIC, max=8)
3. **Test statistic**: -3.94
4. **Critical values (intercept only)**: 1% = -3.44, 5% = -2.87, 10% = -2.57
5. **Decision**: -3.94 < -3.44 → **Reject at 1%**. No unit root.

**But Pesavento cautions**: Inflation is very persistent ($\rho \approx 0.9$-$0.95$). The result could change with different sample sizes. Many researchers historically treated inflation as I(1). It's a borderline case — one of the hardest in applied macro.

### 8.2 Exam 2 Q7: "Why Is It Important to Test for a Unit Root?" (10 pts)

**Model answer** (combining Pesavento's lecture points):

Testing for a unit root is important because the answer determines:

1. **How to transform the data.** If the data has a unit root, we must take first differences to achieve stationarity. If the data is trend stationary, we should detrend instead. Using the wrong transformation causes problems — differencing a trend stationary series introduces an MA unit root (non-invertible); detrending a unit root process leaves the variance growing over time.

2. **How to forecast.** With a deterministic trend, the long-run forecast converges to the trend line regardless of today's value. With a unit root, the forecast depends entirely on today's value — every new observation shifts the entire forecast path. The forecast MSE is finite for trend stationary but grows without bound for a unit root.

3. **Whether shocks are permanent or temporary.** Under a deterministic trend, the dynamic multiplier goes to zero — shocks die out and the economy returns to trend. Under a unit root, the dynamic multiplier converges to $\Psi(1) \neq 0$ — shocks have a permanent effect. This matters for policy: if I implement a policy shock, I need to know if the effect will persist.

4. **Whether standard inference is valid.** Under a unit root, the usual t-statistics do not follow a normal distribution. Using standard critical values (like -1.96) leads to incorrect conclusions. Special critical values (the Dickey-Fuller distribution) are required.

### 8.3 Exam 2 Q8: Interpreting DF Test Output (5 pts)

**Given** (from the exam):

Without trend: Test statistic = -0.309, 5% CV = -2.885, p = 0.9242

With trend: Test statistic = -1.989, 5% CV = -3.441, p = 0.6073

**Answer**:

First, determine which specification is appropriate. Carspend (car expenditure) is an economic variable that shows an upward drift over time — this suggests using the specification **with trend**.

With trend: the test statistic (-1.989) is NOT more negative than the 5% critical value (-3.441). We **fail to reject** the null of a unit root. The p-value of 0.6073 confirms — it's nowhere close to rejecting.

Even without trend: -0.309 is far from -2.885. Fail to reject in both cases.

**Conclusion**: The data appears to have a unit root. We should work with first differences ($\Delta$carspend) when modeling.

---

## Common Exam Traps

### Trap 1: Using -1.96 as the critical value

**Wrong**: "The test statistic is -2.3. Since -2.3 < -1.96, we reject the unit root."

**Right**: The DF distribution is NOT normal. With intercept only, the 5% CV is **-2.86**, not -1.96. Since -2.3 > -2.86, we **fail to reject**. The data has a unit root.

This is the #1 unit root mistake. Pesavento's slides say explicitly: *"You cannot use the tables for the Normal."*

### Trap 2: Forgetting the test is one-sided (left-tail only)

You reject when the statistic is very **negative** (more negative than the CV). A positive test statistic (e.g., +0.5) means you're nowhere near rejecting — it actually suggests the coefficient is on the wrong side entirely.

### Trap 3: Using the wrong specification's critical values

If your data has a trend and you use the "intercept only" critical values (-2.86), you're using the wrong table. The "intercept + trend" critical values are more negative (-3.41). Always match the specification to the critical values.

### Trap 4: Thinking "difference everything to be safe"

Over-differencing a trend-stationary series introduces an MA unit root (non-invertibility). It's NOT safe. You must test first.

### Trap 5: Confusing the null hypothesis direction

| Test | H0 | H1 | "Reject" means... |
|------|----|----|-------------------|
| **ADF** | Unit root ($\alpha = 0$) | Stationary ($\alpha < 0$) | No unit root (good!) |
| **KPSS** | Stationary | Unit root | Has unit root |

ADF and KPSS have **opposite** null hypotheses. Don't mix them up. ADF's null is "bad" (unit root), so rejecting is the "good" outcome.

### Trap 6: Ignoring structural breaks

A structural break (like the 2008 crisis) can look like a unit root to the ADF test — the persistent shift mimics non-stationarity. If you know there's a break, include it in the test regression or note the caveat.

### Trap 7: Thinking $\rho = 0.95$ means "stationary, no problem"

$\rho = 0.95$ is technically stationary, but with a half-life of $\log(0.5)/\log(0.95) \approx 14$ periods. A shock takes 14 quarters (3.5 years) to lose half its effect. In a 20-year sample, this is nearly indistinguishable from a unit root. Pesavento: *"Is 0.95 really different from 1 when I only have 20 years?"*

---

## How Everything Connects

```
UNIT ROOT DECISION TREE

  START: Is my data stationary?
    │
    ├── Yes (I(0)) → Model in levels with ARMA
    │     • Shocks are temporary
    │     • Forecast converges to mean
    │     • Standard inference works
    │
    └── No → WHY is it non-stationary?
          │
          ├── Deterministic trend?
          │     • Include trend in regression (detrend)
          │     • Shocks are temporary
          │     • Forecast → trend line (starting point irrelevant)
          │
          ├── Structural break?
          │     • Include break dummy
          │     • Watch out: break can mimic unit root
          │
          └── Unit root (stochastic trend)?
                • Take first difference: Δy_t
                • Model Δy_t with ARMA
                • Shocks are PERMANENT
                • Forecast = today + drift (starting point is everything)
                • MSE grows without bound
                • DF critical values required (not -1.96!)

  HOW TO DECIDE: Run ADF test
    │
    ├── Reject H0 → Not a unit root
    │     Action: model in levels (with trend if visible)
    │
    ├── Fail to reject → Unit root
    │     Action: difference and model Δy_t
    │
    └── Borderline → Think carefully
          • Run multiple tests (ADF, KPSS, DF-GLS)
          • Check for structural breaks
          • Make a defensible decision
```

---

## Cheat Sheet (Exam Morning Review)

```
================================================================
          UNIT ROOTS — EVERYTHING ON ONE PAGE
================================================================

DEFINITIONS
  Random walk:      y_t = y_{t-1} + ε_t        (AR(1) with ρ=1)
  RW with drift:    y_t = c + y_{t-1} + ε_t
  Back-substitution: y_t = y_0 + Σε_j           (sum of ALL past shocks)
  I(d): need d differences to be stationary
  Random walk = unit root = stochastic trend = I(1)

================================================================
PROPERTIES OF RANDOM WALK (why it's NOT stationary)

  E(y_t) = 0  (or ct with drift)
  Var(y_t) = t·σ²          ← grows with t!
  γ_k = (t-k)·σ²           ← depends on t, not just k!
  ρ_k = √((t-k)/t) → 1    ← ACF barely decays
  Initial condition y_0 never disappears

================================================================
DETERMINISTIC TREND vs UNIT ROOT

                    Det. Trend           Unit Root
  Forecast:         → trend line         → y_t + s·c
  Starting pt:      doesn't matter       EVERYTHING
  Shock effect:     temporary (→ 0)      PERMANENT (→ Ψ(1))
  MSE:              finite               grows forever
  Fix:              detrend              difference (Δy_t)
  Don't:            difference it!       detrend it!

================================================================
DICKEY-FULLER TEST

  Reparameterize: Δy_t = α·y_{t-1} + ε_t    (α = ρ-1)

  H0: α = 0  (unit root)
  H1: α < 0  (stationary)

  Test stat: t = α̂/SE(α̂)

  ⚠ NOT normal! Use DF critical values:

  Intercept only:       10%: -2.57    5%: -2.86    1%: -3.43
  Intercept + trend:    10%: -3.12    5%: -3.41    1%: -3.96

  Reject if test stat < critical value (MORE NEGATIVE)
  One-sided test, left tail only

  ADF: same test + lagged Δy terms (same critical values)
  Lag selection: AIC/BIC

================================================================
PRACTICAL STEPS (PESAVENTO)

  1. Plot the data
  2. Trend visible? → include trend in test
  3. Run ADF test
  4. Clearly reject → no unit root, model in levels
  5. Clearly fail to reject → unit root, take Δy_t
  6. Borderline → think, run multiple tests, justify

  Near-unit-root (ρ ≈ 0.95): very persistent but
    technically stationary. Hard to distinguish from ρ=1
    with finite data. "Most macro data is around 0.9-0.95"

================================================================
WHY TEST? (Exam 2 Q7 — 10 pts)

  1. Determines transformation (detrend vs difference)
  2. Wrong transform makes things WORSE
  3. Determines if shocks permanent vs temporary
  4. Standard t-critical values don't work under H0
  5. Forecast behavior completely different

EXAM TIPS
  • NEVER use -1.96 as DF critical value
  • Match specification to critical value table
  • The test is ONE-SIDED (left tail)
  • H0 = unit root (rejecting is the "good" result)
  • Structural breaks can mimic unit roots
================================================================
```

---

## Practice Problems

### Practice 1: Properties (5 min)
A random walk has $\sigma^2 = 4$ and you've observed 50 periods. Compute: (a) Var($y_{50}$), (b) Var($y_{100}$), (c) $\gamma_2$ at $t = 50$, (d) $\rho_2$ at $t = 50$.

<details>
<summary>Solution</summary>

(a) $\text{Var}(y_{50}) = 50 \times 4 = 200$

(b) $\text{Var}(y_{100}) = 100 \times 4 = 400$ — doubled! Variance grows linearly with $t$.

(c) $\gamma_2 = (50 - 2) \times 4 = 192$

(d) $\rho_2 = \sqrt{(50-2)/50} = \sqrt{48/50} = \sqrt{0.96} = 0.980$ — very close to 1!
</details>

### Practice 2: ADF Interpretation (3 min)
ADF test on quarterly GDP (with intercept and trend):
- Test statistic: -2.85
- p-value: 0.18

Does GDP have a unit root?

<details>
<summary>Solution</summary>

With intercept + trend, the 5% critical value is **-3.41**. The test statistic (-2.85) is NOT more negative than -3.41. We **fail to reject** the null of a unit root.

The p-value of 0.18 confirms — far from significant.

**Conclusion**: GDP appears to have a unit root. We should model GDP growth ($\Delta \log(\text{GDP})$) rather than GDP levels.

(Note: if you mistakenly used -1.96 as the CV, you would have rejected — this is the classic trap!)
</details>

### Practice 3: Transformation Choice (2 min)
You determine that CPI has a unit root. Which is correct?
- (a) Detrend CPI and fit ARMA to residuals
- (b) Take first difference of CPI and fit ARMA to $\Delta$CPI
- (c) Either works fine

<details>
<summary>Solution</summary>

**(b)** is correct. If CPI has a unit root, detrending removes the trend in the mean but NOT the variance — the detrended series still has $\text{Var} = t\sigma^2$. You must difference.

(c) is wrong — there is no universal fix. The correct transformation depends on the type of non-stationarity.
</details>

### Practice 4: Shock Persistence (3 min)
Model A: $y_t = 0.3 + 0.85 y_{t-1} + \varepsilon_t$ (stationary, $\rho = 0.85$)
Model B: $y_t = 0.3 + y_{t-1} + \varepsilon_t$ (unit root, $\rho = 1$)

A shock of size 1 hits at time $t$. What is the effect on $y_{t+10}$ under each model?

<details>
<summary>Solution</summary>

**Model A** (stationary): Effect at $t+10$ = $\rho^{10} = 0.85^{10} = 0.197$. The shock has decayed to about 20% of its original size. It's temporary — eventually goes to zero.

**Model B** (unit root): Effect at $t+10$ = 1. The shock has not decayed at all. It's permanent — it stays at full magnitude forever.

This is the fundamental difference: temporary vs. permanent shocks. A policymaker using Model A would expect the shock to fade. A policymaker using Model B would expect it to persist indefinitely.
</details>

### Practice 5: Forecasting Comparison (3 min)
You're at $t = 100$, $y_{100} = 50$. Estimated drift $c = 0.5$. Forecast $y_{110}$ under:
(a) Deterministic trend model ($\hat{\beta}_0 = 2$, $\hat{\beta}_1 = 0.5$)
(b) Random walk with drift

<details>
<summary>Solution</summary>

**(a) Deterministic trend**: $\hat{y}_{110} = \hat{\beta}_0 + \hat{\beta}_1 \times 110 = 2 + 0.5(110) = 57$

Note: this does NOT depend on $y_{100} = 50$ at all! The forecast is on the trend line regardless of where you are today.

**(b) Random walk with drift**: $\hat{y}_{110} = y_{100} + c \times 10 = 50 + 0.5(10) = 55$

This DOES depend on $y_{100}$. If instead $y_{100} = 45$, the forecast would be 50. The starting point is everything.

Different answers (57 vs 55) from the same data — this is why knowing which model you have matters!
</details>
