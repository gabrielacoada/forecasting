# MA Autocovariance: The Complete Guide

**What this is**: A from-scratch explanation of everything you need to understand and compute MA autocovariances. This is the #1 most tested hand-calculation topic on Professor Pesavento's exams. It appeared on all three old finals.

**How to use this**: Read Parts 1-4 slowly the first time (60-90 min). On exam morning, skip to the Cheat Sheet at the end (5 min refresher).

---

## Lecture Reference Guide

Use these file paths to review the original source material:

| Topic | File Path | What's There |
|-------|-----------|-------------|
| **White noise definition & properties** | `course-materials/lectures/week-03/summary.md` (lines 42-62) | Formal definitions of γ(k), ρ(s), sample ACF distribution |
| **Wold Representation Theorem** | `course-materials/lectures/week-03/summary.md` (lines 78-82) | Statement: any stationary process = infinite MA |
| **MA(1) step-by-step derivation** | `course-materials/lectures/week-04/recordings/arma-feb-3-recording.txt` (middle section, ~500+ lines in) | Pesavento's full live walkthrough of E[y_t], Var(y_t), γ(1), and why cross terms vanish |
| **MA(2) cutoff explanation** | `course-materials/lectures/week-04/recordings/arma-feb-3-recording.txt` (after MA(1) derivation) | "Now I have epsilon t, t-1, t-2 on one side and t-3, t-4, t-5 on the other" |
| **MA properties summary** | `course-materials/lectures/week-04/summary.md` (lines 73-91) | Clean formulas for MA(1): mean, variance, γ(1), ρ(1) |
| **ACF/PACF identification table** | `course-materials/lectures/week-04/summary.md` (lines 122-131) | AR: ACF decays, PACF cuts off. MA: ACF cuts off, PACF decays |
| **ACF/PACF identification table (extended)** | `course-materials/lectures/week-04/key-concepts.md` (lines 113-119) | Includes memory duration column |
| **AR to MA conversion** | `course-materials/lectures/week-04/recordings/arma-feb-5-recording.txt` | "I substitute y_{t-1} = rho*y_{t-2} + epsilon and keep going forever" |
| **Near-cancellation warning** | `course-materials/lectures/week-04/summary.md` (lines 201-211) | GDP growth ARMA(1,1) example where ρ≈0.3 and θ≈-0.3 cancel |
| **Common exam traps** | `course-materials/lectures/week-04/key-concepts.md` (lines 245-277) | "Saying MA processes can be non-stationary" and invertibility warning |
| **MA forecasting horizon limit** | `course-materials/lectures/week-06/key-concepts.md` (lines 77-115) | MA(q) can only forecast q steps; includes MA(2) worked example |
| **PS2 Q1 proof framework** | `problem-sets/problem-set-2/context-brief.md` (lines 11-28) | "The proof should show: (1) substitute, (2) eliminate, (3) verify MA(1) structure, (4) Wold" |
| **PS2 Q1 full solution** | `problem-sets/problem-set-2/hwk2_analysis.ipynb` (cell `34d0052b`) | Complete analytical proof with all 4 steps |
| **Old Exam 1, Q2** | `exams/past-exams/422oldfinal2.pdf` (page 3) | MA(2) with θ₁=0.3, θ₂=0.7: compute Var, γ, ρ |
| **Old Exam 3, Q3a** | `exams/past-exams/422Final02.pdf` (page 8) | Var for MA(2) with θ₁=0.8, θ₂=0.2 |
| **Old Exam 3, Q3b** | `exams/past-exams/422Final02.pdf` (page 8) | Full γ and ρ for MA(1) with θ=0.8 |

---

## Part 1: The Building Blocks (Start Here)

Before you can understand MA autocovariance, you need three things nailed down: what a time series model is trying to do, what white noise is, and what autocovariance measures.

### 1.1 What Are We Doing in This Course?

In economics, we observe variables over time: GDP each quarter, inflation each month, stock prices each day. These aren't random — today's GDP is related to yesterday's. The economy has **momentum**. Good quarters tend to follow good quarters. Bad follows bad.

The goal of this course is to build mathematical models that capture this momentum, so we can **forecast** future values.

Professor Pesavento makes a critical distinction: we don't need to understand **why** GDP grows (that's causal econometrics). We just need to capture **the pattern** well enough to predict what comes next. As she says (Week 4, `week-04/summary.md` line 58):

> "If we only care about **forecasting** prices and/or quantities, then we could just regress q on p or vice-versa and get good forecasts even if we can't exactly estimate the demand function."

The two main families of models we use are **AR** (autoregressive — today depends on yesterday's VALUE) and **MA** (moving average — today depends on yesterday's SHOCKS). Both capture momentum. Both can produce good forecasts. They're mathematically interchangeable (the Wold theorem guarantees this).

### 1.2 What is White Noise?

White noise is the **foundation** of everything in time series. It represents the unpredictable, random part of a variable — the "shocks" or "surprises" that no model can forecast.

We write it as $\varepsilon_t$ (epsilon subscript t), and it has three defining properties:

**Property 1: Mean zero**
$$E[\varepsilon_t] = 0 \quad \text{for all } t$$

On average, shocks are neither positive nor negative. Sometimes good news, sometimes bad, but it averages out.

**Property 2: Constant variance**
$$E[\varepsilon_t^2] = \sigma^2 \quad \text{for all } t$$

Every shock has the same "size" on average. The variability doesn't change over time. (This $\sigma^2$ is just a number — think of it as measuring how volatile the shocks are.)

**Why does $E[\varepsilon_t^2] = \sigma^2$?** This is a stats fact Pesavento emphasizes (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt`):

> "Remember that the variance can always be written as $E[\varepsilon_t^2] - (E[\varepsilon_t])^2$. Now what is $E[\varepsilon_t]$? Zero. So $\varepsilon_t^2$ is equal to the variance. Every time you have something with mean zero, the expectation of the squared is the variance."

So when we see $E[\varepsilon_t^2]$ in a derivation, we can immediately replace it with $\sigma^2$.

**Property 3: Uncorrelated across time** (THE key property)
$$E[\varepsilon_t \cdot \varepsilon_s] = 0 \quad \text{whenever } t \neq s$$

Today's shock tells you **nothing** about tomorrow's shock. They're completely unrelated. This is Pesavento's "different timing" rule (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt`):

> "Every time I have an expectation of a product and the two things have a different timing, that's going to be zero if this is a white noise."

This single sentence is the engine that drives every MA autocovariance derivation. If you understand nothing else, understand this: **when you multiply two epsilon terms with different time subscripts and take the expectation, you get zero.**

**Combining Properties 2 and 3 into one rule:**

$$E[\varepsilon_i \cdot \varepsilon_j] = \begin{cases} \sigma^2 & \text{if } i = j \quad \text{(same time period)} \\ 0 & \text{if } i \neq j \quad \text{(different time periods)} \end{cases}$$

This is the **only rule** you need to compute any MA autocovariance. Everything else follows from multiplying things out and applying this rule.

### 1.3 What is a Moving Average Process?

An **MA(q) process** says: today's value of $y_t$ is a weighted combination of the current shock and the q most recent past shocks.

**MA(1)** — today depends on this period's shock and last period's:
$$y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}$$

**MA(2)** — today depends on this period's shock and the last two:
$$y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2}$$

**MA(q)** — general form:
$$y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2} + \cdots + \theta_q\varepsilon_{t-q}$$

**What $\mu$ is**: The long-run average of the series. It's just a constant. When we compute autocovariances, we subtract $\mu$ from everything, so it drops out immediately.

**What $\theta$ is**: The weight on the past shock. If $\theta_1 = 0.5$, then last period's surprise carries over at half strength into today's value.

**What the "1" in front of $\varepsilon_t$ is**: Notice there's no $\theta$ on $\varepsilon_t$ itself — the coefficient is implicitly **1**. Today's shock hits with full force. This is easy to forget and it matters.

**Economic intuition**: Think about a one-time policy announcement (a shock). In an MA(1) world, it affects the economy this quarter (full force: coefficient 1) and next quarter (partial force: coefficient $\theta$), then it's gone. In an MA(2) world, it lingers for two additional quarters. The $\theta$ values tell you how much of the shock carries over.

Pesavento explains why this connects to the Wold theorem (Week 4 Feb 3 lecture; theorem stated in `week-03/summary.md` lines 78-82):

> "The Wold theorem says that any stationary time series can be represented by an infinite sum of white noises. Now I say, I can't estimate an infinite number. What if I stop at a certain point? Is that enough? Hopefully, if the correlations decay fast enough, I can stop at a finite number."

So an MA(q) is a **practical approximation**: we stop the infinite MA representation after q terms and hope that's enough.

### 1.4 What is Autocovariance?

Autocovariance $\gamma(h)$ measures **how related today's value is to the value h periods ago**.

**Definition:**
$$\gamma(h) = \text{Cov}(y_t, y_{t-h}) = E[(y_t - \mu)(y_{t-h} - \mu)]$$

In words: subtract the mean from both observations, multiply them, and take the average.

**Special case — h = 0:**
$$\gamma(0) = E[(y_t - \mu)^2] = \text{Var}(y_t)$$

When h = 0, autocovariance is just the **variance**.

**What it tells you economically:**
- $\gamma(h) > 0$: When the series is above average today, it tends to be above average h periods later too. **Positive momentum.**
- $\gamma(h) < 0$: Above average today, below average h periods later. **Mean reversion.**
- $\gamma(h) = 0$: Today's value tells you nothing about the value h periods from now. **No memory at lag h.**

**Autocorrelation $\rho(h)$** is just the normalized version:
$$\rho(h) = \frac{\gamma(h)}{\gamma(0)}$$

This rescales to $[-1, 1]$ so you can compare across different series. The ACF (Autocorrelation Function) is the plot of $\rho(h)$ for h = 1, 2, 3, ...

### 1.5 Why MA Autocovariance Matters

The autocovariance function is the **fingerprint** of a time series process. If you know $\gamma(0), \gamma(1), \gamma(2), \ldots$, you know everything about the process's linear structure.

For MA processes specifically, the autocovariance has a distinctive pattern: **it cuts off to zero after lag q.** This is the key to identification:

> Pesavento: "If I see an autocorrelation that looks like that, where I have a couple of points that are big and then it dropped to zero, I know that this is probably a moving average model. Which order? Potentially I can look at how many of them are different than zero."

So computing autocovariances isn't just a math exercise — it's how you figure out what model to use.

---

## Part 2: The Derivation Method (The Core Skill)

This is the actual hand-calculation skill you need for the exam. There are three types of calculations: γ(0) (variance), γ(h) for h within the MA order (nonzero autocovariance), and γ(h) for h beyond the order (zero — the cutoff).

### 2.1 Computing γ(0): The Variance

**Goal**: Find $\gamma(0) = \text{Var}(y_t) = E[(y_t - \mu)^2]$

**Step 1**: Write out $y_t - \mu$. The $\mu$ subtracts away, leaving just the epsilon terms.

For MA(2): $y_t - \mu = \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2}$

**Step 2**: Square it. You're computing $(a + b + c)^2$.

Remember from algebra: $(a + b + c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$

So:
$$(\varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2})^2 = \varepsilon_t^2 + \theta_1^2\varepsilon_{t-1}^2 + \theta_2^2\varepsilon_{t-2}^2 + 2\theta_1\varepsilon_t\varepsilon_{t-1} + 2\theta_2\varepsilon_t\varepsilon_{t-2} + 2\theta_1\theta_2\varepsilon_{t-1}\varepsilon_{t-2}$$

**Step 3**: Take the expectation of each term using the white noise rule.

The **squared terms** (same index):
- $E[\varepsilon_t^2] = \sigma^2$
- $E[\theta_1^2\varepsilon_{t-1}^2] = \theta_1^2\sigma^2$
- $E[\theta_2^2\varepsilon_{t-2}^2] = \theta_2^2\sigma^2$

The **cross terms** (different indices) — ALL ZERO:
- $E[2\theta_1\varepsilon_t\varepsilon_{t-1}] = 0$ because $t \neq t-1$
- $E[2\theta_2\varepsilon_t\varepsilon_{t-2}] = 0$ because $t \neq t-2$
- $E[2\theta_1\theta_2\varepsilon_{t-1}\varepsilon_{t-2}] = 0$ because $t-1 \neq t-2$

Pesavento walks through this exact reasoning (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt` — the full MA(1) derivation section):

> "I have $E[\varepsilon_t^2]$ plus $\theta^2 E[\varepsilon_{t-1}^2]$ plus $2\theta E[\varepsilon_t \varepsilon_{t-1}]$... Now what is this? Because $\varepsilon_t$ is a white noise, what does it mean? That $\varepsilon_t$ is uncorrelated with $\varepsilon_{t-1}$, so this is equal to zero. So you have that the variance of $y_t$ is $(1 + \theta^2)\sigma^2$."

**Result**:
$$\gamma(0) = (1 + \theta_1^2 + \theta_2^2)\sigma^2$$

**The shortcut you should use on the exam**: Don't even bother writing out cross terms. Just **square each coefficient and add them up, then multiply by $\sigma^2$**. The cross terms always die.

$$\boxed{\gamma(0) = \left(\text{sum of squared coefficients}\right) \times \sigma^2}$$

The coefficients are: 1 (on $\varepsilon_t$), $\theta_1$ (on $\varepsilon_{t-1}$), $\theta_2$ (on $\varepsilon_{t-2}$), etc.

So: $\gamma(0) = (1^2 + \theta_1^2 + \theta_2^2 + \cdots + \theta_q^2)\sigma^2$

### 2.2 Computing γ(h) for h within the MA order: The Matching Game

**Goal**: Find $\gamma(h) = E[(y_t - \mu)(y_{t-h} - \mu)]$ for $1 \leq h \leq q$.

This is where students lose points. The method is simple but you must be systematic.

**Step 1**: Write out $y_t - \mu$ as a list of epsilon terms with their coefficients.

**Step 2**: Write out $y_{t-h} - \mu$ as a list of epsilon terms with their coefficients.

**Step 3**: Play the matching game. Go through every possible pair (one from each list). Ask: do these two epsilon terms have the **same time subscript**?
- If YES: that pair contributes (coefficient 1) $\times$ (coefficient 2) $\times$ $\sigma^2$
- If NO: that pair contributes **zero**

**Step 4**: Add up all the surviving (matched) contributions.

**Why this works**: When you multiply $(y_t - \mu)(y_{t-h} - \mu)$ and take the expectation, you get a sum of terms like $E[\theta_i\varepsilon_{t-i} \cdot \theta_j\varepsilon_{t-h-j}]$. This equals $\theta_i\theta_j E[\varepsilon_{t-i}\varepsilon_{t-h-j}]$. By the white noise rule, this is $\theta_i\theta_j\sigma^2$ if $t-i = t-h-j$ (i.e., $i = h+j$), and zero otherwise.

Let me show this with a concrete example. For **MA(2) computing γ(1)**:

$y_t - \mu$:
| Term # | Coefficient | Epsilon |
|--------|------------|---------|
| 1 | 1 | $\varepsilon_t$ |
| 2 | $\theta_1$ | $\varepsilon_{t-1}$ |
| 3 | $\theta_2$ | $\varepsilon_{t-2}$ |

$y_{t-1} - \mu$:
| Term # | Coefficient | Epsilon |
|--------|------------|---------|
| A | 1 | $\varepsilon_{t-1}$ |
| B | $\theta_1$ | $\varepsilon_{t-2}$ |
| C | $\theta_2$ | $\varepsilon_{t-3}$ |

Now check every pair:

| Pair | $y_t$ epsilon | $y_{t-1}$ epsilon | Same subscript? | Contribution |
|------|-------------|----------------|-----------------|-------------|
| 1-A | $\varepsilon_t$ | $\varepsilon_{t-1}$ | NO (t vs t-1) | 0 |
| 1-B | $\varepsilon_t$ | $\varepsilon_{t-2}$ | NO (t vs t-2) | 0 |
| 1-C | $\varepsilon_t$ | $\varepsilon_{t-3}$ | NO (t vs t-3) | 0 |
| **2-A** | $\varepsilon_{t-1}$ | $\varepsilon_{t-1}$ | **YES!** | $\theta_1 \times 1 \times \sigma^2 = \theta_1\sigma^2$ |
| 2-B | $\varepsilon_{t-1}$ | $\varepsilon_{t-2}$ | NO (t-1 vs t-2) | 0 |
| 2-C | $\varepsilon_{t-1}$ | $\varepsilon_{t-3}$ | NO (t-1 vs t-3) | 0 |
| 3-A | $\varepsilon_{t-2}$ | $\varepsilon_{t-1}$ | NO (t-2 vs t-1) | 0 |
| **3-B** | $\varepsilon_{t-2}$ | $\varepsilon_{t-2}$ | **YES!** | $\theta_2 \times \theta_1 \times \sigma^2 = \theta_1\theta_2\sigma^2$ |
| 3-C | $\varepsilon_{t-2}$ | $\varepsilon_{t-3}$ | NO (t-2 vs t-3) | 0 |

**Result**: $\gamma(1) = (\theta_1 + \theta_1\theta_2)\sigma^2$

Only 2 out of 9 pairs survived. The rest died because of the "different timing" rule.

### 2.3 The Cutoff: Why γ(h) = 0 for h > q

This is the conceptually most important result. For MA(q), the autocovariance is **exactly zero** at all lags beyond q.

**Why?** Look at what epsilon terms each expression uses:

- $y_t - \mu$ uses: $\varepsilon_t, \varepsilon_{t-1}, \varepsilon_{t-2}, \ldots, \varepsilon_{t-q}$
- $y_{t-h} - \mu$ uses: $\varepsilon_{t-h}, \varepsilon_{t-h-1}, \varepsilon_{t-h-2}, \ldots, \varepsilon_{t-h-q}$

The **most recent** epsilon in $y_{t-h}$ is $\varepsilon_{t-h}$.
The **oldest** epsilon in $y_t$ is $\varepsilon_{t-q}$.

For a match, we'd need $t - h \geq t - q$, which means $h \leq q$.

When $h > q$: the oldest term in $y_t$ ($\varepsilon_{t-q}$) is still more recent than the newest term in $y_{t-h}$ ($\varepsilon_{t-h}$). There is **zero overlap**. Every pair you form has different subscripts. Every expectation is zero.

Pesavento makes this vivid (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt`; summarized in `week-04/summary.md` line 90):

> "If I have MA(2), gamma(2) is not zero because I have one term that is the same timing. But gamma(3)? Now I have epsilon t, epsilon t-1, epsilon t-2 on one side and epsilon t-3, t-4, t-5 on the other. None of them have the same timing, so it's zero."

**This is why the ACF of an MA(q) process cuts off after lag q.** It's not an approximation or an empirical observation — it's an exact mathematical fact. And it's the single most important property for identifying MA models from data.

---

## Part 3: Complete Worked Derivations

### 3.1 MA(1): $y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}$

This is the simplest case. Master this first, then MA(2) is just more terms.

#### γ(0) = Variance

$$y_t - \mu = \varepsilon_t + \theta\varepsilon_{t-1}$$

Coefficients: 1 on $\varepsilon_t$, $\theta$ on $\varepsilon_{t-1}$.

Square and add: $1^2 + \theta^2 = 1 + \theta^2$

$$\boxed{\gamma(0) = (1 + \theta^2)\sigma^2}$$

**Check**: If $\theta = 0$ (no MA component, just white noise), $\gamma(0) = \sigma^2$. Makes sense — variance of WN is $\sigma^2$.

#### γ(1)

Write both expressions:
- $y_t - \mu = \varepsilon_t + \theta\varepsilon_{t-1}$
- $y_{t-1} - \mu = \varepsilon_{t-1} + \theta\varepsilon_{t-2}$

Multiply and take expectation:

$$\gamma(1) = E[(\varepsilon_t + \theta\varepsilon_{t-1})(\varepsilon_{t-1} + \theta\varepsilon_{t-2})]$$

Four terms to check:

| From $y_t$ | From $y_{t-1}$ | Same subscript? | Result |
|-----------|---------------|-----------------|--------|
| $\varepsilon_t$ | $\varepsilon_{t-1}$ | No | 0 |
| $\varepsilon_t$ | $\theta\varepsilon_{t-2}$ | No | 0 |
| $\theta\varepsilon_{t-1}$ | $\varepsilon_{t-1}$ | **Yes** (t-1 = t-1) | $\theta \cdot 1 \cdot \sigma^2$ |
| $\theta\varepsilon_{t-1}$ | $\theta\varepsilon_{t-2}$ | No | 0 |

$$\boxed{\gamma(1) = \theta\sigma^2}$$

**Intuition**: Only the $\varepsilon_{t-1}$ shock appears in both $y_t$ and $y_{t-1}$. It enters $y_t$ with weight $\theta$ and $y_{t-1}$ with weight 1. So the covariance is $\theta \times 1 \times \sigma^2$.

#### γ(2) and beyond

- $y_t - \mu$ uses $\{\varepsilon_t, \varepsilon_{t-1}\}$
- $y_{t-2} - \mu$ uses $\{\varepsilon_{t-2}, \varepsilon_{t-3}\}$

No overlap between $\{t, t-1\}$ and $\{t-2, t-3\}$.

$$\boxed{\gamma(h) = 0 \quad \text{for all } h \geq 2}$$

#### Autocorrelations

$$\rho(1) = \frac{\gamma(1)}{\gamma(0)} = \frac{\theta\sigma^2}{(1+\theta^2)\sigma^2} = \frac{\theta}{1+\theta^2}$$

$$\boxed{\rho(1) = \frac{\theta}{1+\theta^2}}, \qquad \rho(h) = 0 \text{ for } h \geq 2$$

#### The MA(1) Autocorrelation Bound (from PS1 Q1)

An important result: no matter what $\theta$ is, $|\rho(1)| \leq 0.5$.

You can verify this by plugging in: at $\theta = 1$, $\rho(1) = 1/2 = 0.5$. At $\theta = -1$, $\rho(1) = -1/2 = -0.5$. At $\theta = 2$, $\rho(1) = 2/5 = 0.4$ (already smaller). At $\theta = 10$, $\rho(1) = 10/101 \approx 0.1$.

The denominator $(1 + \theta^2)$ grows faster than the numerator $\theta$, so the fraction can never exceed 0.5 in absolute value.

**This is why you'd be surprised if someone told you $y_t$ is MA(1) but $\rho(1) = 0.7$** — it's mathematically impossible.

---

### 3.2 MA(2): $y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2}$

#### γ(0) = Variance

Coefficients: 1, $\theta_1$, $\theta_2$.

Square them: $1, \theta_1^2, \theta_2^2$.

$$\boxed{\gamma(0) = (1 + \theta_1^2 + \theta_2^2)\sigma^2}$$

#### γ(1)

$y_t - \mu$: uses $\varepsilon_t$ (coeff 1), $\varepsilon_{t-1}$ (coeff $\theta_1$), $\varepsilon_{t-2}$ (coeff $\theta_2$)

$y_{t-1} - \mu$: uses $\varepsilon_{t-1}$ (coeff 1), $\varepsilon_{t-2}$ (coeff $\theta_1$), $\varepsilon_{t-3}$ (coeff $\theta_2$)

**Matches**:
- $\varepsilon_{t-1}$ appears in both: $y_t$ has it with coeff $\theta_1$, $y_{t-1}$ has it with coeff 1 → contributes $\theta_1 \cdot 1 \cdot \sigma^2$
- $\varepsilon_{t-2}$ appears in both: $y_t$ has it with coeff $\theta_2$, $y_{t-1}$ has it with coeff $\theta_1$ → contributes $\theta_2 \cdot \theta_1 \cdot \sigma^2$

$$\boxed{\gamma(1) = (\theta_1 + \theta_1\theta_2)\sigma^2 = \theta_1(1 + \theta_2)\sigma^2}$$

**Intuition**: Two shocks ($\varepsilon_{t-1}$ and $\varepsilon_{t-2}$) are shared between $y_t$ and $y_{t-1}$, each contributing to the covariance.

#### γ(2)

$y_t - \mu$: uses $\varepsilon_t$ (coeff 1), $\varepsilon_{t-1}$ (coeff $\theta_1$), $\varepsilon_{t-2}$ (coeff $\theta_2$)

$y_{t-2} - \mu$: uses $\varepsilon_{t-2}$ (coeff 1), $\varepsilon_{t-3}$ (coeff $\theta_1$), $\varepsilon_{t-4}$ (coeff $\theta_2$)

**Matches**:
- $\varepsilon_{t-2}$ appears in both: $y_t$ has it with coeff $\theta_2$, $y_{t-2}$ has it with coeff 1 → contributes $\theta_2 \cdot 1 \cdot \sigma^2$
- No other matches ($\varepsilon_t$ and $\varepsilon_{t-1}$ from $y_t$ don't appear in $y_{t-2}$)

$$\boxed{\gamma(2) = \theta_2\sigma^2}$$

**Intuition**: Only one shock ($\varepsilon_{t-2}$) is shared between observations 2 periods apart. It enters $y_t$ with the last MA coefficient ($\theta_2$) and $y_{t-2}$ with coefficient 1.

#### γ(3) = The Cutoff

$y_t - \mu$: uses $\{\varepsilon_t, \varepsilon_{t-1}, \varepsilon_{t-2}\}$

$y_{t-3} - \mu$: uses $\{\varepsilon_{t-3}, \varepsilon_{t-4}, \varepsilon_{t-5}\}$

Sets $\{t, t-1, t-2\}$ and $\{t-3, t-4, t-5\}$ have **no elements in common**.

$$\boxed{\gamma(3) = 0}$$

And $\gamma(h) = 0$ for all $h \geq 3$.

Pesavento:
> "Now I have epsilon t, epsilon t-1, epsilon t-2 on one side and epsilon t-3, t-4, t-5 on the other. None of them have the same timing, so it's zero."

#### Autocorrelations

$$\rho(1) = \frac{\theta_1 + \theta_1\theta_2}{1 + \theta_1^2 + \theta_2^2}$$

$$\rho(2) = \frac{\theta_2}{1 + \theta_1^2 + \theta_2^2}$$

$$\rho(h) = 0 \quad \text{for } h \geq 3$$

---

### 3.3 Seeing the Pattern: General MA(q)

For $y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \cdots + \theta_q\varepsilon_{t-q}$ (define $\theta_0 = 1$):

**Variance:**
$$\gamma(0) = \sigma^2\sum_{i=0}^{q}\theta_i^2 = (1 + \theta_1^2 + \theta_2^2 + \cdots + \theta_q^2)\sigma^2$$

**Autocovariance at lag h (for $1 \leq h \leq q$):**
$$\gamma(h) = \sigma^2\sum_{i=0}^{q-h}\theta_i\theta_{i+h}$$

In words: slide the two lists of coefficients past each other by h positions and multiply the overlapping pairs.

**Cutoff (for $h > q$):**
$$\gamma(h) = 0$$

**Autocorrelation:**
$$\rho(h) = \gamma(h) / \gamma(0)$$

---

## Part 4: Every Exam and Problem Set Appearance

### Old Final #1 (422 FINAL) — Question 2 [20 points]

**The question**: "You know that $y_t$ is given by the MA(2): $y_t = \varepsilon_t + 0.3\varepsilon_{t-1} + 0.7\varepsilon_{t-2}$. Compute:
(a) (5pts) VAR($y_t$)
(b) (10pts) $\gamma(1), \gamma(2), \gamma(3)$
(c) (5pts) $\rho(1), \rho(2), \rho(3)$"

**Solution** ($\theta_1 = 0.3$, $\theta_2 = 0.7$):

**(a)** $\gamma(0) = (1^2 + 0.3^2 + 0.7^2)\sigma^2 = (1 + 0.09 + 0.49)\sigma^2 = 1.58\sigma^2$

**(b)**
$\gamma(1)$: Two matches between $y_t$ and $y_{t-1}$:
- $\varepsilon_{t-1}$: coefficients $0.3 \times 1 = 0.3$
- $\varepsilon_{t-2}$: coefficients $0.7 \times 0.3 = 0.21$
- $\gamma(1) = (0.3 + 0.21)\sigma^2 = 0.51\sigma^2$

$\gamma(2)$: One match between $y_t$ and $y_{t-2}$:
- $\varepsilon_{t-2}$: coefficients $0.7 \times 1 = 0.7$
- $\gamma(2) = 0.7\sigma^2$

$\gamma(3) = 0$ — MA(2) cutoff. The epsilon sets $\{t, t-1, t-2\}$ and $\{t-3, t-4, t-5\}$ don't overlap.

**(c)**
$\rho(1) = 0.51 / 1.58 = 0.3228$
$\rho(2) = 0.70 / 1.58 = 0.4430$
$\rho(3) = 0$

**Grading notes**: This is 20 points. Show all your work. Write out both epsilon lists explicitly. State the cutoff property and why. Pesavento says "a correct answer with no explanation will NOT give you full credit."

---

### Old Final #3 (Fall 08) — Question 3a [5 points]

**The question**: "Compute VAR($y_t$) where $y_t = \varepsilon_t + 0.8\varepsilon_{t-1} + 0.2\varepsilon_{t-2}$."

**Solution**: $\gamma(0) = (1 + 0.64 + 0.04)\sigma^2 = 1.68\sigma^2$

This is just the variance — the easiest version. Don't forget to square: $0.8^2 = 0.64$, not $0.8$.

---

### Old Final #3 (Fall 08) — Question 3b [10 points]

**The question**: "Compute $\gamma(1), \gamma(2), \rho(1), \rho(2)$ for $y_t = \varepsilon_t + 0.8\varepsilon_{t-1}$."

**Solution** (MA(1), $\theta = 0.8$):

$\gamma(0) = (1 + 0.64)\sigma^2 = 1.64\sigma^2$

$\gamma(1)$: One match — $\varepsilon_{t-1}$ appears in both with coefficients $0.8$ and $1$:
$\gamma(1) = 0.8\sigma^2$

$\gamma(2) = 0$ — MA(1) cutoff at lag 1.

$\rho(1) = 0.8 / 1.64 = 0.4878$

$\rho(2) = 0$

---

### Problem Set 1 — Question 1

**The question**: "Why would you be surprised if I told you that $y_t$ was MA(1) but that corr$(y_t, y_{t-1}) = 0.7$?"

**Solution**: For MA(1), $\rho(1) = \theta / (1 + \theta^2)$. The maximum value of this is 0.5 (achieved at $\theta = 1$). Since 0.7 > 0.5, no MA(1) process can produce this autocorrelation. It's impossible.

To prove the bound: at $\theta = 1$, $\rho = 1/2$. At $\theta = -1$, $\rho = -1/2$. At any other $\theta$, $|\rho| < 0.5$ because $1 + \theta^2$ grows faster than $|\theta|$.

---

### Problem Set 2 — Question 1

**The question**: "Show that $y_t = x_t + e_t$ with $x_t = \alpha x_{t-1} + u_t$ is ARMA(1,1)."

**Where MA autocovariance appears**: You need to prove the composite noise $\eta_t = u_t + e_t - \alpha e_{t-1}$ has **MA(1) autocovariance structure** — meaning its autocovariance cuts off after lag 1.

Compute:
- $\text{Cov}(\eta_t, \eta_{t-1})$: The only overlap comes from $e_t - \alpha e_{t-1}$ and $e_{t-1} - \alpha e_{t-2}$. The matching term is $-\alpha \cdot 1 \cdot \sigma_e^2$ from $\varepsilon_{t-1}$. So $\gamma_\eta(1) = -\alpha\sigma_e^2 \neq 0$.
- $\text{Cov}(\eta_t, \eta_{t-2}) = 0$ because no epsilon terms overlap at lag 2.

Since $\gamma_\eta(1) \neq 0$ but $\gamma_\eta(h) = 0$ for $h \geq 2$, the noise has MA(1) structure, confirming $y_t$ is ARMA(1,1).

---

## Part 5: Why MA is Always Stationary

A process is **(weakly) stationary** if three things don't change over time:
1. The mean $E[y_t]$ is constant
2. The variance $\text{Var}(y_t)$ is constant
3. The autocovariance $\gamma(h)$ depends only on the lag $h$, not on the time $t$

For MA(q), check each:

1. **Mean**: $E[y_t] = \mu + E[\varepsilon_t] + \theta_1 E[\varepsilon_{t-1}] + \cdots = \mu + 0 + 0 + \cdots = \mu$. Constant.

2. **Variance**: $\gamma(0) = (1 + \theta_1^2 + \cdots + \theta_q^2)\sigma^2$. This depends only on $\theta$ values and $\sigma^2$, not on $t$. Constant.

3. **Autocovariance**: $\gamma(h)$ depends only on $h$ and the $\theta$ values, not on $t$. Constant.

All three conditions hold regardless of what the $\theta$ values are!

Pesavento (Week 4 Feb 3 lecture, `week-04/recordings/arma-feb-3-recording.txt`; also `week-04/key-concepts.md` line 273):
> "The mean is constant. The variance is constant. The autocovariances don't change with time. So a moving average is always stationary."

**Contrast with AR**: An AR(1) $y_t = \rho y_{t-1} + \varepsilon_t$ is stationary only when $|\rho| < 1$. At $\rho = 1$ (unit root), the variance becomes infinite and the process is non-stationary (see `week-07/Unit+Root+Tests.pdf` slides 4-8 and `week-07/transcripts/Forecasting.txt` for full unit root treatment). MA has no such restriction.

---

## Part 6: Connection to ACF/PACF and Model Identification

> **Lecture reference**: `week-04/summary.md` lines 122-131 (table), `week-04/key-concepts.md` lines 113-119 (extended table with memory column), and the Feb 3 recording for Pesavento's live explanation.

The reason you compute autocovariances is to understand what the **Autocorrelation Function (ACF)** should look like. The ACF is the primary tool for identifying which model fits your data.

### The Identification Table

| Model | ACF Pattern | PACF Pattern |
|-------|-------------|-------------|
| **MA(1)** | One spike at lag 1, then zero | Gradual decay |
| **MA(2)** | Spikes at lags 1 and 2, then zero | Gradual decay |
| **MA(q)** | q spikes, then zero | Gradual decay |
| AR(1) | Gradual decay (geometric) | One spike at lag 1, then zero |
| AR(p) | Gradual decay | p spikes, then zero |
| ARMA(p,q) | Gradual decay | Gradual decay |

The key distinction:
- **"Cuts off"** means drops to exactly zero after a specific lag (sharp, like a cliff)
- **"Decays"** means gradually gets smaller (like a hill tapering off)

Pesavento:
> "If I see an autocorrelation that looks like that, where I have a couple of points that are big and then it dropped to zero, I know this is probably a moving average model. Which order? Potentially I can look at how many of them are different than zero."

The cutoff in the ACF is a **direct consequence** of $\gamma(h) = 0$ for $h > q$ — which is exactly what we derived above. The math produces the pattern you see in the data.

---

## Part 7: Connection to Forecasting

> **Lecture reference**: `week-06/key-concepts.md` lines 77-115 (MA forecasting horizon limit with MA(2) worked example), `week-06/summary.md` lines 152-174 (complete MA(2) forecast walkthrough with error variances).

The autocovariance structure also determines how far ahead an MA(q) model can forecast.

**MA(q) forecasting rule** (from Week 6):
- Replace any **future** $\varepsilon$ (which you don't know yet) with zero
- Keep any **past** $\varepsilon$ (which you observe as residuals from your fitted model)

**MA(2) example**: At the end of period $T$, you know $\varepsilon_T$ and $\varepsilon_{T-1}$ (from residuals).

- **1-step forecast**: $\hat{y}_{T+1} = \mu + 0 + \theta_1\varepsilon_T + \theta_2\varepsilon_{T-1}$ (replace $\varepsilon_{T+1}$ with 0)
- **2-step forecast**: $\hat{y}_{T+2} = \mu + 0 + 0 + \theta_2\varepsilon_T$ (replace $\varepsilon_{T+2}$ and $\varepsilon_{T+1}$ with 0)
- **3-step forecast**: $\hat{y}_{T+3} = \mu$ (all epsilon terms are future → all replaced with 0)

After q steps, the forecast is just the mean $\mu$. The model "runs out of memory." This is the forecasting analog of the autocovariance cutoff — and the reason AR models are preferred in practice (they can forecast further ahead).

---

## Part 8: Common Mistakes and How to Avoid Them

### Mistake 1: Not squaring coefficients in the variance

**Wrong**: $\gamma(0) = (1 + 0.3 + 0.7)\sigma^2 = 2.0\sigma^2$

**Right**: $\gamma(0) = (1 + 0.3^2 + 0.7^2)\sigma^2 = (1 + 0.09 + 0.49)\sigma^2 = 1.58\sigma^2$

You're computing $E[(...)^2]$. The square distributes to each coefficient individually.

### Mistake 2: Keeping cross terms in the variance

When expanding $(a+b+c)^2$, you get cross terms like $2ab$. But $E[\varepsilon_t \varepsilon_{t-1}] = 0$ for white noise, so **every cross term vanishes**. You never need to write them at all — but on the exam, you might write them to show you know they're zero (earns partial credit if anything else goes wrong).

### Mistake 3: Misidentifying which epsilon terms match

The most dangerous error. **Always write out both expressions in full** before looking for matches. Don't try to do it in your head.

For $\gamma(1)$ of MA(2):
- $y_t$ has: $\varepsilon_t$, $\varepsilon_{t-1}$, $\varepsilon_{t-2}$
- $y_{t-1}$ has: $\varepsilon_{t-1}$, $\varepsilon_{t-2}$, $\varepsilon_{t-3}$

Visually scan for matches: $\varepsilon_{t-1}$ appears in both. $\varepsilon_{t-2}$ appears in both. Nothing else matches.

### Mistake 4: Forgetting the implicit coefficient of 1

In $y_t = \varepsilon_t + 0.3\varepsilon_{t-1}$, the coefficient on $\varepsilon_t$ is **1**, not 0.3. When $\varepsilon_{t-1}$ matches in a $\gamma(1)$ computation, one coefficient is 0.3 (from $y_t$) and the other is 1 (from $y_{t-1}$), not 0.3 and 0.3.

### Mistake 5: Getting the cutoff lag wrong

MA(q) autocovariance is zero for $h > q$. The **last nonzero** value is $\gamma(q)$. Common mistake: saying MA(2) cuts off after lag 1 (wrong — it cuts off after lag 2).

### Mistake 6: Claiming MA can be non-stationary

**MA is always stationary.** Period. No conditions on $\theta$ needed. This is because MA is a finite sum of white noise terms, and any finite sum of WN is stationary. (AR requires $|\rho| < 1$. MA does not.)

Note: $\theta$ does affect **invertibility** (whether you can write the MA as an AR($\infty$)), but not stationarity. Invertibility requires $|\theta| < 1$ for MA(1).

---

## Part 9: PS2 Q1 — Proving a Composite Noise Has MA(1) Structure

> **Lecture references**: `week-04/recordings/arma-feb-5-recording.txt` (AR-to-MA conversion, lag operator), `week-03/summary.md` lines 22-30 (lag operator definition), lines 78-82 (Wold theorem). **Problem source**: `problem-sets/problem-set-2/Hwk2.pdf` page 1, Q1. **Full solution**: `problem-sets/problem-set-2/hwk2_analysis.ipynb` cell `34d0052b`. **Framework**: `problem-sets/problem-set-2/context-brief.md` lines 11-28.

This is a different APPLICATION of the MA autocovariance skill. Instead of being given an MA process and asked to compute its autocovariances, here you're given a messy expression and need to PROVE it behaves like an MA(1) by showing its autocovariances match the MA(1) pattern.

### 9.1 The Setup: What's the Problem?

You observe $y_t$. You think there's a hidden "true signal" $x_t$ that follows AR(1), but you can't see it directly — you only see it contaminated with measurement noise $e_t$:

$$y_t = x_t + e_t \qquad \text{(what you observe = signal + noise)}$$
$$x_t = \alpha x_{t-1} + u_t \qquad \text{(the signal follows AR(1))}$$

Where:
- $e_t$ is measurement error (white noise with variance $\sigma_e^2$)
- $u_t$ is the shock to the true signal (white noise with variance $\sigma_u^2$)
- $e_t$ and $u_t$ are **independent** of each other (knowing one tells you nothing about the other)

**The claim**: Even though the setup looks complicated, the observed $y_t$ is actually just an ARMA(1,1). The goal is to prove it.

**Why this matters economically**: This "signal plus noise" model shows up everywhere. GDP measurements have revisions (noise). Survey data is imprecise. Stock prices reflect a true value plus trading noise. The fact that signal-plus-noise always produces ARMA is a foundational result.

### 9.2 Step 1: Write y_t Using the AR(1)

Start with what you know:
- $y_t = x_t + e_t$
- $x_t = \alpha x_{t-1} + u_t$

Substitute the second equation into the first:

$$y_t = (\alpha x_{t-1} + u_t) + e_t = \alpha x_{t-1} + u_t + e_t$$

**Problem**: This still has $x_{t-1}$ in it, and $x$ is unobservable. We need to get rid of it.

### 9.3 Step 2: Eliminate the Unobservable (The Key Trick)

Here's the clever part. We know that $y_{t-1} = x_{t-1} + e_{t-1}$, so:

$$x_{t-1} = y_{t-1} - e_{t-1}$$

Substitute this into our equation:

$$y_t = \alpha(y_{t-1} - e_{t-1}) + u_t + e_t$$

$$\boxed{y_t = \alpha\, y_{t-1} + \underbrace{u_t + e_t - \alpha\, e_{t-1}}_{w_t}}$$

Now $y_t$ depends on its own lag $y_{t-1}$ (that's the AR part) plus a composite noise term $w_t = u_t + e_t - \alpha e_{t-1}$.

**What Pesavento's framework says** (from the PS2 context brief): "The proof should show: (1) substitute the AR(1) equation, (2) use lag to eliminate the unobservable $x_{t-1}$, (3) verify the composite noise has MA(1) autocovariance structure, (4) invoke Wold theorem."

We've done steps 1-2. Now comes the part where MA autocovariance skills come in.

### 9.4 Step 3: Prove w_t Has MA(1) Autocovariance Structure

We need to compute the autocovariances of $w_t = u_t + e_t - \alpha e_{t-1}$ and show they match the MA(1) pattern:
- $\gamma_w(0) \neq 0$ (some nonzero variance — always true)
- $\gamma_w(1) \neq 0$ (nonzero covariance at lag 1)
- $\gamma_w(h) = 0$ for $h \geq 2$ (cutoff — this is the critical part)

This uses **exactly the same technique** as our MA derivations, but now we have two independent white noise processes ($u_t$ and $e_t$) instead of one.

**The extended white noise rules:**

Since $u_t$ and $e_t$ are independent:
- $E[u_t \cdot u_s] = \sigma_u^2$ if $t = s$, zero otherwise (same timing rule for $u$)
- $E[e_t \cdot e_s] = \sigma_e^2$ if $t = s$, zero otherwise (same timing rule for $e$)
- $E[u_t \cdot e_s] = 0$ for ALL $t, s$ (independence — they NEVER interact, regardless of timing)

That third rule is new. When we had just one white noise, we only needed same-index vs different-index. Now we also need to know that $u$ and $e$ terms always kill each other.

#### Computing $\gamma_w(0)$ — the variance

$$\gamma_w(0) = E[w_t^2] = E[(u_t + e_t - \alpha e_{t-1})^2]$$

Expand the square:
$$= E[u_t^2] + E[e_t^2] + \alpha^2 E[e_{t-1}^2] + 2E[u_t e_t] - 2\alpha E[u_t e_{t-1}] - 2\alpha E[e_t e_{t-1}]$$

Apply the rules:
- $E[u_t^2] = \sigma_u^2$ (Property 2 of WN)
- $E[e_t^2] = \sigma_e^2$ (Property 2 of WN)
- $\alpha^2 E[e_{t-1}^2] = \alpha^2 \sigma_e^2$ (Property 2 of WN)
- $E[u_t e_t] = 0$ (independence of $u$ and $e$)
- $E[u_t e_{t-1}] = 0$ (independence of $u$ and $e$)
- $E[e_t e_{t-1}] = 0$ (different timing: $t \neq t-1$)

$$\boxed{\gamma_w(0) = \sigma_u^2 + (1 + \alpha^2)\sigma_e^2}$$

This is nonzero (it's a variance, so it's always positive). Good.

#### Computing $\gamma_w(1)$ — the lag-1 autocovariance

This is the critical one. We need it to be nonzero.

$$\gamma_w(1) = E[w_t \cdot w_{t-1}] = E[(u_t + e_t - \alpha e_{t-1})(u_{t-1} + e_{t-1} - \alpha e_{t-2})]$$

Now do the matching game. Write out every term in $w_t$ and every term in $w_{t-1}$, then check all pairs:

**Terms in $w_t$**: $u_t$ (coeff 1), $e_t$ (coeff 1), $e_{t-1}$ (coeff $-\alpha$)

**Terms in $w_{t-1}$**: $u_{t-1}$ (coeff 1), $e_{t-1}$ (coeff 1), $e_{t-2}$ (coeff $-\alpha$)

| $w_t$ term | $w_{t-1}$ term | Same process? | Same time? | Result |
|-----------|---------------|--------------|-----------|--------|
| $u_t$ | $u_{t-1}$ | Yes ($u$) | No ($t$ vs $t-1$) | **0** |
| $u_t$ | $e_{t-1}$ | No ($u$ vs $e$) | — | **0** (independence) |
| $u_t$ | $-\alpha e_{t-2}$ | No ($u$ vs $e$) | — | **0** (independence) |
| $e_t$ | $u_{t-1}$ | No ($e$ vs $u$) | — | **0** (independence) |
| $e_t$ | $e_{t-1}$ | Yes ($e$) | No ($t$ vs $t-1$) | **0** |
| $e_t$ | $-\alpha e_{t-2}$ | Yes ($e$) | No ($t$ vs $t-2$) | **0** |
| $-\alpha e_{t-1}$ | $u_{t-1}$ | No ($e$ vs $u$) | — | **0** (independence) |
| **$-\alpha e_{t-1}$** | **$e_{t-1}$** | **Yes ($e$)** | **Yes ($t-1 = t-1$)** | $(-\alpha)(1)\sigma_e^2 = -\alpha\sigma_e^2$ |
| $-\alpha e_{t-1}$ | $-\alpha e_{t-2}$ | Yes ($e$) | No ($t-1$ vs $t-2$) | **0** |

Out of **9 pairs**, only **ONE survives**: the $e_{t-1}$ term that appears in both $w_t$ (with coefficient $-\alpha$) and $w_{t-1}$ (with coefficient $1$).

$$\boxed{\gamma_w(1) = -\alpha\sigma_e^2}$$

This is nonzero (as long as $\alpha \neq 0$ and $\sigma_e^2 > 0$). The minus sign makes sense — it comes from the $-\alpha e_{t-1}$ term.

**Intuition**: The $e_{t-1}$ shock shows up in both $w_t$ (as part of $-\alpha e_{t-1}$, because we're "undoing" last period's noise) and $w_{t-1}$ (as part of $+e_{t-1}$, because it was that period's fresh noise). This creates lag-1 dependence.

#### Computing $\gamma_w(2)$ — the critical cutoff test

$$\gamma_w(2) = E[(u_t + e_t - \alpha e_{t-1})(u_{t-2} + e_{t-2} - \alpha e_{t-3})]$$

**Terms in $w_t$**: use times $\{t, t, t-1\}$ (the $u_t$, $e_t$, and $e_{t-1}$ subscripts)

**Terms in $w_{t-2}$**: use times $\{t-2, t-2, t-3\}$

The sets $\{t, t, t-1\}$ and $\{t-2, t-2, t-3\}$ have **no overlap** (the closest are $t-1$ and $t-2$, which are still different). Plus any cross-process pairs ($u$ vs $e$) are zero by independence.

$$\boxed{\gamma_w(2) = 0}$$

And $\gamma_w(h) = 0$ for all $h \geq 2$ by the same argument.

#### The conclusion: MA(1) signature confirmed

We found:
- $\gamma_w(0) = \sigma_u^2 + (1 + \alpha^2)\sigma_e^2 \neq 0$
- $\gamma_w(1) = -\alpha\sigma_e^2 \neq 0$
- $\gamma_w(h) = 0$ for $h \geq 2$

This is **exactly** the autocovariance pattern of an MA(1): nonzero at lag 0 and lag 1, then a sharp cutoff to zero. This is the same cutoff property we derived for MA(1) and MA(2) earlier — it's the fingerprint of an MA process.

### 9.5 Step 4: Invoke Wold and Write the Final ARMA(1,1)

The Wold Representation Theorem (Week 3) says: any covariance-stationary process with MA(q) autocovariance structure can be written as an MA(q).

Since $w_t$ has MA(1) autocovariance structure, there exists a white noise process $\eta_t$ and a parameter $\theta$ such that:

$$w_t = \eta_t + \theta\eta_{t-1}$$

The values of $\theta$ and $\sigma_\eta^2$ are found by **matching moments** — setting the autocovariances of $\eta_t + \theta\eta_{t-1}$ equal to the autocovariances of $w_t$:

From the MA(1) formulas we already know:
- $\gamma_{MA}(0) = (1 + \theta^2)\sigma_\eta^2$
- $\gamma_{MA}(1) = \theta\sigma_\eta^2$

Set these equal to the $w_t$ autocovariances:
- $(1 + \theta^2)\sigma_\eta^2 = \sigma_u^2 + (1 + \alpha^2)\sigma_e^2$
- $\theta\sigma_\eta^2 = -\alpha\sigma_e^2$

Dividing the second by the first:

$$\frac{\theta}{1+\theta^2} = \frac{-\alpha\sigma_e^2}{\sigma_u^2 + (1+\alpha^2)\sigma_e^2}$$

This determines $\theta$ as a function of $\alpha$ and the signal-to-noise ratio.

### 9.6 Putting It All Together

Substituting $w_t = \eta_t + \theta\eta_{t-1}$ back into our equation from Step 2:

$$y_t = \alpha y_{t-1} + \eta_t + \theta\eta_{t-1}$$

$$\boxed{y_t = \alpha y_{t-1} + \eta_t + \theta\eta_{t-1} \quad \text{— this is ARMA(1,1)}}$$

- The **AR(1) part** ($\alpha y_{t-1}$) comes from the original signal's persistence
- The **MA(1) part** ($\eta_t + \theta\eta_{t-1}$) comes from the mixing of signal shocks and measurement noise

### 9.7 What Makes This Different From the Standard MA Derivations

In Parts 3-4 you were given an MA process and computed its autocovariances (forward direction). Here you're going **backward**:

1. You have a composite noise $w_t = u_t + e_t - \alpha e_{t-1}$
2. You compute its autocovariances using the same matching technique
3. You recognize the autocovariance pattern as MA(1)
4. You conclude $w_t$ can be written as MA(1) (by Wold)

The autocovariance computation is the same skill — write out both terms, find matching indices, zero out everything else. The only new wrinkle is handling **two independent** white noise processes ($u$ and $e$) instead of one, which just adds the rule: terms from different processes are always zero, regardless of timing.

### 9.8 Why Pesavento Assigns This Problem

From the context brief: "The professor values seeing the autocovariance derivation step by step — 'the math is important to understand where they come from.'"

This problem tests whether you can:
1. Manipulate equations to eliminate unobservables (algebra skill)
2. Compute autocovariances of a composite noise term (the MA skill from this deep dive)
3. Recognize the MA(1) pattern from the autocovariance structure (identification skill)
4. Connect to the Wold theorem (theoretical understanding)

It's a synthesis question that ties together multiple course concepts.

---

## Cheat Sheet (Exam Morning Review)

```
================================================================
         MA AUTOCOVARIANCE — EVERYTHING ON ONE PAGE
================================================================

SETUP
  y_t = μ + ε_t + θ₁ε_{t-1} + ... + θ_qε_{t-q}
  ε_t ~ WN(0, σ²)
  The coefficient on ε_t is 1 (implicit!)

THE ONE RULE
  E[ε_i · ε_j] = σ²  if i = j
                = 0   if i ≠ j
  "Different timing → zero." — Pesavento

VARIANCE  γ(0)
  Square each coefficient, add them up, multiply by σ²:
  γ(0) = (1² + θ₁² + θ₂² + ... + θ_q²) σ²

AUTOCOVARIANCE  γ(h) for 1 ≤ h ≤ q
  Write y_t and y_{t-h} side by side
  Find matching ε subscripts
  Each match: (coeff in y_t) × (coeff in y_{t-h}) × σ²
  Sum all matches

CUTOFF  γ(h) = 0  for h > q
  No overlapping ε indices → everything is zero
  This is the MA SIGNATURE in the ACF

AUTOCORRELATION
  ρ(h) = γ(h) / γ(0)

================================================================
                    QUICK REFERENCE
================================================================

MA(1): y_t = ε_t + θε_{t-1}
  γ(0) = (1 + θ²)σ²
  γ(1) = θσ²
  γ(h≥2) = 0
  ρ(1) = θ/(1+θ²)     max |ρ(1)| = 0.5

MA(2): y_t = ε_t + θ₁ε_{t-1} + θ₂ε_{t-2}
  γ(0) = (1 + θ₁² + θ₂²)σ²
  γ(1) = (θ₁ + θ₁θ₂)σ²
  γ(2) = θ₂σ²
  γ(h≥3) = 0

IDENTIFICATION TABLE
  MA(q): ACF cuts off at q, PACF decays
  AR(p): ACF decays, PACF cuts off at p
  ARMA:  both decay

KEY FACTS
  MA is ALWAYS stationary (no conditions on θ)
  MA(q) can only forecast q steps ahead
  AR is preferred because easier to estimate (OLS) and forecast
================================================================
```

---

## Practice Drills

### Drill 1: MA(2) with specific numbers (3 minutes)
Compute $\gamma(0), \gamma(1), \gamma(2), \gamma(3)$ for $y_t = \varepsilon_t - 0.5\varepsilon_{t-1} + 0.3\varepsilon_{t-2}$.

<details>
<summary>Click for solution</summary>

$\theta_1 = -0.5$, $\theta_2 = 0.3$

$\gamma(0) = (1 + 0.25 + 0.09)\sigma^2 = 1.34\sigma^2$

$\gamma(1)$: Matches at $\varepsilon_{t-1}$ (coeffs $-0.5 \times 1$) and $\varepsilon_{t-2}$ (coeffs $0.3 \times (-0.5)$):
$\gamma(1) = (-0.5 + (-0.15))\sigma^2 = -0.65\sigma^2$

$\gamma(2)$: Match at $\varepsilon_{t-2}$ (coeffs $0.3 \times 1$):
$\gamma(2) = 0.3\sigma^2$

$\gamma(3) = 0$ (cutoff)

$\rho(1) = -0.65/1.34 = -0.485$, $\rho(2) = 0.3/1.34 = 0.224$
</details>

### Drill 2: MA(1) (2 minutes)
Compute $\gamma(0), \gamma(1), \rho(1)$ for $y_t = \varepsilon_t + 1.2\varepsilon_{t-1}$.

<details>
<summary>Click for solution</summary>

$\gamma(0) = (1 + 1.44)\sigma^2 = 2.44\sigma^2$

$\gamma(1) = 1.2\sigma^2$

$\gamma(2) = 0$

$\rho(1) = 1.2/2.44 = 0.492$

Note: $\theta = 1.2 > 1$, so this MA is not invertible. But it IS still stationary.
</details>

### Drill 3: Conceptual (1 minute)
True or False: An MA(3) process can have $\gamma(4) \neq 0$.

<details>
<summary>Click for solution</summary>

**False.** $\gamma(h) = 0$ for $h > q$. For MA(3), $\gamma(h) = 0$ for all $h \geq 4$.
</details>

### Drill 4: From the actual exam (5 minutes)
This is Exam 1 Q2. Do it cold, then check against Part 4 above.

$y_t = \varepsilon_t + 0.3\varepsilon_{t-1} + 0.7\varepsilon_{t-2}$. Compute $\gamma(0), \gamma(1), \gamma(2), \gamma(3), \rho(1), \rho(2), \rho(3)$.
