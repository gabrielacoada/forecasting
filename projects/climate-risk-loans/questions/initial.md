# Research Questions: How Do NGFS Climate Scenarios Impact Banking Loan Portfolios?

## Primary Question
**How can NGFS climate scenario data be used to forecast the impact of climate risk on aggregate commercial (BUSLOANS) and consumer (CONSUMER) loan portfolios in the U.S. banking industry?**

## Supporting Questions

### Q1: What are the NGFS climate scenarios and what variables do they contain?
- Type: factual
- Priority: high
- Likely sources: web (NGFS portal documentation), course materials
- Status: unanswered
- Notes: Need to understand scenario narratives (Net Zero 2050, Delayed Transition, Current Policies, etc.), model families (GCAM, REMIND, MESSAGEix), and available variables (carbon prices, GDP, temperature, CO2 emissions, energy costs). Critical foundation for all downstream work.

### Q2: What is the theoretical transmission mechanism from climate risk to bank loan portfolios?
- Type: analytical
- Priority: high
- Likely sources: academic papers (Acharya et al. 2023, Jung et al. 2024), web
- Status: unanswered
- Notes: Must establish the causal chain — how do physical risks and transition risks (carbon taxes, policy changes, GDP shocks) flow through to commercial and consumer credit? Distinguishing direct vs. indirect channels.

### Q3: What macroeconomic variables mediate the climate-to-loans relationship?
- Type: analytical
- Priority: high
- Likely sources: academic papers, FRED documentation, course materials
- Status: unanswered
- Notes: Identify which FRED macro series (unemployment, CPI, interest rates, GDP) serve as intermediate variables linking NGFS scenario outputs to loan portfolio dynamics. Feature selection with economic rationale is a key evaluation criterion.

### Q4: What are the key data characteristics and challenges for modeling this relationship?
- Type: methodological
- Priority: high
- Likely sources: FRED data exploration, NGFS data exploration, course materials
- Status: unanswered
- Notes: Frequency mismatch (NGFS annual vs. FRED monthly/quarterly), time series stationarity, structural breaks (COVID), training window selection, regional vs. national granularity. How do different NGFS model families compare?

### Q5: What forecasting frameworks are appropriate for climate stress testing of loan portfolios?
- Type: methodological
- Priority: high
- Likely sources: course materials (AR, ARMA, ARIMA, VAR), academic papers, web
- Status: unanswered
- Notes: Must be transparent and explainable (no black-box ML). Consider: VAR models for multivariate relationships, scenario-conditional forecasting, bridge equations. How does the course methodology (weeks 1-5: trends, seasonality, ARMA, dynamic causal effects) apply here?

### Q6: How have regulators and central banks approached climate stress testing?
- Type: factual
- Priority: medium
- Likely sources: web (ECB, Fed publications), academic papers
- Status: unanswered
- Notes: European vs. U.S. regulatory timelines. ECB climate stress tests, Fed's 2023 pilot exercise (rescinded in 2025). What methodologies did they use? What can we learn from their frameworks?

### Q7: How do loan portfolio outcomes differ across NGFS scenarios?
- Type: comparative
- Priority: medium
- Likely sources: analysis of model outputs, academic papers
- Status: unanswered
- Notes: Compare Net Zero 2050 vs. Delayed Transition vs. Current Policies. Which scenarios pose the greatest risk to commercial vs. consumer loans? Are transition risks or physical risks more impactful?

### Q8: What are the implications for financial stability and risk management?
- Type: analytical
- Priority: medium
- Likely sources: synthesis of findings, academic papers, regulatory publications
- Status: unanswered
- Notes: Translate model results into strategic insights for bank executives and regulators. What portfolio adjustments or hedging strategies might be warranted? This is the "so what?" that BofA sponsors care about.
