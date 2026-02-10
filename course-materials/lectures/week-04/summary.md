# Week 4: Cycles Modeling, Structural vs Time Series Models & ARMA Models

## Main Topic
Understanding cyclical dynamics in time series, the role of autocorrelation in detecting persistence, why stationarity is a prerequisite for modeling cycles, the critical distinction between structural econometric models (causality) and pure time series models (forecasting), and the formal properties and identification of AR, MA, and ARMA models.

## Key Concepts

### 1. Cycles Definition
**Definition:** Cycles capture any dynamics not explained by trend and seasonality. This includes persistence, momentum, and any way the present is linked to the past or future.
**Intuition:** The economy is subject to shocks that persist over time. Good years tend to follow good years, bad follow bad. Eventually something unusual happens (end of recession, start of boom). Think of technology shocks slowly diffusing across sectors.
**Example:** GDP growth, inflation rates, business cycles.

### 2. Autocorrelation as Evidence of Cycles
**Definition:** Serial correlation (autocorrelation) is the correlation of a series with its own lagged values. High autocorrelation = strong cyclical behavior.

**Key examples from class:**

| Series | $\rho(1)$ | $\rho(2)$ | Interpretation |
|--------|-----------|-----------|----------------|
| Inflation (Philippines) | 0.983 | 0.952 | Very high persistence (annotation: "very high") |
| Log GDP | 0.991 | 0.982 | Extremely persistent (still 0.82 at lag 20) |
| GDP Growth ($\Delta \log$ GDP) | 0.261 | 0.255 | Much less persistent after differencing, but still significant |
| Change in Inflation | 0.444 | 0.312 | Moderately persistent |

**Key insight:** Taking log differences eliminates much of the persistence (from 0.99 to 0.26), but remaining autocorrelation is still statistically significant and worth modeling.

### 3. Modeling Cycles in Practice
**How:** Include lagged dependent variables as explanatory variables (autoregressive terms).
- AR(1): $y_t = c + \phi y_{t-1} + \varepsilon_t$ — simplest, often sufficient
- AR(2): $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$ — rarely need more than this
- Can also use MA or ARMA models

**Practical notes:**
- Most time series need **at least** an AR(1), often not more than AR(2)
- Adding lags may make other coefficients insignificant (multicollinearity intuition)
- $R^2$ increases significantly when you add AR terms
- "AR terms are your best friends when it comes to forecasting"

### 4. Stationarity as Prerequisite
**Why it matters for cycles:** We can only model cycles if the data is stationary. We observe a finite window of an infinite process — we need the underlying probabilistic structure to be stable over time.
**Key quote:** "If the underlying probabilistic structure of the series were changing over time, we'd be doomed — there would be no way to relate the future to the past."
**Limitation:** We cannot forecast a structural break. We can model it and forecast the detrended data.

### 5. Structural vs Time Series Models
**This is a major conceptual distinction for the course.**

**Structural models** (causal interpretation):
- Goal: estimate specific parameters (e.g., price elasticity of demand)
- Requires: exogenous/predetermined regressors ($E[p|\varepsilon] = 0$)
- Problem: simultaneity bias when both variables are endogenous (supply & demand example)

**Time series models** (forecasting):
- Goal: predict future values
- Do NOT need causal interpretation of coefficients
- Endogeneity doesn't ruin forecasts — biased coefficients can still produce good predictions
- From annotation: "OLS assumes regressor is exogenous... for forecasting, it doesn't matter"

**Key takeaway (from annotation, circled in class):** "If we only care about **forecasting** prices and/or quantities, then we could just regress q on p or vice-versa and get good forecasts even if we can't exactly estimate the demand function."

### 6. Supply/Demand Simultaneity Example
**Setup:** Regress price (p) on quantity (q).
**Problem:** Is the estimated line the demand curve or supply curve?
**Answer (annotation):** "Neither — combination." The estimated slope is a mixture of true supply and demand slopes. There is simultaneity bias.
**But for forecasting:** This doesn't matter! The biased regression still captures the correlation structure needed for prediction.
**From annotation:** "Think about what question you're asking."

### 7. Exogeneity and Causal Interpretation
**Rule:** To interpret coefficients causally (e.g., price elasticity), the RHS variable must be exogenous: $E[p|\varepsilon] = 0$
**Example:** Use weather as an instrument — it's truly exogenous to demand.
**If unsure:** Do NOT give too much weight to estimated elasticities — bias is probably there.
**Bottom line:** Endogeneity affects causal interpretation but NOT forecast quality.

### 8. MA (Moving Average) Models
**Definition:** Current value depends on current and past shocks (not past values of the series itself).
- MA(1): $y_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$
- MA(2): $y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2}$
- MA(q): $y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \ldots + \theta_q \varepsilon_{t-q}$

**From lecture:** "Moving Average is called Moving Average because it's an average of these white noises... The Wold theorem says that any stationary time series can be represented by an infinite sum of white noises. Now I say, I can't estimate an infinite number. What if I stop at a certain point? Is that enough?"

**Key property:** MA processes are **always stationary** regardless of parameter values, because they are finite sums of white noise. From lecture: "The mean is constant. The variance is constant. The autocovariances don't change with time. So a moving average is always stationary."

**MA(1) properties (derived step-by-step in Feb 3 lecture):**
- $E(Y_t) = \mu$ — "The expectation of mu plus zero plus theta times zero. What am I left with? Just the mu."
- $\text{Var}(Y_t) = \sigma^2(1 + \theta^2)$ — Key step: $E[\varepsilon_t^2] = \sigma^2$ because "every time you have something with mean zero, the expectation of the squared is the variance"
- $\gamma(1) = \theta \sigma^2$ — "The only term that survives is when the timing matches"
- $\gamma(k) = 0$ for $k \geq 2$ — "All the products of things that are not the same timing go to zero"
- $\rho(1) = \theta / (1 + \theta^2)$

**Why MA ACF cuts off (from lecture):** "If I have MA(2), gamma(2) is not zero because I have one term that is the same timing. But gamma(3)? Now I have epsilon t, epsilon t-1, epsilon t-2 on one side and epsilon t-3, t-4, t-5 on the other. None of them have the same timing, so it's zero."

### 9. AR (Autoregressive) Models
**Definition:** Current value depends on past values of the series.
- AR(1): $y_t = c + \rho y_{t-1} + \varepsilon_t$, or $(1 - \rho L)y_t = c + \varepsilon_t$
- AR(2): $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$
- AR(p): $\phi(L) y_t = c + \varepsilon_t$ where $\phi(L) = 1 - \phi_1 L - \ldots - \phi_p L^p$

**AR(1) properties (derived via MA(∞) representation in Feb 3 lecture):**
- $E(Y_t) = c / (1 - \rho)$ — requires $|\rho| < 1$; uses $1 + \rho + \rho^2 + \cdots = 1/(1-\rho)$
- $\text{Var}(Y_t) = \sigma^2 / (1 - \rho^2)$ — same infinite sum technique with squared terms
- $\rho(s) = \rho^s$ (ACF decays geometrically)

**AR to MA conversion (key derivation from lecture):** "I substitute $y_{t-1} = \rho y_{t-2} + \varepsilon_{t-1}$ and keep going forever... What is this? It's a moving average of infinite order. I can go from AR(1) to MA(∞)."

If $|\rho| < 1$: $y_t = \frac{c}{1-\rho} + \sum_{j=0}^{\infty} \rho^j \varepsilon_{t-j}$

**From lecture:** "Which one would you rather estimate? One parameter or infinite parameters? ... If they are exactly the same, you may as well estimate this [the AR]."

### 9a. Impulse Response / Dynamic Multiplier (from Feb 5 lecture)
**This is how Pesavento interprets AR(1) economically.**

"Suppose I have a shock today equal to 1, and $y_{t-1} = 0$. What is $y_t$? It's 1. What is $y_{t+1}$? $\rho$. What is $y_{t+2}$? $\rho^2$."

**$\rho$ is the dynamic multiplier:** It tells you how much of today's shock persists into the future.
- $\rho = 0.5$: shock dies quickly — "maybe in a year it's going to be irrelevant"
- $\rho = 0.9$: shock very persistent — "going to be like 15-20 quarters before it's irrelevant"
- $\rho = 1$: "the shock is permanent. It never goes away."
- $\rho > 1$: "explosive. We don't believe many macro variables are actually explosive."

**On bubbles (from lecture):** "When you think about housing bubbles, financial bubbles — that's where you start thinking about situations where things may explode. But we often think about them happening for a short time, and then they pop."

### 10. ACF/PACF Identification Patterns
**This is the key diagnostic tool for model selection.**

| Model | ACF Pattern | PACF Pattern |
|-------|-------------|--------------|
| AR(p) | Decays (exponential or oscillating) | Cuts off after lag p |
| MA(q) | Cuts off after lag q | Decays (exponential or oscillating) |
| ARMA(p,q) | Decays | Decays |

**Critical distinction:** "Cuts off" means drops to zero sharply at a specific lag. "Decays" means gradually diminishes toward zero.

### 11. Unit Root and Stationarity Conditions
**Pesavento's emphasis: "We're going to spend a whole module just on this."**

**AR(1) stationarity:** Requires $|\rho| < 1$. If $\rho = 1$ (unit root):
- Variance becomes infinite: $\text{Var}(Y_t) = \sigma^2 / (1 - 1) \to \infty$
- Process is a random walk — non-stationary
- All theoretical results break down
- "The usual [normal] distribution does not apply, and everything is much more complicated. We're going to have to use different distributions, different tables."

**From lecture:** "Is rho equal to one or less than one? We never think about rho being bigger than one. But is that coefficient less than one? Because being less than one is the key component for being stationary."

**Why $\rho = 1$ matters so much (from lecture):**
- "I cannot construct sensible forecasts, especially in the long run"
- "When rho is equal to one, it's called a unit root model... there are millions of papers on this"
- "If you ask Python — even Claude, when I asked it — one of the first things it does is test for a unit root. Because it's very traditional."
- Testing for unit root = testing for stationarity. This will be a full module later.

**AR(2) stationarity:** Factor $\phi(L) = (1 - \lambda_1 L)(1 - \lambda_2 L)$. Stationarity requires both roots of the characteristic polynomial to lie **outside the unit circle** (equivalently, $|\lambda_1| < 1$ and $|\lambda_2| < 1$).

**From lecture:** "Now instead of having one value that needs to be less than one, I have two values that need to be less than one. It's more complicated because $\rho$ is not actually the root itself — the root is $1/\rho$. So you'll see the statement 'the roots are outside the unit circle,' which is doubly confusing because we're talking about bigger than one."

**General AR(p):** All roots of $\phi(z) = 0$ must lie outside the unit circle.

### 12. ARMA(p,q) Models
**Definition:** $\phi(L) y_t = c + \theta(L) \varepsilon_t$, combining AR and MA components.
- ARMA(1,1): $y_t = c + \phi y_{t-1} + \varepsilon_t + \theta \varepsilon_{t-1}$
- Both ACF and PACF decay — neither cuts off cleanly
- Stationarity determined by the AR part; invertibility determined by the MA part

**ARMA to MA representation:** Any stationary ARMA can be written as $y_t = \mu + \psi(L)\varepsilon_t$ where $\psi(L) = \theta(L)/\phi(L)$. This connects back to the Wold theorem.

### 13. Invertibility
**Definition:** An MA process is invertible if it can be written as an AR($\infty$) process.
- MA(1) invertible if $|\theta| < 1$: $(1 + \theta L)^{-1} y_t = \varepsilon_t$
- Ensures unique mapping between ACF and model parameters
- Required for well-defined forecasting

**Why it matters:** Without invertibility, two different MA parameter values produce the same ACF — the model is not identified. Convention: always choose the invertible representation.

### 14. Estimation: Pesavento's Practical Recipe (from Feb 5 lecture)
**Box-Jenkins approach:** "Gave rise in the 90s to an iterated approach... not used that much anymore per se, but I still teach it because it's very useful to have this idea."

**Pesavento's step-by-step recipe:**
1. **Make data stationary:** Remove trend and seasonality first. "Take the residuals from that regression — that's your deseasonalized data."
2. **Plot the correlogram:** "If the correlogram is completely flat, you're done. It's going to be unlikely for any macro variable, except maybe financial returns."
3. **Use ACF/PACF as starting point:** Determine if AR, MA, or ARMA. "Using what we learned about how the correlogram should give you a starting point."
4. **Start LARGE, eliminate small (key emphasis):** "The ideal way to go is from large to small, rather than small to large. Always add a few extra lags if you're unsure, and then eliminate."
5. **Estimate and check significance:** Drop insignificant terms.
6. **Compare with information criteria:** "If it's marginally significant, what do you do? Here's where the information criteria comes to help. Remember, the smaller the better."
7. **Plot correlogram of residuals:** "The most important thing is: if you compute the autocorrelation function of the residuals, you should quickly be able to see whether you still have serial correlation."
8. **Iterate:** "Stop when you think you've exploited anything that there is to exploit."

**Modern approach (from lecture):** "The more modern way is we just do a bunch of regressions, look at information criteria, look at key statistics... put all of this in a holistic way."

**On estimation method (from lecture):** "AR is estimated by simply ordinary OLS. To estimate MA, you need nonlinear maximization of the likelihood. Python does it super fast, but it can take longer."

### 15. AR/MA Mathematical Interchangeability (from Feb 5 lecture)
**Key insight Pesavento emphasizes:** AR and MA representations are mathematically equivalent.

"Whether you go autoregressive or moving average, you and I may end up with something mathematically identical, and therefore nobody says that we will end up in the same place, but they both explain the same amount."

**Example from class:** An MA(2) data set was also well-approximated by AR(3). The AIC values were nearly identical (1401 vs 1402). "I started one way. You started another way. We end up with slightly different models. You can use the information criteria to tell you which is better."

**Why AR is preferred in practice (from lecture):**
- "People don't tend to like moving average more... because AR is easy to interpret, easy to forecast with"
- AR estimation is just OLS; MA requires nonlinear MLE
- "This [AR] is estimated by simply ordinary OLS"

### 16. Near-Cancellation Problem (from Feb 5 lecture — GDP growth example)
**Critical practical warning from Pesavento:**

When AR and MA coefficients are similar in magnitude but opposite in sign, they cancel each other out.

**GDP growth example:** ARMA(1,1) estimated $\hat{\rho} \approx 0.3$ and $\hat{\theta} \approx -0.3$. "This is $(1 - 0.3L)y_t = (1 - 0.3L)\varepsilon_t$. This cancels out! I can divide everything by $(1 - 0.3L)$, and I get $y_t = \varepsilon_t$."

**From lecture:** "When these two are so similar, things go crazy. They cancel each other out. But if I only give them one of them... the other one becomes very significant. It's almost like having close multicollinearity in the linear regression."

**Lesson:** "Just because both were not significant together doesn't mean that taken singularly they are not significant. Always be careful about eliminating two variables at the same time."

## Important Formulas

| Formula | Expression | When to Use |
|---------|-----------|-------------|
| AR(1) | $y_t = c + \phi y_{t-1} + \varepsilon_t$ | Simplest cycle model |
| AR(2) | $y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \varepsilon_t$ | When AR(1) is insufficient |
| MA(1) | $y_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$ | Short-memory shock process |
| MA(q) | $y_t = \mu + \theta(L) \varepsilon_t$ | ACF cuts off at lag q |
| ARMA(p,q) | $\phi(L) y_t = c + \theta(L) \varepsilon_t$ | Both ACF and PACF decay |
| AR(1) mean | $E(Y_t) = c/(1 - \rho)$ | Requires $\|\rho\| < 1$ |
| AR(1) variance | $\text{Var}(Y_t) = \sigma^2/(1 - \rho^2)$ | Requires $\|\rho\| < 1$ |
| AR(1) ACF | $\rho(s) = \rho^s$ | Geometric decay |
| MA(1) variance | $\text{Var}(Y_t) = \sigma^2(1 + \theta^2)$ | Always stationary |
| MA(1) ACF at lag 1 | $\rho(1) = \theta/(1 + \theta^2)$ | Only nonzero autocorrelation |
| AR to MA | $y_t = c/(1-\rho) + \sum \rho^j \varepsilon_{t-j}$ | Converting representations |
| Invertibility | $(1 + \theta L)^{-1}$ exists if $\|\theta\| < 1$ | MA to AR conversion |
| Exogeneity condition | $E[p \| \varepsilon] = 0$ | Required for causal interpretation |
| Autocorrelation | $\rho(s) = \gamma(s)/\gamma(0)$ | Measuring persistence/cycles |

## Examples from Class

### Example 1: Inflation Rate (Philippines)
- **Setup:** Monthly inflation rate 1955–2024
- **Key finding:** $\rho(1) = 0.983$ — extremely persistent
- **Takeaway:** Last month's inflation is highly informative about this month. Change in inflation rate is less persistent ($\rho(1) = 0.44$).

### Example 2: Log GDP vs GDP Growth
- **Setup:** Compare autocorrelation of log GDP (levels) vs first difference (growth)
- **Key finding:** Log GDP has $\rho(1) = 0.991$; GDP growth has $\rho(1) = 0.261$
- **Takeaway:** Differencing removes trend-driven persistence, but residual autocorrelation from cyclical dynamics remains significant.

### Example 3: Supply/Demand Simultaneity
- **Setup:** Price-quantity scatter plot, regress p on q
- **Key finding:** Estimated slope is neither demand nor supply, but a combination
- **Annotation:** "OLS assumes regressor is exogenous... for forecasting, it doesn't matter"
- **Takeaway:** Forecasting doesn't require causal identification; structural interpretation does.

### Example 4: AR(1) Persistence / Impulse Response (from Feb 5 lecture)
- **Setup:** Compare AR(1) with $\phi = 0.5$, $\phi = 0.7$, $\phi = 0.9$
- **From lecture:** Pesavento showed simulated data for each. "This is $\rho = 0.5$. This is $\rho = 0.7$... I add a little bit more persistence and look at how it changed. And if I do $0.9$, look at the data itself — the swings are much more obvious. The cycle is much more persistent."
- **Impulse response thought experiment:** Shock of 1 at time $t$, then $\varepsilon = 0$ after. Response: $\rho, \rho^2, \rho^3, \ldots$
- **Takeaway:** $\rho$ IS the dynamic multiplier. Higher $\rho$ = shocks linger longer.

### Example 5: MA(1) Properties Derivation (full walkthrough, Feb 3 lecture)
- **Setup:** Derive mean, variance, and autocovariances of MA(1): $y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}$
- **Key finding:** $\gamma(1) = \theta\sigma^2$, but $\gamma(k) = 0$ for all $k \geq 2$
- **From lecture on the key step:** "Every time I have an expectation of a product and the two things have a different timing, that's going to be zero if this is a white noise."
- **Takeaway:** Sharp ACF cutoff = signature of MA model. Number of nonzero autocorrelations = order.

### Example 6: Simulated AR(2) Identification (from Feb 5 lecture)
- **Setup:** Pesavento generated AR(2) data, showed students the correlogram
- **Key observation:** "If you plot the residuals like this, your eyes will tell you this is random. This is where the autocorrelation functions come into play."
- **Process:** Started with AR(1) → coefficient significant but residuals still showed correlation. Then AR(2) → both significant, residuals clean. AR(3) → third lag not significant → stop.
- **From lecture:** "I would always suggest you go from big to small. If in doubt, start at two or maybe three, find that the last one was not significant, and then go down."

### Example 7: MA(2) vs AR(3) — Model Equivalence (from Feb 5 lecture)
- **Setup:** Same MA(2) simulated data, but estimated as AR instead
- **Key finding:** AR(3) gave AIC = 1402; MA(2) gave AIC = 1401. Nearly identical.
- **From lecture:** "I started one way. You started another way. We end up with slightly different models. Which one is better? The information criteria tells you."
- **Takeaway:** AR and MA are mathematically interchangeable. Different starting points can give equivalent models.

### Example 8: Unemployment Rate — Real Data (from Feb 5 lecture)
- **Setup:** Monthly unemployment 2000–2024 (includes COVID spike). Downloaded from FRED live in class.
- **Key finding:** $\hat{\rho}_1 = 0.95$ — "Unemployment is very, very persistent."
- **Model selection process:** AR(1) → significant. AR(2) → second lag barely significant. Added MA → didn't help. AR(3) → all significant. AR(4) → fourth lag not significant → stop at AR(3).
- **From lecture:** "I highly recommend that you do the correlogram of the residuals for that last step."
- **Takeaway:** Real data is messy. Start with AR(1), build up, check residuals. Unemployment needs ~AR(3).

### Example 9: GDP Growth — Near-Cancellation (from Feb 5 lecture)
- **Setup:** Quarterly GDP growth 1990–2024 (post-Great Moderation, includes COVID)
- **Key finding:** ARMA(1,1) estimated $\hat{\rho} \approx 0.3$, $\hat{\theta} \approx -0.3$ — both insignificant together because they cancel!
- **Resolution:** Drop to AR(1) alone → significant. "The moment I took one out, this one became significant."
- **From lecture:** "This is exactly what happens. When these two are so similar, things go crazy. They cancel each other out. It's almost like close multicollinearity."
- **Takeaway:** Near-cancellation is a real trap. Don't eliminate both AR and MA simultaneously.

### Example 10: Inflation Rate — Model Selection (from Feb 5 lecture)
- **Setup:** Inflation rate with 2% target line plotted
- **Key finding:** Correlogram showed persistent autocorrelation. AR(3) was a good starting point.
- **From lecture:** "Most things, almost everything, needs at least one lag. So at least AR(1), maybe sometimes more than one. Occasionally you will need a moving average in there, one, maybe."
- **Observation:** Adding MA to the inflation model made other coefficients unstable — "the extra moving average part was making everything else not significant"
- **Takeaway:** AR is the workhorse. MA additions can destabilize when not warranted.

## Pesavento's Priorities (from transcripts)

Based on what she spent the most time on, returned to repeatedly, and explicitly flagged:

1. **$\rho = 1$ (unit root) is THE critical boundary.** She says "we're going to spend a whole module just on this" and keeps returning to what happens when $\rho = 1$ vs $\rho < 1$. This will be a major topic later.
2. **Start large, eliminate small.** She explicitly says this is the correct approach to model selection, and demonstrates it multiple times.
3. **AR models are almost always enough.** "Most things, almost everything, needs at least one lag. So at least AR(1), maybe sometimes more. Occasionally you will need a moving average, one, maybe."
4. **Always plot the residual correlogram.** This is her single most important diagnostic. She repeats it in every real data example.
5. **Information criteria (AIC/BIC) for comparison.** When significance tests are ambiguous, AIC/BIC break the tie.
6. **AR and MA are interchangeable.** She demonstrates this mathematically and empirically. Don't get hung up on choosing one — they can represent the same thing.
7. **Watch for near-cancellation in ARMA.** The GDP growth example is a cautionary tale she clearly wants students to remember.
8. **The math matters for understanding, not memorization.** "You don't have to necessarily be able to replicate all of it" but "the math is important to understand where they come from."

## Connections
- **Builds on:** Week 3 concepts of ACF, PACF, stationarity, white noise, Wold theorem
- **Related to:** Problem Set 1, Question 3 (testing for serial correlation in BTC returns)
- **Prerequisite for:** Unit root testing module (Pesavento flagged this repeatedly), Week 5+ forecasting, information criteria
- **Practical skill:** The unemployment/GDP/inflation examples from Feb 5 are a template for how to approach any time series

## Questions to Consider
1. Why does differencing log GDP reduce autocorrelation so dramatically (0.99 → 0.26)?
2. If a regression coefficient is biased due to endogeneity, why can it still produce good forecasts?
3. When would you choose AR(2) over AR(1)? How would you decide?
4. Why can't we forecast a structural break? What can we do instead?
5. In your own work, when do you need causal interpretation vs just forecasting?
6. Why are MA processes always stationary but AR processes are not?
7. Given an ACF that cuts off after lag 2 and a PACF that decays, what model would you fit?
8. Why does invertibility matter for MA models? What goes wrong without it?
9. For an AR(1) with $\phi = 0.95$, how many periods until a shock decays to less than 10% of its original size?
10. Why does the ARMA-to-MA conversion (Wold representation) only work for stationary ARMA models?
11. In the GDP growth example, why did ARMA(1,1) fail but AR(1) succeed? What caused the near-cancellation?
12. If you're given a correlogram of residuals that still shows significant autocorrelation at lag 3, what would you do?
13. Pesavento says "start large, eliminate small." Why is this better than starting with AR(1) and adding lags?

## Review Checklist
- [ ] Understand what "cycles" capture (dynamics beyond trend and seasonality)
- [ ] Can interpret autocorrelation tables and explain persistence
- [ ] Know why differencing reduces persistence
- [ ] Understand why stationarity is required before modeling cycles
- [ ] Can articulate the difference between structural and time series models
- [ ] Understand the supply/demand simultaneity example
- [ ] Know when endogeneity matters (causal inference) vs when it doesn't (forecasting)
- [ ] Can explain why AR terms are the "best friends" for forecasting
- [ ] Can derive mean, variance, and ACF for MA(1) and AR(1)
- [ ] Know the ACF/PACF identification patterns for AR, MA, and ARMA
- [ ] Understand stationarity conditions for AR (roots outside unit circle)
- [ ] Understand invertibility conditions for MA ($|\theta| < 1$)
- [ ] **Key:** Can explain what happens at the unit root ($\phi = 1$) — variance, forecasting, distributions
- [ ] Know the Box-Jenkins estimation procedure (identify → estimate → diagnose → forecast)
- [ ] Can convert AR(1) to MA($\infty$) representation
- [ ] **Key:** Know Pesavento's practical recipe: start large, eliminate, check residual correlogram, compare AIC/BIC
- [ ] Understand the impulse response / dynamic multiplier interpretation of $\rho$
- [ ] Understand near-cancellation in ARMA models (GDP growth example)
- [ ] Know that AR is estimated by OLS but MA requires nonlinear MLE
- [ ] Can walk through model selection on real data (unemployment, GDP, inflation examples)
