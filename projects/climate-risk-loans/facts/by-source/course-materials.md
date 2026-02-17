# Facts Extracted from Course Materials (Weeks 3, 4, 5 Lecture Summaries)

**Source documents**:
- `/workspaces/forecasting-problemset0/course-materials/lectures/week-03/summary.md`
- `/workspaces/forecasting-problemset0/course-materials/lectures/week-04/summary.md`
- `/workspaces/forecasting-problemset0/course-materials/lectures/week-05/summary.md`

---

## From Week 3: Univariate Time Series Introduction

### Fact 1
- **Claim**: A time series y_t is a process observed sequentially over time; univariate if m=1, multivariate if m>1. Observations close in time are expected to be dependent, which distinguishes time series econometrics from cross-sectional analysis and requires different distributional theory.
- **Source**: week-03/summary.md, Section 1 (Time Series Definition)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 2
- **Claim**: Common transformations before time series analysis include: first difference (Delta y_t = y_t - y_{t-1}), second difference (acceleration), year-on-year change, and growth rate (approximately log(y_t) - log(y_{t-1})). Log transformations flatten exponential growth.
- **Source**: week-03/summary.md, Section 2 (Differences and Growth Rates)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 3
- **Claim**: White noise is the building block for AR and MA models: a sequence with E(e_t) = 0, E(e_t * e_s) = 0 for t != s, and E(e_t^2) = sigma^2. The best forecast of a white noise process is zero (its mean). Correlation = 0 does NOT imply independence; the equivalence holds only under normality.
- **Source**: week-03/summary.md, Section 4 (White Noise)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 4
- **Claim**: The Autocorrelation Function (ACF) rho(s) = gamma(s)/gamma(0) measures normalized dependence at lag s, where gamma(s) is the autocovariance. The sample ACF has distribution approximately N(0, 1/T). The Box-Pierce Q-statistic Q_BP = T * sum(rho_hat^2(s)) provides a joint test for white noise.
- **Source**: week-03/summary.md, Section 7 (ACF)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 5
- **Claim**: The Partial Autocorrelation Function (PACF) measures correlation at lag s after controlling for intermediate lags. ACF and PACF together are the main tools for identifying time series models. ACF captures total correlation; PACF captures partial correlation analogous to multiple regression coefficients.
- **Source**: week-03/summary.md, Section 8 (PACF)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 6
- **Claim**: Weak (covariance) stationarity requires E(y_t) = mu and cov(y_t, y_{t-s}) = gamma_s to not depend on t. This is what is used in practice. Non-stationary examples include structural breaks (mean changes) and random walks (variance grows with time).
- **Source**: week-03/summary.md, Section 9 (Stationarity)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 7
- **Claim**: A covariance stationary process is ergodic for the mean if the time average converges in probability to the population mean. Sufficient condition: autocovariances decay fast enough (sum of |gamma_j| < infinity). Ergodicity justifies using time averages to estimate population moments.
- **Source**: week-03/summary.md, Section 10 (Ergodic Theorem)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 8
- **Claim**: The Wold Representation Theorem states that any zero-mean covariance-stationary process can be written as an infinite MA representation plus a deterministic component. In practice, this is approximated with finite-order ARMA models.
- **Source**: week-03/summary.md, Section 11 (Wold Representation Theorem)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 9
- **Claim**: Models for cycles include AR (current value depends on past values), MA (current value depends on past shocks), ARMA (combination), and White Noise (no dependence). White noise has ACF/PACF that are 1 at lag 0 and 0 everywhere else.
- **Source**: week-03/summary.md, Section 12 (Models for Cycles)
- **Confidence**: high
- **Relevant to**: Q5

---

## From Week 4: Cycles Modeling, Structural vs Time Series Models & ARMA Models

### Fact 10
- **Claim**: Cycles capture dynamics not explained by trend and seasonality, including persistence and momentum. The economy is subject to shocks that persist over time -- good years follow good years, bad follow bad.
- **Source**: week-04/summary.md, Section 1 (Cycles Definition)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 11
- **Claim**: High autocorrelation indicates strong cyclical behavior. Example: Log GDP has rho(1) = 0.991, extremely persistent. After taking log differences (GDP growth), rho(1) drops to 0.261 -- much less persistent but still statistically significant and worth modeling.
- **Source**: week-04/summary.md, Section 2 (Autocorrelation as Evidence of Cycles)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 12
- **Claim**: Most time series need at least an AR(1) and often not more than AR(2). Adding AR lags may make other coefficients insignificant due to multicollinearity. R-squared increases significantly when AR terms are added. "AR terms are your best friends when it comes to forecasting."
- **Source**: week-04/summary.md, Section 3 (Modeling Cycles in Practice)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 13
- **Claim**: Stationarity is a prerequisite for modeling cycles: we can only model cycles if the data is stationary. If the underlying probabilistic structure were changing over time, there would be no way to relate the future to the past. We cannot forecast a structural break, but we can model it and forecast the detrended data.
- **Source**: week-04/summary.md, Section 4 (Stationarity as Prerequisite)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 14
- **Claim**: There is a critical distinction between structural models (causal interpretation, requiring exogenous regressors) and time series models (forecasting, where endogeneity does not ruin forecasts). Biased coefficients can still produce good predictions. For forecasting, causal identification is not required.
- **Source**: week-04/summary.md, Section 5 (Structural vs Time Series Models)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 15
- **Claim**: For forecasting purposes, even a biased regression that captures the correlation structure can produce good predictions. The key quote: "If we only care about forecasting prices and/or quantities, then we could just regress q on p or vice-versa and get good forecasts even if we can't exactly estimate the demand function."
- **Source**: week-04/summary.md, Section 5 (Key takeaway from annotation)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 16
- **Claim**: MA (Moving Average) processes are always stationary regardless of parameter values because they are finite sums of white noise. MA(1) has ACF that cuts off after lag 1 (gamma(k) = 0 for k >= 2). The number of nonzero autocorrelations equals the MA order.
- **Source**: week-04/summary.md, Section 8 (MA Models)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 17
- **Claim**: AR(1) model y_t = c + rho * y_{t-1} + epsilon_t is stationary if |rho| < 1. The ACF decays geometrically: rho(s) = rho^s. The parameter rho is the dynamic multiplier -- it determines how much of today's shock persists into the future. rho = 0.5 means shock dies quickly; rho = 0.9 means very persistent (15-20 quarters); rho = 1 means permanent (unit root); rho > 1 means explosive.
- **Source**: week-04/summary.md, Sections 9 and 9a (AR Models and Impulse Response)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 18
- **Claim**: ACF/PACF identification patterns: AR(p) has decaying ACF and PACF that cuts off after lag p. MA(q) has ACF that cuts off after lag q and decaying PACF. ARMA(p,q) has both ACF and PACF decaying. This is the key diagnostic tool for model selection.
- **Source**: week-04/summary.md, Section 10 (ACF/PACF Identification Patterns)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 19
- **Claim**: If rho = 1 (unit root), the variance becomes infinite, the process is a random walk (non-stationary), all theoretical results break down, and the usual normal distribution does not apply. Testing for unit root is equivalent to testing for stationarity and is traditionally the first step in time series analysis.
- **Source**: week-04/summary.md, Section 11 (Unit Root and Stationarity Conditions)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 20
- **Claim**: Pesavento's practical model selection recipe (Box-Jenkins approach): (1) Make data stationary, (2) Plot the correlogram, (3) Use ACF/PACF as starting point, (4) Start LARGE and eliminate small (never start small and add), (5) Estimate and check significance, (6) Compare with information criteria (AIC/BIC -- smaller is better), (7) Plot correlogram of residuals to check for remaining serial correlation, (8) Iterate until no exploitable pattern remains.
- **Source**: week-04/summary.md, Section 14 (Estimation: Practical Recipe)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 21
- **Claim**: AR models are estimated by ordinary OLS, while MA models require nonlinear maximum likelihood estimation. In practice, AR is preferred because it is easy to interpret and easy to forecast with.
- **Source**: week-04/summary.md, Section 15 (AR/MA Interchangeability) and Section 14
- **Confidence**: high
- **Relevant to**: Q5

### Fact 22
- **Claim**: Near-cancellation is a practical trap in ARMA models: when AR and MA coefficients are similar in magnitude but opposite in sign, they cancel each other out. Example: GDP growth ARMA(1,1) estimated rho ~= 0.3, theta ~= -0.3, both insignificant together but each significant alone. This is analogous to multicollinearity. Lesson: never eliminate both AR and MA simultaneously.
- **Source**: week-04/summary.md, Section 16 (Near-Cancellation Problem)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 23
- **Claim**: Information criteria (AIC/BIC) are used to compare models when significance tests are ambiguous. AIC values for MA(2) vs AR(3) on the same data were 1401 vs 1402 -- nearly identical, demonstrating that different model specifications can explain the same data equally well.
- **Source**: week-04/summary.md, Section 15 and Example 7
- **Confidence**: high
- **Relevant to**: Q5

### Fact 24
- **Claim**: Real-world model selection example with unemployment rate data (monthly, 2000-2024, includes COVID spike, from FRED): AR(1) rho_hat = 0.95 (very persistent). Model selection process led to AR(3) as the best specification. The process involved checking residual correlograms at each step.
- **Source**: week-04/summary.md, Example 8 (Unemployment Rate)
- **Confidence**: high
- **Relevant to**: Q3, Q5

### Fact 25
- **Claim**: Pesavento's priorities for time series modeling: (1) rho = 1 (unit root) is THE critical boundary, (2) start large and eliminate small, (3) AR models are almost always enough, (4) always plot residual correlograms, (5) use AIC/BIC for comparison, (6) AR and MA are interchangeable, (7) watch for near-cancellation in ARMA, (8) understand the math for intuition, not memorization.
- **Source**: week-04/summary.md, "Pesavento's Priorities" section
- **Confidence**: high
- **Relevant to**: Q5

---

## From Week 5: Dynamic Causal Effects

### Fact 26
- **Claim**: A dynamic causal effect measures the effect on Y of a change in X over time -- not just the immediate impact but the response at 1, 2, ..., k periods into the future. Examples include the effect of Fed Funds rate changes on inflation over months and years.
- **Source**: week-05/summary.md, Section 1 (Dynamic Causal Effects)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 27
- **Claim**: The distributed lag model regresses Y_t on current and lagged values of X_t: Y_t = beta_0 + beta_1 * X_t + beta_2 * X_{t-1} + ... + beta_{r+1} * X_{t-r} + u_t. Coefficients represent the impact effect (beta_1), dynamic multipliers (beta_2, beta_3, ...), and cumulative dynamic multipliers (sums of coefficients).
- **Source**: week-05/summary.md, Section 4 (Distributed Lag Model)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 28
- **Claim**: For distributed lag models, the exogeneity condition E(u_t | X_t, X_{t-1}, ...) = 0 is required for causal interpretation. Strict exogeneity (conditioning on future X values too) is stronger but rarely plausible due to feedback effects. If X is exogenous, OLS estimates the dynamic causal effect.
- **Source**: week-05/summary.md, Section 6 (Exogeneity in Time Series)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 29
- **Claim**: The Federal Funds rate is NOT exogenous when studying its effect on GDP growth because the Fed reacts to GDP (simultaneous causality). The unemployment rate is NOT exogenous for inflation due to the Phillips curve (simultaneous causality). These are key examples of endogeneity in macroeconomic time series.
- **Source**: week-05/summary.md, Section 6 (Exogeneity examples)
- **Confidence**: high
- **Relevant to**: Q2, Q3

### Fact 30
- **Claim**: The distributed lag model requires four assumptions: (1) X is exogenous, (2a) Y and X have stationary distributions, (2b) (Y_t, X_t) and (Y_{t-j}, X_{t-j}) become independent as j gets large, (3) Y and X have eight nonzero finite moments (needed for HAC estimators), and (4) no perfect multicollinearity.
- **Source**: week-05/summary.md, Section 7 (Distributed Lag Model Assumptions)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 31
- **Claim**: Conventional OLS standard errors fail in time series when errors are serially correlated. The variance formula has an additional correction factor f_T = 1 + 2 * sum of weighted autocorrelations, which can be large. Ignoring this gives wrong standard errors.
- **Source**: week-05/summary.md, Section 8 (Why Conventional OLS SEs Fail)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 32
- **Claim**: HAC (Heteroskedasticity and Autocorrelation-Consistent) standard errors, specifically the Newey-West estimator, correct for serial correlation in errors. The truncation parameter m (number of autocorrelation lags to include) can be chosen using the rule of thumb m = 0.75 * T^(1/3). The professor recommends always using HAC standard errors as a default unless absolutely certain errors are not serially correlated.
- **Source**: week-05/summary.md, Section 9 (HAC Standard Errors)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 33
- **Claim**: HAC standard errors are needed for distributed lag regressions but usually unnecessary for AR and ADL (Autoregressive Distributed Lag) models if enough lags of Y are included, because the errors become serially uncorrelated with sufficient autoregressive terms.
- **Source**: week-05/summary.md, Section 9 (Key practical point)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 34
- **Claim**: The dynamic multiplier shows the effect on Delta Y_t (changes), while the cumulative multiplier shows the effect on Y_t (levels). This distinction is critical for interpretation: the dynamic effect may fade quickly while the level effect persists much longer.
- **Source**: week-05/summary.md, Section 11 (OJ Price Data) and recording notes
- **Confidence**: high
- **Relevant to**: Q5, Q7

### Fact 35
- **Claim**: Subsample instability was observed in the OJ data: the dynamic effect of freezes changed significantly over time (much larger impact in 1950-1966 than in 1984-2000), suggesting the stationarity assumption may be violated. This is relevant to the general concern about parameter stability over long time horizons.
- **Source**: week-05/summary.md, Section 11 and Example 3
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 36
- **Claim**: In multivariate analysis, 68% confidence intervals are common because "there's so much uncertainty," as opposed to the standard 95% confidence intervals. This reflects the general challenge of uncertainty quantification in time series econometrics.
- **Source**: week-05/summary.md, recording notes on interpreting multiplier graphics
- **Confidence**: medium
- **Relevant to**: Q5, Q7

### Fact 37
- **Claim**: Researchers construct exogenous variation when raw X is endogenous by isolating truly exogenous events: for oil prices, changes due to Middle East wars; for monetary policy, high-frequency market surprises around Fed announcements; for government spending, war-related spending changes. Propensity score and conditioning on covariates from microeconometrics can also apply.
- **Source**: week-05/summary.md, Section 6 (recording notes on creating exogenous measures)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 38
- **Claim**: The course previews VAR (Vector Autoregression) models as "the same autoregressive model but in vector form, multivariate at the same time," where exogeneity questions become even more important. This is directly relevant to modeling climate-macro-loan relationships with multiple interacting variables.
- **Source**: week-05/summary.md, Connections section
- **Confidence**: high
- **Relevant to**: Q5

### Fact 39
- **Claim**: The stationarity assumption in time series has two practical implications: (2a) coefficients don't change within sample (internal validity) and results extrapolate outside sample (external validity); (2b) widely separated time periods act as separate experiments, enabling a version of the Central Limit Theorem.
- **Source**: week-05/summary.md, Section 7 (Stationarity interpretation)
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 40
- **Claim**: The lag operator L is fundamental notation for time series models: L^k * y_t = y_{t-k}. Lag polynomials a(L) enable compact representation of AR, MA, and ARMA models. Inversion (1 - rho*L)^{-1} = sum(rho^i * L^i) is valid if |rho| < 1, connecting AR and MA representations.
- **Source**: week-03/summary.md, Section 3 (Lag Operator)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 41
- **Claim**: ARMA(p,q) models combine AR and MA components: phi(L) * y_t = c + theta(L) * epsilon_t. Stationarity is determined by the AR part (roots of phi(z) outside unit circle); invertibility is determined by the MA part (|theta| < 1). Both ACF and PACF decay for ARMA models.
- **Source**: week-04/summary.md, Section 12 (ARMA Models)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 42
- **Claim**: GDP measured quarterly (s=4) and stock prices measured daily (s=252) are standard time series frequencies. The course uses real FRED data throughout examples, including unemployment rate (monthly, 2000-2024), GDP growth (quarterly, 1990-2024), and inflation rate.
- **Source**: week-03/summary.md, Section 1 and week-04/summary.md, Examples 8-10
- **Confidence**: high
- **Relevant to**: Q4

### Fact 43
- **Claim**: The Autoregressive Distributed Lag (ADL) model is mentioned as a more efficient estimator when strict exogeneity holds, combining lagged dependent variables with lagged independent variables. This is a potential framework for modeling loan portfolio dynamics with macroeconomic drivers.
- **Source**: week-05/summary.md, Section 10 (Estimation with Strictly Exogenous Regressors)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 44
- **Claim**: Endogeneity affects causal interpretation but NOT forecast quality. This is a major conceptual distinction: for the climate-loans project, even if the relationship between macro variables and loans involves simultaneity, the forecasting goal means standard regression approaches can still work.
- **Source**: week-04/summary.md, Section 7 (Exogeneity and Causal Interpretation)
- **Confidence**: high
- **Relevant to**: Q2, Q5

### Fact 45
- **Claim**: The structural break concept is directly relevant to climate modeling: non-constant mean violates weak stationarity (example: y_t = beta + e_t for t <= k, y_t = beta + lambda + e_t for t > k). We cannot forecast a structural break, but we can model it and forecast the detrended data.
- **Source**: week-03/summary.md, Example 2 and week-04/summary.md, Section 4
- **Confidence**: high
- **Relevant to**: Q4, Q5

### Fact 46
- **Claim**: The impulse response function framework from AR models (shock of 1 at time t, then tracking the response rho, rho^2, rho^3, ...) provides a template for understanding how climate shocks propagate through the economy to loan portfolios over time.
- **Source**: week-04/summary.md, Section 9a (Impulse Response / Dynamic Multiplier)
- **Confidence**: medium
- **Relevant to**: Q2, Q5

### Fact 47
- **Claim**: When choosing the number of lags for distributed lag models, the specification choice matters: include lags and stop when they are no longer significant. The Goldilocks method or information criteria can help determine the right number. For a series with T=612 observations, r=18 lags was used in the textbook example.
- **Source**: week-05/summary.md, Section 11 (recording notes on lag selection)
- **Confidence**: high
- **Relevant to**: Q5

### Fact 48
- **Claim**: The distinction between structural econometric models (estimating specific parameters like price elasticity) and time series forecasting models (predicting future values) is described as "a major conceptual distinction for the course" by Professor Pesavento. For the climate-loans project, the forecasting framing means we do not need to identify the exact causal mechanism, only the predictive relationship.
- **Source**: week-04/summary.md, Section 5 (Structural vs Time Series Models)
- **Confidence**: high
- **Relevant to**: Q2, Q5
