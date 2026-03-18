# The MA(∞) Representation of AR(1)

**What this is**: A complete explanation of how AR(1) can be rewritten as an infinite moving average, why this matters, and how it connects to variance, forecast errors, and the unit root.

**Lecture references**:
| Topic | File Path | What's There |
|-------|-----------|-------------|
| **AR to MA conversion derivation** | `course-materials/lectures/week-04/recordings/arma-feb-5-recording.txt` | "I substitute y_{t-1} = rho*y_{t-2} + epsilon and keep going forever... It's a moving average of infinite order" |
| **AR to MA summary** | `course-materials/lectures/week-04/summary.md` (lines 98-107) | Clean formula: y_t = c/(1-ρ) + Σρʲε_{t-j} |
| **Lag operator definition** | `course-materials/lectures/week-03/summary.md` (lines 22-30) | L operator, polynomial notation, inversion rule |
| **Wold Representation Theorem** | `course-materials/lectures/week-03/summary.md` (lines 78-82) | Any stationary process = infinite MA |
| **AR/MA interchangeability** | `course-materials/lectures/week-04/summary.md` (lines 189-200) | "Whether you go AR or MA, you may end up with something mathematically identical" |
| **Impulse response / dynamic multiplier** | `course-materials/lectures/week-04/summary.md` (lines 109-121) | "Shock of 1 today → ρ, ρ², ρ³..." |
| **Unit root: ρ = 1** | `course-materials/lectures/week-07/Unit+Root+Tests.pdf` (slides 4-10) | Variance → ∞, shocks permanent, non-stationary |
| **Unit root: drunk person analogy** | `course-materials/lectures/week-07/transcripts/Forecasting.txt` | "Best prediction is where he is right now" |
| **Forecast error variance** | `course-materials/lectures/week-06/summary.md` (lines 169-174, 200-208) | Error grows with h, converges to Var(y_t) |

---

## 1. Start with AR(1)

$$y_t = c + \rho y_{t-1} + \varepsilon_t$$

The question: can we rewrite this so $y_t$ only depends on shocks ($\varepsilon$), not on its own past values?

---

## 2. The Substitution Trick

Pesavento walks through this live (`week-04/recordings/arma-feb-5-recording.txt`):

> "I substitute $y_{t-1} = \rho y_{t-2} + \varepsilon_{t-1}$ and keep going forever... What is this? It's a moving average of infinite order."

**Step 1**: The model says $y_{t-1} = c + \rho y_{t-2} + \varepsilon_{t-1}$. Substitute into the original:

$$y_t = c + \rho(c + \rho y_{t-2} + \varepsilon_{t-1}) + \varepsilon_t$$
$$= c + \rho c + \rho^2 y_{t-2} + \varepsilon_t + \rho\varepsilon_{t-1}$$

**Step 2**: Now substitute $y_{t-2} = c + \rho y_{t-3} + \varepsilon_{t-2}$:

$$y_t = c(1 + \rho + \rho^2) + \rho^3 y_{t-3} + \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2}$$

**Step 3**: Keep going forever. The $\rho^k y_{t-k}$ term gets pushed further into the past. If $|\rho| < 1$, then $\rho^k \to 0$ as $k \to \infty$, so that term vanishes. What remains:

$$\boxed{y_t = \frac{c}{1-\rho} + \sum_{j=0}^{\infty} \rho^j \varepsilon_{t-j} = \mu + \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \rho^3\varepsilon_{t-3} + \cdots}$$

where $\mu = c/(1-\rho)$ is the unconditional mean.

Pesavento in the Feb 5 lecture (`week-04/recordings/arma-feb-5-recording.txt`):

> "So what do we learn? I can write $y_t$ as a sum for $j$ equals zero to infinite of $\rho^j \varepsilon_{t-j}$. What is this? What does this look like? It is a moving average of infinite order. I can go from AR(1) to MA(∞)."

---

## 3. What This Tells You

**This IS an MA process** — just with infinitely many terms. The "coefficients" are $\theta_j = \rho^j$:

| Term | Shock | Weight |
|------|-------|--------|
| j=0 | $\varepsilon_t$ (today's shock) | $\rho^0 = 1$ |
| j=1 | $\varepsilon_{t-1}$ (yesterday's) | $\rho^1 = \rho$ |
| j=2 | $\varepsilon_{t-2}$ (two periods ago) | $\rho^2$ |
| j=3 | $\varepsilon_{t-3}$ | $\rho^3$ |
| ... | ... | ... (decaying toward 0) |

**Every past shock contributes to today's value**, but with geometrically decaying weight. Recent shocks matter most; ancient shocks barely register.

---

## 4. Why This Matters: Four Key Uses

### Use 1: It proves the AR(1) variance, mean, and autocovariance formulas

This is the full derivation Pesavento does in the Feb 3 lecture (`week-04/recordings/arma-feb-3-recording.txt`). She starts from the MA(∞) representation and derives all the AR(1) properties using the same technique you already know from the MA autocovariance deep dive — plus one new tool: the geometric series formula.

#### The geometric series (the one new piece of math)

You need this fact: when $|x| < 1$,

$$1 + x + x^2 + x^3 + \cdots = \frac{1}{1-x}$$

This is just the infinite version of the formula you may know from algebra. It works because each added term is smaller than the last, so the sum converges.

#### Deriving the mean: $E[y_t] = c/(1-\rho)$

From the MA(∞): $y_t = \mu + \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \cdots$

But wait — we need to figure out what $\mu$ actually is. Go back to the original AR(1) and take expectations:

$$E[y_t] = c + \rho E[y_{t-1}] + E[\varepsilon_t]$$

Since $y_t$ is stationary, $E[y_t] = E[y_{t-1}]$ (call it $\mu$), and $E[\varepsilon_t] = 0$:

$$\mu = c + \rho\mu$$
$$\mu - \rho\mu = c$$
$$\mu(1-\rho) = c$$

$$\boxed{E[y_t] = \mu = \frac{c}{1-\rho}}$$

This requires $\rho \neq 1$ (otherwise you'd divide by zero).

Pesavento derives this via the infinite sum route too (`week-04/recordings/arma-feb-3-recording.txt`):

> "You know what this infinite sum is equal to? This is one over one minus rho times mu."

She's using the geometric series: the constant $c$ appears as $c(1 + \rho + \rho^2 + \cdots) = c/(1-\rho)$.

> "This is a condition that allows the mean to be defined... if rho is not less than one, this summation, infinite summation, is going to explode. If I sum one plus one plus one plus one, this is going to explode."

#### Deriving the variance: $\text{Var}(y_t) = \sigma^2/(1-\rho^2)$

This is the key derivation. Start from the MA(∞) with the mean subtracted:

$$y_t - \mu = \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \rho^3\varepsilon_{t-3} + \cdots$$

The variance is $E[(y_t - \mu)^2]$. Square the whole thing and take expectations.

You already know from the MA deep dive that when you square a sum of $\varepsilon$ terms, **all cross terms vanish** (different timing → zero) and only the squared terms survive. Each coefficient gets squared:

$$\text{Var}(y_t) = E[(\varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \cdots)^2]$$

Pesavento (`week-04/recordings/arma-feb-3-recording.txt`):

> "What is the variance of $y_t$? Remember it's $E$ of $\varepsilon_t$ plus $\rho \varepsilon_{t-1}$ plus $\rho^2 \varepsilon_{t-2}$ plus... squared. What is this? We have $\sigma^2$ plus — now we have to be careful, because it's squared — so I have $\rho^2 \sigma^2$ plus $\rho$ to the fourth $\sigma^2$ plus $\rho$ to the sixth $\sigma^2$ plus... This is $(1 + \rho^2 + \rho^4 + \rho^6 + \text{etc.})\sigma^2$."

Writing this out explicitly — the squared coefficients are:

| MA(∞) coefficient | Squared |
|-------------------|---------|
| 1 (on $\varepsilon_t$) | $1^2 = 1$ |
| $\rho$ (on $\varepsilon_{t-1}$) | $\rho^2$ |
| $\rho^2$ (on $\varepsilon_{t-2}$) | $\rho^4$ |
| $\rho^3$ (on $\varepsilon_{t-3}$) | $\rho^6$ |
| ... | ... |

So the variance is:

$$\text{Var}(y_t) = (1 + \rho^2 + \rho^4 + \rho^6 + \cdots)\sigma^2$$

Now apply the geometric series with $x = \rho^2$:

$$1 + \rho^2 + (\rho^2)^2 + (\rho^2)^3 + \cdots = \frac{1}{1-\rho^2}$$

This works because $|\rho| < 1$ implies $\rho^2 < 1$. Pesavento:

> "This is also an infinite sum of something, and if $\rho$ is less than one, also $\rho^2$ is less than one. So this is one over one minus $\rho^2$."

$$\boxed{\text{Var}(y_t) = \frac{\sigma^2}{1-\rho^2}}$$

**What happens at $\rho = 1$**: The denominator becomes $1 - 1 = 0$, so the variance is infinite. Pesavento:

> "What happens if $\rho$ is equal to one? It would turn into zero, and then it would not be valid — so it would explode."

This is one of the key reasons $\rho = 1$ (unit root) breaks the entire stationary framework.

#### Deriving autocovariance γ(1) and autocorrelation ρ(1)

Using the same MA(∞) matching technique. Write $y_t - \mu$ and $y_{t-1} - \mu$:

$$y_t - \mu = \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \rho^3\varepsilon_{t-3} + \cdots$$
$$y_{t-1} - \mu = \varepsilon_{t-1} + \rho\varepsilon_{t-2} + \rho^2\varepsilon_{t-3} + \rho^3\varepsilon_{t-4} + \cdots$$

Find matching $\varepsilon$ indices. Every $\varepsilon_{t-k}$ in $y_t$ (with coefficient $\rho^k$) matches $\varepsilon_{t-k}$ in $y_{t-1}$ (with coefficient $\rho^{k-1}$). So the matches are:

| Matching $\varepsilon$ | Coefficient in $y_t$ | Coefficient in $y_{t-1}$ | Product |
|-----------|-------------------|----------------------|---------|
| $\varepsilon_{t-1}$ | $\rho$ | $1$ | $\rho$ |
| $\varepsilon_{t-2}$ | $\rho^2$ | $\rho$ | $\rho^3$ |
| $\varepsilon_{t-3}$ | $\rho^3$ | $\rho^2$ | $\rho^5$ |
| ... | ... | ... | ... |

$$\gamma(1) = (\rho + \rho^3 + \rho^5 + \cdots)\sigma^2 = \rho(1 + \rho^2 + \rho^4 + \cdots)\sigma^2 = \frac{\rho}{1-\rho^2}\sigma^2$$

Pesavento confirms (`week-04/recordings/arma-feb-3-recording.txt`):

> "But this is $\rho$ divided by one minus $\rho$ squared, $\sigma^2$."

The autocorrelation:

$$\rho(1) = \frac{\gamma(1)}{\gamma(0)} = \frac{\rho\sigma^2/(1-\rho^2)}{\sigma^2/(1-\rho^2)} = \rho$$

The $\sigma^2/(1-\rho^2)$ cancels top and bottom!

$$\boxed{\rho(1) = \rho}$$

The first-order autocorrelation of an AR(1) is just $\rho$ itself. Elegant.

#### Deriving γ(2), γ(h), and the general ACF

By the same matching technique at lag 2, you get:

$$\gamma(2) = \frac{\rho^2}{1-\rho^2}\sigma^2, \qquad \rho(2) = \rho^2$$

Pesavento:
> "If I do two, it's going to be equal to $\rho^2$ divided by one minus $\rho^2$ $\sigma^2$... and you can do it yourself. It's just a lot of math and knowing that the infinite summation converges."

In general:

$$\boxed{\gamma(h) = \frac{\rho^h}{1-\rho^2}\sigma^2, \qquad \rho(h) = \rho^h}$$

> "So I have that $\rho(2)$ is $\rho^2$, $\rho(3)$ is $\rho^3$, and so forth."

**Key contrast with MA**: For MA(q), the autocovariance **cuts off** to exactly zero after lag $q$. For AR(1), it **never** cuts off — it decays geometrically as $\rho^h$ but is never exactly zero. This is because the MA(∞) has infinitely many terms, so $y_t$ and $y_{t-h}$ always share some $\varepsilon$ terms no matter how large $h$ is.

#### Summary of all AR(1) properties (from MA(∞))

| Property | Formula | Geometric series used |
|----------|---------|----------------------|
| Mean | $\mu = c/(1-\rho)$ | $1 + \rho + \rho^2 + \cdots = 1/(1-\rho)$ |
| Variance | $\gamma(0) = \sigma^2/(1-\rho^2)$ | $1 + \rho^2 + \rho^4 + \cdots = 1/(1-\rho^2)$ |
| Autocovariance | $\gamma(h) = \rho^h\sigma^2/(1-\rho^2)$ | $\rho^h(1 + \rho^2 + \rho^4 + \cdots) = \rho^h/(1-\rho^2)$ |
| Autocorrelation | $\rho(h) = \rho^h$ | Cancellation of $\sigma^2/(1-\rho^2)$ |

All four require $|\rho| < 1$. At $\rho = 1$, the geometric series diverges and everything breaks.

### Use 2: It explains why AR autocovariance never cuts off

An MA(q) has $\gamma(h) = 0$ for $h > q$ because there are only $q$ terms — at some point the epsilon lists stop overlapping. But MA(∞) has infinitely many terms, so there's **always** overlap no matter how large $h$ is.

That's why AR(1) has $\rho(h) = \rho^h \neq 0$ for all $h$ — the ACF decays geometrically but never reaches exactly zero. This is the **ACF signature of AR**: gradual decay, no cutoff.

### Use 3: It's how you compute forecast error variance

The h-step forecast error for AR(1) is (from `week-06/summary.md` lines 200-208):

$$e_{T+h,T} = \varepsilon_{T+h} + \rho\varepsilon_{T+h-1} + \rho^2\varepsilon_{T+h-2} + \cdots + \rho^{h-1}\varepsilon_{T+1}$$

That's the first $h$ terms of the MA(∞). So:

$$\text{Var}(e_{T+h,T}) = (1 + \rho^2 + \rho^4 + \cdots + \rho^{2(h-1)})\sigma^2 = \frac{1 - \rho^{2h}}{1 - \rho^2}\sigma^2$$

This **grows with h** and converges to $\text{Var}(y_t) = \sigma^2/(1-\rho^2)$ as $h \to \infty$.

**Key insight**: At $h = 1$, error variance is just $\sigma^2$. At $h = \infty$, it equals the full variance of the process. You're always more precise at short horizons.

### Use 4: It shows AR and MA are the same thing

Pesavento emphasizes this (`week-04/summary.md` lines 189-200):

> "Whether you go autoregressive or moving average, you and I may end up with something mathematically identical... Which one would you rather estimate? One parameter or infinite parameters?"

That's the practical argument for AR: one parameter $\rho$ captures the same structure as infinitely many MA coefficients. AR is estimated by simple OLS; MA requires nonlinear MLE.

---

## 5. What Happens at ρ = 1 (Unit Root)

If $\rho = 1$, the weights $\rho^j = 1$ for all $j$ — they never decay. Every past shock has **equal weight forever** (see `week-07/Unit+Root+Tests.pdf` slides 4-8):

$$y_t = \varepsilon_t + \varepsilon_{t-1} + \varepsilon_{t-2} + \cdots$$

This is an infinite sum of shocks with no decay:
- **Variance is infinite**: $\sum_{j=0}^{\infty} 1^2 = \infty$
- The process is **non-stationary** — it wanders without bound
- Shocks are **permanent** — they never fade

Pesavento (`week-04/summary.md` line 117, and `week-07/transcripts/Forecasting.txt`):
> "When $\rho$ is equal to one, the shock is permanent. It never goes away."

The **forecast** under a unit root is simply $\hat{y}_{T+h} = y_T$ for all $h$ — just the current value. The forecast error variance grows linearly: $\text{Var}(e_{T+h}) = h\sigma^2$, which never converges.

**Contrast with stationary AR(1)** ($|\rho| < 1$):
- Shocks decay: weight $\rho^j \to 0$
- Variance is finite: $\sigma^2/(1-\rho^2)$
- Forecast converges to the mean: $\hat{y}_{T+h} \to \mu$
- Forecast error variance converges to $\text{Var}(y_t)$

---

## 6. The Lag Operator Shortcut

In lag operator notation (`week-03/summary.md` lines 22-30):

$$y_t = c + \rho L y_t + \varepsilon_t$$
$$(1 - \rho L)y_t = c + \varepsilon_t$$
$$y_t = \frac{c}{1-\rho L} + \frac{\varepsilon_t}{1-\rho L}$$

The key identity: if $|\rho| < 1$, then:

$$(1 - \rho L)^{-1} = 1 + \rho L + \rho^2 L^2 + \rho^3 L^3 + \cdots = \sum_{j=0}^{\infty} \rho^j L^j$$

So:

$$\frac{\varepsilon_t}{1-\rho L} = (1 + \rho L + \rho^2 L^2 + \cdots)\varepsilon_t = \varepsilon_t + \rho\varepsilon_{t-1} + \rho^2\varepsilon_{t-2} + \cdots$$

This is the same MA(∞) we derived by substitution, but in one compact line.

Pesavento in the Feb 3 lecture (`week-04/recordings/arma-feb-3-recording.txt`):
> "If I use the lag operator, this is $(1 - \rho L) y_t = \varepsilon_t$. Now I have this little, nice polynomial of order one."

**This lag operator inversion** is the same technique used in the PS2 Q1 proof (see `exams/study-notes/MA-autocovariance-deep-dive.md`, Part 9) to eliminate unobservable variables and reveal ARMA structure.

---

## 7. Connection to the Wold Theorem

The Wold Representation Theorem (`week-03/summary.md` lines 78-82) says:

> Any zero-mean covariance-stationary process can be written as $Y_t = \sum_{j=0}^{\infty} \psi_j \varepsilon_{t-j}$ where $\psi_0 = 1$ and $\sum \psi_j^2 < \infty$.

The MA(∞) representation of AR(1) is a **specific case** of this theorem where $\psi_j = \rho^j$. The condition $\sum \psi_j^2 = \sum \rho^{2j} = 1/(1-\rho^2) < \infty$ holds precisely when $|\rho| < 1$ (stationarity).

When $\rho = 1$, $\sum \psi_j^2 = \sum 1 = \infty$, so the Wold representation doesn't apply — the process is non-stationary, and the whole framework breaks down.

---

## Quick Reference

```
================================================================
     MA(∞) REPRESENTATION OF AR(1) — KEY FORMULAS
================================================================

AR(1): y_t = c + ρy_{t-1} + ε_t    (requires |ρ| < 1)

MA(∞): y_t = μ + Σ(j=0 to ∞) ρʲ ε_{t-j}
      = μ + ε_t + ρε_{t-1} + ρ²ε_{t-2} + ρ³ε_{t-3} + ...

where μ = c/(1-ρ)

Lag operator: y_t = c/(1-ρL) + ε_t/(1-ρL)
             (1-ρL)⁻¹ = 1 + ρL + ρ²L² + ...

VARIANCE (from MA formula):
  Var(y_t) = (1 + ρ² + ρ⁴ + ...)σ² = σ²/(1-ρ²)

ACF:
  ρ(h) = ρʰ  (never zero — decays but no cutoff)

FORECAST ERROR VARIANCE AT HORIZON h:
  Var(e_{T+h}) = σ²(1 + ρ² + ... + ρ^{2(h-1)})
               = σ² × (1 - ρ^{2h})/(1 - ρ²)
  → grows with h, converges to Var(y_t)

UNIT ROOT (ρ = 1):
  Weights = 1 forever → shocks permanent
  Variance = ∞ → non-stationary
  Forecast = y_T → just the current value
  Error variance = hσ² → grows linearly, never converges
================================================================
```
