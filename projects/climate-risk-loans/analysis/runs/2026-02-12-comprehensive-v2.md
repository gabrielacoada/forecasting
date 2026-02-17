# Comprehensive Analysis: Climate Risk Impact on Banking Loan Portfolios (v2)
Date: 2026-02-12
Factbase: ~401 facts from 9 sources (including 162 directly from PDF papers)

## Executive Summary

This updated analysis integrates 162 new facts extracted directly from the two NY Fed Staff Reports -- Acharya et al. (2023, SR 1059) and Jung et al. (2024, SR 1058) -- with page-level attribution. These PDF-sourced facts substantially sharpen the quantitative precision and methodological specificity of the analysis compared to v1, which relied on training-knowledge-based summaries of these papers. Key upgrades include: (1) precise GDP impact figures from the NGFS scenarios -- Net Zero 2050 causes a 1.97% average world GDP reduction due to chronic physical risk, Delayed Transition causes 2.86%, and Current Policies causes 5.66% (sr1059 Fact 16, p. 10); (2) specific bank exposure bounds from Jung et al. showing that the average bank's transition risk exposure does not exceed 14% of loan portfolios even under the strictest policies and most extreme stress assumptions (sr1058 Fact 3, p. 3); (3) the CRISK market-based methodology from Acharya et al. showing that a 50% decline in the stranded asset factor would increase aggregate CRISK of the top four U.S. banks by $425 billion, or approximately 47% of their market capitalization (sr1059 Fact 57, p. 30); and (4) ECB combined credit and market risk losses of approximately 70 billion EUR under a short-term disorderly scenario for 41 banks (sr1059 Fact 44, p. 26).

The PDF extractions also reveal important methodological nuance not captured in v1. Jung et al. use three distinct general equilibrium models -- Jorgenson/IGEM (36 industries), Goulder-Hafstead/E3 (35 industries), and G-Cubed (12-20 industries) -- that produce meaningfully different exposure estimates, ranging from -1% to 6.4% for the average bank depending on the model and policy scenario (sr1058 Facts 4-6, pp. 3-4, 15, 17). The paper is exclusively focused on C&I loans using Y-14Q data from 42 unique banks over 2012-2023, and explicitly notes that consumer loan exposure cannot be estimated with their methodology because general equilibrium models do not provide household-level effects (sr1058 Fact 53, p. 8). Acharya et al. emphasize that unlike traditional stress scenarios, "no historical precedent exists for either extreme physical or transition risk realizations," minimizing the usefulness of purely statistical approaches (sr1059 Fact 8, p. 8). Both papers note that carbon emissions can explain at most 60% of bank transition risk exposures, with at least 40% driven by other factors captured only by forward-looking general equilibrium models (sr1058 Fact 7, pp. 4, 29).

Together, these findings reinforce the v1 conclusion that disorderly transition poses the greatest near-term financial risk, but they add critical quantitative guardrails: even extreme stress scenarios produce exposure losses bounded at around 14% of C&I loan portfolios, and the system-wide finding across all major exercises is that climate risks do not yet pose an existential threat to financial stability -- though the caveats behind this conclusion are substantial (sr1059 Fact 48, p. 26). For this BofA-sponsored project, the implication is that the forecasting model should aim to capture the direction and relative magnitude of scenario differentiation rather than precise dollar losses, and should explicitly discuss why aggregate BUSLOANS/CONSUMER data understates the heterogeneity documented in the granular Y-14Q analysis.

---

## Question-by-Question Analysis

### Q1: What are the NGFS climate scenarios and what variables do they contain?
**Answer confidence**: strong

The NGFS (Network for Greening the Financial System) was launched at the Paris One Planet Summit in 2017 and as of October 2022 consisted of 121 members and 19 observers committed to developing climate risk management in the financial sector (sr1059 Fact 80, p. 4). The NGFS does not assess the likelihood of each scenario and emphasizes that scenarios "aim at exploring the bookends of plausible futures (neither the most probable nor desirable) for financial risk assessment" (sr1059 Fact 12, p. 9 -- direct quote from the PDF).

In June 2021, the NGFS published six scenarios across three categories (sr1059 Fact 11, p. 9):

- **Orderly Transition**: Net Zero 2050 (limiting warming to 1.5C, global net zero CO2 by 2050) and Below 2C (gradually increasing policy stringency). These minimize both physical and transition risks.
- **Disorderly Transition**: Divergent Net Zero (net zero by 2050 but with uncoordinated sector-specific policies) and Delayed Transition (no new climate policy until 2030, then abrupt strong policies). Annual emissions do not decrease until 2030 under Delayed Transition (sr1059 Fact 14, p. 10).
- **Hot House World**: Nationally Determined Contributions (current Paris pledges only) and Current Policies (no new action, temperatures exceeding 3C by 2100). Transition risk is limited but physical risk is severe (sr1059 Fact 13, p. 10).

The scenarios are produced by three IAM families -- GCAM, REMIND-MAgPIE, and MESSAGEix-GLOBIOM (web-ngfs Fact 5). The NGFS modeling framework uses three sets of models to map scenario narratives to variables (sr1059 Fact 15, p. 10): (1) climate impact models generating temperature and disaster losses; (2) transition pathway models generating carbon prices and temperature trajectories; and (3) economic impact models such as NiGEM and IAMs producing GDP, unemployment, and inflation projections. In Phase IV (November 2023), NiGEM translates IAM outputs into country-level financial variables including GDP growth, CPI inflation, unemployment, short- and long-term interest rates, exchange rates, and equity prices (web-ngfs Fact 8).

**Quantitative scenario differentiation** (directly from the PDF): On average, the Net Zero 2050 scenario causes a **1.97% reduction in world GDP** due to chronic physical risk compared to baseline. The Delayed Transition scenario causes a **2.86% GDP decline**. The Current Policies scenario causes the greatest average GDP reduction of **5.66%** (sr1059 Fact 16, p. 10). These figures represent chronic physical risk only; transition costs add additional GDP drag in the orderly and disorderly scenarios.

Cross-jurisdictional variations are substantial. The Bank of Canada projects a 13% GDP reduction under orderly transition and 21% under delayed action by 2050 (sr1059 Fact 63, p. 42). The Bank of England projects UK GDP 1.4% below counterfactual under Early Action, 4.6% under Late Action, and 7.8% under No Additional Action by 2050 (sr1059 Fact 65, p. 45). The U.S. Federal Reserve pilot projects US GDP of approximately $24,030B under Current Policies and $23,574B under Net Zero 2050 by 2030, with carbon prices of $17/ton vs. $162/ton respectively (sr1059 Fact 66, p. 46).

Carbon prices from the G-Cubed model used in Jung et al. provide specific U.S. trajectories: Current Policy has $3.72/ton in 2021 growing to $26.50 in 2050; Orderly Transition has $16.75 in 2021 growing to $119.14 in 2050; Disorderly Transition has no tax until 2030, then $31.52 growing to $121.97 in 2050 (sr1058 Fact 23, p. 16).

**Supporting evidence**:
- sr1059 Fact 11 (p. 9): "six scenarios across three categories: Orderly Transition, Disorderly Transition, Hot House World"
- sr1059 Fact 12 (p. 9): NGFS scenarios "aim at exploring the bookends of plausible futures"
- sr1059 Fact 16 (p. 10): GDP impacts of -1.97%, -2.86%, -5.66% across scenarios
- sr1059 Fact 15 (p. 10): Three sets of models (climate impact, transition pathway, economic impact)
- sr1059 Facts 63-66 (pp. 42-46): Cross-jurisdictional GDP projections
- sr1058 Fact 23 (p. 16): G-Cubed carbon price paths ($3.72-$121.97/ton)
- sr1058 Fact 12 (p. 9): Three GE models with different industry coverage (36, 35, 12-20)
- web-ngfs Facts 3-5: Scenario descriptions, IAM families
- case-study Facts 6, 10, 17: NGFS data portal and model families

**Contradicting or qualifying evidence**:
- sr1059 Fact 12 (p. 9): NGFS does not assess likelihood -- scenarios are not forecasts.
- sr1059 Fact 21 (p. 11): NGFS and IPCC scenarios are not equivalent; NGFS focuses on transition pathways while IPCC focuses on physical risks.
- sr1058 Fact 77 (p. 2): General equilibrium model outputs are conditional on specific policy realizations and do not factor in uncertainty about which policy would be implemented.
- web-ngfs Fact 37: Different IAMs produce "meaningfully different quantitative outputs" for the same scenario.

---

### Q2: What is the theoretical transmission mechanism from climate risk to bank loan portfolios?
**Answer confidence**: strong

Climate-related risks are categorized into physical risks (direct manifestations of climate change such as floods, heat waves, wildfires) and transition risks (effects from regulatory interventions, carbon emission taxes, renewable energy subsidies, or changes in technologies and preferences) (sr1059 Fact 4, p. 7). Among investment professionals, regulatory and technological risks are seen as "somewhat more important" than physical risks in the near term, while physical risks are thought to become important "only over longer horizons" (sr1059 Fact 5, p. 7). A joint FSB-NGFS review found that almost 90% of central bank exercises explored transition risk implications, while about 67% analyzed physical risks (sr1059 Fact 7, p. 8).

Acharya et al. identify **three distinct channels** through which climate risk affects banks (sr1059 Fact 27, p. 16, adapted from Grippa et al. 2019 and Bolton et al. 2020):
1. **Credit Risk** through residential and corporate loans
2. **Market Risk** through equities, bonds, and commodities
3. **Liquidity Risk** through inability to refinance (e.g., deposit withdrawals after hurricanes -- sr1059 Fact 43, p. 25)

These are transmitted via lower property and corporate asset values, lower corporate profits, lower household wealth, and lower growth and productivity. The transmission flows through both **direct** channels (firm-level exposure to shocks) and **indirect** channels (climate pathways to macro indicators to risk models to loss projections), as depicted in the paper's Figure 1 cascade framework (sr1059 Fact 59, p. 6).

**Physical risk and credit**: Declining house prices from sea level rise may induce mortgage defaults; flood and wildfire cash flow shocks reduce homeowners' ability to make payments; collateral values are negatively affected by abnormal temperatures; heat waves raise energy expenditures with negative effects on consumer financial health; supply chain disruptions affect firms' ability to service loans (sr1059 Fact 29, p. 17). However, many physical risk cash-flow impacts are expected to materialize "only at longer horizons," and Painter (2020) documents that sea-level rise exposure is priced only in municipal bonds with maturities exceeding twenty years (sr1059 Fact 30, pp. 17-18). Acharya et al. (2022) find that heat stress affects Expected Default Frequency beyond one year, with the effect at years five and ten being twice that for year two (sr1059 Fact 31, p. 18).

**Transition risk and credit**: A large carbon tax reduces profitability of high-emission, highly-leveraged firms, reducing their ability to repay bank loans (sr1059 Fact 32, p. 18). Unlike physical risks, "the effects of transition risks on banks' loan books might materialize more quickly" because carbon taxes could be introduced at any moment (sr1059 Fact 34, p. 18). Importantly, the paper argues that extreme carbon taxes leading to bankruptcy of high-emission industries "may be deemed implausible in most countries" since transition policies are dynamic political choices (sr1059 Fact 23, p. 12).

**Maturity mismatch matters**: The average maturity of U.S. bank loans at origination is between 3 and 5 years (sr1059 Fact 28, p. 17). This means that long-horizon physical risks (decades away) may not directly impair current loan books, while transition risks can affect near-term creditworthiness more immediately, particularly if policy changes are sudden.

**An important nuance**: Blickle et al. (2021b) find that loan losses due to natural disasters are offset by increased loan demand, resulting in "insignificant or small effects on bank performance and stability" (sr1059 Fact 37, p. 19). Banks also actively respond -- charging higher rates on properties exposed to sea level rise, shortening maturities, and reducing access to permanent financing for high-emission firms (sr1059 Fact 36, p. 19).

Jung et al. provide a complementary perspective focused exclusively on **transition risk** and **C&I loans** (sr1058 Fact 47, p. 1). Their approach differs from emissions-based methods: "Emissions are backward-looking and are only one of the dimensions that will be affected in a transition to a low-carbon economy" (sr1058 Fact 49, p. 6). Carbon emissions can explain at most 60% of transition risk exposures estimated from general equilibrium models; at least 40% of variation is unexplained by emissions alone (sr1058 Fact 7, pp. 4, 29).

Physical and transition risks interact in complex ways: in early stages, increasing physical damages cause more forceful regulatory responses, moving risks together. Over longer periods, effective regulation reduces physical risk but increases transition risk. Delays reduce transition risk but increase long-run physical risk (sr1059 Fact 81, p. 8). The concept of **compound risk** is also important -- multiple risks realized simultaneously, with feedback loops between growth and climate risk creating causal ordering (sr1059 Fact 26, p. 14).

**Supporting evidence**:
- sr1059 Fact 4 (p. 7): Physical and transition risk definitions
- sr1059 Fact 27 (p. 16): Three channels -- credit, market, liquidity risk
- sr1059 Fact 59 (p. 6): Cascade framework (Figure 1)
- sr1059 Facts 29-34 (pp. 17-18): Physical and transition risk credit channels
- sr1059 Fact 36 (p. 19): Banks already responding to climate risks
- sr1059 Fact 81 (p. 8): Physical-transition risk interaction
- sr1058 Fact 7 (pp. 4, 29): Emissions explain at most 60% of exposure
- sr1058 Fact 47 (p. 1): Transition risk definition, paper scope
- sr1058 Fact 49 (p. 6): Emissions are backward-looking

**Contradicting or qualifying evidence**:
- sr1059 Fact 37 (p. 19): Disaster loan losses offset by demand increases -- insignificant net effects
- sr1059 Fact 23 (p. 12): Extreme carbon taxes may be politically implausible
- sr1059 Fact 30 (pp. 17-18): Physical risk pricing only in very long maturity bonds
- sr1058 Fact 53 (p. 8): Consumer loan exposure cannot be estimated with industry-level GE models

---

### Q3: What macroeconomic variables mediate the climate-to-loans relationship?
**Answer confidence**: strong

The stress testing cascade flows through macro indicators as the critical bridge. Acharya et al.'s Figure 1 framework shows climate models producing transition pathways (GHG emissions, temperature, carbon prices), which feed into macro models that generate GDP, unemployment, and other macro indicators, which then feed into risk modelling for interest rate risk, credit risk, and market risk (sr1059 Fact 83, p. 6; sr1059 Fact 82, pp. 5, 9-10). The key macroeconomic variables that mediate the climate-to-financial-outcomes relationship include: **GDP, unemployment, inflation, house prices, and interest rates** (sr1059 Fact 82, pp. 5, 9-10).

**GDP growth** is the single most important mediating variable. Loan growth is procyclical (web-ngfs Fact 27). Under NGFS scenarios, the GDP impacts range from -1.97% (Net Zero 2050) to -5.66% (Current Policies) on average from chronic physical risk alone (sr1059 Fact 16, p. 10). DICE-type models treat climate damages as a tax on consumption largest when GDP is highest, while Weitzman/Barro-type models consider low-probability catastrophic events where substantial physical risk and low GDP occur jointly (sr1059 Fact 25, p. 13). This modeling choice matters because it determines whether the worst economic outcomes coincide with the worst climate outcomes.

**Unemployment rate** is critical for consumer defaults. Under NGFS scenarios with abrupt transitions, unemployment may spike as carbon-intensive workers are displaced. The FRED series UNRATE (monthly, AR(1) coefficient ~0.95) captures this channel (fred Fact 33; course Fact 24).

**Interest rates** serve dual roles: monetary policy responses to climate-driven inflation tighten conditions, while climate risk premia increase borrowing costs (web-ngfs Fact 29). The G-Cubed model used in Jung et al. endogenously determines how carbon tax revenue is recycled -- infrastructure investment, government debt reduction, or lump-sum transfers -- and this choice significantly affects the macro transmission (sr1058 Fact 23, p. 16).

**Carbon prices** are the direct policy instrument distinguishing scenarios. Under the G-Cubed model: Current Policy reaches $26.50/ton by 2050; Orderly reaches $119.14/ton; Disorderly reaches $121.97/ton (sr1058 Fact 23, p. 16). The Jorgenson model tests initial taxes of $25 and $50 with growth rates of 1% and 5% per year (sr1058 Fact 19, p. 13). The Goulder model assumes a $20 tax growing at 4% annually to $60/ton by 2048 (sr1058 Fact 21, p. 15).

**Revenue recycling matters**: The form of carbon tax revenue redistribution significantly affects exposure. Under Goulder/E3, a corporate tax cut combined with carbon pricing actually increases profits for 20 of 35 industries, producing negative average bank exposure (-1%), meaning banks would benefit (sr1058 Fact 22, p. 15). Under Jorgenson/IGEM, a capital or labor tax cut reduces average exposure to approximately 0.5% versus 3.5% under the most stringent carbon tax without redistribution (sr1058 Fact 20, p. 14).

**Bank-level control variables** that Jung et al. use in their regressions provide additional context: bank assets, loan-to-assets ratio, return on assets, leverage ratio, deposit ratio, loan-loss-reserves ratio, and ratio of non-interest income to net income (sr1058 Fact 26, p. 18).

**C&I vs. consumer differentiation**: Consumer loans are driven more by unemployment, household income, and consumer confidence. C&I loans are more exposed to sector-specific carbon pricing. Jung et al. focus exclusively on C&I loans because general equilibrium models do not provide estimates of how carbon taxes impact heterogeneous households (sr1058 Fact 53, p. 8). This consumer-exposure gap is a meaningful limitation for the project, which targets both BUSLOANS and CONSUMER.

**Supporting evidence**:
- sr1059 Fact 82 (pp. 5, 9-10): GDP, unemployment, inflation, house prices, interest rates as key mediators
- sr1059 Fact 83 (p. 6): Figure 1 cascade from climate to macro to risk to loss
- sr1059 Fact 16 (p. 10): GDP impacts of -1.97%, -2.86%, -5.66%
- sr1059 Fact 25 (p. 13): DICE vs. Weitzman damage function approaches
- sr1058 Fact 23 (p. 16): G-Cubed carbon price trajectories
- sr1058 Facts 19-22 (pp. 13-15): Jorgenson and Goulder carbon tax and redistribution designs
- sr1058 Fact 26 (p. 18): Bank-level control variables in regressions
- sr1058 Fact 53 (p. 8): Consumer loan gap -- GE models lack household-level effects
- case-study Fact 7: Explicit list of relevant macro variables

**Contradicting or qualifying evidence**:
- sr1058 Fact 22 (p. 15): Corporate tax cut can make average bank exposure *negative* -- policy design matters as much as carbon price level.
- sr1058 Fact 54 (p. 10): GE models do not account for international leakage.
- fred Fact 35: GDP and interest rates are endogenous with respect to lending, requiring VAR-style models.

---

### Q4: What are the key data characteristics and challenges for modeling this relationship?
**Answer confidence**: strong

**Unprecedented nature of the shock**: A fundamental challenge, directly from the PDF: "Unlike other stress scenarios such as housing price declines, no historical precedent exists for either extreme physical or transition risk realizations that would allow a careful calibration of their broader economic effects" (sr1059 Fact 8, p. 8). This means understanding the climate-GDP relationship "requires the use of structural economic models" rather than purely statistical extrapolation (sr1059 Fact 24, p. 13).

**Y-14Q data characteristics** (from Jung et al.): The Federal Reserve's Y-14 data covers large banks with more than $50 billion in assets (threshold raised to $100 billion in 2020:Q2), required to report detailed information on C&I loans with commitments of $1 million or more (sr1058 Fact 9, p. 8). The sample covers 42 unique banks from 2012:Q3 to 2023:Q1, producing 1,340 bank-quarterly observations after merging with emissions and industry-level data (sr1058 Facts 11, 18, pp. 8-9, 12). The Y-14 includes both syndicated and non-syndicated loans, providing complete portfolio snapshots (sr1058 Fact 70, p. 8). Trucost emissions data is available from 2013:Q1 to 2021:Q4, covering scope 1 emissions from CDP disclosures (sr1058 Fact 13, p. 9).

**Industry classification granularity**: The three GE models use different industry resolutions. Jorgenson/IGEM covers 36 NAICS-mapped industries; Goulder/E3 covers 35 industries with granular energy sub-sectors (coal mining, coal-fired electricity, nonfossil electricity, oil extraction, etc.); G-Cubed covers 12 industries with a 20-industry extended version (sr1058 Fact 12, pp. 9, 13, 15, 16). Matching Y-14 loans to these models drops between 1.2% and 6.9% of loans depending on the model (sr1058 Fact 17, pp. 10, 13, 15, 16).

**Emissions data limitations**: Bank-level emission models generate "sizable discrepancies of emission estimates for the same counterparty" (sr1059 Fact 76, p. 27). The FSB-NGFS identifies major data gaps including: granular climate-related information such as carbon emissions, geographical location data, forward-looking transition plans, industry classification codes, and climate-related projections (sr1059 Fact 50, p. 27). Carbon emissions explain at most 60% of bank transition exposures -- emission intensity explains even less (sr1058 Fact 41, p. 29).

**Frequency mismatch**: NGFS scenario data is annual. BUSLOANS and CONSUMER are monthly. GDP is quarterly. This fundamental mismatch requires interpolation, aggregation, or mixed-frequency modeling (web-ngfs Fact 24; fred Fact 21; stress-testing Fact 28). The G-Cubed model is the only GE model providing annual estimates along the transition path (2020-2050); Jorgenson and Goulder provide only cumulative end-horizon effects (sr1058 Fact 68, pp. 4, 26).

**COVID-19 structural break**: The PPP spike in BUSLOANS (~$700B in weeks) is a structural break that does not reflect normal dynamics (fred Fact 6). BofA explicitly flagged this: "We regularly ask people doing models, how do you treat the COVID period?" (kickoff Facts 33-34).

**Static balance sheet assumption**: Both papers assume banks maintain the same industry shares over time (sr1058 Fact 16, pp. 2, 11). Only 20% of climate exercises adopted dynamic or hybrid balance sheet approaches (sr1059 Fact 35, p. 19). This assumption overstates losses since banks would reduce exposures to stressed sectors over time.

**Within-industry sorting**: Jung et al. test whether banks sort borrowers within industries based on emissions at the 4-digit NAICS level. They find the R-squared is at most 5% and the fitted trend is flat, indicating no evidence of within-industry sorting (sr1058 Fact 36, p. 25).

**Financial frictions omitted**: The GE models do not consider how financial frictions affect the implications of transition risks (sr1058 Fact 64, p. 3). They also do not capture how firms may endogenously change business models in response to policies (sr1058 Fact 55, p. 11).

**Book vs. market value**: Regulatory stress tests mark loan books at book values, whereas market values may be substantially lower (market-to-book ratio less than one), as illustrated by the Silicon Valley Bank failure (sr1059 Fact 51, p. 27).

**Supporting evidence**:
- sr1059 Fact 8 (p. 8): No historical precedent for extreme climate risk realizations
- sr1059 Fact 24 (p. 13): Structural models required; statistical methods insufficient alone
- sr1059 Fact 50 (p. 27): FSB-NGFS data gaps
- sr1059 Fact 76 (p. 27): Emission estimate discrepancies across bank models
- sr1058 Facts 9, 11, 13, 18 (pp. 8-9, 12): Y-14Q data details (42 banks, 2012-2023, Trucost)
- sr1058 Fact 12 (pp. 9, 13, 15, 16): Three GE models with different industry coverage
- sr1058 Fact 17 (pp. 10, 13, 15, 16): Loan matching drop rates by model
- sr1058 Fact 36 (p. 25): No within-industry borrower sorting
- sr1058 Fact 68 (pp. 4, 26): Only G-Cubed provides annual path estimates
- fred Facts 5-6, 21-28: FRED data characteristics and structural breaks

**Contradicting or qualifying evidence**:
- sr1058 Fact 71 (pp. 13-14): Bank loan portfolio composition is persistent, supporting the static portfolio assumption.
- sr1059 Fact 36 (p. 19): Banks are already dynamically responding to climate risks, partly invalidating the static assumption.

---

### Q5: What forecasting frameworks are appropriate for climate stress testing of loan portfolios?
**Answer confidence**: strong

Climate stress tests commonly have three components: scenario, model, and outcome (sr1059 Fact 1, p. 5). The scenario designs both direct and indirect impact pathways. The model translates scenarios into financial outcomes. Outcomes include bank capital shortfalls, net interest income (NII), pre-provision net revenue (PPNR), and balance sheet projections (sr1059 Fact 3, p. 5).

**The two-stage conditional forecasting framework** remains the most defensible approach:

1. **Stage 1**: Estimate historical relationships between macro variables and loan outcomes using FRED data.
2. **Stage 2**: Feed NGFS-scenario-implied macro paths through the estimated model.

This parallels CCAR/DFAST methodology, which can be "adapted for climate stress testing by replacing the macroeconomic scenario paths with climate-scenario-conditioned macro paths, while retaining the same credit loss modeling infrastructure" (sr1059 Fact 4, p. 5; stress-testing Fact 4).

**The three general equilibrium models from Jung et al.** provide an important methodological benchmark:

1. **Jorgenson/IGEM** (sr1058 Facts 12, 19, pp. 9, 13): 36 NAICS-mapped industries. Tests carbon taxes with initial levels of $25 and $50, growth rates of 1% and 5%, and three redistribution mechanisms (lump sum, capital tax cut, labor tax cut). Provides cumulative end-horizon effects. Average bank exposure: 0.5%-3.5%.

2. **Goulder-Hafstead/E3** (sr1058 Facts 12, 21, pp. 9, 15): 35 industries with granular energy sub-sectors. Models a $20 carbon tax growing at 4%/year to $60/ton by 2048. Provides changes in industry profits over infinite horizon. Average bank exposure: -1% to 1%. Uniquely, corporate tax cut scenario shows *positive* net effects for 20 of 35 industries.

3. **G-Cubed / NGFS** (sr1058 Facts 12, 23, pp. 9, 16): 12-20 industries. Endogenously determines carbon tax needed for climate goals. Only model providing annual transition path estimates (2020-2050). Average bank exposure: 2%-6.4%. Orderly and disorderly scenarios produce highest exposures.

The **CRISK market-based methodology** from Acharya et al. offers an alternative top-down approach (sr1059 Fact 52, p. 28). It involves three steps: (1) propose a climate risk factor measurable at high frequency -- the "stranded asset portfolio" goes long 30% XLE + 70% KOL and short SPY (sr1059 Fact 53, p. 28); (2) measure banks' stock return sensitivity to this factor ("climate beta") using Dynamic Conditional Beta (sr1059 Fact 55, p. 28); (3) compute expected capital shortfall: CRISK = kD - (1-k)W(1 - LRMES), where k is the prudential capital level (sr1059 Fact 54, p. 29). The approach is validated against Y-14 loan-weighted climate betas (sr1059 Fact 56, pp. 29-30). Key limitation: CRISK only measures shortfall to the extent markets price climate risk (sr1059 Fact 58, p. 29).

**The exposure measure from Jung et al.** is: Exposure = sum of (bank's loan share to industry j) * (industry j markdown under policy P). This assumes proportional impairment of loans to industry output/profit changes (sr1058 Fact 15, p. 10). Three alternative approaches are presented: (1) one-to-one proportional; (2) adjusting for historical PD and LGD from Y-14; (3) assuming riskiest industries lose entire value (sr1058 Fact 30, p. 3). Adjusting for PD/LGD reduces exposures by 1-5%, bringing estimates to about 1-2% after adjustment (sr1058 Fact 31, p. 22).

**For the project specifically**, the recommended approach is: VAR or ADL models trained on FRED data (GDP, unemployment, CPI, interest rates linked to BUSLOANS/CONSUMER growth), with NGFS NiGEM paths as scenario inputs. This aligns with how central banks structure their climate stress tests (stress-testing Facts 21-23, 35, 37). Transparency is paramount -- "the audience is regulators and executives" (kickoff Fact 13).

**Key course methods**: AR models as baseline (course Fact 12); distributed lag models for dynamic multipliers (course Fact 27); ADL for combining autoregressive and exogenous components (course Fact 43); VAR for multivariate dynamics (course Fact 38). HAC standard errors for distributed lag specifications (course Fact 32). Box-Jenkins model selection recipe (course Fact 20).

**Important paper-sourced limitations**: There is "much model risk involved in projecting climate change in different scenarios and mapping them into economic damages and bank loan loss or mark-to-market corrections" (sr1059 Fact 60, p. 33). General equilibrium models do not capture firm-level endogenous business model changes (sr1058 Fact 55, p. 11), international leakage effects (sr1058 Fact 54, p. 10), or financial frictions (sr1058 Fact 64, p. 3).

**Supporting evidence**:
- sr1059 Fact 1 (p. 5): Three components of climate stress tests
- sr1059 Facts 52-58 (pp. 28-30): CRISK methodology, stranded asset factor, validation
- sr1059 Fact 60 (p. 33): "Much model risk" in projections
- sr1058 Fact 15 (p. 10): Core exposure measure formula
- sr1058 Facts 12, 19, 21, 23 (pp. 9, 13, 15, 16): Three GE model specifications
- sr1058 Facts 30-31 (pp. 3, 22): PD/LGD-adjusted exposure measures
- stress-testing Facts 21-22, 35: VAR, bridge equations, transparent models
- course Facts 12, 20, 27, 38, 43: AR, Box-Jenkins, distributed lags, VAR, ADL

**Contradicting or qualifying evidence**:
- sr1059 Fact 8 (p. 8): No historical precedent -- statistical techniques have limited usefulness for climate risk calibration.
- sr1059 Fact 58 (p. 29): CRISK only captures market-priced risk; underpriced risks are missed.
- sr1059 Fact 35 (p. 19): Only 20% of exercises adopted dynamic balance sheet approaches.

---

### Q6: How have regulators and central banks approached climate stress testing?
**Answer confidence**: strong

At least 23 jurisdictions have conducted a total of 35 scenario analyses and climate stress tests (sr1059 Fact 17, p. 10). The regulatory landscape is broad and evolving.

**U.S. Federal Reserve**: The Fed's 2023 pilot used Current Policies and Net Zero 2050 for the transition risk module, and IPCC SSP2-4.5/RCP4.5 and SSP5-8.5/RCP8.5 for the physical risk module (sr1059 Fact 20, p. 11). Under Net Zero 2050, the projected U.S. carbon price reaches $162/ton by 2030 (sr1059 Fact 66, p. 46). Fed Chair Powell stated in January 2023: "Without explicit congressional legislation, it would be inappropriate for us to use our monetary policy or supervisory tools to promote a greener economy" (sr1059 Fact 61, p. 31). The exercise was rescinded in 2025 (kickoff Fact 10). The Fed distinguishes between scenario analysis (exploratory, long-term) and stress testing (regulatory, short-term capital adequacy) (sr1059 Fact 79, p. 3).

**European Central Bank**: The 2022 exercise found that under a short-term three-year disorderly transition scenario and two physical risk scenarios, combined credit and market risk losses for 41 banks would amount to approximately **70 billion EUR** -- though the ECB cautioned there was no economic downturn accompanying the negative climate effects in the scenario design (sr1059 Fact 44, p. 26). The ECB projected cumulative GDP growth of 65% under orderly, 58% under disorderly, and 57% under hot house world from 2021 to 2050, with the short-term disorderly scenario showing 7.4% growth vs. 10.5% baseline from 2021-2024 (sr1059 Fact 64, p. 43). The ECB also noted that bank models generate "sizable discrepancies of emission estimates for the same counterparty" (sr1059 Fact 76, p. 27). The later ECB exercise (2023) found expected losses of European banks' credit portfolios around 0.7% of total loan exposure under accelerated and delayed transitions, and 0.9% under "late push" (sr1058 Fact 50, pp. 3, 5-6).

**Bank of England**: The CBES used Early Action, Late Action, and No Additional Action scenarios. Credit losses were 30% higher in Late Action than Early Action (sr1059 Fact 46, p. 26). UK GDP projections: 1.4% below counterfactual (Early), 4.6% (Late), 7.8% (No Additional Action) by 2050 (sr1059 Fact 65, p. 45).

**Banque de France**: Under Orderly Transition, cost of credit risk estimated at 15.8 bps in 2050; under Sudden Transition, 17.2 bps -- 8.9% higher (sr1059 Fact 47, p. 26). Under a swift/abrupt transition, GDP down 5.5% vs. reference scenario by 2050 (sr1059 Fact 68, p. 44).

**Bank of Canada**: Projects 13% GDP reduction under orderly (consistent with Net Zero 2050) and 21% under delayed action by 2050. Largest impacts in fossil-fuel sectors: asset values 80-100% below baseline in 2050 (sr1059 Facts 45, 63, pp. 26, 42).

**De Nederlandsche Bank**: Tested a $100/ton carbon price rise, projecting 0.5% GDP reduction. A technology shock (doubling renewables share) projected 2.0% GDP *increase*. Combined policy + technology yielded 0.9% GDP increase (sr1059 Fact 69, p. 45).

**Common finding with caveat**: "While many stress test reports commonly conclude that climate-related risks do not (yet) pose a significant threat to financial stability, this conclusion usually includes caveats regarding the many assumptions behind the analyses" (sr1059 Fact 48, p. 26).

**Supporting evidence**:
- sr1059 Fact 17 (p. 10): 23 jurisdictions, 35 exercises
- sr1059 Facts 44, 46-47 (p. 26): ECB 70B EUR, BoE 30% higher losses, BdF credit costs
- sr1059 Fact 48 (p. 26): Common conclusion with caveats
- sr1059 Fact 61 (p. 31): Powell quote on Fed mandate limits
- sr1059 Fact 79 (p. 3): Scenario analysis vs. stress test distinction
- sr1059 Facts 63-69 (pp. 42-46): Cross-jurisdictional GDP and loss projections
- sr1058 Fact 50 (pp. 3, 5-6): ECB 2023 exercise -- 0.7-0.9% loss rates
- kickoff Facts 6-10: European and U.S. regulatory timeline

**Contradicting or qualifying evidence**:
- sr1059 Fact 61 (p. 31): Fed explicitly limiting climate work to existing mandates.
- sr1059 Fact 48 (p. 26): "Not yet a significant threat" conclusion comes with heavy caveats.
- kickoff Fact 10: U.S. CSA rescinded in 2025, reducing near-term regulatory pressure.

---

### Q7: How do loan portfolio outcomes differ across NGFS scenarios?
**Answer confidence**: moderate-to-strong (substantially improved from v1 with specific numbers)

The PDF extractions provide specific quantitative benchmarks for scenario differentiation.

**Average bank exposure across general equilibrium models (Jung et al., as of 2023)**:

| Model | Scenario | Average Bank Exposure |
|-------|----------|----------------------|
| Jorgenson/IGEM | $25 tax, 1% growth | ~0.5% |
| Jorgenson/IGEM | $50 tax, 5% growth | ~3.5% |
| Jorgenson/IGEM | Most severe + redistribution (lump sum) | ~2% |
| Goulder/E3 | Carbon tax, lump sum | ~1% |
| Goulder/E3 | Carbon tax + corporate tax cut | **-1%** (banks benefit) |
| G-Cubed/NGFS | Current Policy | ~2% |
| G-Cubed/NGFS | Orderly Transition | ~6% |
| G-Cubed/NGFS | Disorderly Transition | ~6.4% |

Source: sr1058 Facts 4-6 (pp. 3-4, 15, 17)

The **maximum exposure** under the strictest scenarios does not exceed 14% of loan portfolios, even assuming the top two deciles of affected industries lose their entire value (sr1058 Fact 3, p. 3). For reference, banks projected a 7% C&I loss rate under the 2023 Stress Test severely adverse scenario.

**Cross-sectional variation**: Under NGFS Disorderly, the 10th-to-90th percentile range of bank exposures is 0.02 to 0.14 (2% to 14%), showing substantial heterogeneity (sr1058 Fact 58, p. 46). Under Jorgenson, the range is narrow (3%-4% for the most stringent scenario -- sr1058 Fact 59, p. 46).

**Extreme stress scenarios**: Assuming the top two deciles of industries lose all value under Jorgenson yields ~14% exposure. Under Goulder, ~5%. Under NGFS, ~7% (sr1058 Facts 33-34, pp. 4, 24). Under NGFS disorderly, gas extraction and utilities are assumed to see output drop by 100%, and coal by about 96% by 2050 (sr1058 Fact 35, p. 24).

**Temporal dynamics under NGFS scenarios**: Under Disorderly Transition, banks face no exposure from 2020 to 2029 (no policy in place), but experience a steep increase after 2030 policy enactment, leading to at most a 4% immediate decline in loan portfolio value (sr1058 Fact 37, pp. 4, 26). The decrease in bank loan values is gradual for all scenarios, and exposures have fallen by about 3 percentage points since 2014, primarily due to increased lending to the "services" sector (sr1058 Fact 24, p. 17).

**PD/LGD adjustment effect**: Adjusting for historical probability of default and loss given default reduces exposures by 1-5%, bringing most estimates to about 1-2% (sr1058 Fact 31, p. 22).

**Scaling by capital**: When exposures are scaled by bank capital (equity) rather than total loans, they approximately double: 12% for NGFS, 6% for Jorgenson, 3% for Goulder (sr1058 Fact 39, pp. 27-28).

**CRISK results (Acharya et al.)**: Under a stress scenario where the stranded asset factor falls by 50%, aggregate CRISK of the top four U.S. banks increased by **$425 billion**, approximately **47% of their market capitalization**. 40% of the increase came from rising climate betas and 40% from declining equity values (sr1059 Fact 57, p. 30).

**Cross-jurisdictional comparisons**:
- ECB combined losses: ~70 billion EUR under short-term disorderly + physical risk (sr1059 Fact 44, p. 26)
- Bank of England: Late Action losses 30% higher than Early Action (sr1059 Fact 46, p. 26)
- Bank of Canada: Fossil fuel assets 80-100% below baseline by 2050 (sr1059 Fact 45, p. 26)
- Banque de France: Disorderly credit risk cost 8.9% higher than orderly (sr1059 Fact 47, p. 26)

**Supporting evidence**:
- sr1058 Facts 3-6 (pp. 3-4, 15, 17): Average bank exposures across three models
- sr1058 Facts 33-34 (pp. 4, 24): Extreme stress scenario bounds (max 14%)
- sr1058 Fact 37 (pp. 4, 26): Disorderly transition temporal dynamics
- sr1058 Fact 58 (p. 46): Cross-sectional variation in NGFS disorderly
- sr1059 Fact 57 (p. 30): CRISK $425B increase for top 4 banks
- sr1059 Facts 44-47 (p. 26): Cross-jurisdictional loss comparisons
- sr1058 Fact 31 (p. 22): PD/LGD adjustment effect

**Contradicting or qualifying evidence**:
- sr1059 Fact 48 (p. 26): Most reports conclude climate risks do not yet pose a significant threat -- but with heavy caveats.
- sr1058 Fact 24 (p. 17): Exposures have fallen ~3 percentage points since 2014 due to portfolio shifts toward services.
- sr1058 Fact 22 (p. 15): Under Goulder/E3 with corporate tax cuts, average bank exposure is *negative*.

---

### Q8: What are the implications for financial stability and risk management?
**Answer confidence**: moderate

**System-wide assessment**: The average bank's exposure to transition risk does not exceed 14% of C&I loan portfolios even under extreme stress assumptions (sr1058 Fact 3, p. 3). For reference, the 2023 Fed severely adverse scenario projected a 7% C&I loss rate. However, the CRISK analysis shows that a stranded asset stress event could increase capital shortfall of the top four banks by $425 billion (sr1059 Fact 57, p. 30), suggesting that market-based measures capture additional risk dimensions beyond loan book analysis.

**Concentration risk, not systemic collapse**: The risk is concentrated in banks with heavy exposure to carbon-intensive industries. Under NGFS Disorderly, some banks face up to 14% exposure while others face only 2% (sr1058 Fact 58, p. 46). Banks' exposures are about 5% higher in NGFS orderly and 6% higher in disorderly than current policy, with effects strongest for high-emitting banks (sr1058 Fact 42, pp. 30-31).

**Banks are already responding**: After the Paris Agreement, highly-exposed banks reduced lending to the riskiest industries (sr1058 Fact 43, pp. 32-34). Banks that signed the Net-Zero Banking Alliance reduced exposures relative to non-signatories, mainly by cutting lending to riskiest industries. The odds ratio of the riskiest industries switching from signatory to non-signatory banks increased from 5.2 to 6.1 (sr1058 Facts 44-46, pp. 34-36). However, this raises a concern about **risk migration**: borrowers in risky industries disproportionately switched from signatory to non-signatory banks (sr1058 Fact 46, pp. 35-36), suggesting risk is being transferred rather than eliminated from the financial system.

**Network and contagion effects**: Battiston et al. (2017) find that while direct exposures to fossil fuels via equity holdings are small, combined exposures through counterparties are "substantially larger" (sr1059 Fact 49, pp. 26-27). Roncoroni et al. (2021) extend this to four rounds of contagion, finding that stronger market conditions support more ambitious climate policies at the same level of risk (sr1059 Fact 75, p. 27). Climate change also affects non-bank institutions -- insurance companies, mutual funds, pension funds -- creating additional systemic channels (sr1059 Fact 74, p. 33).

**Green capital requirements create subtle effects**: Oehmke and Opp (2021) find that raising capital requirements for brown loans might crowd out green lending if the marginal loan is green (income effect). Reducing requirements for green firms might raise bank leverage and reduce financial stability (sr1059 Fact 77, pp. 31-32).

**Climate risk underpricing**: In a Stroebel and Wurgler (2021) survey, 60% of respondents said climate risks were not priced enough in equity markets and 67% said they were not priced enough in real estate markets. Essentially no investor believed these risks were overpriced (sr1059 Fact 42, p. 24). Coastal homes vulnerable to sea level rise are priced at a 6.6% discount (Bernstein et al. 2019), and flood zone houses sell for 2.8% less (Baldauf et al. 2020) (sr1059 Fact 41, p. 22).

**The "act early" policy message**: Across all exercises -- ECB, BoE, Fed pilot, Banque de France -- orderly/early action produces lower losses than disorderly/delayed action (sr1059 Fact 46, p. 26; stress-testing Fact 45). This is the single most important strategic insight.

**Research priorities** identified by Acharya et al. (sr1059 Fact 62, p. 2):
1. Identify channels through which plausible scenarios lead to meaningful short-run credit risk impacts given typical loan maturities
2. Incorporate bank-lending responses to climate risks
3. Assess adequacy of climate risk pricing in financial markets
4. Understand how market participants form climate risk expectations

**Emerging risks**: Biodiversity risks may become similarly important and regulators may want to incorporate them into stress testing frameworks (sr1059 Fact 78, p. 33).

**Supporting evidence**:
- sr1058 Fact 3 (p. 3): Max 14% exposure bound
- sr1058 Facts 43-46 (pp. 32-36): Bank behavioral responses, Net-Zero Alliance, risk migration
- sr1059 Fact 57 (p. 30): CRISK $425B capital shortfall
- sr1059 Facts 41-42 (pp. 22, 24): Asset mispricing evidence
- sr1059 Fact 49 (pp. 26-27): Network/contagion effects
- sr1059 Fact 62 (p. 2): Research agenda
- sr1059 Fact 77 (pp. 31-32): Green capital requirement unintended effects
- sr1059 Fact 74 (p. 33): Non-bank institution channels
- sr1059 Fact 78 (p. 33): Biodiversity risk horizon

**Contradicting or qualifying evidence**:
- sr1059 Fact 48 (p. 26): Most exercises conclude climate risks are not yet a significant threat -- but with heavy caveats about assumptions.
- sr1059 Fact 37 (p. 19): Disaster-driven loan losses may be offset by increased loan demand.
- sr1058 Fact 39 (pp. 27-28): Even scaled by capital, exposures do not change the "modest exposure" conclusion.

---

## Cross-Cutting Themes

### Theme 1: The "Double Translation" Problem with Quantitative Guardrails
The cascade from climate scenarios through IAMs through macro models through credit models compounds model uncertainty at each step. Acharya et al. acknowledge "much model risk" in this chain (sr1059 Fact 60, p. 33). However, the PDF extractions now provide quantitative guardrails: Jung et al. bound average bank exposure at 0.5%-6.4% in baseline scenarios and at most 14% under extreme stress assumptions (sr1058 Facts 3-6). This means that while the point estimates are imprecise, the range of plausible outcomes is bounded.

### Theme 2: Orderly Beats Disorderly -- Confirmed Across All Jurisdictions
Every central bank exercise confirms that early, gradual action produces lower financial losses than delayed, abrupt action (sr1059 Facts 44-47, p. 26). The Bank of England found late action losses 30% higher; the Banque de France found disorderly credit costs 8.9% higher; the Bank of Canada found fossil fuel assets 80-100% below baseline under transition scenarios.

### Theme 3: Model Choice Matters as Much as Scenario Choice
The three GE models in Jung et al. produce dramatically different exposure estimates for essentially similar climate policies: Jorgenson yields 0.5-3.5%, Goulder yields -1% to 1%, and G-Cubed/NGFS yields 2-6.4% (sr1058 Facts 4-6). The difference between models (up to 7 percentage points) is comparable to the difference between scenarios within any single model. Revenue recycling policy (lump sum vs. corporate tax cut) can swing exposures by 2-3 percentage points. This structural model uncertainty should be prominently discussed.

### Theme 4: C&I vs. Consumer -- An Acknowledged Gap
Jung et al. explicitly state that their analysis is limited to C&I loans because general equilibrium models "do not provide estimates of how carbon taxes would impact heterogeneous households" (sr1058 Fact 53, p. 8). For this project, which targets both BUSLOANS and CONSUMER, the consumer loan channel must rely on indirect macroeconomic transmission (unemployment, inflation, income effects) rather than the sector-specific methodology that anchors the C&I analysis.

### Theme 5: Banks Are Already Adapting
The static balance sheet assumption in most stress tests overstates realized losses. Post-Paris Agreement, exposed banks reduced lending to riskiest industries (sr1058 Fact 43). Net-Zero Alliance signatories cut brown lending. Lenders charge higher rates for climate-exposed properties and shorten loan maturities for high-emission firms (sr1059 Fact 36, p. 19). However, risk migration to non-signatory banks means total financial system exposure may not decline as much as individual bank exposure.

### Theme 6: Market-Based vs. Balance-Sheet Approaches Complement Each Other
Acharya et al. propose complementing bottom-up regulatory stress tests with the top-down CRISK market-based approach (sr1059 Fact 60, p. 33). The CRISK method captures risk to the extent markets price it (sr1059 Fact 58, p. 29), while balance sheet approaches capture exposures markets may not yet have priced. A Stroebel-Wurgler survey suggests significant underpricing in both equity and real estate markets (sr1059 Fact 42, p. 24).

---

## Knowledge Gaps

**Gap 1: Quantitative NGFS NiGEM outputs for the U.S.** The actual numerical GDP, unemployment, inflation, and interest rate paths under each NGFS scenario for the U.S. have not been downloaded from the IIASA portal. These are the exogenous inputs required for Stage 2 scenario-conditional forecasting. The Fed pilot projects specific U.S. GDP levels ($24,030B vs. $23,574B by 2030 under Current Policies vs. Net Zero -- sr1059 Fact 66, p. 46), but the full time series paths are needed.

**Gap 2: Historical statistical properties of BUSLOANS and CONSUMER.** The series have not been downloaded, transformed, or tested for unit roots, ACF/PACF structures, or preliminary model fits. This is essential before specifying the forecasting model.

**Gap 3: Consumer loan exposure methodology.** Jung et al. explicitly cannot estimate consumer exposure using their GE model approach (sr1058 Fact 53, p. 8). For the CONSUMER series, the project must rely on indirect macroeconomic channels (unemployment, inflation, energy costs), which is a less precise methodology than the sector-specific approach available for C&I.

**Gap 4: Within-model-family scenario comparison.** While the three GE models in Jung et al. are well-documented, the NGFS NiGEM outputs across multiple IAM families (GCAM, REMIND, MESSAGEix) for the same scenario have not been compared for U.S.-specific macro variables. The differences between GCAM and REMIND for the same scenario may be as large as differences between scenarios.

**Gap 5: Short-term NGFS scenarios.** Phase IV introduced quarterly macro-financial scenarios for 1-5 year horizons (stress-testing Fact 30). These would partially resolve the frequency mismatch issue and are more directly applicable to near-term forecasting, but their availability has not been confirmed.

**Gap 6: Revenue recycling assumptions in NGFS scenarios.** Jung et al. show that revenue recycling policy (lump sum vs. corporate tax cut) swings average bank exposure by 2-3 percentage points (sr1058 Facts 20, 22). It is unclear what revenue recycling assumptions the NGFS NiGEM macro projections embed, and this could materially affect the scenario-conditional forecasts.

---

## Methodological Notes

### Three General Equilibrium Models: A Detailed Comparison

| Feature | Jorgenson/IGEM | Goulder-Hafstead/E3 | G-Cubed/NGFS |
|---------|---------------|---------------------|--------------|
| Industries | 36 (NAICS-mapped) | 35 (granular energy) | 12 (20 extended) |
| Carbon tax design | $25-$50 initial, 1-5% growth | $20 initial, 4% growth to $60 | Endogenous ($3.72-$121.97) |
| Revenue recycling | Lump sum, capital cut, labor cut | Lump sum, payroll cut, income cut, corporate cut | Infrastructure, debt, lump sum |
| Output type | Cumulative end-horizon | Infinite-horizon profit changes | Annual path (2020-2050) |
| Avg bank exposure | 0.5%-3.5% | -1% to 1% | 2%-6.4% |
| Loans dropped (matching) | 1.2% | 6.9% | 3.6% |
| Key insight | Redistribution policy dominates | Corporate tax cut makes exposure negative | Highest exposures; only annual path model |

Sources: sr1058 Facts 12, 17, 19-24 (pp. 9-17)

### CRISK Formula and Components

CRISK_it = kD_it - (1-k)W_it(1 - LRMES_it)

Where:
- k = prudential capital level (e.g., 8%)
- D = bank book value of debt
- W = bank market capitalization
- LRMES = Long-Run Marginal Expected Shortfall (estimated via Dynamic Conditional Beta)

Climate beta estimated from the stranded asset portfolio: 30% XLE + 70% KOL, short SPY.

Sources: sr1059 Facts 52-57 (pp. 28-30)

### Recommended Model-Building Workflow (Updated)

1. **Download and transform data**: BUSLOANS, CONSUMER from FRED. Apply log-differencing. Unit root tests (ADF, KPSS).
2. **Univariate baseline**: AR(1) or AR(2) for loan growth. ACF/PACF diagnostics.
3. **Multivariate estimation**: ADL or VAR with GDP growth, unemployment change, interest rate changes. AIC/BIC for lag selection.
4. **COVID treatment**: Test at least two approaches (exclusion vs. dummy). Document sensitivity.
5. **NGFS scenario conditioning**: Download NiGEM U.S. macro paths. Interpolate to quarterly if needed. Feed through estimated model.
6. **Scenario comparison**: Compare loan trajectories across Net Zero 2050, Delayed Transition, Current Policies. Include at least two NGFS model families if feasible.
7. **Contextualize against PDF benchmarks**: Compare project aggregate results against Jung et al. exposure bounds (0.5%-6.4% baseline, max 14% extreme) and Acharya et al. CRISK magnitudes ($425B for top 4 banks).
8. **Robustness**: Subsample stability, alternative COVID treatments, model family comparisons.

### Key Quantitative Benchmarks from the PDFs

| Metric | Value | Source |
|--------|-------|--------|
| World GDP impact, Net Zero 2050 (chronic physical) | -1.97% | sr1059 Fact 16, p. 10 |
| World GDP impact, Delayed Transition | -2.86% | sr1059 Fact 16, p. 10 |
| World GDP impact, Current Policies | -5.66% | sr1059 Fact 16, p. 10 |
| Max bank C&I exposure, extreme stress | 14% | sr1058 Fact 3, p. 3 |
| CRISK increase, top 4 banks, 50% stranded asset decline | $425B (~47% mkt cap) | sr1059 Fact 57, p. 30 |
| ECB combined credit + market losses, disorderly | ~70B EUR | sr1059 Fact 44, p. 26 |
| BoE Late vs. Early Action credit loss differential | 30% higher | sr1059 Fact 46, p. 26 |
| Banque de France orderly vs. sudden credit cost | 15.8 bps vs. 17.2 bps | sr1059 Fact 47, p. 26 |
| ECB 2023 expected losses, all scenarios | 0.7%-0.9% of exposure | sr1058 Fact 50, pp. 3, 5-6 |
| Goulder/E3 corporate tax cut scenario | -1% (banks benefit) | sr1058 Fact 22, p. 15 |
| G-Cubed orderly carbon price by 2050 | $119.14/ton | sr1058 Fact 23, p. 16 |
| G-Cubed disorderly carbon price by 2050 | $121.97/ton | sr1058 Fact 23, p. 16 |
| Y-14Q sample | 42 banks, 2012:Q3-2023:Q1 | sr1058 Fact 11, pp. 8-9 |
| Heat stress effect on S&P500 returns | +45 bps/yr per 1 SD exposure | sr1059 Fact 39, p. 21 |
| Heat stress effect on sub-IG bond spreads | +40 bps per 1 SD exposure | sr1059 Fact 40, p. 22 |
| Coastal home sea-level-rise discount | 6.6% | sr1059 Fact 41, p. 22 |
| Emissions explain of bank exposure (max) | 60% | sr1058 Fact 7, pp. 4, 29 |
| Average U.S. bank loan maturity at origination | 3-5 years | sr1059 Fact 28, p. 17 |

---

## Recommendations

### Immediate Next Steps (Phase 1: Before Feb 20 Q&A)

1. **Download NGFS NiGEM data** from IIASA portal. Filter for U.S.-specific GDP, unemployment, CPI, interest rate paths across at least two model families and three scenarios (Net Zero 2050, Delayed Transition, Current Policies). This closes Gap 1.

2. **Download and analyze BUSLOANS and CONSUMER** from FRED. Compute growth rates, run unit root tests, plot ACF/PACF. This closes Gap 2 and determines model specification.

3. **Prepare Q&A questions for Feb 20** focused on: (a) BofA's preferred COVID treatment approach; (b) whether they have a view on modeling frequency (quarterly vs. annual); (c) their perspective on the consumer loan exposure gap (sr1058 Fact 53); (d) whether they see the project as more analogous to Jung et al.'s sector-specific approach or to aggregate macro transmission.

### Modeling Phase (Phase 2: Feb 20 - March)

4. **Estimate ADL or VAR model** linking loan growth to GDP growth, unemployment, and interest rates. Start large, eliminate insignificant lags following Pesavento recipe (course Fact 20).

5. **Address frequency mismatch** by aggregating to quarterly (matching GDP) or interpolating NGFS to quarterly using cubic spline. Test sensitivity to this choice.

6. **Generate scenario-conditional forecasts** using NGFS NiGEM paths. Produce forecasts under at least three scenarios.

7. **Contextualize results** against the specific PDF benchmarks: are aggregate loan growth impacts consistent with 0.5-6.4% exposure ranges from Jung et al.? If much larger or smaller, explain why (aggregate vs. granular, C&I-only vs. total, static vs. dynamic assumptions).

### Presentation Phase (Phase 3: March - April 9)

8. **Lead with the "act early" finding**: Orderly transition produces lower financial losses across every jurisdiction and methodology examined. This is the single most important takeaway for the BofA audience.

9. **Present results as ranges, not point estimates**: Given the three GE models that produce -1% to 6.4% exposures for similar policies, emphasize that scenario ranking matters more than precise magnitudes.

10. **Explicitly discuss the consumer loan gap**: Acknowledge that the project's CONSUMER analysis operates through indirect macro channels only, while the literature's strongest results (from Jung et al.) are for C&I loans using sector-specific GE models. Frame this as an area for refinement, not a weakness.

11. **Include the CRISK methodology as a conceptual complement**: Even if not replicated, discussing how market-based approaches (using stranded asset factors and climate betas) could complement the balance-sheet approach adds methodological depth.

12. **Discuss limitations with page citations**: Reference sr1059 Fact 8 (p. 8) on lack of historical precedent, sr1059 Fact 60 (p. 33) on model risk, sr1058 Fact 53 (p. 8) on consumer loan gap, and sr1058 Fact 55 (p. 11) on firms' endogenous responses. These are not weaknesses -- they demonstrate engagement with the primary literature.

---

## Fact Attribution Index

### SR 1059 -- Acharya et al. (2023) "Climate Stress Testing" (85 facts, directly from PDF)

Key facts used by question:
- **Q1**: Facts 4, 5, 10-16, 18-23, 63-69, 80-81, 84 (scenario descriptions, GDP impacts, carbon prices, cross-jurisdictional)
- **Q2**: Facts 4-6, 23, 26-34, 36-39, 41-43, 49, 81 (transmission channels, physical/transition risk, maturity mismatch)
- **Q3**: Facts 16, 25, 82-83 (mediating variables, damage functions, cascade framework)
- **Q4**: Facts 8, 24, 35, 50-51, 76 (no precedent, data gaps, static balance sheet, emission discrepancies)
- **Q5**: Facts 1, 3, 52-60, 71 (stress test components, CRISK methodology, model risk)
- **Q6**: Facts 7, 12, 17, 20, 44-48, 61, 64-69, 79-80 (regulatory exercises, cross-jurisdictional results)
- **Q7**: Facts 16, 44-47, 57, 63-69 (specific loss estimates, CRISK results, cross-jurisdictional)
- **Q8**: Facts 37, 42, 48-49, 57, 62, 74-75, 77-78 (financial stability, network effects, research agenda)

### SR 1058 -- Jung et al. (2024) "U.S. Banks' Exposures to Climate Transition Risks" (77 facts, directly from PDF)

Key facts used by question:
- **Q1**: Facts 4-6, 12, 19, 21, 23-25, 28, 35, 37, 68-69, 72-73, 77 (GE model specifics, NGFS carbon prices, industry output)
- **Q2**: Facts 1, 7, 15, 30, 47, 49, 64 (exposure methodology, emissions limitations, transition risk focus)
- **Q3**: Facts 22-23, 26, 53 (revenue recycling, carbon prices, consumer loan gap)
- **Q4**: Facts 2, 9-13, 16-18, 36, 41, 51-53, 55, 57, 61-63, 66, 70-71 (Y-14Q data, industry classification, Trucost, sample stats)
- **Q5**: Facts 1, 12, 15-16, 19, 21, 23, 30-32, 40-41, 52, 54-56, 67-68 (GE model specifications, exposure formula, PD/LGD adjustment)
- **Q6**: Facts 2, 9, 25, 50 (Y-14Q regulatory data, ECB comparison)
- **Q7**: Facts 3-6, 20, 22, 24, 27-29, 31, 33-35, 37-39, 58-60, 74-76 (exposure estimates across all models and scenarios)
- **Q8**: Facts 3, 8, 34, 39, 42-46, 48, 65 (modest exposure conclusion, bank responses, risk migration, research agenda)

### Academic Papers -- Training Knowledge (52 facts, supplementary)
Used as supplement where sr1059/sr1058 PDF facts provide primary evidence. Training-knowledge facts corroborate directional findings but are deprioritized in favor of page-cited PDF sources for specific claims.

### Case Study PDF (24 facts)
Primary reference for project scope, deliverables, learning objectives, data sources.

### Kickoff Transcript (42 facts)
Primary reference for BofA sponsor expectations, evaluation criteria, COVID treatment importance, regulatory context.

### Course Materials (48 facts)
Primary reference for applicable forecasting methods: AR, ARMA, distributed lags, ADL, VAR, unit root testing, model selection, HAC standard errors.

### Web: NGFS and Transmission (40 facts)
Supplementary reference for NGFS scenario framework, NiGEM variables, transmission mechanisms. Training-knowledge-based; cross-referenced against PDF sources where possible.

### Web: Stress Testing Methods (45 facts)
Supplementary reference for regulatory exercises (ECB, BoE, Fed CSA), methodological frameworks. Training-knowledge-based; cross-referenced against PDF sources where possible.

### Web: FRED Data (40 facts)
Reference for FRED series characteristics, data challenges, historical patterns. Based on established FRED documentation.
