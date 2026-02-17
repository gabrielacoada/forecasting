# Week 6: Key Concepts - Forecasting with ARMA Models

## Concept Map

```mermaid
graph TD
    A[Week 6: Forecasting with ARMA] --> B[Loss Functions]
    A --> C[Optimal Forecast]
    A --> D[Forecasting Mechanics]
    A --> E[Forecast Properties]
    A --> F[Interval & Density Forecasts]

    B --> B1["Quadratic: L(e) = e²"]
    B --> B2["Absolute: L(e) = |e|"]
    B --> B3["Linlin: asymmetric slopes"]

    C --> C1["Quadratic → Conditional Mean"]
    C --> C2["Absolute → Conditional Median"]
    C --> C3["Linlin → Conditional Quantile"]

    D --> D1["MA(q): forecast q steps, then mean"]
    D --> D2["AR(1): ŷ = φʰyT (recursive)"]
    D --> D3["ARMA: combine AR + MA logic"]

    E --> E1["E(error) = 0"]
    E --> E2["Cov(forecast, error) = 0"]
    E --> E3["Var(actual) > Var(forecast)"]

    F --> F1["CI: ŷ ± 1.96σₕ"]
    F --> F2["Density: N(ŷ, σₕ²)"]
```

## The Forecasting Pipeline

```mermaid
flowchart LR
    MODEL["Estimated ARMA Model<br/>(from Weeks 3-4)"] --> WRITE["Write out model<br/>at T+h"]
    WRITE --> REPLACE{"What can you<br/>observe?"}
    REPLACE -->|"Future ε → 0"| FUTURE["Replace future shocks<br/>with zero"]
    REPLACE -->|"Future y → forecast"| RECUR["Replace future y<br/>with ŷ (recursive)"]
    REPLACE -->|"Past ε, y → known"| KNOWN["Keep observed values"]

    FUTURE --> FORECAST["h-step Forecast<br/>ŷ_{T+h,T}"]
    RECUR --> FORECAST
    KNOWN --> FORECAST

    FORECAST --> ERROR["Forecast Error<br/>e = y - ŷ"]
    ERROR --> VARIANCE["Error Variance σₕ²"]
    VARIANCE --> CI["95% CI:<br/>ŷ ± 1.96σₕ"]

    style FUTURE fill:#ffcdd2
    style RECUR fill:#fff3e0
    style KNOWN fill:#c8e6c9
    style CI fill:#e3f2fd
```

## Loss Function Decision Tree

```mermaid
flowchart TD
    START{"Is the cost of<br/>over- and under-<br/>prediction equal?"} -->|"Yes"| SYM["Symmetric Loss"]
    START -->|"No"| ASYM["Asymmetric Loss"]

    SYM --> QUAD{"Do you want to<br/>heavily penalize<br/>large errors?"}
    QUAD -->|"Yes"| QUADRATIC["Quadratic: L(e) = e²<br/>→ Conditional Mean<br/>(OLS / ARMA forecast)"]
    QUAD -->|"No, equal penalty"| ABSOLUTE["Absolute: L(e) = |e|<br/>→ Conditional Median"]

    ASYM --> LINLIN["Linlin Loss<br/>L(e) = a|e| if e>0<br/>L(e) = b|e| if e≤0"]
    LINLIN --> QUANTILE["→ Conditional Quantile<br/>d = b/(a+b)"]

    style QUADRATIC fill:#c8e6c9
    style ABSOLUTE fill:#e3f2fd
    style QUANTILE fill:#fff3e0
```

**Pesavento's examples of asymmetric loss:**
- **Stock prediction:** Under-predicting a stock's rise → you miss investment gains (costly). Over-predicting → you invest more but it doesn't rise as much (less costly). → Penalize under-prediction more.
- **Bus arrival time:** Under-predicting arrival time → you miss the bus (costly). Over-predicting → you wait a bit longer (not costly). → Penalize under-prediction more.

## Which Model for Forecasting? MA vs AR vs ARMA

```mermaid
flowchart TD
    MODEL{"What model<br/>did you estimate?"} -->|"MA(q)"| MA["MA(q) Forecast"]
    MODEL -->|"AR(p)"| AR["AR(p) Forecast"]
    MODEL -->|"ARMA(p,q)"| ARMA["ARMA(p,q) Forecast"]

    MA --> MA_RULE["Can forecast q steps ahead<br/>After q steps: forecast = μ"]
    MA_RULE --> MA_LIMIT["❌ Limited horizon<br/>'People don't like MA<br/>for forecasting'"]

    AR --> AR_RULE["ŷ_{T+h} = φʰyT<br/>Recursive: ŷ_{T+h} = φ·ŷ_{T+h-1}"]
    AR_RULE --> AR_ADV["✓ Forecast any horizon<br/>Quality decays with h"]

    ARMA --> ARMA_RULE["h=1: use both AR + MA parts<br/>h>q: only AR part survives<br/>ŷ_{T+h} = φ·ŷ_{T+h-1}"]
    ARMA_RULE --> ARMA_ADV["✓ Best of both worlds<br/>'ARMA preferred because<br/>you can forecast far'"]

    style MA_LIMIT fill:#ffcdd2
    style AR_ADV fill:#c8e6c9
    style ARMA_ADV fill:#c8e6c9
```

## MA(2) Forecast — Step by Step (from board notes)

```mermaid
flowchart TD
    M["MA(2): yₜ = μ + εₜ + θ₁εₜ₋₁ + θ₂εₜ₋₂"] --> H1["h=1: y_{T+1} = μ + ε_{T+1} + θ₁εT + θ₂ε_{T-1}"]
    H1 --> H1F["ŷ_{T+1,T} = μ + 0 + θ₁εT + θ₂ε_{T-1}<br/>Error: ε_{T+1} (WN)<br/>Var: σ²"]

    M --> H2["h=2: y_{T+2} = μ + ε_{T+2} + θ₁ε_{T+1} + θ₂εT"]
    H2 --> H2F["ŷ_{T+2,T} = μ + 0 + 0 + θ₂εT<br/>Error: ε_{T+2} + θ₁ε_{T+1} (MA(1))<br/>Var: σ²(1 + θ₁²)"]

    M --> H3["h≥3: y_{T+h} = μ + ε_{T+h} + θ₁ε_{T+h-1} + θ₂ε_{T+h-2}"]
    H3 --> H3F["ŷ_{T+h,T} = μ<br/>Error = y_{T+h} - μ (MA(2) itself)<br/>Var: σ²(1 + θ₁² + θ₂²) = Var(y)"]

    style H1F fill:#c8e6c9
    style H2F fill:#fff3e0
    style H3F fill:#ffcdd2
```

**Rule:** Replace future $\varepsilon$ with 0 (can't forecast white noise). Keep past $\varepsilon$ (observed as residuals).

## The Variance Inequality (from board notes)

```mermaid
flowchart TD
    DECOMP["y_{T+h} = ŷ_{T+h,T} + e_{T+h,T}<br/>(actual = forecast + error)"]
    DECOMP --> UNCORR["If forecast is optimal:<br/>Cov(ŷ, e) = 0"]
    UNCORR --> VAR["Var(y_{T+h}) = Var(ŷ_{T+h,T}) + Var(e_{T+h,T})"]
    VAR --> INEQ["Var(actual) > Var(forecast)<br/>ALWAYS"]
    INEQ --> INTERP["When plotting actual vs forecast:<br/>Forecast will ALWAYS be smoother"]
    INTERP --> WARN["⚠️ Don't interpret offset as<br/>model failure — it's mathematical"]

    style INEQ fill:#e3f2fd
    style WARN fill:#fff3e0
```

> **Professor:** "Don't expect your forecast to match the actual data identically. Your forecast will always be a bit smoother, with a smaller variance."

## Out-of-Sample vs Pseudo Out-of-Sample

```mermaid
flowchart LR
    subgraph "Pseudo Out-of-Sample"
        PAST["Historical Data<br/>1970 — 2024"] --> PRETEND["Pretend you're<br/>at end of 2024"]
        PRETEND --> FORECAST_P["Forecast 2025<br/>using ONLY<br/>pre-2025 info"]
        FORECAST_P --> COMPARE["Compare to<br/>actual 2025 data<br/>(which you have)"]
    end

    subgraph "True Out-of-Sample"
        ALL["All Data<br/>1970 — 2025"] --> NOW["You are at<br/>Feb 2026"]
        NOW --> FORECAST_T["Forecast future<br/>(Mar 2026+)"]
        FORECAST_T --> WAIT["Wait and see<br/>what happens"]
    end

    subgraph "Nowcasting"
        AVAIL["Available data<br/>(some series released,<br/>some not yet)"] --> GAP["GDP not released<br/>yet this quarter"]
        GAP --> FILL["Use available info<br/>to estimate NOW"]
    end
```

> **Professor:** "Pseudo out-of-sample has to be done fair — no information past your cutoff date."

## The Big Ideas

### 1. The loss function determines what "optimal" means
Under quadratic loss, the optimal forecast is the conditional mean (what OLS gives you). Under absolute loss, it's the median. Under asymmetric loss, the optimal forecast is deliberately biased. **You must choose your loss function before you can say what the "best" forecast is.**

### 2. MA models have a hard forecast horizon limit
An MA($q$) can only forecast $q$ steps ahead. After that, the best forecast is the unconditional mean $\mu$. This is the practical reason ARMA and AR models dominate in applied forecasting.

### 3. AR models forecast recursively — quality decays but never hits a wall
For AR(1): $\hat{y}_{T+h,T} = \phi^h y_T$. Since $|\phi| < 1$ (stationarity), the forecast decays exponentially toward the mean. Unlike MA, there's no hard cutoff — just gradual loss of predictive power.

### 4. ARMA combines the best of both worlds
- At short horizons ($h \leq q$): the MA component adds forecasting power from recent shocks
- At longer horizons ($h > q$): the AR component keeps forecasting recursively
- This is why ARMA is the preferred specification for applied forecasting

### 5. Forecasts are always smoother than reality
$\text{Var}(y_{T+h}) = \text{Var}(\hat{y}_{T+h,T}) + \text{Var}(e_{T+h,T})$ — the forecast variance is strictly less than the data variance. When you plot forecast vs. actual, the forecast line will always be less volatile. **This is not a bug — it's a mathematical property of optimal forecasts.**

### 6. The forecasting workflow is: estimate → write model → think about what you know
> **Pesavento:** "Spend all the time you have to get the best model you can. Then write it down and think about what happens in the future."

The mechanical process: write out $y_{T+h}$ from the model, replace future $\varepsilon$ with 0, replace future $y$ with forecasts, keep everything observed.

### 7. Parameter estimation uncertainty is typically ignored in forecast intervals
The exact forecast error includes terms like $(\theta - \hat{\theta})\varepsilon_T$. In practice, we approximate by assuming estimated = true parameters. This underestimates the true forecast uncertainty slightly, but the approximation is standard.

### 8. Pseudo out-of-sample testing is how you validate before the future arrives
You pretend you're at time $T$, forecast $h$ steps ahead using only data through $T$, then compare to the actual realization (which you already have). **The key requirement is fairness — no peeking at future data.**

## Formulas to Know

1. **Forecast error:** $e_{T+h,T} = y_{T+h} - \hat{y}_{T+h,T}$
2. **Quadratic loss:** $L(e) = e^2$ → optimal = $E(y \mid \Omega_T)$
3. **Absolute loss:** $L(e) = |e|$ → optimal = median$(y \mid \Omega_T)$
4. **Linlin loss:** $L(e) = a|e|$ ($e>0$), $b|e|$ ($e \leq 0$) → quantile $d = b/(a+b)$
5. **MA($q$) forecast ($h \leq q$):** $\hat{y}_{T+h,T} = \theta_h \varepsilon_T + \theta_{h+1}\varepsilon_{T-1} + \ldots + \theta_q \varepsilon_{T-q+h}$
6. **MA($q$) forecast ($h > q$):** $\hat{y}_{T+h,T} = \mu$
7. **MA($q$) error variance ($h \leq q$):** $\sigma_h^2 = (1 + \theta_1^2 + \ldots + \theta_{h-1}^2)\sigma^2$
8. **AR(1) forecast:** $\hat{y}_{T+h,T} = \phi^h y_T$
9. **ARMA(1,1) 1-step:** $\hat{y}_{T+1,T} = \phi y_T + \theta \varepsilon_T$
10. **ARMA recursive ($h > q$):** $\hat{y}_{T+h,T} = \phi \hat{y}_{T+h-1,T}$
11. **Variance decomposition:** $\text{Var}(y_{T+h}) = \text{Var}(\hat{y}_{T+h,T}) + \text{Var}(e_{T+h,T})$
12. **95% interval:** $\hat{y}_{T+h,T} \pm 1.96\sigma_h$
13. **Density forecast:** $N(\hat{y}_{T+h,T}, \sigma_h^2)$
14. **Trend forecast:** $\hat{y}_{T+h,T} = \hat{\beta}_0 + \hat{\beta}_1(T+h)$
15. **ARMA(1,1) 2-step error variance:** $\sigma_2^2 = \sigma^2(1 + (\phi + \theta)^2)$

## Common Exam Traps

- **Trap:** Forgetting to replace future $\varepsilon$ with zero. Any white noise shock in the future CANNOT be forecast — your best guess is always zero (its mean).

- **Trap:** Thinking MA(2) can forecast 3+ steps ahead. After $q$ steps, the MA($q$) forecast is just $\mu$. The forecast error at $h > q$ is the process itself — you've lost all predictive power.

- **Trap:** Forgetting the recursive substitution for AR. For $h = 2$: $\hat{y}_{T+2,T} = \phi \hat{y}_{T+1,T}$ (NOT $\phi y_{T+1}$, because you don't observe $y_{T+1}$). You must substitute your forecast, not the unknown true value.

- **Trap:** Being alarmed that forecast doesn't match actual data. $\text{Var}(y) > \text{Var}(\hat{y})$ is a mathematical identity for optimal forecasts. The forecast will ALWAYS be smoother.

- **Trap:** Confusing out-of-sample with pseudo out-of-sample. True out-of-sample = forecasting into the unknown future. Pseudo = pretending you don't know data you already have, to test your model.

- **Trap:** Thinking optimal forecast is always unbiased. Under quadratic loss, yes — the conditional mean is unbiased. Under asymmetric loss, the optimal forecast is deliberately biased to avoid errors on the costlier side.

- **Trap:** Ignoring parameter estimation uncertainty. The forecast error $e_{T+2,T} = \varepsilon_{T+2} + \theta_1\varepsilon_{T+1} + (\theta_2 - \hat{\theta}_2)\varepsilon_T$. We approximate by dropping the last term, but this underestimates true forecast uncertainty.

- **Trap:** Not knowing the forecast error structure grows with horizon. At $h=1$: error is WN ($\sigma^2$). At $h=2$: error is MA(1) ($\sigma^2(1 + \theta_1^2)$). Variance grows with horizon until it reaches $\text{Var}(y_t)$.

## Connections to the Climate-Risk-Loans Project

This lecture is directly relevant to Phase 2 modeling:

1. **AR baseline models** (from empirical analysis notebook): We estimated AR(12) for BUSLOANS and AR(4) for CONSUMER — the recursive forecast formula $\hat{y}_{T+h,T} = \hat{\phi} \hat{y}_{T+h-1,T}$ is how we'll generate baseline loan growth forecasts.

2. **Loss function choice**: BofA cares about scenario ranges (best/worst case), not just point forecasts. This maps to interval/density forecasts, and potentially asymmetric loss if downside risk matters more.

3. **Pseudo out-of-sample validation**: The professor's framework for fair testing is exactly what we need — train on pre-2020 data, forecast 2020-2025, compare to actuals.

4. **Forecast variance inequality**: When we present forecast plots to BofA, the forecast will be smoother than actual loan data. We should explain this, not apologize for it.

5. **Thursday preview**: Forecast evaluation methods are coming — this will give us the tools (RMSE, Diebold-Mariano test) to compare our AR baseline against VAR/ADL models.
