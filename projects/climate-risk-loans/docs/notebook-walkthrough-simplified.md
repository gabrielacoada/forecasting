# What Our Code Actually Does — The Plain English Version

This explains everything in our three notebooks without assuming you know anything about statistics, coding, or econometrics. If you're making slides, writing the report, or doing the narrative section, this is your guide.

---

## The 30-Second Summary

We built three notebooks that answer one question: **"If the world takes different approaches to climate change, what happens to the loans that US banks hold?"**

Here's the flow:

```
Notebook 1                    Notebook 2                    Notebook 3
"Understand the               "Understand the               "Connect them and
 historical loan data"         climate scenario data"         predict the future"
        |                            |                            |
        v                            v                            v
What patterns exist            What do the climate          If unemployment goes
in past loan growth?           scenarios say will           up under Scenario X,
What drives it?                happen to the economy?       what happens to loans?
        |                            |                            |
        +----------------------------+----------------------------+
                                     |
                                     v
                        FINAL OUTPUT: "Under Net Zero 2050,
                        C&I loans grow to 243% of today's level.
                        Under Delayed Transition, only 226%."
```

---

## Notebook 1: Understanding the Historical Loan Data

### What are we looking at?

We downloaded 7 spreadsheets from FRED (the Federal Reserve's public database). Think of FRED as a giant library of economic data that anyone can access. Each spreadsheet is a long list of numbers over time:

| Spreadsheet | What it tracks | In plain English |
|------------|---------------|-----------------|
| BUSLOANS | Commercial & Industrial loans | How much money banks have lent to businesses, in total, across the whole US |
| CONSUMER | Consumer loans | How much money banks have lent to regular people (car loans, credit cards, personal loans) |
| GDPC1 | GDP | How big is the US economy? (Total value of everything produced) |
| UNRATE | Unemployment rate | What percentage of people who want jobs can't find one? |
| FEDFUNDS | Federal Funds Rate | The interest rate the Federal Reserve sets. Think of it as the "price of money" that affects everything else. |
| DGS10 | 10-Year Treasury Yield | The interest rate on a 10-year government bond. This is what drives mortgage rates and other long-term borrowing costs. |
| CPIAUCSL | Consumer Price Index | A measure of inflation — are prices going up? |

### Step 1: Just look at the data

First, we just plotted everything to see what it looks like over time. Three things jump out immediately:

1. **Loan balances go up and up.** C&I loans are at $2,700 billion. Consumer loans at $1,858 billion. Both have been climbing for decades. This is a problem for prediction (more on that next).

2. **COVID is massive.** In the charts, we shaded March 2020 through June 2021 in red. The C&I loans line spikes upward violently during COVID. Consumer loans dip.

3. **The economic variables (unemployment, interest rates, etc.) move in interesting patterns** that seem related to loan movement.

### Step 2: Convert to growth rates (and why)

Here's a fundamental problem: you can't predict something that just keeps going up forever. If I told you "loans were $2,700 billion last month," that doesn't help you guess next month — the answer is "probably a little more than $2,700 billion" but that's useless.

Instead, we ask a better question: **"By what percentage did loans grow this month compared to last month?"**

Growth rates bounce around a stable average (sometimes positive, sometimes negative, but averaging around the same number). That makes them predictable.

**The formula:** We use `100 x ln(this month / last month)`. This is a fancy version of "percentage change" that the professor prefers. For small numbers (like 0.5% growth), it gives almost the same answer as regular percentage change. The advantage is that it adds up nicely over time — if January grew 1% and February grew 1%, the two-month growth is exactly 2%. Regular percentages don't do that cleanly.

**What we found:** On average, C&I loans grow about 0.58% per month. Consumer loans grow about 0.64% per month. Those are the "normal" numbers.

### Step 3: Stationarity tests (is the data predictable?)

"Stationarity" is a fancy word for: **"Does this data behave consistently over time?"**

Imagine you're trying to predict the weather. If you lived somewhere where the temperature was always between 60-80 degrees with random daily variation, that's "stationary" — you can make reasonable predictions. But if you lived somewhere where the temperature was rising 5 degrees every year with no end in sight, that's "non-stationary" — the past doesn't tell you much about the future because the rules keep changing.

We ran two formal tests:
- **ADF test** — asks "is this series wandering randomly?" (like a drunk person stumbling — each step is random, so knowing where they are now doesn't help you predict where they'll be in 10 steps)
- **KPSS test** — asks "is this series stable?" (does it keep coming back to some average?)

**Results:**
- Loan *levels* (dollar amounts): NOT stable. They just keep going up. Confirmed by both tests.
- Loan *growth rates*: Stable. They bounce around a consistent average. This confirms that growth rates are what we should model.

**Bottom line:** We work in growth rates for everything from here on out.

### Step 4: ACF/PACF (how much does the past matter?)

These are two charts with intimidating names but a simple idea:

**ACF (Autocorrelation Function):** "If loan growth was high this month, is it likely to be high next month? What about 2 months from now? 3 months?"

It measures how much each past month's growth is correlated with today's growth. Imagine a line chart where the x-axis is "how many months ago" and the y-axis is "how correlated." If the bars are tall, the past matters a lot. If they're short, the past doesn't help much.

**PACF (Partial Autocorrelation Function):** Same idea, but it isolates the *direct* effect of each lag. Think of it this way: maybe last month's growth predicts today's — and two months ago also seems to predict today. But is two months ago actually giving you NEW information, or is it just correlated with last month? PACF strips out the indirect effects and shows only the direct ones.

**Why we care:** These charts tell us how many months of history our model should use. If only the first 4 bars in the PACF are significant, we should use 4 months of history. Using 12 would be wasteful.

**What we found:**
- C&I loans: significant autocorrelation out to ~12 months (there's a seasonal pattern — businesses follow annual budget cycles)
- Consumer loans: significant out to ~4 months (simpler pattern)

### Step 5: How bad was COVID?

We measured COVID's impact by asking: "How unusual were those months compared to what's normal?"

We calculated **z-scores** — basically, "how many standard deviations away from normal was each month?" A z-score of 2 means "this is unusual." A z-score of 3 means "this almost never happens." A z-score of 13.9 means "this is essentially impossible under normal conditions."

**C&I loans during COVID:**
- April 2020: z-score of **+13.9**. That's not a typo. This month was so extreme it's basically off the charts. Why? The government's PPP (Paycheck Protection Program) funneled hundreds of billions of dollars through the banking system as loans to businesses to keep them alive during lockdowns.
- 8 total months exceeded a z-score of 3 (all between March 2020 and June 2021)

**Consumer loans during COVID:**
- April 2020: z-score of **-3.5**. Still extreme, but nothing like C&I. People stopped spending during lockdowns, so they borrowed less.
- Only 1 month exceeded a z-score of 3

**The key insight:** COVID hit C&I and consumer loans in *opposite directions*. Business loans surged (because of government programs), consumer loans dropped (because of lockdowns). This tells us they respond to shocks differently, so we need separate models for each.

**One more thing:** After COVID ended, both types of loans settled into a "new normal" with lower growth rates than before. C&I went from averaging 0.61% per month to 0.17%. Consumer went from 0.68% to 0.32%. The post-COVID economy is different.

### Step 6: Building the "dumb" baseline model

Before we build anything fancy, we need to build the simplest possible model so we can measure whether our fancy model is actually better.

**What is an AR model?** AR stands for "autoregressive," which just means "predict the future using the past." An AR(4) model says: "To predict this month's loan growth, look at the last 4 months of loan growth and use a weighted average."

It's like predicting tomorrow's weather by averaging the last few days. Simple, but often surprisingly effective.

**How do we pick how many months to use?** We tried AR(1) through AR(12) and used something called BIC to pick the best one.

**What is BIC?** BIC (Bayesian Information Criterion) is a scoring system that balances two things:
1. How well does the model fit the data? (Better fit = better score)
2. How complicated is the model? (More complicated = penalty)

You want the model that fits well without being unnecessarily complicated. Think of it like buying a car: you want something reliable (good fit) without paying for features you'll never use (complexity penalty). BIC tells you which car is the best value.

**Why BIC over AIC?** AIC is a similar scoring system but with a lighter complexity penalty — it tends to pick more complex models. Our professor prefers BIC because with limited data (we only have ~30 years), simpler models are more reliable. It's the "don't overfit" philosophy.

**What we found:**
- Best model for C&I: AR(12) — uses a full year of history (seasonal lending patterns)
- Best model for consumer: AR(4) — uses 4 months (simpler, no seasonality)

**Residual check (Ljung-Box test):** After building the model, we checked: "Is there any predictable pattern left in the errors?" If yes, the model is missing something. If no, we've captured everything we can.

Both models passed — no leftover patterns. The "dumb" model is as good as a dumb model can be.

### Step 7: What economic variables help predict loans?

Now the interesting part: do things like unemployment and interest rates help predict loan growth? Or is past loan growth all you need?

We measured **cross-correlations** — basically, "when unemployment goes up, does loan growth tend to go down? And if so, how many months later?"

**What we found:**
- **Unemployment changes and loan growth: strongly correlated** (negative — when unemployment rises, loans fall). Makes total sense: when people lose jobs and businesses struggle, everyone borrows less.
- **Fed Funds rate changes and loan growth: correlated.** When the Fed raises rates, borrowing gets more expensive, and loan growth slows.
- **Inflation and loan growth: weakly correlated.** Some relationship, but not as clear.

**What this means:** When we build our real model, we should include unemployment and interest rates as predictors. They contain useful information beyond what past loan growth tells us.

### Step 8: Rolling statistics (how has the world changed?)

We computed a "rolling average" — instead of one average for the whole 75-year history, we calculated the average over a sliding 2-year window. This shows how the typical growth rate and the typical volatility have changed over time.

**What we saw:**
- The **"Great Moderation"** (mid-1980s): Volatility dropped dramatically. Before 1984, the economy was bumpy. After, it smoothed out. This is a well-known phenomenon.
- **Post-2008**: Average growth rates dropped. The financial crisis permanently shifted the lending environment.
- **COVID**: Sticks out like a sore thumb — a massive spike in both average and volatility.
- **Post-COVID**: Growth rates are even lower than post-2008. We're in a structurally different world.

---

## Notebook 2: Understanding the Climate Scenario Data

### What is the NGFS?

The NGFS (Network for Greening the Financial System) is a club of 121 central banks from around the world. They got together and said: "Let's create standardized 'what if' stories about how climate change could play out, so banks and regulators can all use the same assumptions."

Think of it like this: instead of every bank making up their own guesses about the future, the NGFS provides official, scientifically-grounded stories that everyone can use. Each story is called a **scenario**.

### What are the scenarios?

Each scenario tells a different story about how governments respond to climate change:

**Net Zero 2050** — "Governments act now, aggressively"
- Countries impose high carbon taxes starting immediately
- Short-term economic pain (businesses have to change how they operate)
- But long-term, the economy does better because the worst physical damage is avoided
- Think: paying for a home renovation now to avoid much bigger repair costs later

**Below 2 Degrees** — "Governments act now, moderately"
- Like Net Zero but less extreme
- Moderate carbon taxes, gradual transition
- A middle ground

**Delayed Transition** — "Governments do nothing until 2030, then panic"
- No climate policy at all until 2030
- Then suddenly, aggressive policies hit all at once
- The economy gets whiplash — everything looks fine, then BAM
- Think: ignoring a leaky roof until it collapses, then paying for emergency repairs

**Fragmented World** — "Some countries act, others don't"
- No global coordination
- Some regions impose strict policies, others don't
- Trade disruptions, inequality between regions
- The worst of both worlds

**NDCs (Nationally Determined Contributions)** — "Countries keep their current promises"
- Governments follow through on their Paris Agreement commitments but don't do more
- Moderate transition costs
- But not enough to prevent significant physical climate damage long-term

**Current Policies** — "Nobody does anything new"
- No new climate policy at all
- No transition costs (no carbon taxes, no regulations)
- But temperatures rise past 3 degrees Celsius
- Massive physical damage: more storms, flooding, droughts, sea level rise

### The two data files

The NGFS gave us two Excel files. This is important because they contain *different types of information* and are structured differently:

**File 1: NiGEM (the economics file, 27 MB)**

This is the one that matters most for us. It contains projections for economic variables:
- GDP (how big is the economy)
- Unemployment
- Inflation
- Interest rates (short-term and long-term)
- Stock prices
- House prices

These are exactly the same kinds of numbers we have in our historical FRED data, but projected into the future (2022 to 2050) under each climate scenario.

**One critical quirk:** The data is stored in a confusing way. For the "Baseline" scenario, the file stores actual numbers (GDP = $23 trillion, unemployment = 4.2%, etc.). For every other scenario, it stores *differences from the baseline* (GDP is 2% lower, unemployment is 0.3% higher, etc.). So before we can use the data, we have to do math to reconstruct the actual numbers for each scenario.

For things measured in dollars or quantities (GDP, stock prices, house prices), the differences are percentages: "GDP is 5% below baseline." The formula is: `actual = baseline × (1 + percentage/100)`.

For things measured in rates (unemployment, interest rates, inflation), the differences are in percentage points: "unemployment is 0.3 points above baseline." The formula is: `actual = baseline + difference`.

Getting this wrong causes blank charts and wrong numbers — we had to fix several bugs related to this.

**File 2: IAM (the climate science file, 63 MB)**

This contains the physical climate data:
- Carbon prices (how much it costs to emit CO2)
- CO2 emissions (how much pollution is being released)
- Energy mix (how much comes from fossil fuels vs. renewables)
- Temperature projections
- GDP with physical damage estimates

This file is structured more simply — all scenarios store actual numbers directly. But it goes much further into the future (out to 2100) and uses 5-year steps instead of annual.

### What are the IAM model families?

The NGFS didn't use just one scientific model to create the scenarios — they used three, each built by a different research group:

- **GCAM** (from the US)
- **REMIND** (from Germany)
- **MESSAGEix** (from Austria)

They all take the same climate assumptions and produce projections for the same variables, but because they model the economy differently, they give somewhat different answers. The spread across models for the same scenario is about 3%.

This is actually useful for us: instead of pretending we know the exact answer, we can show a range. "Under Net Zero 2050, GDP will be between X and Y, depending on which model you trust." BofA explicitly said they value this kind of honest uncertainty.

### What does the scenario data tell us?

**The big finding: acting early is better in the long run, even though it costs more up front.**

| Scenario | GDP in 2050 | Versus Best |
|----------|------------|-------------|
| Net Zero 2050 (act now) | $31,460 B | Best |
| Below 2 Degrees | $31,209 B | $251 B less |
| Delayed Transition (wait then panic) | $30,573 B | $887 B less |
| NDCs (keep current promises) | $30,374 B | $1,086 B less |
| Fragmented World | $30,300 B | $1,160 B less |

Net Zero 2050 — the most aggressive policy — actually ends up with the HIGHEST GDP by 2050. Why? Because the physical damage from uncontrolled climate change (storms, droughts, flooding) is so expensive that avoiding it more than makes up for the transition costs.

**But there's a twist:** In the *short run* (by 2030), Net Zero looks WORSE. GDP under Net Zero in 2030 is $24,169 B, while Delayed Transition is $24,620 B. That's because Net Zero is paying the transition costs NOW, while Delayed Transition hasn't started paying yet. It's only after 2030 that Delayed Transition gets hit with both the sudden policy shock AND the physical damage.

This is like choosing between: (A) pay $500/month for 30 years for a good roof, or (B) pay nothing for 10 years and then $200,000 for emergency repairs.

### The bridge: how do climate scenarios connect to our loan model?

This is the most important conceptual step in the whole project. The climate scenarios give us projections for GDP, unemployment, interest rates, etc. Our historical FRED data gives us the same variables for the past. So:

1. We learn from history: "When unemployment went up by 1%, loan growth dropped by X%"
2. We read from the scenarios: "Under Net Zero 2050, unemployment will be 4.56% in 2040"
3. We combine: "Therefore, under Net Zero 2050, loan growth will be approximately Y%"

The mapping between NGFS variables and FRED variables is:

| What NGFS calls it | What FRED calls it | Match quality |
|---|---|---|
| GDP (2017 PPP dollars) | GDPC1 | Good (need to adjust scale) |
| Unemployment rate | UNRATE | Direct match |
| Inflation rate | CPI growth | Direct match |
| Central bank policy rate | FEDFUNDS | Direct match |
| Long-term interest rate | DGS10 | Direct match |

### Risk decomposition: where does the economic damage come from?

For each scenario, we can break down the GDP impact into two sources:

**Transition risk** = the cost of climate policy itself (carbon taxes, regulations forcing businesses to change). This is higher in scenarios with aggressive policy (like Net Zero).

**Physical risk** = the cost of actual climate damage (storms, flooding, heat waves, crop failures). This is higher in scenarios with weak policy (like Current Policies).

Under Net Zero 2050: GDP is about 4% below baseline by 2030, mostly from transition costs. Physical damage is small because the aggressive policy prevents the worst outcomes.

Under Delayed Transition: GDP is fine until 2030 (no policy yet), then gets hit by a sharp transition shock AND growing physical damage. By 2050, both sources are contributing.

Under NDCs: Moderate transition costs throughout, but physical risk keeps growing because the policy isn't strong enough to fully prevent climate damage.

---

## Notebook 3: Connecting History to the Future

This is where everything comes together. Notebook 1 told us what drives loan growth historically. Notebook 2 told us what the future economy looks like under each climate scenario. Notebook 3 builds a model that translates scenario economic paths into loan forecasts.

### Step 1: Prepare the data

We take all the monthly FRED data and convert it to annual. Why? Because the NGFS climate scenarios are annual (one number per year). If our historical data is monthly but our future data is annual, they don't line up. The simplest solution: make everything annual.

This means taking 12 monthly numbers and computing their average to get one annual number. We end up with 36 annual observations (1990 through 2025).

**Why start from 1990?** BofA said we need at least 3 decades of history to capture enough recessions and business cycles. Going further back (like to the 1940s) would include a very different banking world where most of our modern financial system didn't exist.

**COVID treatment:** We create a "dummy variable" — a column of 0s and 1s where 1 means "this was a COVID year." This lets the model say "okay, 2020 and 2021 were weird, let me adjust for that" without throwing those years away entirely. BofA confirmed this is the standard approach they use.

### Step 2: Extract the scenario paths

We re-read the NGFS data and transform it into the same format as our FRED data. For example:
- NGFS gives us GDP levels; we convert to growth rates (same transformation we did for FRED)
- NGFS gives us unemployment levels; we convert to year-over-year changes

This way, the future scenario numbers are in the exact same units as the historical numbers. You can't mix apples and oranges — if the model learned relationships using annual unemployment *changes*, the scenario inputs need to be annual unemployment *changes* too.

We extract 9 paths: 3 scenarios (Net Zero, Delayed Transition, NDCs) times 3 scientific models (GCAM, REMIND, MESSAGEix).

### Step 3: Build the AR baseline (the "dumb" model)

Same concept as Notebook 1, but now on annual data. We fit simple models that predict loan growth using only past loan growth. These models know nothing about the economy — they just say "if loans grew a lot last year, they'll probably grow a lot this year too."

Both loan types picked AR(4) — use the last 4 years of loan growth to predict next year.

This is our benchmark. Any model we build that uses economic variables must beat this.

### Step 4: Build the VAR model (the "smart" model)

**What is a VAR?**

VAR stands for "Vector Autoregression." Don't let the name scare you. Here's what it means:

- **Auto** = using past values to predict the future (same as AR)
- **Regression** = a mathematical formula that links things together
- **Vector** = multiple things at once (not just loans, but also unemployment, rates, etc.)

A regular AR model says: "Predict loan growth using past loan growth."

A VAR says: "Predict loan growth, unemployment, interest rates, and inflation ALL AT ONCE, using ALL of their past values." It's a system of equations where everything can affect everything else.

Why is this better? Because the economy is interconnected. Unemployment affects loan growth, but loan growth also reflects the state of the economy which feeds back into unemployment. A VAR captures these feedback loops.

**What is VAR(1)?**

The "(1)" means "use 1 year of past data." VAR(2) would use 2 years. We used BIC (the same scoring system from before) to pick, and it chose VAR(1). Why only 1 lag? Because with 4-5 variables and only 35 observations, every extra lag adds a LOT of parameters to estimate. With limited data, simpler is better — you don't want to estimate 40 parameters from 35 data points.

### Step 5: The C&I Loan Model

The C&I model tracks 4 variables as a system:
1. **C&I loan growth** (what we want to predict)
2. **Unemployment change** (are people losing jobs?)
3. **Fed Funds rate change** (is the Fed raising or lowering rates?)
4. **Inflation** (are prices rising?)

**What the model learned:**

The most important finding: **unemployment is the dominant driver of C&I loan growth.** When unemployment rises by 1 percentage point, C&I loan growth drops by about 5.8 percentage points the following year. This is statistically very strong (p < 0.001, meaning there's less than a 0.1% chance this is random noise).

Intuition: when people are losing jobs, it means businesses are struggling. Struggling businesses don't take out new loans, and some can't repay existing ones. The banking system contracts.

The Fed Funds rate has a weaker but interesting effect: rate hikes actually *boost* C&I loan growth slightly (coefficient: +2.04). This seems backwards, but there's a logic — when the Fed raises rates, banks earn higher interest on new loans, making lending more profitable. This effect is only marginally significant though (p = 0.085).

The COVID dummy confirms what we already knew: COVID boosted C&I loans by about 12 percentage points (PPP lending).

**Granger causality tests:**

This is a formal test that asks: "Does knowing past unemployment help predict future loan growth, beyond what past loan growth alone tells you?" It's named after Clive Granger who won a Nobel Prize for this idea.

Results:
- Unemployment → C&I loans: YES (p = 0.0004). Very strong.
- Fed Funds → C&I loans: YES (p = 0.019). Moderate.
- Inflation → C&I loans: NO (p = 0.39). Inflation doesn't add useful information.

**Impulse Response Functions (IRFs):**

These answer: "If unemployment suddenly jumps, what happens to loan growth over the next several years?"

Think of it like dropping a rock in a pond. The IRF traces the ripples.

What we found: an unemployment shock depresses C&I loan growth for about 4 years before the effect fades. The initial impact is large (about -6 percentage points in year 1), then gradually shrinks.

**Residual diagnostics (did we miss anything?):**

After the model makes its predictions, we look at the errors (the gap between what it predicted and what actually happened). If the errors have no pattern, the model captured everything useful. If the errors show a pattern, we missed something.

The Ljung-Box test checks for patterns in the errors. Our p-value is 0.72 — way above the 0.05 threshold. This means: no patterns left, the model is doing its job.

### Step 6: The Consumer Loan Model

The consumer model uses 5 variables (one more than C&I):
1. **Consumer loan growth** (what we want to predict)
2. **Unemployment change**
3. **Fed Funds rate change**
4. **Inflation**
5. **10-Year Treasury yield change** (NEW — not in the C&I model)

**Why add the 10-year yield?**

Consumer loans include mortgages and car loans. Mortgage rates are tied to the 10-year Treasury yield, not the Fed Funds rate. When the 10-year yield goes up, mortgages get more expensive, and fewer people borrow.

For businesses (C&I), the relevant rate is the short-term Fed Funds rate because business loans are typically short-term or floating-rate. For consumers, the long-term rate matters more because mortgages are 15-30 year commitments.

BofA also specifically asked us to be "more thorough about consumer drivers."

**What the model learned:**

Surprise: the consumer model tells a completely different story from C&I.

- **Consumer loan growth has mean reversion** (coefficient: -0.40, p = 0.02). This means if growth was high last year, it tends to be lower next year, and vice versa. Think of it like a pendulum swinging back and forth.

- **COVID had the opposite effect** (coefficient: -12.87, p = 0.04). While PPP boosted C&I loans by +12pp during COVID, consumer loans dropped by -13pp. People weren't buying cars or taking out personal loans during lockdowns.

- **Unemployment is NOT the main driver** (p = 0.21 — not statistically significant). This was surprising. For C&I loans, unemployment was the star of the show. For consumer loans, it matters less.

- **The 10-year yield IS a significant driver** in the Granger test (p = 0.023). Long-term borrowing costs are what drive consumer lending decisions.

**In plain English:** Businesses borrow based on how the economy is doing (unemployment). Consumers borrow based on how expensive it is to borrow (long-term interest rates). Different drivers for different types of loans.

*A caveat:* the unemployment result might be partly because we only have 35 annual data points. With more data (quarterly), unemployment might show up as significant for consumer loans too. Annual data averages out within-year dynamics that could matter.

### Step 7: Testing the models (Out-of-Sample Evaluation)

Building a model that fits past data well is easy. The hard part is: **does it predict the future well?**

To test this, we use a trick called **pseudo out-of-sample evaluation**. Here's how it works:

1. Pretend it's 2006. Use only data from 1990-2005 to build the model. Predict 2006.
2. Now pretend it's 2007. Use 1990-2006. Predict 2007.
3. Keep going: predict 2008, 2009, ... 2025.
4. Compare each prediction to what actually happened.

This simulates what it would have been like to use the model in real time. The model never gets to "cheat" by seeing the future.

We skip COVID years (2020-2021) when measuring accuracy, because BofA said those are essentially unpredictable one-off events.

**How do we measure accuracy?** We use RMSE (Root Mean Squared Error). Think of it as "the average size of the prediction mistakes." Lower = better.

**Results:**

| | "Dumb" model (AR) | "Smart" model (VAR) | Improvement |
|---|---|---|---|
| C&I loans | 10.09% error | 9.05% error | 10.4% better |
| Consumer loans | 16.85% error | 14.03% error | 16.7% better |

The VAR beats the AR baseline for both loan types. Adding economic variables (unemployment, rates) actually helps predict loans better than just using past loan growth alone. The improvement is especially large for consumer loans — adding the 10-year yield makes a meaningful difference.

### Step 8: Scenario-Conditional Forecasts (the main event)

This is the whole point of the project. Here's what happens:

We have a model that says: "Given last year's loan growth, unemployment change, interest rate change, and inflation, here's what loan growth will be this year."

For history (1990-2025), we used actual data. For the future (2026-2050), we don't have actual data — but we DO have the NGFS scenarios telling us what unemployment, rates, and inflation will be under each climate policy path.

So we plug in the scenario values:

- "Under Net Zero 2050, the NGFS says unemployment will change by X in 2030. Our model says that translates to Y% loan growth."
- "Under Delayed Transition, unemployment will change by Z in 2030. Our model says that translates to W% loan growth."

We repeat this for every year from 2026 to 2050, for each of the 3 scenarios, using each of the 3 scientific models. That gives us 9 forecast paths per loan type (3 scenarios times 3 models = 9).

**Fan charts:** Instead of showing 9 separate lines (confusing), we show the *median* of the 3 scientific models for each scenario, with a shaded band showing the range. This gives a visual sense of both "which scenario is best/worst" and "how uncertain are we within each scenario."

### Step 9: Cumulative Impact (translating growth rates to dollar terms)

Growth rates are useful for modeling but hard to explain to an executive. "3.6% annual growth" means what, exactly?

So we convert growth rates into a **balance index**. We set 2025 = 100 (today's loan balance). Then each year, we apply the forecasted growth rate. By 2050, the index tells you: "Loans will be X% of today's level."

**The headline results:**

| Loan Type | Scenario | 2050 Balance (2025 = 100) |
|-----------|----------|--------------------------|
| C&I | Net Zero | **243** (loans are 2.43x today's level) |
| C&I | Delayed Transition | 226 |
| C&I | NDCs | 229 |
| Consumer | Net Zero | 351 |
| Consumer | Delayed Transition | **410** (loans are 4.1x today's level) |
| Consumer | NDCs | 385 |

### The Most Important Finding

**C&I and consumer loans respond in OPPOSITE directions to climate policy:**

- **C&I loans do BEST under Net Zero** (the aggressive policy). Why? Because Net Zero keeps unemployment low through gradual transition, and unemployment is what drives business lending.

- **Consumer loans do BEST under Delayed Transition** (the wait-then-panic policy). Why? Because Delayed Transition keeps long-term interest rates lower for longer, and long-term rates are what drive consumer borrowing costs.

This creates a genuine strategic dilemma: there is no single "best" scenario for the entire loan book. What's good for one half is bad for the other.

The difference is material:
- Under Delayed Transition, C&I loans are 7.1% LOWER than under Net Zero
- Under Delayed Transition, consumer loans are 16.8% HIGHER than under Net Zero

This is exactly the kind of insight BofA said they want — not just "loans go up or down" but "here's a tension that executives need to think about."

### Step 10: Diagnostics (did everything work?)

Final sanity checks:
- Residuals pass Ljung-Box test (no leftover patterns) for both models
- Residuals are stationary (ADF test p < 0.0001)
- All 9 forecast paths per loan type generated successfully (no NaN, no blanks)
- All 8 figures saved correctly
- Summary table has 18 rows (2 loan types x 3 scenarios x 3 time horizons) with zero missing values

Everything checks out.

---

## What Each Notebook Gives to the Next

```
NOTEBOOK 1 teaches us:                    NOTEBOOK 3 uses this to:
─────────────────────                     ─────────────────────
"Work in growth rates, not levels"    →   Transform all data to growth rates
"AR(4) is the baseline to beat"       →   Compare VAR against AR(4)
"COVID needs a dummy variable"        →   Include COVID dummy in VAR
"Unemployment and rates matter"       →   Put them in the VAR

NOTEBOOK 2 teaches us:                    NOTEBOOK 3 uses this to:
─────────────────────                     ─────────────────────
"NiGEM has the economic variables"    →   Read from the NiGEM file
"Baseline = levels, others = diffs"   →   Reconstruct scenario paths correctly
"5 variables map to FRED"             →   Use same 5 variables in VAR
"3 scientific models available"       →   Run each scenario through all 3
```

---

## Glossary

| Term | What it means |
|------|--------------|
| **ADF test** | A statistical test that checks whether a data series is "wandering randomly" (non-stationary) or has a stable average (stationary). If it's wandering, you need to transform it before modeling. |
| **AR model** | "Autoregressive" model. Predicts the future using past values of the same series. AR(4) uses the last 4 time periods. |
| **BIC** | A scoring system for models that rewards good fit but penalizes complexity. Lower BIC = better model. Prevents overfitting. |
| **C&I loans** | Commercial and Industrial loans. Money banks lend to businesses. |
| **Cholesky ordering** | A technical choice about which variables respond to shocks first when computing IRFs. We put loans first (they react slowest) and macro variables after. |
| **Consumer loans** | Money banks lend to individuals. Includes auto loans, credit cards, personal loans. |
| **COVID dummy** | A variable that is 1 during COVID (2020-2021) and 0 otherwise. Lets the model adjust for COVID without throwing away those years. |
| **Cross-correlation** | Measures whether two series move together. If unemployment goes up and loan growth goes down at the same time (or with a lag), they're cross-correlated. |
| **Fan chart** | A visualization that shows a forecast line with a shaded band around it representing uncertainty. Wider band = more uncertain. |
| **FRED** | Federal Reserve Economic Data. A public database of US economic statistics. Free for anyone to access. |
| **Granger causality** | A test that asks: "Does knowing the past of variable X help predict variable Y, beyond what Y's own past tells you?" Named after Nobel laureate Clive Granger. |
| **Growth rate** | The percentage change from one period to the next. We use log growth: `100 × ln(today/yesterday)`. |
| **IAM** | Integrated Assessment Model. A scientific model that simulates the interaction between the economy, energy system, and climate. |
| **IRF** | Impulse Response Function. Shows what happens to one variable over time after a sudden shock to another. Like ripples in a pond. |
| **KPSS test** | A statistical test that checks whether a series is stationary. Opposite null hypothesis from ADF — both agreeing gives stronger evidence. |
| **Ljung-Box test** | Checks whether the errors from a model have any leftover patterns. If p > 0.05, the residuals are "clean" and the model hasn't missed anything obvious. |
| **MIDAS** | Mixed Data Sampling. A technique for combining data at different frequencies (like monthly loans with annual climate data) without forcing everything to the same frequency. |
| **NGFS** | Network for Greening the Financial System. A group of 121 central banks that created standardized climate scenarios. |
| **NiGEM** | National Institute Global Econometric Model. The macro model used by NGFS to project how climate scenarios affect GDP, unemployment, rates, etc. |
| **OOS evaluation** | Out-of-sample evaluation. Testing a model on data it wasn't trained on, to see if it actually predicts well (not just fits the past well). |
| **p-value** | The probability that the result is due to random chance. p < 0.05 means "probably real." p < 0.001 means "almost certainly real." p > 0.05 means "could be random noise." |
| **RMSE** | Root Mean Squared Error. The average size of prediction errors. Lower = better predictions. |
| **Stationarity** | A series is "stationary" if its behavior is consistent over time — same average, same variability. Non-stationary series trend or wander, making them harder to predict. |
| **VAR model** | Vector Autoregression. Like AR but for multiple variables at once. Captures how variables affect each other over time. |
| **z-score** | How many standard deviations a value is from the average. z = 0 is perfectly average. z = 2 is unusual. z = 13.9 is essentially impossible under normal conditions. |
