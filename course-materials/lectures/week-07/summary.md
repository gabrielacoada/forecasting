# Week 7: MIDAS — Mixed Data Sampling for Time Series Analysis

## The Problem MIDAS Solves

Economic variables come at different frequencies: GDP is quarterly, CPI is monthly, stock returns and interest rates are daily. Traditional approaches all have drawbacks:
- **Aggregation** (average daily to quarterly): loses within-period dynamics, treats all days equally
- **Interpolation** (create fake daily GDP): creates spurious patterns
- **Skip-sampling** (use only last observation): discards 99% of data

MIDAS uses **all** the high-frequency data directly to predict the low-frequency outcome, without forcing them to the same frequency. Developed by Ghysels, Santa-Clara, and Valkanov (2004).

## The Model

**General form:** `y_t = B0 + B1 * SUM(w(k; theta) * x_{t-k/m}) + e_t`

- `y_t` = low-frequency variable (e.g., annual loan growth)
- `x_{t-k/m}` = high-frequency variable (e.g., monthly unemployment) at lag k
- `m` = number of high-frequency periods per low-frequency period (e.g., 12 months per year)
- `w(k; theta)` = **weights** that sum to 1, controlled by just 2-3 parameters theta

The key trick: instead of estimating a separate coefficient for each lag (which would require 12 or 65 parameters), MIDAS specifies a smooth **weighting function** controlled by only 2 hyperparameters. This is what makes it parsimonious.

## Two Weighting Schemes

### 1. Exponential Almon (most popular, Ghysels et al. 2007)

`w(k; theta1, theta2) = exp(theta1*k + theta2*k^2) / SUM(exp(theta1*j + theta2*j^2))`

- theta1 < 0: weights decline with lag (recent data matters most)
- theta2 < 0: hump-shaped (middle lags peak)
- theta2 = 0: pure exponential decay
- theta1, theta2 > 0: weights increase with lag

### 2. Beta Weighting

`w(k; theta1, theta2) = (k/K)^(theta1-1) * (1-k/K)^(theta2-1) / SUM(...)`

- Weights automatically stay in [0,1]
- Very flexible shapes
- Well-understood statistical properties

## Estimation

Estimated via **Nonlinear Least Squares (NLS)** because theta enters the weight function nonlinearly. Steps:
1. Choose weighting scheme (Exponential Almon or Beta)
2. Choose maximum lag K (trade-off: more lags vs. parameter uncertainty)
3. Set starting values (important for convergence)
4. Optimize via NLS to find B0, B1, theta
5. Compute robust/HAC standard errors

## Interpreting Parameters

- **B1 (slope coefficient):** overall effect of the high-frequency variable on the low-frequency outcome. If B1 > 0, higher stock returns predict higher GDP growth. Magnitude shows economic significance.
- **theta (hyperparameters):** shape of the lag structure. theta1 < 0 means recent observations matter more. theta2 < 0 means middle-of-period observations peak in importance.

**Example:** With estimated theta1 = -0.05, theta2 = -0.001, the weights on daily stock returns for predicting quarterly GDP are: yesterday = 0.025, 1 week ago = 0.020, 1 month ago = 0.012, 2 months ago = 0.005. Recent returns are weighted most heavily.

## Advantages

1. **Information preservation** — uses all available high-frequency data
2. **Flexible dynamics** — captures complex lag structures
3. **Nowcasting capability** — can update forecasts as new high-frequency data arrives
4. **No artificial data** — no interpolation or arbitrary aggregation
5. **Parsimonious** — few parameters despite many lags

## Limitations

1. Must choose weighting scheme — results can be sensitive to this choice
2. Nonlinear optimization can be slow and have convergence issues
3. Assumes weight pattern is stable over time — may not hold during structural breaks

## Extensions

- **U-MIDAS** (Unrestricted MIDAS): uses regularization (ridge, LASSO) instead of parametric weights. More flexible but less parsimonious (Foroni et al. 2015).
- **ADL-MIDAS**: Autoregressive Distributed Lag — includes lags of the dependent variable
- **Multi-frequency MIDAS**: combine daily, weekly, and monthly predictors simultaneously
- **Nonlinear MIDAS**: threshold effects, time-varying parameters

## Applications in Practice

- GDP nowcasting (the Fed's GDPNow model is MIDAS-type)
- Inflation forecasting with commodity prices
- Volatility prediction using high-frequency returns
- Central bank policy analysis
- Macroeconomic surveillance

## Relevance to Climate Risk Project

Directly applicable to our frequency mismatch: annual NGFS scenarios + monthly FRED loan/macro data. Instead of aggregating monthly loans to annual (losing dynamics) or interpolating NGFS to monthly (creating fake data), MIDAS could use monthly data directly. The ADL-MIDAS variant (with lagged dependent variable) would be closest to our current VAR approach but without forcing frequency alignment.
