# Comprehensive Analysis: Climate Risk Impact on Banking Loan Portfolios
Date: 2026-02-12
Factbase: ~291 facts from 7 sources

## Executive Summary

NGFS climate scenarios provide a structured, publicly available framework for assessing how climate change -- through both physical and transition risk channels -- could affect U.S. banking loan portfolios. Drawing on 291 extracted facts across seven source categories (the Emory case study PDF, BofA kickoff transcript, course materials from Weeks 3-5, NGFS and transmission mechanism research, stress testing methods literature, FRED data documentation, and two NY Fed academic papers), this analysis establishes that the standard approach to climate stress testing follows a two-stage "cascade": (1) NGFS scenario variables (carbon prices, GDP paths, temperature trajectories) feed into macroeconomic mediating variables (GDP growth, unemployment, inflation, interest rates), and (2) those macro variables drive loan portfolio outcomes via historically estimated relationships. The most critical mediating variables are GDP growth (procyclical with lending), unemployment (key for consumer defaults), and interest rates (affecting both loan demand and credit quality). This approach is well supported by both the academic literature (Acharya et al. 2023, Jung et al. 2024) and regulatory practice (ECB 2022 climate stress test, Fed 2023 CSA pilot, Bank of England CBES 2022).

Across all major exercises and both reference papers, a consistent finding emerges: disorderly transition scenarios (especially Delayed Transition) pose the greatest short-to-medium-term financial risk to banks because abrupt carbon price shocks create sharper GDP contractions and unemployment spikes, amplifying credit losses. Orderly scenarios (Net Zero 2050, Below 2C) produce lower peak losses because gradual policy allows time for adaptation. Hot house world scenarios (Current Policies) defer costs but accumulate severe long-run physical risk. For this project, a VAR or autoregressive distributed lag (ADL) model trained on historical FRED data -- linking BUSLOANS and/or CONSUMER to GDP, unemployment, CPI, and interest rates -- and then conditioned on NGFS macro-financial paths represents the most defensible, transparent, and course-aligned approach. Key practical challenges include the annual-vs-monthly frequency mismatch between NGFS and FRED data, the COVID-19 structural break in lending series, and the deep uncertainty inherent in compounding multiple layers of models over 30-year horizons.

This analysis is designed to be directly actionable for the semester project: every claim is traced to specific facts, recommendations are connected to applicable course methods, and confidence levels reflect the strength and convergence of the underlying evidence. The goal is not a perfect forecast but a defensible, transparent, and well-communicated framework for understanding how climate scenarios could reshape the aggregate lending landscape.

---

## Question-by-Question Analysis

### Q1: What are the NGFS climate scenarios and what variables do they contain?

**Answer confidence**: strong

The NGFS (Network for Greening the Financial System) is a coalition of over 130 central banks and financial supervisors that develops climate scenarios for financial sector risk assessment. Crucially, these scenarios are not forecasts or predictions -- they are "what-if" explorations of how climate policy and physical outcomes might unfold and affect the economy (web-ngfs Fact 1). The framework organizes scenarios along two dimensions: the level of physical risk (driven by temperature outcomes) and the level of transition risk (driven by the speed and coordination of climate policy) (web-ngfs Fact 2).

As of Phase IV (November 2023), the NGFS defines six representative scenarios grouped into three risk categories (web-ngfs Facts 3-4):

- **Orderly scenarios**: Net Zero 2050 (limiting warming to 1.5C through immediate stringent policies, reaching net-zero CO2 around 2050) and Below 2C (gradually increasing policy stringency). These minimize both physical and transition risk through early, gradual action.
- **Disorderly scenarios**: Divergent Net Zero (reaches net zero by 2050 but with uncoordinated sector-specific policies creating higher costs) and Delayed Transition (no new policy until 2030, then abrupt strong action). These produce high transition risk from late or uncoordinated policy.
- **Hot house world scenarios**: Nationally Determined Contributions (current Paris pledges only, ~2.5C warming) and Current Policies (no new action, 3C+ warming). These produce severe long-term physical risk but low transition risk.

The scenarios are produced by three Integrated Assessment Model (IAM) families -- GCAM, REMIND-MAgPIE, and MESSAGEix-GLOBIOM -- each generating different numerical paths for the same scenario narrative due to different modeling assumptions about technology, economics, and substitution (web-ngfs Fact 5-6). The NGFS data portal provides variables across multiple categories: emissions (CO2, CH4, N2O by sector), carbon prices ($/tCO2), energy (primary and final energy by fuel type, energy prices), GDP (PPP or market terms), investment (energy infrastructure CapEx), temperature change, and land use (web-ngfs Fact 7). In Phase IV, the NiGEM macroeconomic model translates IAM outputs into financial-system-relevant variables at the country level: GDP growth, CPI inflation, unemployment rate, short- and long-term interest rates, exchange rates, equity prices, and government debt (web-ngfs Fact 8). Data is annual, with projections typically running from ~2020 to 2050 or 2100 (web-ngfs Fact 9), and is downloadable as CSV files in ZIP format from the IIASA portal (web-ngfs Fact 40; case-study Fact 10).

Carbon price is the single most important distinguishing variable across scenarios: under Net Zero 2050, it may rise to $200-$800+/tCO2 by 2050; under Current Policies, it remains near zero; under Delayed Transition, it jumps sharply around 2030 (web-ngfs Fact 10; academic Fact 25). GDP impacts also vary significantly, with orderly scenarios showing modest losses of a few percent by 2050, disorderly scenarios showing larger short-term disruptions, and hot house world scenarios potentially showing 10-25% GDP losses by end of century under severe damage function assumptions (web-ngfs Fact 11).

**Supporting evidence**:
- web-ngfs Fact 1: "NGFS scenarios are not forecasts or predictions; they are 'what-if' explorations"
- web-ngfs Facts 3-4: Six scenarios in three categories with full descriptions
- web-ngfs Facts 5-6: Three IAM families with structural differences
- web-ngfs Facts 7-9: Variable categories, NiGEM macro-financial extensions, annual frequency
- web-ngfs Fact 10: Carbon price as distinguishing variable ($200-$800+/tCO2 range)
- web-ngfs Fact 33: Structured data format with pipe-delimited variable hierarchy
- case-study Facts 6, 10, 17, 24: Scenario portal links, multiple model families, quantitative pathways
- kickoff Facts 7, 16, 22: NGFS macro and climate variables, zip file format
- academic Fact 6: NGFS Phase III scenario descriptions used in Acharya et al.

**Contradicting or qualifying evidence**:
- web-ngfs Fact 37: Different IAM families can produce "meaningfully different quantitative outputs" for the same scenario, creating model uncertainty that must be acknowledged.
- web-ngfs Fact 38: Scenarios are designed for financial stability assessment, not investment decisions; probability of any scenario materializing is not specified.
- academic Fact 14: Results are sensitive to IAM choice, since different models produce different GDP and carbon price paths for the same narrative.

---

### Q2: What is the theoretical transmission mechanism from climate risk to bank loan portfolios?

**Answer confidence**: strong

Climate risks transmit to bank loan portfolios through two primary channels -- physical risk and transition risk -- operating via both direct and indirect mechanisms. This transmission framework is well established across the academic literature and regulatory practice.

**Physical risk** affects lending through direct asset damage from extreme weather (property destruction, business interruption, supply chain disruption), reduced collateral values, and increased insurance costs (web-ngfs Fact 12; kickoff Fact 3, 39). For banks, this is most relevant for commercial real estate lending and for businesses operating in geographically vulnerable areas (kickoff Fact 11; academic Fact 19).

**Transition risk** affects lending through policy-driven cost increases (carbon taxes raising operating costs), stranded assets in fossil-fuel sectors, shifts in consumer demand away from carbon-intensive products, regulatory compliance costs, and macroeconomic disruption from structural economic transformation (web-ngfs Fact 12; kickoff Facts 3, 38; academic Fact 18).

The critical conceptual distinction is between **direct** and **indirect** channels (web-ngfs Fact 14). The direct channel: climate events or policies directly affect a specific borrower's ability to repay (a flooded factory cannot generate revenue; a coal company faces higher carbon costs). The indirect channel: climate risks affect the broader macroeconomy (lower GDP, higher unemployment, higher inflation), which increases default rates across the entire loan portfolio, even for borrowers not directly exposed to climate risk.

For **commercial and industrial (C&I) loans** specifically, the key transmission channels are: carbon pricing increasing operating costs for carbon-intensive borrowers; energy price shifts changing input costs; GDP growth slowdowns reducing business revenue; interest rate changes affecting debt servicing; and physical damage disrupting operations (web-ngfs Fact 16). Jung et al. (2024) find that C&I loans are the loan category most directly exposed to transition risk because they are industry-classified and include loans to carbon-intensive firms (academic Fact 37). Approximately 10-15% of large U.S. banks' total loan portfolios are allocated to high-carbon-intensity industries (academic Fact 29).

For **consumer loans**, the transmission is primarily indirect through macroeconomic channels: unemployment from economic restructuring reduces household income; inflation from carbon pricing erodes purchasing power; energy cost increases reduce disposable income; and interest rate changes affect affordability of variable-rate debt (web-ngfs Fact 17; stress-testing Fact 32).

The standard approach used by central banks and in the academic literature follows a "cascade" or "waterfall" structure: (1) IAMs produce climate and energy outputs; (2) NiGEM translates these into macro-financial variables; (3) banks use those macro variables as inputs to credit risk models to estimate loan losses (web-ngfs Fact 19; academic Facts 3-4; stress-testing Fact 1).

A critical insight from the course materials is that **endogeneity affects causal interpretation but NOT forecast quality** (course Fact 44). For this project's forecasting goal, even if the relationship between macro variables and loans involves simultaneity, standard regression approaches can still produce good conditional forecasts. We do not need to identify the exact causal mechanism, only the predictive relationship (course Fact 48).

**Supporting evidence**:
- web-ngfs Facts 12-14: Two risk channels, direct vs. indirect, full transmission framework
- web-ngfs Facts 16-17: Specific C&I and consumer loan transmission channels
- web-ngfs Fact 19: Three-stage cascade (IAM -> NiGEM -> credit risk models)
- kickoff Facts 3, 4, 11, 38, 39: Physical vs. transition risk definitions and banking examples
- academic Facts 2, 4, 10, 18-19: Acharya et al. transmission chain
- academic Facts 26, 30, 35, 37: Jung et al. on industry-level and loan-type transmission
- case-study Facts 1, 8: Two risk channels and macro variable influence
- course Facts 14, 44, 48: Forecasting vs. causal interpretation distinction
- stress-testing Facts 1, 22: Two-stage satellite model approach

**Contradicting or qualifying evidence**:
- web-ngfs Fact 35: NGFS scenarios do NOT directly model banking outcomes -- the translation step is what the project must build.
- academic Fact 15: Deep uncertainty in compounding multiple model layers (climate -> IAM -> macro -> credit).
- academic Fact 22: Static balance sheet assumption does not capture banks' adaptive behavior.

---

### Q3: What macroeconomic variables mediate the climate-to-loans relationship?

**Answer confidence**: strong

There is strong convergence across all sources on the key mediating macroeconomic variables. The case study PDF explicitly identifies GDP growth, unemployment, inflation (CPI), carbon prices, and energy use as "most relevant to the banking sector" (case-study Fact 7; fred Fact 12). The academic literature and stress testing frameworks confirm and extend this list.

**GDP growth** is the single most important mediating variable. Loan growth is procyclical -- bank lending expands during booms and contracts during recessions (web-ngfs Fact 27). GDP captures the aggregate demand channel and is consistently the most statistically significant predictor of aggregate loan volumes in both academic studies and regulatory stress tests (fred Fact 13; academic Fact 46). The relevant FRED series include GDPC1 (real GDP, chained 2017 dollars, quarterly) and A191RL1Q225SBEA (real GDP growth rate) (fred Fact 13). NGFS NiGEM outputs provide U.S.-specific GDP growth paths under each scenario (web-ngfs Fact 25).

**Unemployment rate** is particularly critical for consumer loan portfolios. Higher unemployment directly reduces household income and increases default probability on consumer debt (web-ngfs Fact 28). Under NGFS scenarios with abrupt transitions, unemployment may spike as workers in carbon-intensive industries are displaced. The FRED series is UNRATE (monthly, seasonally adjusted) (fred Fact 14). Course materials show unemployment has an AR(1) coefficient of ~0.95, indicating very persistent dynamics that must be modeled carefully (fred Fact 33; course Fact 24).

**Interest rates** serve a dual role: monetary policy responses to climate-driven inflation tighten financial conditions and reduce loan demand, while climate risk premia increase borrowing costs (web-ngfs Fact 29). Key FRED series include FEDFUNDS (Federal Funds Rate), DGS10 (10-Year Treasury yield), and the yield curve spread T10Y2Y (fred Facts 15, 29). NGFS NiGEM outputs include U.S. short- and long-term interest rate paths (web-ngfs Fact 25).

**Inflation / CPI** acts as a transmission channel because carbon pricing creates cost-push inflationary pressure. Higher inflation erodes real incomes (affecting consumer loan repayment) and may trigger monetary tightening (web-ngfs Fact 36; fred Fact 16). FRED series include CPIAUCSL (CPI) and PCEPI (PCE price index).

**Carbon prices** are the direct policy instrument for transition risk and the primary variable distinguishing NGFS scenarios (web-ngfs Fact 10; academic Fact 25). Carbon prices are available directly from the NGFS data portal. Since historical U.S. carbon prices have been minimal, carbon price may need to be treated as an exogenous scenario input rather than a historically estimated relationship, or mapped to energy costs as a proxy (fred Fact 30).

**Energy prices** affect both business input costs and household budgets. FRED provides crude oil (DCOILWTICO), natural gas (DHHNGSP), and electricity price series (fred Fact 38). These can supplement or proxy for NGFS energy variables.

Additional secondary variables worth considering include corporate bond spreads (BAA10Y, indicating credit conditions and financial stress -- fred Fact 31), industrial production (INDPRO), bank lending standards from SLOOS surveys (DRTSCILM -- fred Fact 32), and financial conditions indices (NFCI -- fred Fact 29).

The kickoff transcript notes that "the macro variables and all that is going to be a little bit different" for consumer vs. commercial loans (kickoff Fact 29; fred Fact 11). Consumer loans are more driven by unemployment, household income, and consumer confidence, while C&I loans are more driven by business investment, corporate profitability, and trade conditions.

**Supporting evidence**:
- case-study Fact 7: Explicit list of relevant macro variables
- web-ngfs Facts 18, 25, 27-29, 32, 36: Detailed variable-by-variable transmission analysis
- fred Facts 12-16, 29-31, 38: FRED series identifiers and economic rationale
- academic Facts 5, 46: GDP, unemployment, and carbon prices as three most critical variables
- academic Fact 37: C&I loans most exposed to transition risk; consumer loans to macro channels
- kickoff Fact 29: Macro variables differ between commercial and consumer
- stress-testing Fact 38: Bridge variable mapping from NGFS to FRED

**Contradicting or qualifying evidence**:
- fred Fact 35: Macro variables like GDP and interest rates are endogenous with respect to bank lending, requiring VAR-style models rather than simple regressions for proper treatment.
- course Fact 29: Fed Funds rate is NOT exogenous to GDP; unemployment is NOT exogenous to inflation. These simultaneity concerns argue for VAR models.

---

### Q4: What are the key data characteristics and challenges for modeling this relationship?

**Answer confidence**: strong

Multiple significant data challenges have been identified across sources, and addressing them thoughtfully is a key evaluation criterion for this project.

**Frequency mismatch**: NGFS scenario data is annual. BUSLOANS and CONSUMER are monthly. GDP is quarterly. This is flagged as a critical challenge by the case study, the kickoff transcript, and the academic literature (web-ngfs Fact 24; fred Fact 21; stress-testing Fact 28, 42). Solutions include: (a) aggregating FRED data to annual frequency to match NGFS -- simplest but loses information; (b) interpolating NGFS annual data to quarterly/monthly using cubic spline, linear interpolation, or Denton-Cholette temporal disaggregation; or (c) using mixed-frequency models such as MIDAS regression (web-ngfs Fact 24). The recommended practical approach is a two-stage framework: estimate the historical model at quarterly frequency using FRED data, then feed annually-interpolated NGFS paths through the model (fred Fact 39).

**Non-stationarity**: BUSLOANS and CONSUMER are nominal dollar-denominated level series with strong upward trends and are almost certainly non-stationary in levels (fred Fact 5). Standard practice requires transformation -- typically log-differencing to get growth rates, or deflating by CPI and then differencing. Unit root tests (ADF, PP, KPSS) should be applied to confirm (course Facts 6, 13, 19). The course materials emphasize that stationarity is a prerequisite for modeling cycles (course Fact 13) and that testing for unit root "is traditionally the first step in time series analysis" (course Fact 19).

**COVID-19 structural break**: The PPP loan spike in BUSLOANS (approximately $700 billion in a matter of weeks in March-June 2020) is a major structural break that does not reflect normal business-cycle dynamics (fred Fact 6). The CONSUMER series shows a different but also anomalous COVID pattern. This was explicitly flagged as a key modeling question by the BofA team: "We regularly ask people doing models, how do you treat the COVID period?" (kickoff Facts 33-34; fred Fact 24). Options include excluding the COVID period, using dummy variables, modeling pre/post-COVID separately, or winsorizing extreme observations. The course materials note that structural breaks violate weak stationarity and "we cannot forecast a structural break, but we can model it and forecast the detrended data" (course Fact 45).

**Training window selection**: This is explicitly a design choice (kickoff Fact 30). The window must balance covering enough business cycles for robust estimation (kickoff Fact 32) against including structural regime changes that make older data less relevant. Some FRED series go back to the 1940s while others only to the 1990s, constraining the effective window (kickoff Fact 31; fred Fact 22). The Great Moderation (~1984-2007) represents a period of reduced volatility, and starting in the mid-1980s or early 1990s is common in applied models (fred Fact 27). The 2008 GFC is another major structural break where C&I loans contracted ~25% (fred Fact 28).

**Multiple NGFS model families**: The three IAMs (GCAM, REMIND, MESSAGEix) produce meaningfully different outputs for the same scenario. For example, REMIND tends to project higher carbon prices than GCAM (web-ngfs Fact 37; academic Fact 14). Comparing results across model families adds robustness (case-study Facts 16-17).

**National-level aggregation**: BUSLOANS and CONSUMER are national aggregates with no regional or sector-level breakdown, limiting the ability to capture the geographic heterogeneity of climate impacts (fred Fact 25). The case study acknowledges "improved sectoral granularity" as an area for refinement (case-study Fact 20).

**Data revision artifacts**: The FRED H.8 data underwent a methodological revision in March 2010, potentially creating apparent level shifts unrelated to economic changes (fred Fact 40).

**Supporting evidence**:
- web-ngfs Fact 24: Frequency mismatch and interpolation methods
- fred Facts 5-6, 10, 21-28, 33, 37, 39-40: Comprehensive data characteristics
- kickoff Facts 20, 22, 30-34: Data challenges discussed in kickoff
- case-study Facts 9, 11, 17, 19: Data sources and limitations
- course Facts 2, 6, 11, 13, 19, 35, 39, 45: Stationarity, transformations, structural breaks, subsample instability
- stress-testing Facts 28, 42: Frequency mismatch in stress testing literature
- academic Facts 14, 21, 40, 50: IAM sensitivity, frequency challenges, data gaps

**Contradicting or qualifying evidence**:
- None directly contradicting. The challenge is that all sources agree these are genuine obstacles with no single correct resolution, which is itself informative: the project must demonstrate awareness and justify choices.

---

### Q5: What forecasting frameworks are appropriate for climate stress testing of loan portfolios?

**Answer confidence**: strong

The evidence strongly converges on a **scenario-conditional forecasting framework** using transparent, interpretable time series models. This approach is supported by the academic literature, regulatory practice, and course methodology.

**Core approach: Two-stage conditional forecasting**. The recommended framework has two steps (stress-testing Facts 22-23, 37; academic Facts 20, 47; web-ngfs Fact 26, 34):

1. **Stage 1 (Historical estimation)**: Estimate the historical relationship between macroeconomic variables (GDP growth, unemployment, CPI, interest rates) and loan portfolio outcomes (BUSLOANS growth, CONSUMER growth) using FRED data and time series methods from the course.
2. **Stage 2 (Scenario projection)**: Take NGFS-provided macro-financial scenario paths as given (exogenous scenario inputs) and feed them through the estimated model to generate conditional loan forecasts under each NGFS scenario.

This approach parallels the Federal Reserve's CCAR/DFAST stress testing methodology, adapted for climate-specific scenarios and longer horizons (stress-testing Fact 4; academic Fact 20). It is also how the ECB, Bank of England, and the six largest U.S. banks approached their respective climate stress tests (stress-testing Facts 17, 19-20, 24; academic Fact 47).

**Model class recommendations**, grounded in course methodology:

- **VAR (Vector Autoregression)**: The most strongly recommended framework for capturing the dynamic interdependencies among multiple macro variables and loan growth jointly (stress-testing Fact 21; course Fact 38). VAR models are "transparent and interpretable" (stress-testing Fact 35), capture feedback effects between variables (important since GDP and lending are simultaneously determined -- fred Fact 35), and are previewed in the course as "the same autoregressive model but in vector form" (course Fact 38).

- **ADL (Autoregressive Distributed Lag)**: An alternative single-equation approach that includes lagged dependent variables and lagged macro regressors (course Fact 43). More efficient than a pure distributed lag model when strict exogeneity holds, and combines the AR structure with explicit modeling of how macro shocks propagate through lags to loan outcomes.

- **Distributed Lag Models**: Directly estimate how a change in a macro variable (e.g., GDP) affects loans over multiple future periods (course Fact 27). The impulse response framework provides a natural interpretation for how climate shocks propagate to loan portfolios over time (course Fact 46). Require HAC standard errors if not combined with autoregressive terms (course Facts 31-33).

- **AR/ARMA as baseline**: Most time series need at least an AR(1) and often not more than AR(2) (course Fact 12). "AR terms are your best friends when it comes to forecasting" (course Fact 12). Starting with a univariate AR model as a baseline, then adding macro regressors to assess marginal forecasting value, is a sound model-building strategy consistent with the Box-Jenkins approach (course Fact 20).

**Model selection process** should follow the Pesavento practical recipe (course Fact 20): (1) make data stationary, (2) plot the correlogram, (3) use ACF/PACF as starting point, (4) start LARGE and eliminate small, (5) estimate and check significance, (6) compare with AIC/BIC, (7) plot residual correlograms, (8) iterate.

**Transparency and explainability** are "extremely important" (kickoff Fact 13). Complex black-box ML models are explicitly inappropriate -- the audience is regulators and executives making strategic decisions. This constraint aligns with regulatory expectations across all climate stress testing exercises (stress-testing Fact 35).

**Key methodological points from the course**:
- Endogeneity does not ruin forecasts (course Fact 44) -- even biased coefficients can produce good predictions.
- HAC (Newey-West) standard errors should be used as default for distributed lag regressions but are usually unnecessary for ADL models with sufficient AR lags (course Facts 32-33).
- Subsample instability (course Fact 35) is a real concern and should be tested.
- Information criteria (AIC/BIC) should guide model comparison (course Fact 23).
- In-sample or out-of-sample evaluation is required (case-study Fact 15).

**Important limitations**: Both Acharya et al. and the BIS note that linear VAR models may underestimate tail risks from climate change because of nonlinearities, tipping points, and irreversibilities (stress-testing Fact 41; academic Fact 17). Results should be interpreted as illustrative of relative risk magnitudes, not precise point forecasts (academic Fact 15, 24).

**Supporting evidence**:
- stress-testing Facts 1, 4, 21-23, 35, 37: Two-stage approach, VAR, bridge equations, transparency
- academic Facts 3-4, 15, 20-21, 24, 47: Scenario-conditional forecasting framework
- web-ngfs Facts 26, 34: Standard two-step methodology
- course Facts 12, 14-15, 17-25, 27, 31-33, 38, 40-48: AR/ARMA models, distributed lags, VAR preview, HAC, model selection recipe
- kickoff Facts 13-14, 18-19, 27, 35: Transparency, no single correct answer, methodology over accuracy
- case-study Facts 4-5, 12-15, 21: Forecasting framework design, model evaluation, deliverables
- fred Facts 30, 34-36, 39: Bridge variables, distributed lag analogy, two-stage framework

**Contradicting or qualifying evidence**:
- stress-testing Fact 41: Linear models may underestimate tail risks. Results are lower bounds.
- academic Fact 17: Historical macro-credit relationships may not hold under structural transformation.
- stress-testing Fact 25: Existing bank models are not well-suited for the 30+ year horizons required.

---

### Q6: How have regulators and central banks approached climate stress testing?

**Answer confidence**: strong

The regulatory landscape for climate stress testing has evolved rapidly since the early 2020s, with European regulators leading and the U.S. following more recently.

**European regulators led early**. The NGFS, formed as a coalition of central banks and supervisors, developed both long-term and short-term climate scenarios for financial institution stress testing (kickoff Fact 7). The European Banking Agency signaled interest in incorporating climate risk into supervisory expectations in the early 2020s, requiring banks to take climate scenarios, examine their balance sheets, and assess potential risk (kickoff Facts 6, 8). The EBA published guidelines requiring EU banks to incorporate ESG risks into their internal capital adequacy assessment by 2024 (stress-testing Fact 31).

**ECB 2022 Climate Stress Test**: The ECB conducted its first climate stress test covering 104 significant institutions across three NGFS scenarios over a 30-year horizon to 2050 (stress-testing Fact 17). The exercise used both top-down (ECB models) and bottom-up (banks' own models) components (stress-testing Fact 19). Banks were required to map NGFS macro variables to PD and LGD for their loan portfolios. Key findings: under disorderly transition, aggregate credit losses of approximately EUR 70 billion; orderly scenario losses were 30-40% lower (stress-testing Fact 18). The exercise revealed that many banks lacked granular data on climate vulnerability and that short-term transition risks created larger near-term losses than orderly scenarios (web-ngfs Fact 20). Banks without dedicated climate models relied on "bridge equations" linking NGFS macro variables to credit risk parameters (stress-testing Fact 20).

**Bank of England CBES (2022)**: Among the first central bank climate stress tests, testing three scenarios over 30 years. Found climate risks could generate cumulative losses of up to 10-15% of annual profits, with Late Action (disorderly) producing the largest losses (stress-testing Fact 24). The exercise revealed banks' existing models were not suited for 30+ year horizons (stress-testing Fact 25).

**U.S. Federal Reserve**: Signaled interest around 2022, and in 2023 launched its Climate Scenario Analysis pilot involving the six largest U.S. banks (Bank of America, Citigroup, Goldman Sachs, JPMorgan Chase, Morgan Stanley, Wells Fargo) (stress-testing Fact 12). The exercise tested physical risk (hurricane impact on real estate) and transition risk (net-zero economy impact on corporate lending) (stress-testing Fact 13), using a substantially longer horizon than the typical 9-quarter CCAR/DFAST stress test (stress-testing Fact 14). The 2024 results summary found banks are in "early stages" with significant methodological variation (stress-testing Fact 15). However, the Fed rescinded the CSA requirement in early 2025 (kickoff Fact 10; stress-testing Fact 16).

**The rescission does not eliminate the need**. As the BofA team noted, climate stress testing is still "a strong signal that climate stress testing will become more ubiquitous" (kickoff Fact 10). European regulators continue to advance requirements, and climate risks remain financially material regardless of regulatory mandates (kickoff Fact 5).

**Current state of practice**: There is no established standard method (kickoff Fact 14). Everyone "treats it differently and is still thinking about how to execute" (kickoff Fact 27). The BofA team does not currently work on climate risk for the bank -- this is exploratory (kickoff Fact 26). This means the project is addressing a genuinely open question in banking practice.

**Supporting evidence**:
- kickoff Facts 5-10, 14, 26-27: Regulatory timeline, rescission, exploratory nature
- stress-testing Facts 12-20, 24-25, 30-31, 36: Fed CSA pilot, ECB, BoE details
- web-ngfs Facts 20-21: ECB and Fed exercise summaries
- academic Facts 16-17, 42, 47-49: Regulatory references in academic papers
- case-study Facts 2-3: Regulators use NGFS, transparency concerns

**Contradicting or qualifying evidence**:
- The 2025 rescission of the Fed's CSA could be interpreted as reduced urgency. However, all sources agree the underlying financial risks persist and European requirements continue.

---

### Q7: How do loan portfolio outcomes differ across NGFS scenarios?

**Answer confidence**: moderate

While the directional findings are clear and consistent across sources, exact quantitative loan portfolio outcomes depend on model specification, IAM choice, and scenario vintage, and have not yet been computed for this specific project. The evidence provides strong qualitative and semi-quantitative guidance.

**Delayed Transition poses the greatest short-to-medium-term risk**. This is the single most consistent finding across all sources (academic Facts 7, 11, 36, 45; stress-testing Facts 3, 10, 26, 40, 45; web-ngfs Fact 22). The abrupt carbon price shock around 2030 creates the sharpest GDP contraction and unemployment spike, amplifying credit losses. Peak GDP losses of 2-5% relative to baseline are estimated for the 2030-2040 period (stress-testing Fact 26). The IMF estimates disorderly transition could increase corporate loan default rates by 3-4 percentage points for the most carbon-intensive sectors (stress-testing Fact 34).

**Orderly scenarios (Net Zero 2050, Below 2C) produce lower peak losses**. Gradual carbon price increases and early policy action allow firms and banks to adjust over time (academic Fact 8). GDP growth is modestly lower than Current Policies in the near term but avoids severe long-run physical damages (stress-testing Fact 40). ECB exercise found orderly scenario losses were 30-40% lower than disorderly (stress-testing Fact 18).

**Current Policies (hot house world) defers costs**. No near-term transition costs, but escalating physical damages after mid-century cause significant GDP losses, property value declines, and insurance market disruptions that feed back to bank credit quality (web-ngfs Fact 23; academic Fact 9). For financial institutions with shorter planning horizons, this scenario may appear benign initially but compounds dramatically.

**Divergent Net Zero** is useful for analyzing differential sector impacts because uncoordinated policies create divergent carbon prices across sectors and regions (stress-testing Fact 27).

**C&I vs. consumer loans**: C&I loans are more directly exposed to transition risk through industry-specific carbon pricing and energy cost channels (stress-testing Fact 33; academic Facts 6, 37). Consumer loans are affected primarily through indirect macroeconomic channels: unemployment, household income, energy costs reducing disposable income (stress-testing Fact 32; web-ngfs Fact 17). This suggests the relative impact across scenarios will differ: C&I portfolios may show sharper differentiation across transition scenarios, while consumer portfolios may respond more uniformly to the macro-level effects.

**Across model families**: Results for the same scenario vary depending on the IAM used (academic Fact 14; web-ngfs Fact 37). Presenting results across multiple model families (or at least GCAM and REMIND) adds robustness and demonstrates methodological awareness.

**Supporting evidence**:
- academic Facts 7-9, 11, 36, 45: Scenario-specific findings from Acharya et al. and Jung et al.
- stress-testing Facts 3, 5-6, 10, 18, 24, 26-27, 34, 40, 43-45: Quantitative scenario comparisons
- web-ngfs Facts 22-23: Delayed Transition and Current Policies risk profiles
- case-study Facts 14, 16: Core stress testing question and scenario comparison requirement
- kickoff Facts 12, 24, 29: Commercial vs. consumer and scenario comparison expectations
- course Fact 34: Dynamic vs. cumulative multiplier distinction for interpreting results

**Contradicting or qualifying evidence**:
- Exact magnitudes are highly model-dependent (academic Fact 15). Results should be presented as relative rankings rather than precise forecasts.
- The aggregate BUSLOANS and CONSUMER data cannot capture sector-level concentration effects that drive the largest losses in the literature (academic paper source notes). This means the project's aggregate analysis will understate the heterogeneity of impact.

---

### Q8: What are the implications for financial stability and risk management?

**Answer confidence**: moderate

The implications synthesize across scenario outcomes, transmission mechanisms, and regulatory context. While the directional conclusions are clear, the precise financial stability impact depends on assumptions that remain uncertain.

**Core policy finding**: Early, gradual, and predictable climate policy action (orderly transition) is less destabilizing for the banking system than delayed, abrupt action (disorderly transition), even though both achieve similar emissions reductions (academic Fact 52; stress-testing Fact 45). Policy uncertainty itself is a source of financial risk. This is the single most important strategic insight for bank executives and regulators.

**System-level vs. concentration risk**: Even under the most severe transition scenarios, aggregate U.S. bank capital ratios remain above regulatory minimums for the system as a whole (academic Fact 38). However, individual banks with concentrated fossil fuel exposures -- particularly regional and community banks in energy-producing states -- could face material capital pressure (academic Facts 34, 43). The risk is one of concentration rather than system-wide insolvency.

**Systemic amplification**: Acharya et al. identify fire-sale externalities as a systemic risk channel: when banks suffer climate losses and must deleverage, forced asset sales depress prices further, imposing additional losses on other banks (academic Facts 12-13). Total system-wide losses can exceed the sum of individual direct losses. This amplification is more severe when bank portfolios overlap in climate-sensitive exposures.

**Climate risk is a financial risk**: Regulators increasingly view it as a core financial stability concern (kickoff Fact 5). As climate risk worsens, financial institutions will see more stress from counterparties and credit exposures. For banks, this is tangible and directly impacts the balance sheet (kickoff Fact 4).

**Strategic implications for banks**:
- Portfolio monitoring and diversification: Banks should measure and monitor their exposure to carbon-intensive sectors (academic Fact 42).
- Dynamic balance sheet management: The static balance sheet assumption used in most stress tests overstates losses because banks will reduce exposures over time (academic Facts 22, 39).
- Scenario planning: Banks should use NGFS scenarios not for precise capital calculations but as a risk management and strategic planning tool to understand relative risk rankings across plausible futures (academic Fact 24).
- Regional vulnerability: Banks in fossil-fuel-producing regions face concentrated risks that warrant heightened attention (academic Fact 34).

**Limitations and uncertainties** that must be explicitly discussed (case-study Fact 19; kickoff Fact 25):
- Deep uncertainty in climate damage functions and economic models (academic Fact 15; web-ngfs Fact 31).
- Historical relationships between macro variables and lending may not hold during structural economic transformation (academic Fact 17).
- Aggregate national data cannot capture the geographic and sectoral heterogeneity that drives the largest impacts (fred Fact 25; academic Fact 40).
- The 30+ year horizon is far beyond the calibration window of standard credit risk models (stress-testing Fact 25; academic Fact 16).

**Supporting evidence**:
- academic Facts 7, 11-13, 15, 22, 24, 34, 38-39, 43, 52: Financial stability findings
- stress-testing Facts 18, 24, 34, 41, 45: Quantitative impact estimates
- kickoff Facts 4-5, 25, 37: Financial risk framing, limitations, executive communication
- case-study Facts 18-20, 23: Financial stability discussion, limitations, refinements
- web-ngfs Facts 22-23, 31, 35: Scenario-specific risk profiles and uncertainty

**Contradicting or qualifying evidence**:
- The 2025 rescission of the Fed's CSA could reduce near-term regulatory pressure on U.S. banks. However, the underlying climate risks and European regulatory momentum persist.
- Adaptation behavior means realized losses will likely be lower than static-balance-sheet estimates (academic Fact 22, 39).

---

## Cross-Cutting Themes

### Theme 1: The "Double Translation" Problem
A pervasive theme across all sources is the challenge of translating from climate science to financial outcomes through multiple uncertain model layers (climate scenarios -> IAMs -> macro-financial variables -> credit risk -> loan portfolio outcomes). Each translation introduces model uncertainty, and the errors compound (academic Fact 2, 15; stress-testing Fact 2). This means results should be presented as relative risk rankings across scenarios rather than precise point forecasts, and uncertainty should be explicitly quantified where possible.

### Theme 2: Orderly Beats Disorderly for Financial Stability
The most consistent finding across all academic papers, regulatory exercises, and climate stress testing literature is that early, gradual policy action produces lower financial system losses than delayed, abrupt action -- even when both achieve the same climate outcome (academic Fact 52; stress-testing Fact 45; web-ngfs Fact 22). This has clear strategic value for bank executives and policymakers.

### Theme 3: Transparency Trumps Complexity
Every source emphasizes that model transparency and explainability are paramount (kickoff Fact 13; stress-testing Fact 35; case-study Fact 3). The project evaluation explicitly de-prioritizes raw model accuracy in favor of defensible methodology, thoughtful feature selection, and clear communication (kickoff Facts 18, 35). This aligns with regulatory expectations and the practical needs of executive decision-making.

### Theme 4: Aggregate vs. Granular Tension
The project uses national aggregate loan data (BUSLOANS, CONSUMER) while the literature shows that climate risk impacts are highly heterogeneous across sectors, regions, and individual banks (academic Facts 29, 32, 34, 43). This aggregate approach captures macro-level transmission channels (GDP, unemployment driving aggregate lending) but cannot capture the sector-specific carbon exposure channel that both Acharya et al. and Jung et al. emphasize as driving the largest losses. This limitation should be explicitly discussed as an area for refinement.

### Theme 5: COVID as a Modeling Laboratory
The COVID structural break is flagged by BofA as an active industry question (kickoff Facts 33-34) and represents a practical test of modeling discipline. How a team handles COVID in the data -- whether through exclusion, dummies, regime modeling, or other approaches -- is both a key methodological decision and a signal of analytical maturity that the sponsors will scrutinize.

### Theme 6: Forecasting vs. Causal Inference
The course materials draw a clear distinction between structural models (requiring causal identification) and time series forecasting models (requiring only predictive association) (course Facts 14, 44, 48). For this project, we need good conditional forecasts, not causal identification. This means endogeneity between GDP and lending, or between interest rates and loan demand, does not invalidate the forecasting approach -- but it does argue for VAR-style models that allow for simultaneous determination rather than single-equation regressions with strong exogeneity assumptions.

---

## Knowledge Gaps

- **Gap 1: Quantitative NGFS NiGEM outputs for the U.S.** While we know the NiGEM model produces U.S.-specific GDP, unemployment, inflation, and interest rate paths under each NGFS scenario (web-ngfs Fact 8, 25), the actual numerical values have not been downloaded or examined. This is the most urgent gap -- the project cannot proceed to Stage 2 (scenario projection) without these specific paths. **Why it matters**: These are the exogenous scenario inputs that will drive the conditional forecasts.

- **Gap 2: Historical statistical properties of BUSLOANS and CONSUMER** The data characteristics have been described qualitatively (fred Facts 1-10, 26) but the actual series have not been downloaded and tested for unit roots, estimated ACF/PACF structures, or fitted to preliminary models. **Why it matters**: Model specification depends on the empirical properties of the target series.

- **Gap 3: Exact interpolation/frequency alignment method** While several approaches are identified (web-ngfs Fact 24; stress-testing Fact 42), no method has been selected or tested. **Why it matters**: The choice between annual aggregation and quarterly interpolation fundamentally affects model precision and the number of usable observations.

- **Gap 4: Sector-level granularity within aggregate loan data** Both reference papers emphasize that climate risk is concentrated in specific sectors (academic Facts 23, 29, 32), but the aggregate BUSLOANS and CONSUMER series cannot capture this. **Why it matters**: Aggregate analysis will understate the heterogeneity of impact and may miss important risk concentrations.

- **Gap 5: Short-term NGFS scenarios** Phase IV introduced short-term scenarios with quarterly frequency for 1-5 year horizons (stress-testing Fact 30). It is unclear whether these have been included in the NGFS data download. **Why it matters**: These would be more directly applicable to near-term stress testing and could partially resolve the frequency mismatch issue.

- **Gap 6: Parameter stability across subsamples** The course materials warn about subsample instability (course Fact 35), and the FRED data contains multiple structural regime changes. No stability testing has been performed. **Why it matters**: If the macro-to-lending relationship has shifted over time (e.g., post-2008 vs. pre-2008), the model's out-of-sample validity is compromised.

---

## Methodological Notes

### Applicable Course Methods and Their Roles

**AR Models (Weeks 3-4)**: Baseline univariate models for BUSLOANS and CONSUMER growth rates. Establish the persistence structure of lending dynamics (how much of current lending is driven by its own past values). Expect AR(1) or AR(2) to suffice for most series (course Fact 12). These serve as benchmark models against which multivariate models are compared.

**ARMA Models (Week 4)**: If the ACF/PACF diagnostics suggest MA components, ARMA models may provide marginally better fit. However, the near-cancellation problem (course Fact 22) and the difficulty of MA estimation (course Fact 21) suggest AR models are preferred in practice.

**Distributed Lag Models (Week 5)**: Directly applicable for estimating how changes in macro variables (GDP growth, unemployment) affect loan growth over multiple future periods. The dynamic multiplier (impact on changes) and cumulative multiplier (impact on levels) provide natural tools for interpreting how climate-driven macro shocks propagate to lending (course Facts 27, 34). Require HAC standard errors unless combined with AR terms (course Facts 31-33).

**ADL (Autoregressive Distributed Lag) Models (Week 5)**: The most natural single-equation framework for this project -- combines lagged dependent variables (capturing lending persistence) with lagged macro regressors (capturing the climate-to-macro-to-lending transmission). More efficient than pure distributed lags when the error structure is well specified (course Fact 43).

**VAR Models (upcoming in course)**: The most recommended multivariate framework for jointly modeling the dynamics of GDP, unemployment, interest rates, and loan growth (stress-testing Fact 21; course Fact 38). VAR avoids the need to specify which variables are exogenous vs. endogenous by modeling everything as a system. Well suited for scenario-conditional forecasting: fix the macro paths to NGFS scenario values and compute the implied loan path.

**HAC Standard Errors (Week 5)**: Required for distributed lag regressions where errors are likely serially correlated. Newey-West estimator with truncation parameter m = 0.75 * T^(1/3) (course Fact 32). Less needed for ADL/VAR models with sufficient AR lags.

**Unit Root Tests (Weeks 3-4)**: ADF/PP/KPSS tests are the first step. Apply to all FRED series and to the transformed (log-differenced or growth rate) series to confirm stationarity before modeling.

**Information Criteria (Week 4)**: AIC and BIC for comparing model specifications -- particularly for lag length selection in AR, ADL, and VAR models (course Fact 23).

**Box-Jenkins Model Selection (Week 4)**: The Pesavento recipe (course Fact 20) provides the step-by-step procedure: stationarize, plot correlograms, identify candidate models using ACF/PACF, start large and eliminate, check residuals, compare with AIC/BIC, iterate.

### Recommended Model-Building Workflow

1. **Download and transform data**: BUSLOANS, CONSUMER, GDP, UNRATE, FEDFUNDS, CPI from FRED. Apply log-differencing or growth rate transformations. Test for unit roots.
2. **Univariate analysis**: Fit AR models to loan growth series. Establish persistence structure and residual diagnostics.
3. **Bivariate/multivariate analysis**: Add macro regressors using ADL or distributed lag specification. Test significance of each macro variable. Use HAC standard errors where appropriate.
4. **VAR estimation**: Estimate a VAR system with loan growth and 2-3 macro variables. Use AIC/BIC for lag selection. Check impulse response functions.
5. **Scenario conditioning**: Download NGFS NiGEM U.S. macro paths. Interpolate to quarterly frequency if needed. Feed through estimated model to generate scenario-conditional loan forecasts.
6. **Comparison and visualization**: Compare loan outcomes across scenarios and (if feasible) across NGFS model families. Present dynamic and cumulative multipliers. Include confidence bands using 68% intervals (course Fact 36).
7. **Robustness and stability**: Test for subsample stability (pre/post-2008, pre/post-COVID). Apply COVID treatment and assess sensitivity.

---

## Recommendations

### Immediate Next Steps (Phase 1: Before Feb 20 Q&A)

1. **Download NGFS data from IIASA portal** and explore the CSV structure. Filter for USA-region variables across at least two model families (GCAM and REMIND). Identify which NiGEM macro-financial variables are available for the U.S. under each scenario.

2. **Download BUSLOANS, CONSUMER, and key FRED macro series**. Compute log-differences / growth rates. Run unit root tests. Plot ACF/PACF. Identify obvious structural breaks.

3. **Build a univariate AR model for loan growth** as a baseline. Determine optimal lag length using AIC/BIC.

4. **Prepare Q&A questions for Feb 20** focused on: (a) BofA's preferred approach to COVID treatment in lending models, (b) whether they have a preference for modeling frequency (quarterly vs. annual), (c) their view on which NGFS model family to prioritize.

### Modeling Phase (Phase 2: Feb 20 - March)

5. **Estimate an ADL or VAR model** linking loan growth to GDP growth, unemployment change, and interest rate changes using FRED data. Start with a large specification and pare down.

6. **Address the frequency mismatch** by either aggregating loan data to quarterly (matching GDP) or quarterly/annual (matching NGFS). Test sensitivity to this choice.

7. **Handle the COVID structural break** using at least two approaches (e.g., exclusion vs. dummy variable) and compare how results differ. This will be a strong demonstration of modeling discipline.

8. **Generate scenario-conditional forecasts** by feeding NGFS macro paths through the estimated model. Produce fan charts or confidence intervals.

### Presentation Phase (Phase 3: March - April 9)

9. **Compare results across 3-4 NGFS scenarios** (Net Zero 2050, Delayed Transition, Current Policies, and optionally NDCs or Divergent Net Zero). Visualize the difference in loan trajectories clearly.

10. **Compare results across at least two NGFS model families** (GCAM vs. REMIND) to illustrate model uncertainty.

11. **Frame the "so what?" for bank executives**: Which scenarios pose the greatest risk? How large is the difference between orderly and disorderly transition? What does this imply for portfolio management, capital planning, and strategic decision-making?

12. **Explicitly discuss limitations**: aggregate vs. granular data, static vs. dynamic balance sheet, frequency mismatch, parameter instability, and the compounding uncertainty across model layers. These are not weaknesses -- they are evidence of intellectual honesty that the BofA sponsors will value.

---

## Fact Attribution Index

### Case Study PDF (24 facts used)
- Fact 1: Physical and transition risk channels (Q2, Q8)
- Fact 2: Regulators use NGFS for stress testing (Q1, Q6)
- Fact 3: Existing stress tests lack transparency (Q4, Q5, Q6)
- Fact 4: Simplified stress testing prototype goal (Q5, Q6)
- Fact 5: Forecasting techniques under NGFS scenarios (Q5, Q7)
- Fact 6: NGFS scenario quantitative pathways (Q1)
- Fact 7: Macro variables relevant to banking (Q1, Q3)
- Fact 8: NGFS pathways influence macro variables (Q2, Q3)
- Fact 9: BUSLOANS FRED ticker for C&I loans (Q4)
- Fact 10: NGFS data portal URL (Q1, Q4)
- Fact 11: Supporting FRED macro data (Q3, Q4)
- Fact 12: Model selection and justification (Q4, Q5)
- Fact 13: Feature selection and engineering (Q3, Q5)
- Fact 14: Core stress testing question (Q5, Q7)
- Fact 15: Model performance evaluation (Q5)
- Fact 16: Scenario comparison requirement (Q7)
- Fact 17: Multiple NGFS model families (Q1, Q4)
- Fact 18: Financial stability discussion (Q8)
- Fact 19: Model limitations and uncertainties (Q4, Q8)
- Fact 20: Areas for refinement (Q5, Q8)
- Fact 21: Deliverables (Q5)
- Fact 22: Reference papers cited (Q6, Q5)
- Fact 23: Learning objectives (Q5, Q8)
- Fact 24: NGFS data resources URL (Q1)

### Kickoff Transcript (42 facts used)
- Fact 1: BofA Treasury QA team background (Q5, Q6)
- Fact 3: Physical vs. transition risk categories (Q2)
- Fact 4: Climate risk as financial risk (Q2, Q8)
- Fact 5: Regulators view climate as financial stability concern (Q6, Q8)
- Fact 6: European regulators early signal (Q6)
- Fact 7: NGFS scenario development (Q1, Q6)
- Fact 8: EBA embedding climate into supervision (Q6)
- Fact 9: Fed signaling around 2022-2023 (Q6)
- Fact 10: Fed rescission in 2025 (Q6)
- Fact 11: Bank exposure to commercial real estate and lending (Q2)
- Fact 12: Project focuses on commercial and consumer loans (Q7)
- Fact 13: Model transparency and explainability (Q5)
- Fact 14: No established method exists (Q5, Q6)
- Fact 15: Core research question (Q2, Q7)
- Fact 16: NGFS contains macro and climate variables (Q1)
- Fact 17: Central modeling task (Q2, Q5)
- Fact 18: Critical thinking over perfect models (Q5)
- Fact 19: Defensible models with feature selection (Q3, Q5)
- Fact 20: Data granularity and frequency challenges (Q4)
- Fact 22: NGFS data download format (Q1, Q4)
- Fact 24: Scenario comparisons expected (Q7)
- Fact 25: Implications and limitations discussion (Q8)
- Fact 26: BofA team does NOT do climate risk currently (Q6)
- Fact 27: No one has a definitive answer (Q5, Q6)
- Fact 28: CONSUMER ticker confirmed (Q4)
- Fact 29: Commercial vs. consumer choice (Q3, Q7)
- Fact 30: Training window as design choice (Q4, Q5)
- Fact 31: FRED series varying start dates (Q4)
- Fact 32: Cover enough business cycles (Q4, Q5)
- Fact 33: COVID structural break question (Q4)
- Fact 34: COVID as distinct structural break (Q4, Q5)
- Fact 35: Methodology over accuracy in evaluation (Q5)
- Fact 37: Executive communication emphasis (Q8)
- Fact 38: Transition risk details (Q2, Q3)
- Fact 39: Physical risk examples (Q2)

### Course Materials (48 facts used)
- Fact 2: Data transformations (Q4, Q5)
- Fact 6: Weak stationarity definition and examples (Q4, Q5)
- Fact 12: AR(1)/AR(2) sufficiency (Q5)
- Fact 13: Stationarity as prerequisite (Q4, Q5)
- Fact 14: Structural vs. time series model distinction (Q2, Q5)
- Fact 15: Biased coefficients can still forecast well (Q5)
- Fact 17: AR(1) model and dynamic multiplier (Q5)
- Fact 18: ACF/PACF identification patterns (Q5)
- Fact 19: Unit root testing (Q4, Q5)
- Fact 20: Pesavento practical recipe (Q5)
- Fact 21: AR via OLS, MA via MLE (Q5)
- Fact 22: Near-cancellation problem (Q5)
- Fact 23: AIC/BIC comparison (Q5)
- Fact 24: Unemployment rate AR example (Q3, Q5)
- Fact 25: Pesavento priorities (Q5)
- Fact 27: Distributed lag model specification (Q5)
- Fact 29: Endogenous macro examples (Q2, Q3)
- Fact 31: OLS standard errors fail with serial correlation (Q5)
- Fact 32: HAC/Newey-West standard errors (Q5)
- Fact 33: HAC needed for DL but not ADL (Q5)
- Fact 34: Dynamic vs. cumulative multiplier (Q5, Q7)
- Fact 35: Subsample instability (Q4, Q5)
- Fact 36: 68% confidence intervals (Q5, Q7)
- Fact 38: VAR preview (Q5)
- Fact 39: Stationarity implications (Q4, Q5)
- Fact 43: ADL model as framework (Q5)
- Fact 44: Endogeneity does not ruin forecasts (Q2, Q5)
- Fact 45: Structural break concept (Q4, Q5)
- Fact 46: Impulse response function template (Q2, Q5)
- Fact 48: Structural vs. forecasting distinction (Q2, Q5)

### Web: NGFS and Transmission (40 facts used)
- Fact 1: NGFS definition and purpose (Q1)
- Fact 2: Two-dimension framework (Q1)
- Fact 3: Six scenario descriptions (Q1)
- Fact 4: Three risk categories (Q1)
- Fact 5: Three IAM families (Q1)
- Fact 6: IAM structural differences (Q1)
- Fact 7: Variable categories on portal (Q1, Q3)
- Fact 8: NiGEM macro-financial variables (Q1, Q3)
- Fact 9: Annual frequency, 2020-2100 horizon (Q1)
- Fact 10: Carbon price ranges across scenarios (Q1, Q3)
- Fact 11: GDP impacts across scenarios (Q1, Q3)
- Fact 12: Physical and transition risk channels (Q2)
- Fact 13: Acharya et al. two-stage framework (Q2, Q3)
- Fact 14: Direct vs. indirect transmission channels (Q2)
- Fact 16: C&I loan transmission channels (Q2, Q3)
- Fact 17: Consumer loan transmission channels (Q2, Q3)
- Fact 18: Key mediating macro variables (Q3)
- Fact 19: Three-stage cascade approach (Q1, Q2, Q3)
- Fact 20: ECB climate stress test findings (Q2)
- Fact 21: Fed CSA pilot (Q2)
- Fact 22: Delayed Transition most disruptive (Q1, Q2)
- Fact 23: Current Policies long-term physical risk (Q1, Q2)
- Fact 24: Frequency mismatch challenge (Q1, Q3)
- Fact 25: U.S.-specific NiGEM variables (Q1, Q3)
- Fact 26: Standard two-step methodology (Q2, Q3)
- Fact 27: GDP-lending procyclicality (Q3)
- Fact 28: Unemployment-consumer loan relationship (Q3)
- Fact 29: Interest rate dual role (Q3)
- Fact 31: Physical risk damage function uncertainty (Q1, Q2)
- Fact 33: NGFS data structure (Q1)
- Fact 34: Recommended simplified framework (Q2, Q3)
- Fact 35: NGFS does not directly model banking outcomes (Q1, Q2)
- Fact 36: Inflation/CPI transmission channel (Q3)
- Fact 37: IAM differences in outputs (Q1)
- Fact 38: Scenarios for assessment not investment (Q1)
- Fact 40: Data format and filtering guidance (Q1)

### Web: Stress Testing Methods (45 facts used)
- Fact 1: Acharya et al. two-stage approach (Q5, Q6)
- Fact 2: Double translation problem (Q5, Q6)
- Fact 3: Disorderly scenarios produce higher losses (Q5, Q7)
- Fact 4: CCAR/DFAST adaptation for climate (Q5, Q6)
- Fact 5: Jung et al. carbon-intensity exposure (Q5, Q7)
- Fact 6: C&I more exposed than consumer to transition risk (Q5, Q7)
- Fact 10: Delayed Transition sharpest GDP contraction (Q7)
- Fact 12: Fed CSA pilot six banks (Q6)
- Fact 13: Fed CSA two modules (Q6)
- Fact 14: Longer horizon than CCAR (Q5, Q6)
- Fact 15: Fed CSA results 2024 (Q6)
- Fact 16: CSA rescinded in 2025 (Q6)
- Fact 17: ECB 2022 exercise scope (Q6)
- Fact 18: ECB aggregate credit losses (Q6, Q7)
- Fact 19: ECB top-down/bottom-up methodology (Q5, Q6)
- Fact 20: Bridge equations in ECB exercise (Q5, Q6)
- Fact 21: VAR framework for stress testing (Q5)
- Fact 22: Bridge equation / satellite model approach (Q5)
- Fact 23: Recommended project approach (Q5)
- Fact 24: Bank of England CBES (Q6, Q7)
- Fact 25: Models not suited for 30+ year horizons (Q5, Q6)
- Fact 26: GDP decline ranges under disorderly (Q7)
- Fact 27: Divergent Net Zero for sector analysis (Q7)
- Fact 28: Frequency mismatch challenge (Q5)
- Fact 30: Short-term NGFS scenarios (Q5, Q6)
- Fact 31: EBA ESG risk guidelines (Q6)
- Fact 32: Consumer loan indirect channels (Q5, Q7)
- Fact 33: C&I loan direct and indirect channels (Q5, Q7)
- Fact 34: IMF disorderly transition default rate increases (Q6, Q7)
- Fact 35: Transparent model classes (Q5)
- Fact 36: NiGEM as macro-financial bridge (Q5, Q6)
- Fact 37: Conditional forecasting framework (Q5)
- Fact 38: Key bridge macro variables (Q5)
- Fact 40: Net Zero vs. Delayed Transition GDP profiles (Q7)
- Fact 41: Linear models may underestimate tail risks (Q5)
- Fact 42: Frequency mismatch solutions (Q5)
- Fact 43: Fed CSA sensitivity to assumptions (Q6, Q7)
- Fact 45: Orderly beats disorderly finding (Q6, Q7)

### FRED Data (40 facts used)
- Fact 1: BUSLOANS definition (Q3, Q4)
- Fact 2: BUSLOANS frequency, units, start date (Q4)
- Fact 5: Non-stationarity requiring transformation (Q4, Q5)
- Fact 6: COVID PPP spike structural break (Q4)
- Fact 7: CONSUMER definition (Q3, Q4)
- Fact 8: CONSUMER frequency and start date (Q4)
- Fact 10: CONSUMER different cyclical dynamics (Q4)
- Fact 11: Macro drivers differ for C&I vs. consumer (Q3)
- Fact 12: Case study explicit variable list (Q3)
- Fact 13: GDP as most important driver (Q3)
- Fact 14: Unemployment rate as key mediator (Q3)
- Fact 15: Interest rates as determinants (Q3)
- Fact 16: CPI/inflation channels (Q3)
- Fact 18: Two-step transmission framework (Q3, Q5)
- Fact 19: Transition vs. physical risk macro channels (Q2, Q3)
- Fact 20: NGFS GDP as primary bridge variable (Q3, Q5)
- Fact 21: Frequency mismatch challenge (Q4)
- Fact 22: Varying FRED start dates (Q4)
- Fact 23: Training window tradeoffs (Q4)
- Fact 24: COVID treatment options (Q4)
- Fact 25: National aggregate limitation (Q4)
- Fact 26: BUSLOANS historical structural breaks (Q4)
- Fact 27: Great Moderation regime (Q4)
- Fact 28: 2008 GFC structural break (Q4)
- Fact 29: Commonly used FRED series list (Q3)
- Fact 30: Bridge variable recommendations (Q3, Q5)
- Fact 31: Corporate bond spreads as indicator (Q3)
- Fact 33: Unemployment persistence (Q4)
- Fact 34: Distributed lag framework from course (Q3, Q5)
- Fact 35: Exogeneity of climate variables vs. endogeneity of macro (Q3, Q5)
- Fact 36: OJ price data analogy (Q3, Q5)
- Fact 37: Subsample instability caution (Q4)
- Fact 38: Energy-related FRED series (Q3)
- Fact 39: Two-stage practical approach (Q4, Q5)
- Fact 40: H.8 data revision artifact (Q4)

### Academic Papers (52 facts used)
- Fact 1: Acharya et al. comprehensive framework (Q2, Q5, Q6)
- Fact 2: Two transmission channels (Q2)
- Fact 3: Transmission chain through IAMs to macro to bank (Q2, Q5, Q6)
- Fact 4: Multi-step cascade structure (Q2, Q3, Q5)
- Fact 5: Key mediating macro variables (Q3)
- Fact 6: NGFS Phase III scenario descriptions (Q1, Q7)
- Fact 7: Delayed Transition most severe short-term stress (Q7, Q8)
- Fact 8: Net Zero 2050 moderate manageable costs (Q7)
- Fact 9: Current Policies highest long-run physical risk (Q7)
- Fact 10: PD/LGD mapping for carbon-intensive sectors (Q2, Q3, Q5)
- Fact 11: Credit loss ranges modest to substantial (Q7, Q8)
- Fact 12: Fire-sale externalities (Q8)
- Fact 13: Systemic amplification mechanism (Q8)
- Fact 14: Sensitivity to IAM choice (Q1, Q4, Q5)
- Fact 15: Deep uncertainty in compounding models (Q5, Q8)
- Fact 16: Common challenges across stress tests (Q6)
- Fact 17: Traditional stress tests insufficient for climate (Q5, Q6)
- Fact 18: Transition risk transmission mechanism (Q2, Q3)
- Fact 19: Physical risk transmission mechanism (Q2, Q3)
- Fact 20: Scenario-conditional forecasting approach (Q5)
- Fact 21: VAR and bridge equations, frequency mismatch (Q4, Q5)
- Fact 22: Static balance sheet limitation (Q5, Q8)
- Fact 23: Most exposed sectors (Q2, Q7)
- Fact 24: Risk management tool, not precise capital calculation (Q6, Q8)
- Fact 25: Carbon price as key distinguishing variable (Q1, Q3, Q7)
- Fact 26: Jung et al. bank exposure methodology (Q2, Q3)
- Fact 29: 10-15% of portfolios in high-carbon sectors (Q2, Q7)
- Fact 30: Direct vs. indirect exposure (Q2, Q3)
- Fact 31: NGFS scenarios to estimate industry impacts (Q5, Q7)
- Fact 32: Concentrated transition risk in few sectors (Q2, Q7)
- Fact 34: Regional heterogeneity of exposure (Q7, Q8)
- Fact 35: Carbon price to PD transmission chain (Q2, Q3)
- Fact 36: Delayed Transition highest peak losses (Q7)
- Fact 37: C&I most directly exposed to transition risk (Q2, Q3)
- Fact 38: Aggregate capital ratios above minimums (Q8)
- Fact 39: Static balance sheet limitation (Q5, Q8)
- Fact 40: Regional/sectoral limitation of national data (Q4, Q5)
- Fact 42: Regulatory implications (Q6)
- Fact 43: G-SIB diversification vs. regional concentration (Q7, Q8)
- Fact 45: Delayed Transition greatest short-term risk (Q7, Q8)
- Fact 46: GDP, unemployment, carbon prices as three most critical (Q3)
- Fact 47: Scenario-conditional forecasting endorsed (Q5, Q6)
- Fact 48: Fed CSA pilot reference (Q6)
- Fact 49: ECB climate stress test reference (Q6)
- Fact 50: Lack of standardized data as obstacle (Q4, Q5)
- Fact 52: Orderly transition less destabilizing (Q8)
