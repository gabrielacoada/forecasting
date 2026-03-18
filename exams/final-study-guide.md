# ECON 422 Final Exam Study Guide

**Exam: Thursday, 2:30pm | Format: 2.5 hours, closed book, calculator allowed**

**Source material**: Three old finals (different class — material overlaps but is not identical), three completed problem sets, course lectures Weeks 1-7.

**Not on this exam**: Unit root formal testing (Dickey-Fuller mechanics), smoothing (MA/exponential), MIDAS.

---

## STEP 1: Exam Topic Frequency Analysis

### Exam 1: "422 FINAL" (~2001)

| Q | Topic | Pts | Type |
|---|-------|-----|------|
| 1 | Trend estimation (linear, quadratic, broken trend with dummies), model selection, F-test for joint significance | 20 | Regression interpretation, hypothesis testing |
| 2 | MA(2) autocovariance derivation: Var(y_t), γ(1), γ(2), γ(3), ρ(1), ρ(2), ρ(3) | 20 | **Hand calculation** |
| 3a | ACF/PACF interpretation (levels vs differences), unit root behavior | 10 | Interpretation |
| 3b | Model selection from regression output (trend models) | 5 | Interpretation |
| 3c | Model selection for differenced series | 5 | Interpretation |
| 3d | Forecast evaluation (RMSE, MAE comparison) | 10 | Interpretation |
| 4a | ~~MA smoothing by hand~~ (not in our course) | 10 | ~~Skip~~ |
| 4b | ~~Exponential smoothing by hand~~ (not in our course) | 10 | ~~Skip~~ |
| 5 | R-squared conceptual (TSS, ESS, RSS components) | 10 | Conceptual |
| 6 | OLS minimum assumptions (bonus) | 5 | Conceptual |

### Exam 2: "422 FINAL #2" (~2002)

| Q | Topic | Pts | Type |
|---|-------|-----|------|
| 1 | Confidence interval from regression output (β, SE → CI) | 10 | **Hand calculation** |
| 2 | ACF/PACF of residuals → identify model for error process | 5 | Interpretation |
| 3 | AR(1) correction for serial correlation — is it adequate? Residual ACF/PACF check | 10 | Interpretation |
| 4 | AR(2) correction — compare confidence intervals across models, explain differences | 12 | Interpretation |
| 5 | F-test for joint significance of lags (by hand from regression output) | 10 | **Hand calculation** |
| 6 | Forecasting 1-step and 2-step ahead from AR(2) model by hand (using data table) | 12 | **Hand calculation** |
| 7 | ~~Why test for unit root~~ (conceptual version relevant — see Step 3) | 10 | Conceptual |
| 8 | ~~Dickey-Fuller test interpretation~~ (not in our course) | 5 | ~~Skip~~ |

### Exam 3: "422 Final Fall 08"

| Q | Topic | Pts | Type |
|---|-------|-----|------|
| 1a | Income/price elasticity interpretation from log-log regression | 5 | Interpretation |
| 1b | Structural break / broken trend testing (DBROKEN, TDBROKEN dummies) | 10 | Interpretation + **hand F-test** |
| 1c | Economic interpretation of broken trend | 10 | Conceptual |
| 1d | Seasonality — seasonal dummies significance, interpretation | 10 | Interpretation |
| 1e | F-test: test if two seasonal coefficients are equal (restricted vs unrestricted) | 10 | **Hand calculation** |
| 1f | ACF/PACF of residuals → identify AR, MA, or ARMA for cycles | 10 | Interpretation |
| 1g | Model selection via AIC/BIC from multiple regression outputs | 10 | Interpretation |
| 1h | Compute forecast by hand (1- and 2-step ahead using chosen ARMA model + residuals + seasonal dummies) | 20 | **Hand calculation** |
| Q3a | Compute Var(y_t) for MA(2) | 5 | **Hand calculation** |
| Q3b | Compute γ(1), γ(2), ρ(1), ρ(2) for MA(1) | 10 | **Hand calculation** |
| Bonus | Show white noise is stationary | 5 | Proof |

### Ranked Frequency Table (Filtered to Our Course)

| Rank | Topic | Appearances | Hand Calc? |
|------|-------|-------------|------------|
| 1 | **MA/AR autocovariance derivation** (Var, γ, ρ) | 3/3 exams | YES |
| 2 | **ACF/PACF identification** (ID model from correlogram) | 3/3 exams | Interpretation |
| 3 | **Forecasting by hand** (1-step, 2-step from AR/ARMA) | 3/3 exams | YES |
| 4 | **Structural breaks / broken trend** (dummies, F-test) | 3/3 exams | Mixed |
| 5 | **Model selection via AIC/BIC** | 3/3 exams | Interpretation |
| 6 | **F-test for joint significance** (from regression output) | 3/3 exams | YES |
| 7 | **Confidence intervals / regression interpretation** | 2/3 exams | YES |
| 8 | **Seasonality with dummies** (significance, forecasting) | 2/3 exams | Mixed |
| 9 | **Serial correlation correction** (AR(1)/AR(2) for residuals) | 1/3 exams | Interpretation |
| 10 | **Forecast evaluation** (RMSE, MAE comparison) | 1/3 exams | Interpretation |
| 11 | **R-squared / OLS fundamentals** | 1/3 exams | Conceptual |

---

## STEP 2: Problem Set Coverage & Gap Analysis

### Problem Set Topics

| PS | Topics Covered | Task Types |
|----|---------------|------------|
| **PS1** | MA(1) autocorrelation bounds, white noise properties, financial returns, ACF/PACF of returns and squared returns, volatility clustering | Conceptual reasoning, Python coding, correlogram interpretation |
| **PS2** | ARMA(1,1) derivation proof, ACF vs PACF conceptual, distributed lag model (oil & GDP), dynamic/cumulative multipliers, confidence intervals, F-test, ARMA model selection (PNFIC1), HC vs HAC standard errors, impulse response function | Proof, interpretation, Python coding, hand calculations |
| **PS3** | Forecasting scenario analysis (loss functions, decision environment), trend models (daily vs annual), seasonality (seasonal adjustment, Census Bureau) | Conceptual/discussion, no hand calculations |

### Gap Analysis

| Exam Topic | PS Coverage | Gap Status |
|------------|------------|------------|
| MA autocovariance derivation (Var, γ, ρ) | PS1 touches bounds conceptually | **WEAK** — never done full derivation by hand |
| ACF/PACF identification | PS1 + PS2 cover well | OK |
| Forecasting by hand (multi-step) | Not in any PS | **CRITICAL GAP** |
| Structural breaks / broken trend | Not in any PS | **CRITICAL GAP** |
| F-test by hand from regression output | PS2 conceptual only (F given, not computed) | **WEAK** |
| Loss functions (quadratic/absolute/linlin) | PS3 Q1 covers conceptually | Moderate — review needed |
| Mincer-Zarnowitz regression | Not in any PS | **SIGNIFICANT GAP** |
| Diebold-Mariano test | Not in any PS | **SIGNIFICANT GAP** |
| Unit roots (conceptual) | Not in any PS | **SIGNIFICANT GAP** |
| Seasonality with dummies + forecasting | PS3 discusses conceptually only | **WEAK** |
| Model selection AIC/BIC | PS2 covers well | OK |
| Distributed lag / dynamic multipliers | PS2 Q3 covers well | OK |
| Confidence intervals from output | PS2 touches this | Moderate |

---

## STEP 3: Prioritized Topic List (Top 10)

### 1. MA Autocovariance Derivation
**Exam frequency**: 3/3 | **Hand calc**: YES | **PS coverage**: WEAK

You must be able to: Given MA(q) with specific coefficients, compute Var(y_t), γ(1)...γ(q), ρ(1)...ρ(q) from scratch using E[ε_t ε_s] = σ² if t=s, 0 otherwise. Know that γ(k) = 0 for k > q (the cutoff property) and explain why.

### 2. Forecasting by Hand (AR/ARMA, Multi-Step)
**Exam frequency**: 3/3 | **Hand calc**: YES | **PS coverage**: CRITICAL GAP

You must be able to: Given estimated AR(p) coefficients + last few data values, compute ŷ_{T+1} and ŷ_{T+2} by plugging in recursively. Key rule: for ŷ_{T+2}, use the FORECAST (not actual) for y_{T+1}. For MA: forecast = unconditional mean beyond q steps. For ARMA: combine both components.

### 3. Structural Breaks / Broken Trend
**Exam frequency**: 3/3 | **Hand calc**: Mixed | **PS coverage**: CRITICAL GAP

You must be able to: Interpret DBROKEN (intercept shift) and TDBROKEN (slope shift) coefficients. Slope before break = β₁, slope after = β₁ + β₃. Test significance individually (t-test from output) and jointly (F-test you compute). Explain economic meaning of the structural change.

### 4. F-Test From Regression Output
**Exam frequency**: 3/3 | **Hand calc**: YES | **PS coverage**: WEAK

You must be able to: Compute F = [(SSR_r - SSR_u)/q] / [SSR_u/(n - k_u)]. Know how to identify SSR from regression output ("Sum squared resid"), count q (number of restrictions = variables dropped), determine degrees of freedom, look up F critical value from the table provided.

### 5. Forecast Evaluation (Mincer-Zarnowitz, DM Test, RMSE/MAE)
**Exam frequency**: 1/3 old exams + entire Week 6 lecture | **PS coverage**: SIGNIFICANT GAP

You must be able to: Run Mincer-Zarnowitz regression (y_{t+h} = β₀ + β₁ŷ_{t+h|t} + u_t; optimal requires (β₀,β₁) = (0,1) jointly). Explain Diebold-Mariano test (d_t = e²_{1t} - e²_{2t}, test if E[d_t] = 0 with HAC SEs). Compare RMSE and MAE across models. Week 6 summary flags M-Z as "EXAM MATERIAL."

### 6. ACF/PACF Identification
**Exam frequency**: 3/3 | **Hand calc**: No (interpretation) | **PS coverage**: OK

You must be able to: Instantly identify from a correlogram:
- ACF decays + PACF cuts off at p → AR(p)
- ACF cuts off at q + PACF decays → MA(q)
- Both decay → ARMA(p,q)

"Cuts off" = drops to zero sharply. "Decays" = gradually diminishes.

### 7. Loss Functions & Optimal Forecasts
**Exam frequency**: Week 6 core material + PS3 Q1 | **PS coverage**: Moderate

You must be able to: State that quadratic loss → optimal forecast = conditional mean. Absolute loss → conditional median. Linlin/asymmetric with costs a (under) and b (over) → conditional quantile at d = b/(a+b). Under asymmetric loss, optimal forecasts are deliberately biased. Apply to scenarios (e.g., overprediction costlier → shade forecast down).

### 8. Unit Roots (Conceptual)
**Exam frequency**: Conceptually central to Week 4 | **PS coverage**: SIGNIFICANT GAP

You must be able to explain:

| ρ value | What happens | Forecast |
|---------|-------------|----------|
| ρ = 0.5 | Shock dies quickly | Past matters, but fades |
| ρ = 0.9 | Shock very persistent (15-20 quarters) | Past matters a lot |
| **ρ = 1** | **Shock permanent. Never goes away.** | **Best forecast = y_T. Error = sum of future WN = unforecastable** |
| ρ > 1 | Explosive (bubbles, briefly) | Nonsensical |

Why ρ = 1 breaks everything:
- Var(y_t) = σ²/(1 - ρ²) → **∞ when ρ = 1**
- Process = random walk: y_t = y_{t-1} + ε_t → non-stationary
- Standard distributions don't apply
- Cannot construct sensible long-run forecasts
- Forecast error variance **grows with h** (never converges), unlike stationary case

The forecasting punchline: y_{T+h} = y_T + ε_{T+1} + ... + ε_{T+h}. Best forecast = y_T for all horizons. The accumulated WN errors are unforecastable.

Stationarity conditions:
- AR(1): |ρ| < 1
- AR(2): both roots of characteristic polynomial outside unit circle
- MA(q): **always stationary**

### 9. Seasonality with Dummies
**Exam frequency**: 2/3 | **PS coverage**: WEAK

You must be able to: With quarterly data, use 3 dummies (D1, D2, D3; Q4 = base). Coefficient on D1 = difference between Q1 and Q4 average. Joint F-test for significance of all dummies. Forecasting: seasonal part is deterministic (known in advance), only the cyclical/stochastic residual needs ARMA forecasting.

### 10. Confidence Intervals / Regression Interpretation
**Exam frequency**: 2/3 | **Hand calc**: YES | **PS coverage**: Moderate

You must be able to: CI = β̂ ± t_crit × SE(β̂). For large samples: t_crit ≈ 1.96 at 95%. For predictions: multiply coefficient by Δx, propagate CI. Understand why CIs change when you add lagged dependent variables (serial correlation correction changes SEs).

---

## STEP 4: Day-by-Day Study Plan

### MONDAY (Today — Full Day)

#### 9:00-10:30 — Fast Triage: Identify Weak Spots
- Skim all three old exams (skip smoothing Q4a/Q4b in Exam 1 and Dickey-Fuller Q8 in Exam 2)
- For each remaining question, mark: "confident" / "shaky" / "lost"
- Key self-test: Can you do the MA autocovariance derivation right now? Can you forecast by hand? Do you know the F-test formula? Do you know Mincer-Zarnowitz?

#### 10:30-12:30 — Deep Study: MA/AR Autocovariance Derivations (Priority #1)

**Method**: Write y_t and y_{t-k} side by side. Multiply term by term. Only same-index ε terms survive (E[ε_t ε_s] = σ² if t=s, 0 otherwise).

**Start with MA(1)**: y_t = ε_t + θε_{t-1}
```
Var(y_t) = (1 + θ²)σ²
γ(1) = θσ²
γ(k) = 0 for k ≥ 2
ρ(1) = θ/(1 + θ²)
```

**Then MA(2)**: y_t = ε_t + θ₁ε_{t-1} + θ₂ε_{t-2}
```
Var(y_t) = (1 + θ₁² + θ₂²)σ²
γ(1) = (θ₁ + θ₁θ₂)σ²
γ(2) = θ₂σ²
γ(k) = 0 for k ≥ 3    ← cutoff property!
ρ(k) = γ(k)/γ(0)
```

**Practice problems**:
- Exam 1 Q2: MA(2) with θ₁=0.3, θ₂=0.7 → do it fully by hand
- Exam 3 Q3a: Var for MA(2) with θ₁=0.8, θ₂=0.2
- Exam 3 Q3b: Full γ and ρ for MA(1) with θ=0.8

**Resource**: `course-materials/lectures/week-04/summary.md` (MA properties section)

#### 12:30-1:30 — Lunch

#### 1:30-3:30 — Deep Study: Forecasting by Hand (Priority #2)

**AR forecasting (recursive)**:
```
ŷ_{T+1} = c + φ₁y_T + φ₂y_{T-1}
ŷ_{T+2} = c + φ₁ŷ_{T+1} + φ₂y_T     ← use FORECAST for unknown values
```

**MA forecasting** (from Week 6):
- MA(q) can forecast up to q steps using known residuals
- Beyond q steps: forecast = unconditional mean (no more ε information)
- Key: need to know the past residuals/shocks

**Practice problems**:
- Exam 2 Q6: Compute 1-step and 2-step from AR(2) using data table
- Exam 3 Q1h: Forecast using seasonal dummies + ARMA residual model (hardest version)

**Resource**: `course-materials/lectures/week-06/summary.md` (forecasting with ARMA section)

#### 3:30-5:30 — Deep Study: Structural Breaks & F-Tests (Priority #3 + #4)

**Structural break model**:
```
y_t = c + β₁·TIME + β₂·DBROKEN + β₃·TDBROKEN + ε_t
```
- DBROKEN shifts the intercept (level shift at break date)
- TDBROKEN shifts the slope (trend change)
- Trend before break: β₁
- Trend after break: β₁ + β₃

**F-test formula**:
```
F = [(SSR_restricted - SSR_unrestricted) / q] / [SSR_unrestricted / (n - k_unrestricted)]
```
- SSR = "Sum squared resid" in output
- q = number of restrictions (variables dropped)
- k_u = number of parameters in unrestricted model
- Compare to F critical value from table at back of exam

**Practice problems**:
- Exam 2 Q5: Test joint significance of two lags (compute F from SSR values)
- Exam 3 Q1b: Broken trend test (DBROKEN + TDBROKEN joint significance)
- Exam 1 Q1a: Broken trend with individual and joint tests
- Exam 3 Q1e: Test if two seasonal coefficients are equal (restricted vs unrestricted)

#### 5:30-7:00 — Deep Study: Forecast Evaluation (Priority #5)

**Mincer-Zarnowitz regression**:
```
y_{t+h} = β₀ + β₁·ŷ_{t+h|t} + u_{t+1}
```
- Optimal forecast requires: β₀ = 0 AND β₁ = 1 jointly
- Test with F-test on the joint restriction (q = 2)
- β₀ ≠ 0 → systematic bias
- β₁ ≠ 1 → forecast doesn't track actual movements correctly
- Reject H₀ → forecast is NOT optimal

**Diebold-Mariano test** (comparing two forecasts):
```
d_t = e²_{1t} - e²_{2t}
t_DM = d̄ / SE_HAC(d̄)
```
- H₀: E[d_t] = 0 (equal predictive ability)
- Uses HAC standard errors because d_t is serially correlated
- Reject → one model forecasts significantly better

**Accuracy measures**:
- RMSE (professor's preferred): same units as forecast
- MAE: robust to outliers
- Theil U: relative to naive forecast (U < 1 means model beats naive)

**Resource**: `course-materials/lectures/week-06/summary.md`

#### 7:00-8:00 — Review any derivation you stumbled on

---

### TUESDAY (Full Day)

#### 9:00-11:00 — ACF/PACF Identification Mastery (Priority #6)

Drill this table until it's instant:

| Model | ACF | PACF |
|-------|-----|------|
| AR(p) | Decays (exponential or oscillating) | Cuts off after lag p |
| MA(q) | Cuts off after lag q | Decays |
| ARMA(p,q) | Decays | Decays |

**Practice** — go through every correlogram in the old exams:
- Exam 1: LDM correlogram (slowly decaying ACF = near unit root); DLDM (much less persistent)
- Exam 2 Q2: Residual ACF/PACF → identify error model
- Exam 3 Q1f: Residual correlogram from seasonal dummy model

**Resource**: `course-materials/lectures/week-04/summary.md` lines 122-131; `problem-sets/problem-set-2/context-brief.md` lines 42-53

#### 11:00-1:00 — Loss Functions & Optimal Forecasts (Priority #7)

**Three loss functions**:
- **Quadratic**: L(e) = e² → optimal forecast = conditional mean E[y_{T+h}|Ω_T]
- **Absolute**: L(e) = |e| → optimal forecast = conditional median
- **Linlin (asymmetric)**: L(e) = a|e| if e<0, b|e| if e>0 → optimal = quantile at d = b/(a+b)

**Key insight**: Under asymmetric loss, optimal forecasts are deliberately biased.
- Overprediction costlier (a > b): shade forecast DOWN
- Underprediction costlier (b > a): shade forecast UP

**Pesavento's examples**:
- Stock investing = asymmetric (happy about upside surprises, unhappy about downside)
- Bus stop = asymmetric (late much worse than early)

**Practice**: Review PS3 Q1 scenarios (airline stocks, OMB tax revenue, advertising)

**Resource**: `course-materials/lectures/week-06/summary.md`; `problem-sets/problem-set-3/context-brief.md`

#### 1:00-2:00 — Lunch

#### 2:00-3:00 — Unit Roots Conceptual (Priority #8)

**Core concept**: ρ = 1 is THE critical boundary.

From Pesavento (Week 4):
- ρ = 0.5 → "maybe in a year it's going to be irrelevant"
- ρ = 0.9 → "going to be like 15-20 quarters before it's irrelevant"
- **ρ = 1 → "the shock is permanent. It never goes away."**
- ρ > 1 → "explosive... bubbles... they pop"

**Why ρ = 1 breaks everything**:
- Var(y_t) = σ²/(1 - ρ²) → ∞ when ρ = 1
- Process is a random walk: y_t = y_{t-1} + ε_t
- Non-stationary: mean, variance depend on time
- Standard distributions don't apply
- Cannot construct sensible long-run forecasts

**The forecasting punchline**:
```
y_{T+h} = y_T + ε_{T+1} + ε_{T+2} + ... + ε_{T+h}
Best forecast = y_T  (for ALL horizons h)
Error = sum of WN = unforecastable
Forecast error variance grows with h (never converges)
```

Compare to stationary case: forecast error variance converges to Var(y_t).

**Visual signature**: Slowly decaying ACF (still 0.8+ at lag 20) → near unit root. After differencing, ACF drops dramatically → differenced series is stationary.

**Practice**: Look at LDM/DLDM correlograms from Exam 1 (page 9-10). Explain why LDM looks like a unit root and why DLDM doesn't.

**Stationarity conditions summary**:
- AR(1): |ρ| < 1
- AR(2): both roots of characteristic polynomial outside unit circle
- MA(q): always stationary (finite sum of WN)

#### 3:00-4:00 — Near-Cancellation + AR/MA Interchangeability

**Near-cancellation** (GDP growth example from Week 4):
- ARMA(1,1): ρ̂ ≈ 0.3 and θ̂ ≈ -0.3 → they cancel!
- (1 - 0.3L)y_t = (1 - 0.3L)ε_t → divides out to y_t = ε_t (white noise!)
- Both coefficients insignificant together, but AR(1) alone is significant
- Lesson: like multicollinearity — don't drop both terms simultaneously

**AR/MA interchangeability** (Wold theorem):
- AR(1) = MA(∞): y_t = Σ ρʲε_{t-j}
- An MA(2) dataset was equally well fit by AR(3) (AIC: 1401 vs 1402)
- In practice: AR preferred because OLS estimation, easy interpretation, easy forecasting

**Resource**: `course-materials/lectures/week-04/summary.md` lines 189-211

#### 4:00-5:30 — Seasonality with Dummies (Priority #9)

- Quarterly data → 3 dummies (D1, D2, D3; Q4 = base)
- Coefficient on D_i = average for quarter i minus average for Q4
- Joint F-test for significance of all seasonal dummies
- Forecasting: seasonal part is deterministic and known; only the residual cycle needs ARMA forecasting

**Practice**:
- Exam 3 Q1d: Are seasonal dummies significant?
- Exam 3 Q1e: Test if Q2 = Q3 effect (requires restricted vs unrestricted regression and F-test)

**Resource**: `course-materials/lectures/week-02/` break/seasonality slides

#### 5:30-7:00 — Model Selection & CI Review (Priorities #9-10)

**Model selection**:
- AIC/BIC: lower = better
- BIC penalizes more → favors parsimony
- Pesavento's recipe: start large → eliminate insignificant → compare AIC/BIC → check residual correlogram

**Practice**: Exam 3 Q1g — pick best from AR(1), AR(2), AR(3), MA(1), MA(2), ARMA(1,1)

**Confidence intervals**:
- CI = β̂ ± t_crit × SE(β̂)
- Large samples: t_crit ≈ 1.96 for 95%, ≈ 2.576 for 99%
- Prediction: multiply coefficient by Δx, propagate CI

**Practice**: Exam 2 Q1 (compute CI, predict for $300B change) and Q4 (compare CIs across AR(1) vs AR(2))

#### 7:00-8:00 — Start formula sheet (first draft)

---

### WEDNESDAY (Practice & Mock Exam)

#### 9:00-11:00 — Targeted Practice Problems
- Redo PS2 Q3 without looking (distributed lag, cumulative multiplier, F-test interpretation)
- Do a fresh MA autocovariance with new numbers: y_t = ε_t - 0.5ε_{t-1} + 0.3ε_{t-2}
- Write out Mincer-Zarnowitz test from scratch as if it were an exam question
- Write a paragraph explaining what happens when ρ = 1 as if it were a short-answer question

#### 11:00-1:30 — TIMED MOCK EXAM (2.5 hours)
- Use **Exam 2 (422 FINAL #2)** — skip Q8 (Dickey-Fuller mechanics)
- That leaves Q1-Q7: ~70 pts of directly relevant material
- Supplement with a self-written question: "Explain the Mincer-Zarnowitz test. What does it mean for a forecast to be optimal?"
- Set timer. No notes. Calculator only.

#### 1:30-2:30 — Lunch

#### 2:30-4:30 — Mock Exam Self-Grading & Gap Filling
- For every mistake, identify the exact concept and re-study
- Write clean solutions for anything you got wrong

#### 4:30-6:00 — Final Formula Sheet

```
=== MA(q) AUTOCOVARIANCES ===
γ(0) = (1 + θ₁² + ... + θ_q²)σ²
γ(k) = (θ_k + θ_{k+1}θ₁ + θ_{k+2}θ₂ + ...)σ²   for k ≤ q
γ(k) = 0                                          for k > q
ρ(k) = γ(k)/γ(0)

=== AR(1) PROPERTIES ===
E(y_t) = c/(1-ρ)           requires |ρ| < 1
Var(y_t) = σ²/(1-ρ²)       → ∞ when ρ = 1
ρ(s) = ρˢ                  geometric decay
IRF: shock of 1 → ρ, ρ², ρ³, ...

=== AR FORECAST RECURSION ===
ŷ_{T+1} = c + φ₁y_T + φ₂y_{T-1}
ŷ_{T+2} = c + φ₁ŷ_{T+1} + φ₂y_T    (use FORECAST, not actual)
MA(q): forecast = unconditional mean beyond q steps

=== F-TEST ===
F = [(SSR_r - SSR_u) / q] / [SSR_u / (n - k_u)]
q = # restrictions, k_u = # params in unrestricted model

=== ACF/PACF TABLE ===
AR(p):    ACF decays,     PACF cuts off at p
MA(q):    ACF cuts off q, PACF decays
ARMA:     both decay

=== LOSS FUNCTIONS ===
Quadratic → E[y|Ω]   (mean)
Absolute  → median
Linlin    → quantile d = b/(a+b)

=== MINCER-ZARNOWITZ ===
y_{t+h} = β₀ + β₁ŷ_{t+h|t} + u_t
Optimal ↔ (β₀, β₁) = (0, 1) jointly

=== DIEBOLD-MARIANO ===
d_t = e²_{1t} - e²_{2t}
t_DM = d̄ / SE_HAC(d̄)

=== BROKEN TREND ===
y = c + β₁t + β₂·DBROKEN + β₃·TDBROKEN
Slope before = β₁, slope after = β₁ + β₃

=== UNIT ROOT (ρ = 1) ===
Random walk: y_t = y_{t-1} + ε_t
Best forecast = y_T (all horizons)
Var → ∞, non-stationary, forecast error grows with h

=== CONFIDENCE INTERVAL ===
CI = β̂ ± t_crit × SE(β̂)
95%: t ≈ 1.96 (large sample)
```

#### 6:00-7:00 — Light review of remaining weak spots

---

### THURSDAY MORNING (Exam at 2:30pm)

#### 9:00-10:00 — Light Warmup Only
- One MA(2) autocovariance derivation (5 min)
- One 2-step AR forecast (5 min)
- One F-test from output (5 min)
- Recite loss functions and Mincer-Zarnowitz from memory

#### 10:00-11:00 — Skim Exam 3 (Fall 08) at High Level
- Don't solve — just outline your approach for each relevant question
- Make sure you can identify what to do for every question type

#### 11:00-12:00 — Break. Real meal. Hydrate.

#### 12:00-1:30 — Final formula sheet pass. Confidence building.
- Remind yourself: you've seen every question type that could appear
- The exam recycles the same ~10 patterns

#### 2:00 — Arrive at exam room. 2:30 — Go time.

---

## STEP 5: Highest-Risk Gaps — Worked Reference Examples

### Worked Example 1: MA(2) Autocovariance Derivation

**Problem** (Exam 1 Q2): y_t = ε_t + 0.3ε_{t-1} + 0.7ε_{t-2}. Compute Var(y_t), γ(1), γ(2), γ(3), ρ(1), ρ(2), ρ(3).

**Var(y_t) = γ(0)**:
```
γ(0) = E[(ε_t + 0.3ε_{t-1} + 0.7ε_{t-2})²]
     = E[ε_t²] + 0.09·E[ε_{t-1}²] + 0.49·E[ε_{t-2}²]     (cross terms vanish)
     = σ²(1 + 0.09 + 0.49)
     = 1.58σ²
```

**γ(1) = E[y_t · y_{t-1}]**:
```
y_t     = ε_t   + 0.3·ε_{t-1} + 0.7·ε_{t-2}
y_{t-1} = ε_{t-1} + 0.3·ε_{t-2} + 0.7·ε_{t-3}

Only terms where SAME ε index survives:
  0.3 × 1 × E[ε_{t-1}²]   = 0.3σ²     (ε_{t-1} matches)
  0.7 × 0.3 × E[ε_{t-2}²] = 0.21σ²    (ε_{t-2} matches)

γ(1) = (0.3 + 0.21)σ² = 0.51σ²
```
General formula: γ(1) = (θ₁ + θ₁θ₂)σ²

**γ(2) = E[y_t · y_{t-2}]**:
```
y_t     = ε_t   + 0.3·ε_{t-1} + 0.7·ε_{t-2}
y_{t-2} = ε_{t-2} + 0.3·ε_{t-3} + 0.7·ε_{t-4}

Only match: 0.7 × 1 × E[ε_{t-2}²] = 0.7σ²

γ(2) = θ₂σ² = 0.7σ²
```

**γ(3) = 0** — no overlapping ε terms exist. This is the MA(2) **cutoff property**: autocovariance is zero beyond the order of the MA.

**Autocorrelations**:
```
ρ(1) = γ(1)/γ(0) = 0.51/1.58 = 0.3228
ρ(2) = γ(2)/γ(0) = 0.70/1.58 = 0.4430
ρ(3) = 0
```

**Exam tip**: Always state γ(k) = 0 for k > q and explain WHY (non-overlapping ε terms → E[ε_i · ε_j] = 0 when i ≠ j).

---

### Worked Example 2: 2-Step-Ahead AR(2) Forecast

**Problem** (Exam 2 Q6): AR(2) model:
```
carspend_t = 0.0005992·disposinc_t + 0.5778·carspend_{t-1}
           + 0.3774·carspend_{t-2} + 1.5767
```
Last data: carspend_{2002:3} = 109.192, carspend_{2002:2} = 102.244.
Future disposinc given: 2002:4 = 7935.6, 2003:1 = 8039.2

**1-step ahead** (2002:4):
```
ŷ_{T+1} = 0.0005992(7935.6) + 0.5778(109.192) + 0.3774(102.244) + 1.5767
        = 4.755 + 63.098 + 38.587 + 1.577
        = 108.017
```

**2-step ahead** (2003:1) — use the FORECAST for unknown y_{T+1}:
```
ŷ_{T+2} = 0.0005992(8039.2) + 0.5778(108.017) + 0.3774(109.192) + 1.5767
        = 4.817 + 62.412 + 41.208 + 1.577
        = 110.014
```

**Exam tip**: For multi-step forecasts, replace unknown future y values with your FORECASTS. Exogenous variables (disposinc) use actual given values.

---

### Worked Example 3: F-Test From Regression Output

**Problem** (Exam 2 Q5): Test joint significance of L1 and L2 in AR(2).

Read from the output tables:
- **Restricted model** (just disposinc, no lags): SSR_r = 29406.39, k_r = 2
- **Unrestricted model** (AR(2)): SSR_u = 4214.14, k_u = 4, n = 173
- **Number of restrictions**: q = 2 (dropped L1 and L2)

```
F = [(29406.39 - 4214.14) / 2] / [4214.14 / (173 - 4)]
  = [25192.25 / 2] / [4214.14 / 169]
  = 12596.13 / 24.94
  = 505.1
```

Compare to F_{2,169} ≈ 3.05 at 5% (from table). 505.1 >> 3.05 → **reject H₀**. Lags are jointly significant.

**Exam tip**: Always show the formula, plug in clearly, state the critical value and your conclusion.

---

### Worked Example 4: Mincer-Zarnowitz Test

**Setup**: You have forecast series ŷ_{t+1|t} and actual values y_{t+1}. Run:
```
y_{t+1} = β₀ + β₁·ŷ_{t+1|t} + u_{t+1}
```

**Suppose you get**: β̂₀ = 0.15 (SE = 0.08), β̂₁ = 0.92 (SE = 0.05)

**Test H₀**: (β₀, β₁) = (0, 1) jointly, using F-test with q = 2 restrictions.

**Interpretation**:
- β̂₀ = 0.15: small positive bias (forecast slightly low on average)
- β̂₁ = 0.92: forecast underreacts to actual movements (too smooth)
- If F-test rejects → forecast is NOT optimal; can be improved
- If F-test fails to reject → forecast passes the optimality test

**Why this matters**: Just comparing RMSE tells you which forecast is MORE accurate. Mincer-Zarnowitz tells you whether a forecast is OPTIMAL (using all available information efficiently).

---

## Quick Reference: Key Pesavento Terminology

Use these exact terms in your exam answers:

| Term | Meaning | Context |
|------|---------|---------|
| "impact effect" | Contemporaneous coefficient β₁ in distributed lag | Week 5 |
| "dynamic multiplier" | Effect at each lag; also = impulse response | Week 4-5 |
| "cumulative multiplier" | Sum of coefficients through lag k | Week 5 |
| "cuts off" vs "decays" | ACF/PACF pattern for model identification | Week 4 |
| "start large, eliminate small" | Model selection philosophy | Week 4 |
| "the smaller the better" | Information criteria (AIC/BIC) | Week 4 |
| "plot the residual correlogram" | Primary diagnostic — "the most important thing" | Week 4 |
| "roots outside the unit circle" | Stationarity condition for AR(p) | Week 4 |
| HAC / Newey-West | Default robust SEs — "always use HAC regardless" | Week 5 |
| "unforecastability principle" | If you can forecast the error, the forecast isn't optimal | Week 6 |
