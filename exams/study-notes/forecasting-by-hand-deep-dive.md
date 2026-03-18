# Forecasting by Hand: The Complete Guide

**What this is**: A from-scratch explanation of how to compute 1-step and multi-step forecasts by hand from AR, MA, and ARMA models. This is the #2 most tested hand-calculation skill — it appeared on all three old exams, often for 10-20 points.

**How to use this**: Read Parts 1-6 slowly the first time (60-90 min). On exam morning, skip to the Cheat Sheet at the end.

---

## Lecture Reference Guide

Use these file paths to review the original source material:

| Topic | File Path | What's There |
|-------|-----------|-------------|
| **AR(1) h-step forecast formulas** | `course-materials/lectures/week-06/summary.md` (lines 200-208) | Table: h=1, h=2, h=general; recursive vs direct |
| **ARMA(1,1) forecasting** | `course-materials/lectures/week-06/summary.md` (lines 215-230) | 1-step uses θε_T; 2-step MA component dies |
| **MA(2) forecast walkthrough** | `course-materials/lectures/week-06/summary.md` (lines 152-174) | h=1, h=2, h≥3 with error variances at each step |
| **"Replace future ε with 0" rule** | `course-materials/lectures/week-04/recordings/arma-feb-3-recording.txt` | "Can you forecast white noise? No. Best guess? Zero." |
| **"Use forecast not actual" rule** | `course-materials/lectures/week-06/lecture-transcrip.txt` (~line 1600) | "You don't observe y_{t+1}. But you have your guess." |
| **Forecast error variance (grows with h)** | `course-materials/lectures/week-06/summary.md` (lines 169-174) | Table of error variance by horizon for MA(2) |
| **Properties of optimal forecasts** | `course-materials/lectures/week-06/summary.md` (lines 184-197) | Unbiased, uncorrelated with past, Var(ŷ) < Var(y) |
| **Variance inequality** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | "Forecast will always be smoother, less variance than actual" |
| **Unforecastability principle** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | "If I can forecast my error, my forecast was not optimal" |
| **Mincer-Zarnowitz regression** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | Two formulations; "It's called the Mincer-Zarnowitz regression" |
| **Diebold-Mariano test** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | "It's just a t-statistic for the difference in loss differentials" |
| **MSE = Bias² + Variance** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | "Sometimes you may be willing to take a little bias if it gives you much smaller variance" |
| **RMSE preferred measure** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | "For sure the number one would be the root mean square error" |
| **Southern Company example** | `course-materials/lectures/week-06/Forecasting-evaluation-transcript-feb-19.txt` | DM test: "one team did better, but when we tested... no significant difference" |
| **Loss functions** | `course-materials/lectures/week-06/lecture-transcrip.txt` | Quadratic → mean, Absolute → median, Linlin → quantile |
| **Forecasting deterministic components** | `course-materials/lectures/week-06/summary.md` (lines 131-140) | Trend + seasonality = perfectly forecastable |
| **Interval forecasts** | `course-materials/lectures/week-06/summary.md` (lines 231-238) | ŷ ± 1.96σ_h; parameter estimation approximation |
| **Unit root forecast = y_T** | `course-materials/lectures/week-07/transcripts/Forecasting.txt` | "Best prediction is where he is right now" (drunk person analogy) |
| **Impulse response / dynamic multiplier** | `course-materials/lectures/week-04/summary.md` (lines 109-121) | "Shock of 1 today → ρ, ρ², ρ³..." |
| **AR(2) forecast (Exam 2 Q6)** | `exams/past-exams/422oldfinal2.pdf` (not in our exact exam, but Exam 2 pages 4-5) | Carspend AR(2) with data table |
| **Seasonal + ARMA forecast (Exam 3 Q1h)** | `exams/past-exams/422Final02.pdf` (pages 7-8) | 20-point question with residual table |
| **RMSE/MAE comparison (Exam 1 Q3d)** | `exams/past-exams/422oldfinal2.pdf` (page 8) | DLDM vs LDM forecast evaluation output |
| **Trend/break estimation** | `course-materials/lectures/week-02/Trend+Estimation.pdf` | Linear, quadratic, log trends; DW statistic; AIC/BIC |
| **Structural breaks & seasonal dummies** | `course-materials/lectures/week-02/Breaks+and+Seasonality.pdf` | DBROKEN/TDBROKEN setup; Chow test; seasonal dummies |

---

## Part 1: What Does "Forecasting" Actually Mean?

### 1.1 The Core Idea

You're standing at time T. You have observed data up to and including $y_T$. You want to predict $y_{T+1}$ (one step ahead), $y_{T+2}$ (two steps ahead), and so on.

Your forecast of $y_{T+h}$ made at time T is written as:

$$\hat{y}_{T+h,T} \quad \text{or equivalently} \quad \hat{y}_{T+h|T}$$

The subscript notation means: "my prediction of the value at time $T+h$, given information available at time $T$."

### 1.2 What Information Do You Have?

At time T, you know:
- **All past and current values**: $y_T, y_{T-1}, y_{T-2}, \ldots$
- **All past residuals** (shocks): $\varepsilon_T, \varepsilon_{T-1}, \varepsilon_{T-2}, \ldots$ (estimated from your model)
- **The model parameters**: $\phi, \theta, c$ (estimated from data)
- **Future values of exogenous variables** (if given — like disposable income in Exam 2)

What you do NOT know:
- **Future values of y**: $y_{T+1}, y_{T+2}, \ldots$ (that's what you're trying to predict!)
- **Future shocks**: $\varepsilon_{T+1}, \varepsilon_{T+2}, \ldots$ (white noise is unforecastable by definition)

### 1.3 The Two Golden Rules of Forecasting

Every forecasting calculation comes down to applying two rules:

**Rule 1**: Replace any **future $\varepsilon$** (shock you haven't seen yet) with **zero**.

Why? Because $\varepsilon$ is white noise, and the best prediction of a WN value you haven't observed is its mean, which is zero. Pesavento explains (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt`):

> "What is your best guess for $\varepsilon_{t+1}$? Can you forecast the white noise into the future? No. So what's your best guess? Zero."

**Rule 2**: Replace any **future $y$** (value you haven't observed yet) with **your forecast of it**.

Why? You don't know $y_{T+1}$, but you do have a guess for it — your 1-step forecast. Use that guess when computing the 2-step forecast.

Pesavento on this (Week 6 lecture, `week-06/lecture-transcrip.txt`):
> "What is $y_{T+1}$? You don't have it. So you can think of this being... you don't observe $y_{T+1}$. But you have your guess. You have your forecast."

These two rules handle every situation.

### 1.4 Why This Matters Economically

Forecasting is the entire point of this course. A model is only useful if it can predict the future. On the exam, you'll be given:
- An estimated model (AR, MA, or ARMA with specific coefficients)
- The most recent data values
- Sometimes a table of residuals

And you'll need to produce actual numerical forecasts. This isn't abstract — it's the same calculation a central bank does when forecasting GDP, or a firm does when forecasting demand.

---

## Part 2: Forecasting from AR Models

AR models are the most common forecasting models and the easiest to forecast from by hand. This is where most exam points come from.

### 2.1 AR(1): $y_t = c + \phi y_{t-1} + \varepsilon_t$

#### 1-step ahead forecast

Write the model at time $T+1$:

$$y_{T+1} = c + \phi y_T + \varepsilon_{T+1}$$

Apply the rules:
- $y_T$: **known** (it's the current value) → keep it
- $\varepsilon_{T+1}$: **future shock** → replace with 0

$$\boxed{\hat{y}_{T+1,T} = c + \phi y_T}$$

That's it. Plug in the estimated constant $c$, the estimated coefficient $\phi$, and the last observed value $y_T$.

#### 2-step ahead forecast

Write the model at time $T+2$:

$$y_{T+2} = c + \phi y_{T+1} + \varepsilon_{T+2}$$

Apply the rules:
- $y_{T+1}$: **future value** → replace with your forecast $\hat{y}_{T+1,T}$
- $\varepsilon_{T+2}$: **future shock** → replace with 0

$$\boxed{\hat{y}_{T+2,T} = c + \phi \hat{y}_{T+1,T}}$$

**This is the critical step that students mess up.** You must use your FORECAST of $y_{T+1}$, not the actual (unknown) value. This is what makes it "recursive" — each forecast builds on the previous one.

Substituting the 1-step forecast:

$$\hat{y}_{T+2,T} = c + \phi(c + \phi y_T) = c(1 + \phi) + \phi^2 y_T$$

#### h-step ahead forecast (general)

For AR(1), there's a direct formula:

$$\hat{y}_{T+h,T} = \frac{c(1 - \phi^h)}{1 - \phi} + \phi^h y_T$$

But on the exam, the recursive method is safer — just keep plugging in:

$$\hat{y}_{T+h,T} = c + \phi \hat{y}_{T+h-1,T}$$

#### What happens as h gets large?

If $|\phi| < 1$ (stationary), $\phi^h \to 0$ as $h \to \infty$, so:

$$\hat{y}_{T+h,T} \to \frac{c}{1 - \phi} = \mu \quad \text{(the unconditional mean)}$$

The forecast converges to the long-run average. Makes sense — the further out you forecast, the less today's value matters.

**Compare to unit root** ($\phi = 1$): the forecast is $\hat{y}_{T+h,T} = y_T + c \cdot h$. It never converges — today's value matters forever (see `week-07/Unit+Root+Tests.pdf` slides 9-10 and `week-07/transcripts/Forecasting.txt` for the full derivation). This is why Pesavento says (Week 4 Feb 5 lecture):

> "When $\rho$ is equal to one, the shock is permanent. It never goes away."

### 2.2 AR(2): $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$

This is the most common exam scenario.

#### 1-step ahead

$$y_{T+1} = c + \phi_1 y_T + \phi_2 y_{T-1} + \varepsilon_{T+1}$$

- $y_T$: known → keep
- $y_{T-1}$: known → keep
- $\varepsilon_{T+1}$: future → 0

$$\boxed{\hat{y}_{T+1,T} = c + \phi_1 y_T + \phi_2 y_{T-1}}$$

#### 2-step ahead

$$y_{T+2} = c + \phi_1 y_{T+1} + \phi_2 y_T + \varepsilon_{T+2}$$

- $y_{T+1}$: **unknown future → replace with $\hat{y}_{T+1,T}$**
- $y_T$: known → keep
- $\varepsilon_{T+2}$: future → 0

$$\boxed{\hat{y}_{T+2,T} = c + \phi_1 \hat{y}_{T+1,T} + \phi_2 y_T}$$

Notice: the 2-step forecast uses **one forecasted value** ($\hat{y}_{T+1}$) and **one actual value** ($y_T$). This is because $y_T$ is in the past from the perspective of $T+2$, so we know it.

#### 3-step ahead

$$y_{T+3} = c + \phi_1 y_{T+2} + \phi_2 y_{T+1} + \varepsilon_{T+3}$$

Now BOTH $y$ values are unknown:
- $y_{T+2}$: replace with $\hat{y}_{T+2,T}$
- $y_{T+1}$: replace with $\hat{y}_{T+1,T}$
- $\varepsilon_{T+3}$: → 0

$$\hat{y}_{T+3,T} = c + \phi_1 \hat{y}_{T+2,T} + \phi_2 \hat{y}_{T+1,T}$$

**The pattern**: as you go further ahead, you progressively replace actual $y$ values with forecasts. Each step depends on all previous forecasts.

### 2.3 AR with Exogenous Variables (ARX)

Sometimes the model includes an exogenous variable (one determined outside the model). In Exam 2, the model is:

$$\text{carspend}_t = c + \beta \cdot \text{disposinc}_t + \phi_1 \text{carspend}_{t-1} + \phi_2 \text{carspend}_{t-2} + \varepsilon_t$$

When forecasting:
- Future $\varepsilon$ → 0 (as always)
- Future $y$ (carspend) → use your forecast
- Future exogenous variable (disposinc) → **use the actual given value** (it's exogenous, so the exam provides it)

This is why the exam gives you a data table with future disposable income values — they're treating it as known/predetermined.

### 2.4 Worked Example: Exam 2 Q6 — AR(2) Carspend Forecast

This is the exact question from the exam. Follow the "write the equation with variables first, THEN plug in numbers" approach.

**Given — the AR(2) model (from Q4 regression output):**

$$\text{carspend}_t = 1.576679 + 0.0005992 \cdot \text{disposinc}_t + 0.5777969 \cdot \text{carspend}_{t-1} + 0.3774076 \cdot \text{carspend}_{t-2} + \varepsilon_t$$

So: $\hat{c} = 1.576679$, $\hat{\beta}_1 = 0.0005992$, $\hat{\phi}_1 = 0.5777969$, $\hat{\phi}_2 = 0.3774076$

**Given — data table:**

| Date | CARSPEND | DISPOSINC |
|------|----------|-----------|
| 2002:2 | 102.244 | 7786.5 |
| 2002:3 | 109.192 | 7874.4 |
| 2002:4 | — | 7935.6 |
| 2003:1 | — | 8039.2 |

We stand at **T = 2002:3**. We want h=1 (2002:4) and h=2 (2003:1).

#### h=1: Forecasting 2002:4

**Step 1 — Write the model equation at T+1 with variable names (no numbers yet):**

$$\text{carspend}_{T+1} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+1} + \hat{\phi}_1 \cdot \text{carspend}_{T} + \hat{\phi}_2 \cdot \text{carspend}_{T-1} + \varepsilon_{T+1}$$

**Step 2 — Apply the two rules to each term:**

| Term | Time | Known or future? | Action |
|------|------|-----------------|--------|
| $\hat{c}$ | — | Estimated parameter | Keep: 1.576679 |
| $\hat{\beta}_1 \cdot \text{disposinc}_{T+1}$ | 2002:4 | **Known** — exogenous, given in table | Keep: 0.0005992 × 7935.6 |
| $\hat{\phi}_1 \cdot \text{carspend}_{T}$ | 2002:3 | **Known** — last observed value | Keep: 0.5777969 × 109.192 |
| $\hat{\phi}_2 \cdot \text{carspend}_{T-1}$ | 2002:2 | **Known** — in the past | Keep: 0.3774076 × 102.244 |
| $\varepsilon_{T+1}$ | 2002:4 | **Future shock** | Replace with **0** |

**Step 3 — Write the forecast equation (variables, no numbers):**

$$\hat{y}_{T+1,T} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+1} + \hat{\phi}_1 \cdot \text{carspend}_{T} + \hat{\phi}_2 \cdot \text{carspend}_{T-1}$$

**Step 4 — Plug in numbers:**

$$\hat{y}_{2002:4} = 1.576679 + 0.0005992 \times 7935.6 + 0.5777969 \times 109.192 + 0.3774076 \times 102.244$$

$$= 1.577 + 4.754 + 63.10 + 38.59 = \boxed{108.02}$$

#### h=2: Forecasting 2003:1

**Step 1 — Write the model equation at T+2 with variable names:**

$$\text{carspend}_{T+2} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+2} + \hat{\phi}_1 \cdot \text{carspend}_{T+1} + \hat{\phi}_2 \cdot \text{carspend}_{T} + \varepsilon_{T+2}$$

**Step 2 — Apply the two rules to each term:**

| Term | Time | Known or future? | Action |
|------|------|-----------------|--------|
| $\hat{c}$ | — | Estimated parameter | Keep: 1.576679 |
| $\hat{\beta}_1 \cdot \text{disposinc}_{T+2}$ | 2003:1 | **Known** — exogenous, given in table | Keep: 0.0005992 × 8039.2 |
| $\hat{\phi}_1 \cdot \text{carspend}_{T+1}$ | 2002:4 | **UNKNOWN — future carspend!** | **Replace with forecast** $\hat{y}_{T+1,T}$ = 108.02 |
| $\hat{\phi}_2 \cdot \text{carspend}_{T}$ | 2002:3 | **Known** — this is time T, still observed | Keep: 0.3774076 × 109.192 |
| $\varepsilon_{T+2}$ | 2003:1 | **Future shock** | Replace with **0** |

**Step 3 — Write the forecast equation (variables, no numbers):**

$$\hat{y}_{T+2,T} = \hat{c} + \hat{\beta}_1 \cdot \text{disposinc}_{T+2} + \hat{\phi}_1 \cdot \boxed{\hat{y}_{T+1,T}} + \hat{\phi}_2 \cdot \text{carspend}_{T}$$

The $\hat{\phi}_1$ term now multiplies your **forecast**, not an actual value. This is THE key difference from h=1.

The $\hat{\phi}_2$ term still uses the actual carspend at 2002:3 (= 109.192) because from the perspective of T+2, time T is still in the observed past.

**Step 4 — Plug in numbers:**

$$\hat{y}_{2003:1} = 1.576679 + 0.0005992 \times 8039.2 + 0.5777969 \times 108.02 + 0.3774076 \times 109.192$$

$$= 1.577 + 4.816 + 62.42 + 41.21 = \boxed{110.02}$$

#### What changes at each horizon — summary table

| | h=1 (2002:4) | h=2 (2003:1) | h=3 (if asked) |
|---|---|---|---|
| disposinc | Actual (given) | Actual (given) | Actual (given) |
| $\phi_1$ term (lag 1 of carspend) | Actual $y_T$ = 109.192 | **Forecast** $\hat{y}_{T+1}$ = 108.02 | **Forecast** $\hat{y}_{T+2}$ |
| $\phi_2$ term (lag 2 of carspend) | Actual $y_{T-1}$ = 102.244 | Actual $y_T$ = 109.192 | **Forecast** $\hat{y}_{T+1}$ |
| $\varepsilon$ | 0 | 0 | 0 |

The pattern: as you step further into the future, actual carspend values get "pushed out" and replaced by forecasts, one at a time. Disposable income always stays actual because it's exogenous (the exam gives you future values). The shock is always zero.

---

## Part 3: Forecasting from MA Models

MA forecasting is fundamentally different from AR forecasting. Instead of substituting forecasts for future $y$, you substitute zeros for future $\varepsilon$.

### 3.1 MA(1): $y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}$

#### 1-step ahead

$$y_{T+1} = \mu + \varepsilon_{T+1} + \theta\varepsilon_T$$

- $\varepsilon_{T+1}$: future → 0
- $\varepsilon_T$: **known** (it's the residual from your fitted model at time T)

$$\boxed{\hat{y}_{T+1,T} = \mu + \theta\varepsilon_T}$$

**Key**: You need to know $\varepsilon_T$ — the last residual from your model. On the exam, this is either given directly or you compute it as $\varepsilon_T = y_T - \hat{y}_T$.

#### 2-step ahead

$$y_{T+2} = \mu + \varepsilon_{T+2} + \theta\varepsilon_{T+1}$$

- $\varepsilon_{T+2}$: future → 0
- $\varepsilon_{T+1}$: **future → 0**

$$\boxed{\hat{y}_{T+2,T} = \mu}$$

The forecast has collapsed to just the mean! Both $\varepsilon$ terms are in the future, so both get replaced with zero.

#### h-step ahead for h ≥ 2

$$\hat{y}_{T+h,T} = \mu \quad \text{for all } h \geq 2$$

**MA(1) can only forecast ONE step ahead.** Beyond that, the best you can do is the unconditional mean.

### 3.2 MA(2): $y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2}$

#### 1-step ahead

$$y_{T+1} = \mu + \varepsilon_{T+1} + \theta_1\varepsilon_T + \theta_2\varepsilon_{T-1}$$

- $\varepsilon_{T+1}$: future → 0
- $\varepsilon_T$: known residual → keep
- $\varepsilon_{T-1}$: known residual → keep

$$\boxed{\hat{y}_{T+1,T} = \mu + \theta_1\varepsilon_T + \theta_2\varepsilon_{T-1}}$$

#### 2-step ahead

$$y_{T+2} = \mu + \varepsilon_{T+2} + \theta_1\varepsilon_{T+1} + \theta_2\varepsilon_T$$

- $\varepsilon_{T+2}$: future → 0
- $\varepsilon_{T+1}$: future → 0
- $\varepsilon_T$: known → keep

$$\boxed{\hat{y}_{T+2,T} = \mu + \theta_2\varepsilon_T}$$

Still some forecasting power! The $\varepsilon_T$ shock is known and still contributes through $\theta_2$.

#### 3-step ahead and beyond

$$y_{T+3} = \mu + \varepsilon_{T+3} + \theta_1\varepsilon_{T+2} + \theta_2\varepsilon_{T+1}$$

All three $\varepsilon$ are future → all zero.

$$\hat{y}_{T+h,T} = \mu \quad \text{for all } h \geq 3$$

**MA(q) can forecast exactly q steps ahead.** At horizon $h > q$, the forecast equals the unconditional mean. This is the forecasting analog of the autocovariance cutoff.

### 3.3 Why MA Forecasting Has a Hard Horizon Limit

This connects directly to the autocovariance deep dive. An MA(q) process has "memory" of only q past shocks. Once you're forecasting more than q steps ahead, all the shocks you know about have "expired" — they're no longer in the MA equation. So you're left with nothing but the mean.

From `week-06/key-concepts.md` lines 77-98:
> "An MA(q) can only forecast q steps ahead. After that, the best forecast is the unconditional mean $\mu$."

This is why AR models dominate in practice — they can forecast arbitrarily far ahead (though with decreasing accuracy).

---

## Part 4: Forecasting from ARMA Models

ARMA combines both components: the AR part gives you long-horizon forecasting power, while the MA part gives you extra precision at short horizons.

### 4.1 ARMA(1,1): $y_t = c + \phi y_{t-1} + \varepsilon_t + \theta\varepsilon_{t-1}$

#### 1-step ahead

$$y_{T+1} = c + \phi y_T + \varepsilon_{T+1} + \theta\varepsilon_T$$

- $y_T$: known → keep
- $\varepsilon_{T+1}$: future → 0
- $\varepsilon_T$: known residual → keep

$$\boxed{\hat{y}_{T+1,T} = c + \phi y_T + \theta\varepsilon_T}$$

This uses BOTH the last observed value (through $\phi$) and the last residual (through $\theta$).

#### 2-step ahead

$$y_{T+2} = c + \phi y_{T+1} + \varepsilon_{T+2} + \theta\varepsilon_{T+1}$$

- $y_{T+1}$: unknown → replace with $\hat{y}_{T+1,T}$
- $\varepsilon_{T+2}$: future → 0
- $\varepsilon_{T+1}$: future → 0

$$\boxed{\hat{y}_{T+2,T} = c + \phi\hat{y}_{T+1,T}}$$

The MA part has died! At $h = 2$, the only $\varepsilon$ terms are future ones, so they vanish. From here on, the ARMA forecast behaves exactly like a pure AR forecast.

From `week-06/summary.md` lines 215-230:
> "2-step-ahead: $\hat{y}_{T+2,T} = \phi\hat{y}_{T+1,T}$ (MA component exhausted after 1 step)"

#### General rule for ARMA(p,q) at horizon h > q

Once $h > q$, the MA terms have all been replaced by zero. The forecast becomes purely AR:

$$\hat{y}_{T+h,T} = c + \phi_1\hat{y}_{T+h-1,T} + \phi_2\hat{y}_{T+h-2,T} + \cdots$$

The MA component only helps for the first q steps.

---

## Part 5: Forecasting with Seasonal Dummies + ARMA Residuals

This is the most complex exam forecasting scenario — it appeared on Exam 3 (Fall 08) Q1h for 20 points. The idea: decompose the series into deterministic parts (trend, seasonality) and stochastic parts (cycles modeled by ARMA).

### 5.1 The Decomposition

The full model has two layers:

**Layer 1 — Deterministic** (trend + seasonality):
$$\text{LKWH}_t = \beta_0 + \beta_1 \text{DBROKEN} + \beta_2 \text{TREND} + \beta_3 \text{TDBROKEN} + \beta_4 \text{LY} + \beta_5 \text{LPRICE} + \beta_6 \text{CDD} + \beta_7 \text{HDD} + \delta_1 D_1 + \delta_2 D_2 + \delta_3 D_3 + u_t$$

This regression produces residuals $\hat{u}_t$. These residuals capture the cyclical dynamics.

**Layer 2 — Stochastic** (ARMA model for residuals):
You fit an AR, MA, or ARMA to $\hat{u}_t$. For instance, an ARMA(1,1):
$$\hat{u}_t = \phi\hat{u}_{t-1} + \varepsilon_t + \theta\varepsilon_{t-1}$$

### 5.2 How to Compute the Forecast

**Step 1**: Forecast the deterministic part.

For a future quarter (say 1993:Q1), you know everything deterministic:
- $D_1 = 1, D_2 = 0, D_3 = 0$ (it's Q1)
- TREND = the value of the time counter at that date
- DBROKEN, TDBROKEN = determined by the break date
- CDD, HDD = you'd need these given (or assume some value)

Plug into the regression equation to get the deterministic forecast.

**Step 2**: Forecast the ARMA residual.

Using the technique from Parts 2-4 above, forecast $\hat{u}_{T+1}$ and $\hat{u}_{T+2}$ from the estimated ARMA model, using the table of past residuals.

**Step 3**: Combine.

$$\hat{y}_{T+h} = \text{(deterministic forecast)} + \text{(ARMA residual forecast)}$$

### 5.3 Why the Deterministic Part is "Free"

Pesavento (`week-06/summary.md` lines 131-140; also `week-02/Breaks+and+Seasonality.pdf` slides on seasonal dummies):
> "Anything deterministic, by definition, you can forecast well... Seasonality I can also forecast easily."

Trend and seasonal dummies are perfectly forecastable — you know what quarter it will be next period, and you know the trend value. The uncertainty only comes from the ARMA residual.

---

## Part 6: Forecast Error and Confidence Intervals

> **Lecture references**: `week-06/lecture-transcrip.txt` (lines ~289-370 for forecast error derivation, ~211-212 for confidence intervals), `week-06/Forecasting-evaluation-transcript-feb-19.txt` (lines ~15-54 for error properties and variance growth), `week-06/summary.md` lines 152-236 (clean formulas).

### 6.1 What is the Forecast Error?

The **forecast error** is simply the difference between what actually happened and what you predicted:

$$e_{T+h,T} = y_{T+h} - \hat{y}_{T+h,T}$$

Pesavento (`week-06/lecture-transcrip.txt`):
> "The forecast error tells you how far you are from the forecast."

The notation $e_{T+h,T}$ means: the error of my forecast for time $T+h$, made at time $T$.

**Why you should care**: The forecast error is what determines your confidence intervals. If your forecast errors are large (high variance), your confidence interval is wide and your forecast is imprecise. If they're small, your interval is tight and useful.

### 6.2 How to Derive the Forecast Error (The Subtraction Trick)

This is mechanical: write out the TRUE value, write out the FORECAST, and subtract. Whatever is left is the error.

**MA(2) example** — Pesavento walks through this step by step (`week-06/lecture-transcrip.txt`):

**At h = 1**:

The TRUE value at $T+1$:
$$y_{T+1} = \varepsilon_{T+1} + \theta_1\varepsilon_T + \theta_2\varepsilon_{T-1}$$

Your FORECAST (replace future $\varepsilon_{T+1}$ with 0):
$$\hat{y}_{T+1,T} = 0 + \theta_1\varepsilon_T + \theta_2\varepsilon_{T-1}$$

Subtract forecast from true:
$$e_{T+1,T} = y_{T+1} - \hat{y}_{T+1,T} = \varepsilon_{T+1}$$

The 1-step forecast error is just $\varepsilon_{T+1}$ — **pure white noise**. The $\theta_1\varepsilon_T$ and $\theta_2\varepsilon_{T-1}$ terms cancel out because they appear in both the true value and the forecast.

Pesavento (`week-06/lecture-transcrip.txt`):
> "So you have that your forecast error is $\varepsilon_{T+1}$. So what does it mean that your forecast error one step ahead is a white noise? It's unpredictable."

**Variance of the 1-step error**: $\text{Var}(e_{T+1,T}) = \text{Var}(\varepsilon_{T+1}) = \sigma^2$

**At h = 2**:

Pesavento continues (`week-06/lecture-transcrip.txt`):

TRUE:
$$y_{T+2} = \varepsilon_{T+2} + \theta_1\varepsilon_{T+1} + \theta_2\varepsilon_T$$

FORECAST (both $\varepsilon_{T+2}$ and $\varepsilon_{T+1}$ are future → replaced with 0):
$$\hat{y}_{T+2,T} = 0 + 0 + \theta_2\varepsilon_T$$

Error (subtract):
$$e_{T+2,T} = \varepsilon_{T+2} + \theta_1\varepsilon_{T+1}$$

> "So your forecast error is going to be $\varepsilon_{T+2} + \theta_1\varepsilon_{T+1}$."

This error is an **MA(1)** — it has two terms, not just one. It's bigger than the 1-step error because there are more unknown future shocks contributing to the gap between your forecast and reality.

**Variance of the 2-step error**: Pesavento (`week-06/lecture-transcrip.txt`):
> "What is the variance of this? This is going to be... $\sigma^2$ plus the square of this coefficient... so $(1 + \theta_1^2)\sigma^2$."

$$\text{Var}(e_{T+2,T}) = (1 + \theta_1^2)\sigma^2$$

This is BIGGER than $\sigma^2$ (the 1-step variance). More uncertainty when forecasting further ahead.

**At h = 3 and beyond** (for MA(2)):

Error = $\varepsilon_{T+3} + \theta_1\varepsilon_{T+2} + \theta_2\varepsilon_{T+1}$ = the full MA(2) process itself.

$$\text{Var}(e_{T+h,T}) = (1 + \theta_1^2 + \theta_2^2)\sigma^2 = \text{Var}(y_t) \quad \text{for } h \geq 3$$

You've hit the maximum — your forecast error is now as variable as the series itself. You're no better than just guessing the mean.

### 6.3 The Key Pattern: Error Variance Grows with Horizon

Here's the MA(2) example in a table (`week-06/summary.md` lines 169-174):

| Horizon h | Forecast Error | Error Variance | Interpretation |
|-----------|---------------|----------------|----------------|
| h = 1 | $\varepsilon_{T+1}$ (white noise) | $\sigma^2$ | Best precision — only 1 unknown shock |
| h = 2 | $\varepsilon_{T+2} + \theta_1\varepsilon_{T+1}$ (MA(1)) | $(1 + \theta_1^2)\sigma^2$ | Worse — 2 unknown shocks |
| h ≥ 3 | Full MA(2) | $(1 + \theta_1^2 + \theta_2^2)\sigma^2 = \text{Var}(y_t)$ | Worst — same as the whole process |

**The intuition**: At each additional step ahead, one more future $\varepsilon$ enters the true value that you couldn't predict. Your error accumulates another unpredictable term, so the variance grows.

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "What does it mean that [variance] is non-decreasing in $h$? It means that you are going to be always more precise in forecasting next month than you're going to be forecasting 10 months from now. Your forecast further away is going to be more imprecise, and the forecast variance is going to be larger."

### 6.3b Full Derivation: AR(1) Forecast Error via MA(∞)

> **Lecture references**: `week-04/recordings/arma-feb-5-recording.txt` (AR to MA conversion), `week-06/lecture-transcrip.txt` (lines ~289-315 for the subtraction method), `week-06/summary.md` lines 200-208 (AR(1) forecast formulas). Also see `exams/study-notes/MA-infinity-representation-of-AR1.md` for the full MA(∞) derivation.

For AR(1), the forecast error is harder to see than for MA because the model equation $y_t = c + \phi y_{t-1} + \varepsilon_t$ contains $y_{t-1}$ (an observable), not a clean list of $\varepsilon$ terms. The trick is to use the **MA(∞) representation** to rewrite everything in terms of shocks, then the subtraction becomes clean.

#### Step 1: Write the true value at T+h using the MA(∞)

From the MA(∞) representation (derived in `exams/study-notes/MA-infinity-representation-of-AR1.md`), we can write $y_t$ as an infinite weighted sum of all past shocks:

$$y_t = \mu + \sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j} = \mu + \varepsilon_t + \phi\varepsilon_{t-1} + \phi^2\varepsilon_{t-2} + \phi^3\varepsilon_{t-3} + \cdots$$

So the **true value** at time $T+h$ is:

$$y_{T+h} = \mu + \varepsilon_{T+h} + \phi\varepsilon_{T+h-1} + \phi^2\varepsilon_{T+h-2} + \cdots + \phi^{h-1}\varepsilon_{T+1} + \phi^h\varepsilon_T + \phi^{h+1}\varepsilon_{T-1} + \cdots$$

Let's split this into two groups — shocks you DON'T know at time T (future) and shocks you DO know (past):

$$y_{T+h} = \underbrace{\varepsilon_{T+h} + \phi\varepsilon_{T+h-1} + \cdots + \phi^{h-1}\varepsilon_{T+1}}_{\text{FUTURE shocks (unknown at time T)}} + \underbrace{\mu + \phi^h\varepsilon_T + \phi^{h+1}\varepsilon_{T-1} + \cdots}_{\text{PAST shocks (known at time T)}}$$

#### Step 2: Write the forecast at T+h

Your forecast $\hat{y}_{T+h,T}$ uses the same MA(∞) but replaces all **future** $\varepsilon$ with zero (because you can't forecast white noise). So:

$$\hat{y}_{T+h,T} = \underbrace{0 + 0 + \cdots + 0}_{\text{future ε → all zero}} + \underbrace{\mu + \phi^h\varepsilon_T + \phi^{h+1}\varepsilon_{T-1} + \cdots}_{\text{past shocks → keep as-is}}$$

This simplifies to:

$$\hat{y}_{T+h,T} = \mu + \phi^h\varepsilon_T + \phi^{h+1}\varepsilon_{T-1} + \phi^{h+2}\varepsilon_{T-2} + \cdots$$

Which you can factor: $\hat{y}_{T+h,T} = \mu + \phi^h(\varepsilon_T + \phi\varepsilon_{T-1} + \phi^2\varepsilon_{T-2} + \cdots) = \mu + \phi^h(y_T - \mu)$

So: $\hat{y}_{T+h,T} = \mu + \phi^h(y_T - \mu)$, or equivalently $\hat{y}_{T+h,T} = \phi^h y_T$ when $\mu = 0$ (no constant). This is the direct forecast formula from `week-06/summary.md` line 207.

#### Step 3: Subtract to get the forecast error

$$e_{T+h,T} = y_{T+h} - \hat{y}_{T+h,T}$$

The past-shock terms are identical in both the true value and the forecast, so they cancel perfectly. What survives is **only the future shocks** — the ones you couldn't predict:

$$\boxed{e_{T+h,T} = \varepsilon_{T+h} + \phi\varepsilon_{T+h-1} + \phi^2\varepsilon_{T+h-2} + \cdots + \phi^{h-1}\varepsilon_{T+1}}$$

$$= \sum_{j=0}^{h-1}\phi^j\varepsilon_{T+h-j}$$

This is exactly the **first h terms** of the MA(∞) — the terms involving future $\varepsilon$ that you replaced with zero.

**Intuition**: Your forecast error consists of all the future shocks that you couldn't predict, weighted by the MA(∞) coefficients $1, \phi, \phi^2, \ldots$ The further out you forecast, the more unknown shocks accumulate in your error.

#### Step 4: Compute the error variance

Now use the MA variance formula from the autocovariance deep dive: **square each coefficient, add them up, multiply by $\sigma^2$**. Cross terms vanish because all the $\varepsilon$ terms are white noise with different time indices.

$$\text{Var}(e_{T+h,T}) = (1^2 + \phi^2 + \phi^4 + \cdots + \phi^{2(h-1)})\sigma^2$$

Let's see this for each horizon:

**h = 1**: Error = $\varepsilon_{T+1}$ (just one shock)
$$\text{Var}(e_{T+1,T}) = 1^2 \cdot \sigma^2 = \sigma^2$$

**h = 2**: Error = $\varepsilon_{T+2} + \phi\varepsilon_{T+1}$ (two shocks)
$$\text{Var}(e_{T+2,T}) = (1 + \phi^2)\sigma^2$$

**h = 3**: Error = $\varepsilon_{T+3} + \phi\varepsilon_{T+2} + \phi^2\varepsilon_{T+1}$ (three shocks)
$$\text{Var}(e_{T+3,T}) = (1 + \phi^2 + \phi^4)\sigma^2$$

**General h**:
$$\boxed{\text{Var}(e_{T+h,T}) = (1 + \phi^2 + \phi^4 + \cdots + \phi^{2(h-1)})\sigma^2 = \frac{1 - \phi^{2h}}{1 - \phi^2}\sigma^2}$$

The last step uses the finite geometric series: $1 + x + x^2 + \cdots + x^{n-1} = (1 - x^n)/(1-x)$, with $x = \phi^2$ and $n = h$.

#### Step 5: What happens as h → ∞?

As $h \to \infty$, $\phi^{2h} \to 0$ (because $|\phi| < 1$), so:

$$\text{Var}(e_{T+h,T}) \to \frac{1}{1-\phi^2}\sigma^2 = \text{Var}(y_t)$$

The forecast error variance **converges to the variance of the process itself**. At infinite horizon, you're no better than guessing the unconditional mean — your error is as big as the natural variability of the series.

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "You are going to be always more precise in forecasting next month than you're going to be forecasting 10 months from now. Your forecast further away is going to be more imprecise, and the forecast variance is going to be larger."

#### Summary table

| Horizon h | Forecast Error $e_{T+h,T}$ | # of unknown shocks | Error Variance |
|-----------|---------------------------|-------|----------------|
| 1 | $\varepsilon_{T+1}$ | 1 | $\sigma^2$ |
| 2 | $\varepsilon_{T+2} + \phi\varepsilon_{T+1}$ | 2 | $(1 + \phi^2)\sigma^2$ |
| 3 | $\varepsilon_{T+3} + \phi\varepsilon_{T+2} + \phi^2\varepsilon_{T+1}$ | 3 | $(1 + \phi^2 + \phi^4)\sigma^2$ |
| h | $\sum_{j=0}^{h-1}\phi^j\varepsilon_{T+h-j}$ | h | $\frac{1-\phi^{2h}}{1-\phi^2}\sigma^2$ |
| ∞ | (all future shocks) | ∞ | $\frac{\sigma^2}{1-\phi^2} = \text{Var}(y_t)$ |

#### Numerical example

Suppose $\phi = 0.8$ and $\sigma^2 = 1$:

| h | Error Variance | 95% CI half-width ($1.96\sigma_h$) |
|---|---------------|-------------------------------------|
| 1 | $1.000$ | $\pm 1.960$ |
| 2 | $1 + 0.64 = 1.640$ | $\pm 2.509$ |
| 3 | $1 + 0.64 + 0.410 = 2.050$ | $\pm 2.805$ |
| 5 | $2.594$ | $\pm 3.155$ |
| 10 | $2.716$ | $\pm 3.229$ |
| ∞ | $1/(1-0.64) = 2.778$ | $\pm 3.266$ |

Notice how the CI widens quickly at first (from ±1.96 to ±2.51 to ±2.81) then flattens out as it approaches the limit. By h = 10 you're already at 97.8% of the maximum width — forecasting further out barely adds uncertainty.

#### What about the unit root case (φ = 1)?

When $\phi = 1$, all MA(∞) weights are 1 (no decay), so:

$$e_{T+h,T} = \varepsilon_{T+h} + \varepsilon_{T+h-1} + \cdots + \varepsilon_{T+1}$$

$$\text{Var}(e_{T+h,T}) = h\sigma^2$$

The error variance grows **linearly with h forever** — it never converges. This is fundamentally different from the stationary case. Your confidence interval widens without bound. Pesavento (`week-07/transcripts/Forecasting.txt`):

> "The best prediction is where he is right now" (the drunk person analogy for a random walk)

### 6.4 Confidence Intervals (Interval Forecasts)

Now that you know the forecast error variance at each horizon, you can build **confidence bands** around your forecast.

Pesavento (`week-06/lecture-transcrip.txt`):
> "Once I use my estimated model to forecast, my estimated model has uncertainty, all the parameters have uncertainty, so my forecast is also just an estimate, and therefore there's going to be uncertainty around that as well."

**The idea**: Your forecast $\hat{y}_{T+h,T}$ is the center of a distribution. The forecast error tells you how spread out that distribution is. If the errors are normally distributed, the distribution of the true future value is:

$$y_{T+h} \sim N\!\left(\hat{y}_{T+h,T},\;\; \sigma_h^2\right)$$

where $\sigma_h^2$ is the forecast error variance at horizon $h$.

**A 95% interval forecast** (`week-06/summary.md` lines 231-234):

$$\hat{y}_{T+h,T} \pm 1.96 \cdot \sigma_h$$

In words: your point forecast, plus or minus 1.96 standard deviations of the forecast error.

Pesavento (`week-06/lecture-transcrip.txt`):
> "The density forecast is going to be distributed as a normal with mean $\hat{y}$ and bias $\hat{\sigma}^2$, which is the forecast error variance. So whenever I want to compute a confidence interval, I can do plus or minus 1.96 times $\sigma$."

**Practical note**: You need to estimate $\sigma_h$. For h=1, this is just $\hat{\sigma}$ (the standard error of the regression). For h>1, you need the MA(∞) coefficients from your model.

**Example — ARMA(1,1) at h = 2** (`week-06/summary.md` lines 224-229):

The MA(∞) representation of ARMA(1,1) starts: $y_t = \varepsilon_t + (\phi + \theta)\varepsilon_{t-1} + \cdots$

So the first MA(∞) coefficient is $\psi_1 = \phi + \theta$.

The 2-step error variance is: $\sigma_2^2 = \sigma^2(1 + \psi_1^2) = \sigma^2(1 + (\phi + \theta)^2)$

The 95% interval at h = 2:
$$\hat{y}_{T+2,T} \pm 1.96\hat{\sigma}\sqrt{1 + (\hat{\phi} + \hat{\theta})^2}$$

### 6.5 Interval vs Density vs Fan Chart

Pesavento distinguishes three types of uncertainty representation (`week-06/lecture-transcrip.txt`):

**Interval forecast**: Gives you the range — "best case to worst case."
$$\hat{y}_{T+h,T} \pm 1.96\sigma_h$$

**Density forecast**: Gives the full probability distribution — "what is the probability of ending up in the best or worst case?"
$$y_{T+h} \sim N(\hat{y}_{T+h,T}, \sigma_h^2)$$

**Fan chart**: A visual representation showing how uncertainty widens over time. The Bank of England's interest rate fan chart is the classic example. Pesavento:
> "When they do the fan chart for interest rate — I don't know if you've ever seen the UK fan chart — they have a whole distribution in that sense."

The fan chart gets wider as $h$ increases because $\sigma_h$ grows — this is the error variance growth we derived above, made visual.

### 6.6 Why the Forecast is Always Smoother Than Reality

This is a mathematical consequence of the forecast error being uncorrelated with the forecast itself. Start from the decomposition:

$$y_{T+h} = \hat{y}_{T+h,T} + e_{T+h,T}$$

Since forecast and error are uncorrelated (a property of optimal forecasts):

$$\text{Var}(y_{T+h}) = \text{Var}(\hat{y}_{T+h,T}) + \text{Var}(e_{T+h,T})$$

Since $\text{Var}(e_{T+h,T}) > 0$:

$$\boxed{\text{Var}(\hat{y}_{T+h,T}) < \text{Var}(y_{T+h})}$$

**The forecast always has less variance than the actual data.** Your forecast line will always look "smoother" than the actual data.

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "The forecast will always have less variance than the actual data, so they're never going to overlap."

**Don't be alarmed by this.** When you plot your forecast against actual data and the forecast doesn't swing as much, that's not a sign of a bad model — it's mathematically guaranteed for any optimal forecast.

### 6.7 Properties of Optimal Forecast Errors (EXAM MATERIAL)

Pesavento flags these as things you need to know (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):

> "You should know what the forecast error means... if you take this slide and digest, and say 'I don't understand this, why should this be zero?' — if you are not sure, don't just memorize it, take the two definitions, look at them, and figure out why this is the case."

**Property 1: Mean zero** — $E[e_{T+h,T}] = 0$

The forecast should not systematically over-predict or under-predict. If the average error is positive, your forecast is systematically too low.

**How to check**: Regress the forecast errors on a constant. The constant should be zero.

> "You take your forecast error, you regress on a constant, and that constant coefficient should be zero."

**Property 2: 1-step errors are white noise**

For h=1 forecasts, the errors should be completely random — no serial correlation, no pattern. If you see patterns in 1-step errors, your model missed something predictable.

> "If your forecast is one step ahead, your forecast error should be completely random."

**How to check**: Durbin-Watson test on the forecast errors, or plot their ACF.

**Property 3: h-step errors are at most MA(h-1)**

For multi-step forecasts, the errors WILL be serially correlated — but at most MA(h-1). This isn't a sign of a bad model; it's the natural structure. They should still have zero mean.

> "If I forecast h step ahead, the forecast errors are MA(h-1)... but the more important thing is, what does it mean that [variance] is non-decreasing in h?"

**Property 4: Errors are uncorrelated with your information set** (orthogonality)

Your forecast errors should not be predictable from any information you had when making the forecast. If someone can look at your data and predict your errors, you left predictable content on the table.

> "You can regress the forecast error on your available information, the same information that you used to do your forecast, and it better be that coefficients are all zero."

**This is what the Mincer-Zarnowitz test checks** — see Part 8.3.
Variance = $\sigma^2(1 + \theta_1^2 + \theta_2^2) = \text{Var}(y_t)$

The error variance reaches its maximum at $h = q$ and stays there. Beyond q steps, you're no better than guessing the mean.

### 6.4 Confidence Intervals for Forecasts

If the shocks are normally distributed:

$$y_{T+h} \sim N(\hat{y}_{T+h,T},\; \sigma_h^2)$$

A **95% forecast interval** is:

$$\hat{y}_{T+h,T} \pm 1.96 \cdot \sigma_h$$

where $\sigma_h$ is the forecast error standard deviation at horizon $h$.

**At $h = 1$**: $\sigma_1 = \sigma$ (just the innovation standard deviation)
**At $h = 2$**: $\sigma_2$ depends on the model (see formulas above)

The interval gets **wider** as $h$ increases — more uncertainty at longer horizons.

### 6.5 Properties of Optimal Forecasts

From Week 6, flagged as EXAM MATERIAL (`week-06/summary.md` lines 184-197; `week-06/Forecasting-evaluation-transcript-feb-19.txt`):

1. **Forecast errors have mean zero**: No systematic bias. $E[e_{T+h,T}] = 0$.
2. **1-step errors are white noise**: Uncorrelated with each other and with past information.
3. **Multi-step errors are serially correlated** (at most MA($h-1$)), but still have zero mean.
4. **Forecast is smoother than actual data**: $\text{Var}(\hat{y}) < \text{Var}(y)$.

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "If I can forecast in any way my forecast error, that means there was something in the model that I have not exploited in my forecast... the forecast error should be unforecastable."

---

## Part 7: Every Exam Appearance — Worked Solutions

### Exam 1 (422 FINAL) — Q3d: Forecast Evaluation [10 pts]

**The question**: Compare two forecasting models for the DM/Dollar exchange rate using RMSE and MAE from the provided output.

**The data**: Two forecast outputs are given:
- DLDM model (first differences): RMSE = 0.028349, MAE = 0.022449
- LDM model (levels): RMSE = 0.144335, MAE = 0.106858

**Solution**: The DLDM (first difference) model has dramatically lower RMSE and MAE. It forecasts much better.

**Why**: The level series (LDM) has near-unit-root behavior (ACF slowly decaying). Forecasting a near-random-walk in levels accumulates errors. Forecasting the differenced series (which is closer to stationary) is much more precise.

**Exam tip**: When comparing models, lower RMSE and lower MAE both = better. If they disagree (one model wins on RMSE, another on MAE), discuss which measure is more appropriate (RMSE penalizes large errors more heavily).

---

### Exam 2 (422 FINAL #2) — Q6: AR(2) Forecast by Hand [12 pts]

**The question**: Using the AR(2) model for car spending and a provided data table, compute 1-step and 2-step ahead forecasts.

**The model**:
$$\text{carspend}_t = 0.0005992 \cdot \text{disposinc}_t + 0.5778 \cdot \text{carspend}_{t-1} + 0.3774 \cdot \text{carspend}_{t-2} + 1.5767$$

**Given data**:
- carspend at 2002:Q3 ($y_T$) = 109.192
- carspend at 2002:Q2 ($y_{T-1}$) = 102.244
- disposinc at 2002:Q4 = 7935.6 (exogenous, given)
- disposinc at 2003:Q1 = 8039.2 (exogenous, given)

**1-step ahead** (2002:Q4):

Everything here is known or exogenous:

$$\hat{y}_{T+1} = 0.0005992(7935.6) + 0.5778(109.192) + 0.3774(102.244) + 1.5767$$

Compute each term:
- $0.0005992 \times 7935.6 = 4.755$
- $0.5778 \times 109.192 = 63.098$
- $0.3774 \times 102.244 = 38.587$
- constant = 1.577

$$\hat{y}_{T+1} = 4.755 + 63.098 + 38.587 + 1.577 = 108.017$$

**2-step ahead** (2003:Q1):

$$\hat{y}_{T+2} = 0.0005992(\text{disposinc}_{T+2}) + 0.5778 \cdot \hat{y}_{T+1} + 0.3774 \cdot y_T + 1.5767$$

Note the critical substitution: $y_{T+1}$ is unknown → use **$\hat{y}_{T+1} = 108.017$**. But $y_T = 109.192$ is known (it's in the past from the perspective of $T+2$). And disposinc at 2003:Q1 = 8039.2 is exogenous and given.

$$\hat{y}_{T+2} = 0.0005992(8039.2) + 0.5778(108.017) + 0.3774(109.192) + 1.5767$$

- $0.0005992 \times 8039.2 = 4.817$
- $0.5778 \times 108.017 = 62.412$
- $0.3774 \times 109.192 = 41.208$
- constant = 1.577

$$\hat{y}_{T+2} = 4.817 + 62.412 + 41.208 + 1.577 = 110.014$$

**What the grader wants**: Show each multiplication clearly. State explicitly that you're substituting the forecast for $y_{T+1}$, not an actual value. Label which values are known, which are forecasts, and which are exogenous.

---

### Exam 3 (Fall 08) — Q1h: Forecast with Seasonal Dummies + ARMA [20 pts]

This is the hardest forecasting question across all three exams.

**The question**: "Given your answer in (g), compute your forecast for the first and second quarter of 1993."

**Setup**: The model has two layers:
1. A regression of LKWH on trend, broken trend, seasonal dummies, price, income, weather
2. An ARMA model for the residuals (you select this in Q1g from provided regression outputs)

**Given data table**:

| Date | LKWH | Residuals from ARMA(1,1) |
|------|------|--------------------------|
| 1991:1 | 0.392801 | -0.026877354 |
| 1991:2 | 0.205318 | -0.025993192 |
| ... | ... | ... |
| 1992:3 | 0.408811 | 0.128869546 |
| 1992:4 | 0.338866 | -0.020704755 |

**Step 1**: Identify the ARMA model from Q1g.

Suppose you chose ARMA(1,1) based on AIC/BIC comparison (it had the lowest AIC = -3.569297). The model for residuals is:

$$\hat{u}_t = \phi\hat{u}_{t-1} + \varepsilon_t + \theta\varepsilon_{t-1}$$

with $\phi = 0.926149$ and $\theta = -0.646372$ (from the ARMA(1,1) regression output).

**Step 2**: Forecast the residual for 1993:Q1 (1-step ahead from 1992:Q4).

$$\hat{u}_{T+1} = \phi\hat{u}_T + \theta\varepsilon_T$$

Where:
- $\hat{u}_T$ = residual at 1992:Q4 = $-0.020704755$
- $\varepsilon_T$ = the ARMA(1,1) innovation at 1992:Q4 (this is the difference between the actual residual and what the ARMA predicted — the exam may give this or you approximate it as $\hat{u}_T - \phi\hat{u}_{T-1}$, which requires back-computing)

$$\hat{u}_{T+1} = 0.926149 \times (-0.020704755) + (-0.646372) \times \varepsilon_T$$

**Step 3**: Forecast the residual for 1993:Q2 (2-step ahead).

$$\hat{u}_{T+2} = \phi\hat{u}_{T+1}$$

(MA term dies at $h = 2$ for ARMA(1,1))

**Step 4**: Combine with the deterministic forecast.

For 1993:Q1:
$$\widehat{\text{LKWH}}_{1993:1} = \hat{\beta}_0 + \hat{\beta}_1 D_{\text{BROKEN}} + \hat{\beta}_2 \text{TREND}_{1993:1} + \hat{\beta}_3 T_{\text{DBROKEN}} + \hat{\delta}_1 \cdot 1 + \text{(other terms)} + \hat{u}_{T+1}$$

The $D_1 = 1$ because it's Q1. Trend value and broken trend values are deterministic and known.

**Exam tip**: This problem is 20 points because it requires combining multiple skills. The key is to be methodical: forecast deterministic part first, forecast residual ARMA part separately, then add them. Show clearly what is known vs. forecasted. If you don't have the exact innovation $\varepsilon_T$, state your assumption.

---

### Exam 1 (422 FINAL) — Q3b,c: Model Selection for Forecasting [10 pts]

**The question**: "Look at the output and find what is the best model for $\ln y_t$ / $\Delta\ln y_t$."

This isn't hand-calculation forecasting, but it's about **choosing** which model to forecast with. The key criteria:
- AIC/BIC (lower = better)
- Significance of coefficients
- Durbin-Watson statistic (near 2 = no serial correlation in residuals)
- Adjusted R²

For the LDM models: the AR(2) with quadratic trend has the best AIC (-4.354) and DW near 2 (1.989).

For the DLDM models: the AR(1) has the best AIC (-4.349) with DW = 1.983.

---

## Part 8: The Forecast Error Structure and Forecast Evaluation

### 8.1 How Forecast Errors Grow

| Model | h=1 error | h=2 error | h→∞ error |
|-------|-----------|-----------|-----------|
| AR(1) | $\varepsilon_{T+1}$ | $\varepsilon_{T+2} + \phi\varepsilon_{T+1}$ | Approaches $y_t - \mu$ (full variance) |
| MA(1) | $\varepsilon_{T+1}$ | $\varepsilon_{T+2} + \theta\varepsilon_{T+1}$ = full MA(1) | Already at full variance |
| MA(2) | $\varepsilon_{T+1}$ | $\varepsilon_{T+2} + \theta_1\varepsilon_{T+1}$ | At full variance by h=3 |

**Key insight**: 1-step errors are always just $\varepsilon_{T+1}$ (pure white noise). Multi-step errors accumulate more terms and have higher variance.

### 8.2 The Variance Inequality

For any optimal forecast:

$$\text{Var}(y) = \text{Var}(\hat{y}) + \text{Var}(e)$$

Since $\text{Var}(e) > 0$:

$$\text{Var}(\hat{y}) < \text{Var}(y)$$

**The forecast is always smoother than reality.** Don't be alarmed when your forecast doesn't swing as much as the actual data — that's mathematically guaranteed.

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "Your forecast will always be a bit smoother, will always have a little bit less variance than the actual data... Don't expect your forecast to match the actual data identically."

### 8.3 Mincer-Zarnowitz Test (Exam Material)

> **Lecture reference**: `week-06/summary.md` lines 253-260 (formal statement); `week-06/Forecasting-evaluation-transcript-feb-19.txt` (Pesavento's two formulations and the quote naming it).

To test whether a forecast is optimal:

$$y_{T+h} = \beta_0 + \beta_1\hat{y}_{T+h,T} + u_t$$

Test $H_0: (\beta_0, \beta_1) = (0, 1)$ jointly using an F-test.

- $\beta_0 \neq 0$: forecast has systematic bias
- $\beta_1 \neq 1$: forecast doesn't track actual movements correctly ($\beta_1 < 1$ = too smooth, $\beta_1 > 1$ = too volatile)
- Reject $H_0$: forecast is not optimal

Pesavento (`week-06/Forecasting-evaluation-transcript-feb-19.txt`):
> "If you regress your forecast error on your forecast, these two coefficients should all be zero... It's called the Mincer-Zarnowitz regression."

### 8.4 Diebold-Mariano Test

> **Lecture reference**: `week-06/Forecasting-evaluation-transcript-feb-19.txt` (full explanation with Southern Company example).

To compare two forecasts:

$$d_t = e_{1,t}^2 - e_{2,t}^2$$

$$t_{DM} = \frac{\bar{d}}{SE_{HAC}(\bar{d})}$$

- $H_0: E[d_t] = 0$ (equal predictive ability)
- Use HAC standard errors because $d_t$ may be serially correlated
- Reject → one model is significantly better

**Key from Week 6** (`week-06/Forecasting-evaluation-transcript-feb-19.txt`, Southern Company example): You can't just compare raw RMSE values. Two models might have different RMSE but the difference might not be statistically significant. The DM test formally checks this.

---

## Part 9: Common Mistakes

### Mistake 1: Using the ACTUAL future value instead of the forecast

**Wrong** (2-step from AR(2)):
$$\hat{y}_{T+2} = c + \phi_1 y_{T+1} + \phi_2 y_T$$

**Right**:
$$\hat{y}_{T+2} = c + \phi_1 \hat{y}_{T+1,T} + \phi_2 y_T$$

You don't know $y_{T+1}$ — that's what you're trying to predict! Always use the forecast $\hat{y}$.

### Mistake 2: Replacing PAST ε with zero

**Wrong**: "All ε are unknown, so they're all zero."

**Right**: $\varepsilon_T, \varepsilon_{T-1}, \ldots$ are PAST residuals — you observe them from your fitted model. Only FUTURE $\varepsilon$ get replaced with zero.

### Mistake 3: Forgetting the constant term

Many students omit $c$ from the forecast. The constant shifts the forecast level and matters numerically. Always include it.

### Mistake 4: Confusing exogenous with endogenous variables

In the carspend model, disposable income (disposinc) is **exogenous** — its future values are given. Car spending (carspend) is **endogenous** — its future values must be forecasted. Don't mix these up.

### Mistake 5: Not showing your work on arithmetic

Pesavento: "A correct answer with no explanation will NOT give you full credit." Show each multiplication. Label each term. State which values are known, which are forecasts.

---

## Cheat Sheet (Exam Morning Review)

```
================================================================
         FORECASTING BY HAND — EVERYTHING ON ONE PAGE
================================================================

THE TWO RULES
  1. Future ε (shock) → replace with 0
  2. Future y (value) → replace with your forecast ŷ
  Past ε and past y → keep (you know them)
  Exogenous variables → use given values

================================================================
AR(1): y_t = c + φy_{t-1} + ε_t
  h=1: ŷ_{T+1} = c + φ·y_T
  h=2: ŷ_{T+2} = c + φ·ŷ_{T+1}     ← use FORECAST
  h→∞: ŷ → c/(1-φ) = μ             (converges to mean)

AR(2): y_t = c + φ₁y_{t-1} + φ₂y_{t-2} + ε_t
  h=1: ŷ_{T+1} = c + φ₁·y_T + φ₂·y_{T-1}
  h=2: ŷ_{T+2} = c + φ₁·ŷ_{T+1} + φ₂·y_T
  h=3: ŷ_{T+3} = c + φ₁·ŷ_{T+2} + φ₂·ŷ_{T+1}

MA(1): y_t = μ + ε_t + θε_{t-1}
  h=1: ŷ_{T+1} = μ + θε_T           (use known residual)
  h≥2: ŷ = μ                         (forecast = mean)

MA(2): y_t = μ + ε_t + θ₁ε_{t-1} + θ₂ε_{t-2}
  h=1: ŷ_{T+1} = μ + θ₁ε_T + θ₂ε_{T-1}
  h=2: ŷ_{T+2} = μ + θ₂ε_T
  h≥3: ŷ = μ

ARMA(1,1): y_t = c + φy_{t-1} + ε_t + θε_{t-1}
  h=1: ŷ_{T+1} = c + φy_T + θε_T
  h=2: ŷ_{T+2} = c + φŷ_{T+1}       (MA part dies)
  h≥2: behaves like pure AR

================================================================
FORECAST ERROR VARIANCE
  h=1: σ²                            (always just σ²)
  h=2: σ²(1 + ψ₁²)                  (ψ₁ from MA(∞) rep)
  h→∞: Var(y_t)                      (converges to full var)
  95% CI: ŷ_{T+h} ± 1.96·σ_h

PROPERTIES OF OPTIMAL FORECASTS
  E[error] = 0                       (unbiased)
  1-step errors = white noise
  Var(ŷ) < Var(y)                    (forecast is smoother)

MINCER-ZARNOWITZ
  y_{t+h} = β₀ + β₁ŷ_{t+h|t} + u
  Test: (β₀,β₁) = (0,1) jointly

UNIT ROOT FORECAST
  ŷ_{T+h} = y_T  (for all h)
  Error variance grows linearly: hσ²
================================================================

EXAM PROCEDURE (for any forecasting question)
  1. Write the model at time T+h
  2. Identify each term: known? forecast? future ε?
  3. Replace future ε → 0, future y → ŷ
  4. Plug in numbers, show arithmetic
  5. Repeat for h+1 using your new forecast
================================================================
```

---

## Practice Drills

### Drill 1: AR(1) (2 minutes)
$y_t = 2.5 + 0.7y_{t-1} + \varepsilon_t$. Last observation: $y_T = 10$. Compute $\hat{y}_{T+1}$ and $\hat{y}_{T+2}$.

<details>
<summary>Solution</summary>

$\hat{y}_{T+1} = 2.5 + 0.7(10) = 2.5 + 7.0 = 9.5$

$\hat{y}_{T+2} = 2.5 + 0.7(9.5) = 2.5 + 6.65 = 9.15$

Note: converging toward $\mu = 2.5/(1-0.7) = 8.33$
</details>

### Drill 2: AR(2) (3 minutes)
$y_t = 1.0 + 0.5y_{t-1} + 0.3y_{t-2} + \varepsilon_t$. Data: $y_T = 12$, $y_{T-1} = 11$. Compute $\hat{y}_{T+1}$ and $\hat{y}_{T+2}$.

<details>
<summary>Solution</summary>

$\hat{y}_{T+1} = 1.0 + 0.5(12) + 0.3(11) = 1.0 + 6.0 + 3.3 = 10.3$

$\hat{y}_{T+2} = 1.0 + 0.5(10.3) + 0.3(12) = 1.0 + 5.15 + 3.6 = 9.75$

Note in the 2-step: $y_{T+1}$ replaced by forecast 10.3, but $y_T = 12$ is known.
</details>

### Drill 3: MA(2) (2 minutes)
$y_t = 3.0 + \varepsilon_t + 0.6\varepsilon_{t-1} - 0.4\varepsilon_{t-2}$. Residuals: $\varepsilon_T = 0.5$, $\varepsilon_{T-1} = -0.2$. Compute $\hat{y}_{T+1}$, $\hat{y}_{T+2}$, $\hat{y}_{T+3}$.

<details>
<summary>Solution</summary>

$\hat{y}_{T+1} = 3.0 + 0 + 0.6(0.5) + (-0.4)(-0.2) = 3.0 + 0.3 + 0.08 = 3.38$

$\hat{y}_{T+2} = 3.0 + 0 + 0 + (-0.4)(0.5) = 3.0 - 0.2 = 2.8$

$\hat{y}_{T+3} = 3.0$ (all ε terms are future → all zero → forecast = mean)
</details>

### Drill 4: ARMA(1,1) (3 minutes)
$y_t = 0.5 + 0.8y_{t-1} + \varepsilon_t - 0.3\varepsilon_{t-1}$. Data: $y_T = 6.0$, $\varepsilon_T = 0.4$. Compute $\hat{y}_{T+1}$ and $\hat{y}_{T+2}$.

<details>
<summary>Solution</summary>

$\hat{y}_{T+1} = 0.5 + 0.8(6.0) + 0 + (-0.3)(0.4) = 0.5 + 4.8 - 0.12 = 5.18$

$\hat{y}_{T+2} = 0.5 + 0.8(5.18) + 0 + 0 = 0.5 + 4.144 = 4.644$

At h=2 the MA part is dead — purely AR from here on.
</details>
