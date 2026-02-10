# Week 3: Key Concepts - Univariate Time Series Introduction

## Concept Map

```mermaid
graph TD
    A[Time Series Foundations] --> B[Transformations]
    A --> C[Lag Operator L]
    A --> D[Dependence Concepts]
    A --> E[Measuring Dependence]
    A --> F[Stationarity]
    A --> G[Ergodic Theorem]
    A --> H[Wold Theorem]

    B --> B1[Log transform]
    B --> B2["First difference: Δy_t = y_t - y_{t-1}"]
    B --> B3["Growth rates ≈ log differences"]

    C --> C1["Polynomials a(L)"]
    C --> C2["Inversion (requires |ρ| < 1)"]
    C --> C3["Δ = (1 - L)"]

    D --> D1["Uncorrelated (White Noise)"]
    D --> D2["MDS (no nonlinear predictability)"]
    D --> D3[Independent]
    D1 -->|weaker than| D2
    D2 -->|weaker than| D3

    E --> E1["Autocovariance γ(k)"]
    E --> E2["ACF ρ(s) = γ(s)/γ(0)"]
    E --> E3["PACF p(s)"]
    E --> E4["Correlogram + Box-Pierce test"]

    F --> F1["Strong: entire distribution time-invariant"]
    F --> F2["Weak: mean & covariance time-invariant"]
    F --> F3["Non-stationary: breaks, random walks"]
    F2 -->|what we use| F2

    G --> G1["Time averages → population moments"]

    H --> H1["Stationary process = infinite MA"]
    H1 --> H2["Approximate with finite ARMA"]
```

## Dependence Hierarchy

```mermaid
graph LR
    WN["White Noise<br/>(uncorrelated)"] -->|"stronger"| MDS["Martingale Difference<br/>Sequence"]
    MDS -->|"stronger"| IND["Independent<br/>White Noise"]

    style WN fill:#e8f5e9
    style MDS fill:#fff3e0
    style IND fill:#e3f2fd
```

| | White Noise | MDS | Independent |
|---|---|---|---|
| E(e_t) = 0 | Yes | Yes | Yes |
| E(e_t e_s) = 0 | Yes | Yes | Yes |
| E(e_t \| past) = 0 | Not required | **Yes** | Yes |
| E(e_t² \| past) = σ² | Not required | Not required | **Yes** |
| Correlation = 0 implies... | uncorrelated | unpredictable (in mean) | nothing to do with each other |

## Stationarity Decision Flow

```mermaid
flowchart TD
    Q1{"Is E(y_t) = μ<br/>constant over time?"} -->|No| NS1[Non-stationary<br/>e.g. structural break]
    Q1 -->|Yes| Q2{"Is Var(y_t) = σ²<br/>constant over time?"}
    Q2 -->|No| NS2[Non-stationary<br/>e.g. random walk]
    Q2 -->|Yes| Q3{"Does Cov(y_t, y_{t-s})<br/>depend only on s,<br/>not on t?"}
    Q3 -->|No| NS3[Non-stationary]
    Q3 -->|Yes| WS[Weakly Stationary]
    WS --> Q4{"Is the entire joint<br/>distribution time-invariant?"}
    Q4 -->|Yes| SS[Strongly Stationary]
    Q4 -->|No| WS2[Only weakly stationary]

    style NS1 fill:#ffcdd2
    style NS2 fill:#ffcdd2
    style NS3 fill:#ffcdd2
    style WS fill:#c8e6c9
    style SS fill:#a5d6a7
    style WS2 fill:#c8e6c9
```

## From Theory to Practice

```mermaid
flowchart LR
    WT["Wold Theorem<br/>Any stationary process<br/>= infinite MA"] --> PROBLEM["Problem: can't estimate<br/>infinite parameters"]
    PROBLEM --> SOLUTION["Solution: approximate<br/>with finite-order<br/>AR, MA, or ARMA"]
    SOLUTION --> ID["Identify model order<br/>using ACF & PACF patterns"]
    ID --> EST["Estimate parameters"]
    EST --> DIAG["Check residuals<br/>= white noise?"]
    DIAG -->|Yes| FORECAST["Forecast"]
    DIAG -->|No| SOLUTION

    style WT fill:#e3f2fd
    style SOLUTION fill:#c8e6c9
    style FORECAST fill:#a5d6a7
```

## The Big Ideas

### 1. Dependence is what makes time series special
Cross-sectional data assumes independence between observations. Time series data has inherent temporal dependence. The entire course is about modeling this dependence structure.

### 2. Stationarity = stability over time
We need the data-generating process to be stable so that what we learn from the past applies to the future. Weak stationarity (constant mean, time-invariant covariance structure) is the practical requirement.

### 3. ACF and PACF are the primary diagnostic tools
- **ACF** shows total correlation at each lag
- **PACF** shows correlation at each lag after controlling for intermediate lags
- Together they identify which model fits the data (AR, MA, ARMA)
- This will be the main identification strategy going forward

### 4. White noise is the building block and the diagnostic target
- All models (AR, MA, ARMA) are functions of white noise
- If your model is correct, residuals should be white noise
- Best forecast of WN = 0 (its mean)

### 5. Correlation ≠ Independence
From class annotations: "Correlation only has to do with a linear relationship. This situation [corr=0 implies independence] is true only when we have normality." This is crucial for understanding the WN vs MDS vs independence hierarchy.

### 6. The Wold Theorem bridges theory and practice
Any stationary process has an infinite MA representation. We can't estimate infinite parameters, but we can approximate with finite-order ARMA models. This is the theoretical justification for everything that follows in the course.

## Formulas to Memorize

1. **Lag operator:** $Ly_t = y_{t-1}$, $(1-L)y_t = \Delta y_t$
2. **Lag polynomial inversion:** $(1-\rho L)^{-1} = \sum_{i=0}^{\infty} \rho^i L^i$ when $|\rho| < 1$
3. **ACF:** $\rho(s) = \gamma(s)/\gamma(0)$
4. **Sample ACF distribution:** $\hat{\rho}(s) \sim N(0, 1/T)$ under WN null
5. **Box-Pierce:** $Q_{BP} = T \sum_{s=1}^{m} \hat{\rho}^2(s) \sim \chi^2(m)$
6. **Wold:** $Y_t = \sum_{j=0}^{\infty} \psi_j \varepsilon_{t-j} + k_t$

## Common Exam Traps

- **Trap:** Assuming uncorrelated implies independent. It doesn't, unless Gaussian.
- **Trap:** Confusing ACF with PACF. ACF = simple correlation at lag s. PACF = partial correlation controlling for lags 1 through s-1.
- **Trap:** Forgetting that stationarity requires BOTH constant mean AND time-invariant covariance structure.
- **Trap:** Random walk has constant mean ($E[y_t] = E[\beta + e_t] = \beta$) but growing variance, so it's still non-stationary.
- **Trap:** The Wold theorem applies only to covariance-stationary processes.
