# Facts: FRED Loan Data Series & Macroeconomic Variables

**Research scope**: FRED loan series characteristics, macroeconomic determinants of bank lending, data challenges for climate-to-loans modeling.
**Date compiled**: 2026-02-12
**Note**: WebSearch and WebFetch were unavailable during this research session. Facts below are compiled from (a) project source documents (case study PDF, kickoff transcript, CLAUDE.md), (b) course materials, and (c) well-established knowledge about FRED data series from Federal Reserve documentation. Confidence ratings reflect source reliability. All FRED-specific claims should be verified by downloading the actual series.

---

## BUSLOANS Series Details

## Fact 1
- **Claim**: BUSLOANS (FRED series ID) is titled "Commercial and Industrial Loans, All Commercial Banks." It reports the outstanding balance of C&I loans held by all domestically chartered commercial banks and foreign-related institutions in the United States.
- **Source**: FRED / Federal Reserve Board H.8 release (https://fred.stlouisfed.org/series/BUSLOANS)
- **Confidence**: high
- **Relevant to**: Q3, Q4

## Fact 2
- **Claim**: BUSLOANS is reported at a monthly frequency (not seasonally adjusted in its base form), with units in billions of U.S. dollars. A seasonally adjusted variant also exists. The series begins in January 1947, providing nearly 80 years of historical data.
- **Source**: FRED / Federal Reserve Board H.8 release (https://fred.stlouisfed.org/series/BUSLOANS)
- **Confidence**: high
- **Relevant to**: Q4

## Fact 3
- **Claim**: BUSLOANS is sourced from the Federal Reserve's H.8 statistical release ("Assets and Liabilities of Commercial Banks in the United States"), which is the Fed's primary weekly/monthly report on commercial bank balance sheets.
- **Source**: FRED / Federal Reserve Board H.8 release
- **Confidence**: high
- **Relevant to**: Q4

## Fact 4
- **Claim**: The BUSLOANS series shows strong upward trend over its full history, reflecting nominal growth in bank lending. It exhibits clear cyclical behavior around recessions: C&I loans typically decline or flatten during NBER recessions (notably 2001, 2008-2009) and surge during expansions. The COVID-19 period (March-April 2020) shows an extreme spike due to PPP (Paycheck Protection Program) loans flowing through the commercial banking system, followed by a sharp decline as PPP loans were forgiven.
- **Source**: FRED data characteristics, widely documented in Federal Reserve publications and financial press
- **Confidence**: high
- **Relevant to**: Q4

## Fact 5
- **Claim**: Because BUSLOANS is a nominal dollar-denominated level series with a strong upward trend, it is almost certainly non-stationary in levels. Standard practice requires transformation before modeling -- typically log-differencing (to get growth rates) or deflating by a price index and then differencing. Unit root tests (ADF, PP, KPSS) should be applied to confirm.
- **Source**: Standard time series econometrics practice; consistent with Week 3-4 course materials on stationarity
- **Confidence**: high
- **Relevant to**: Q4, Q5

## Fact 6
- **Claim**: The COVID-19 PPP loan spike in BUSLOANS (approximately March-June 2020) represents a major structural break in the series. C&I loans jumped by roughly $700 billion in a matter of weeks as banks disbursed PPP funds, then declined sharply as those loans were forgiven. This is not a normal business-cycle pattern and poses significant modeling challenges -- it may distort estimated coefficients, autocorrelation structures, and trend estimates if not treated carefully.
- **Source**: Project kickoff transcript (BofA team explicitly flagged COVID treatment as a key modeling question); Federal Reserve data
- **Confidence**: high
- **Relevant to**: Q4

## CONSUMER Series Details

## Fact 7
- **Claim**: CONSUMER (FRED series ID) is titled "Consumer Loans, All Commercial Banks." It reports the outstanding balance of consumer loans (including auto loans, credit card loans, and other consumer credit) held by all commercial banks in the United States.
- **Source**: FRED / Federal Reserve Board H.8 release (https://fred.stlouisfed.org/series/CONSUMER)
- **Confidence**: high
- **Relevant to**: Q3, Q4

## Fact 8
- **Claim**: CONSUMER is reported at a monthly frequency with units in billions of U.S. dollars. Like BUSLOANS, both seasonally adjusted and not-seasonally-adjusted variants exist. The series begins in January 1947.
- **Source**: FRED / Federal Reserve Board H.8 release
- **Confidence**: high
- **Relevant to**: Q4

## Fact 9
- **Claim**: CONSUMER is also sourced from the Federal Reserve H.8 release ("Assets and Liabilities of Commercial Banks"). It represents the consumer credit component of commercial bank balance sheets, complementing BUSLOANS which covers the commercial/industrial component.
- **Source**: FRED / Federal Reserve Board H.8 release
- **Confidence**: high
- **Relevant to**: Q4

## Fact 10
- **Claim**: The CONSUMER series also has a strong upward trend reflecting nominal growth. It shows different cyclical dynamics than BUSLOANS: consumer loans tend to be more sensitive to household income, employment, and consumer confidence. The COVID period shows a different pattern from BUSLOANS -- consumer lending initially contracted as spending fell, then recovered as the economy reopened, without the extreme PPP-driven spike seen in C&I loans.
- **Source**: FRED data characteristics; Federal Reserve publications
- **Confidence**: high
- **Relevant to**: Q4

## Fact 11
- **Claim**: The macro variables that drive consumer loan demand differ somewhat from those driving C&I loans. Consumer loans are more directly influenced by unemployment, household income, consumer confidence, and auto sales (a large component is auto lending). C&I loans are more influenced by business investment, corporate profitability, and trade conditions. This was explicitly noted in the kickoff: "the macro variables and all that is going to be a little bit different" for consumer vs. commercial loans.
- **Source**: Kickoff transcript (Speaker 3); standard banking literature
- **Confidence**: high
- **Relevant to**: Q3

## Macroeconomic Determinants of Bank Lending

## Fact 12
- **Claim**: The case study PDF explicitly identifies the following macroeconomic variables as "most relevant to the banking sector": GDP growth, unemployment, inflation (CPI), carbon prices, and energy use. These serve as the primary candidates for mediating variables in the climate-to-loans relationship.
- **Source**: Emory_Time_Series_Climate_Case_Study.pdf, "Understand NGFS Climate Scenarios" milestone
- **Confidence**: high
- **Relevant to**: Q3

## Fact 13
- **Claim**: GDP growth is the single most important macroeconomic driver of commercial bank lending. Higher GDP growth increases demand for C&I loans (businesses borrow to invest in expansion) and consumer loans (households borrow more when incomes rise). The relevant FRED series include GDP (quarterly, real), GDPC1 (real GDP in chained 2017 dollars), and A191RL1Q225SBEA (real GDP growth rate).
- **Source**: Standard macroeconomic/banking literature; consistent with case study document
- **Confidence**: high
- **Relevant to**: Q3

## Fact 14
- **Claim**: The unemployment rate (FRED: UNRATE, monthly, seasonally adjusted) is a key mediating variable. Higher unemployment reduces demand for consumer loans (fewer employed borrowers) and increases default risk, causing banks to tighten lending standards. It also signals reduced business activity, suppressing C&I loan demand. The kickoff transcript confirmed unemployment as a relevant FRED variable.
- **Source**: Case study PDF; kickoff transcript; standard banking literature
- **Confidence**: high
- **Relevant to**: Q3

## Fact 15
- **Claim**: Interest rates -- particularly the Federal Funds Rate (FRED: FEDFUNDS or DFF) and the 10-Year Treasury yield (FRED: DGS10) -- are critical determinants of bank lending. Higher interest rates increase the cost of borrowing, reducing loan demand. They also affect bank profitability (net interest margins) and thus lending supply. The yield curve spread (10Y-2Y or 10Y-3M) is a commonly used predictor of lending activity and economic recessions.
- **Source**: Standard banking/monetary economics literature; Federal Reserve monetary transmission mechanism research
- **Confidence**: high
- **Relevant to**: Q3

## Fact 16
- **Claim**: Inflation (FRED: CPIAUCSL for CPI, or PCEPI for PCE price index) affects bank lending through multiple channels: it erodes real loan values (benefiting borrowers at the expense of lenders), influences the Fed's interest rate decisions, and affects household purchasing power. The case study PDF lists CPI explicitly as supporting FRED data.
- **Source**: Case study PDF; standard macroeconomic literature
- **Confidence**: high
- **Relevant to**: Q3

## Fact 17
- **Claim**: The Federal Reserve Senior Loan Officer Opinion Survey (SLOOS) provides quarterly data on bank lending standards and demand for loans. While not a standard FRED numeric series, related indicators (like the DRCCLACBS delinquency rate series or the DRTSCLCC charge-off rate series) capture credit quality dynamics that interact with lending volumes. Tightening of lending standards typically leads to reduced loan growth.
- **Source**: Federal Reserve SLOOS documentation; FRED data catalog
- **Confidence**: medium
- **Relevant to**: Q3, Q4

## Fact 18
- **Claim**: In climate stress testing frameworks (including NGFS-based models), the standard transmission mechanism from climate scenarios to bank lending operates through intermediate macroeconomic variables: Climate scenarios produce GDP shocks, unemployment changes, inflation shifts, and interest rate paths. These macro variables then drive loan demand, credit quality, and bank lending decisions. This "two-step" approach (climate -> macro -> loans) is the standard framework used by central banks.
- **Source**: Case study PDF (proposed milestones); Acharya et al. (2023) and Jung et al. (2024) as cited in the case study
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Fact 19
- **Claim**: Transition risk from climate change (carbon taxes, regulatory changes, policy shifts) primarily affects bank lending through GDP and energy cost channels. Carbon pricing increases production costs, which reduces GDP growth and business profitability, which reduces C&I loan demand. Physical risk (extreme weather) affects lending primarily through property damage, insurance costs, and localized economic disruption, which increases loan defaults and reduces collateral values.
- **Source**: Kickoff transcript (Speaker 1's discussion of physical vs. transition risk); case study PDF
- **Confidence**: high
- **Relevant to**: Q2, Q3

## Fact 20
- **Claim**: The NGFS scenarios provide projections for GDP, which is the primary macro variable bridging climate scenarios to loan portfolios. The NGFS also provides carbon prices, energy costs, CO2 emissions, and temperature trajectories. The modeling challenge is to establish historical relationships between GDP (and other macro variables) and loan volumes using FRED data, then apply NGFS scenario GDP paths to project future loan outcomes.
- **Source**: Case study PDF; kickoff transcript
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Data Frequency and Availability Challenges

## Fact 21
- **Claim**: A critical data challenge is the frequency mismatch between sources: BUSLOANS and CONSUMER are monthly, GDP is quarterly, and NGFS scenario data is annual. This requires either temporal aggregation (converting monthly loans to quarterly or annual) or temporal disaggregation/interpolation (converting annual NGFS data to higher frequency). The choice of approach affects model precision and interpretation.
- **Source**: CLAUDE.md (Known Data Challenges section); case study PDF
- **Confidence**: high
- **Relevant to**: Q4

## Fact 22
- **Claim**: FRED macroeconomic data has varying start dates: some series (like CPI, unemployment) go back to the 1940s-1950s, while others (like some interest rate spreads or financial conditions indices) only begin in the 1970s-1990s. The effective training window is constrained by the shortest series used. The kickoff confirmed: "you can go to stuff back to the 1940s but then you have stuff that only goes back to the 1990s."
- **Source**: Kickoff transcript (Speaker 3); FRED data catalog
- **Confidence**: high
- **Relevant to**: Q4

## Fact 23
- **Claim**: The training window selection is a design choice that involves a tradeoff: longer windows capture more business cycles (improving model robustness) but may include structural regime changes (e.g., pre-/post-Great Moderation, pre-/post-2008 financial crisis) that make older data less relevant. The kickoff transcript emphasized: "make sure that you cover enough business cycles to be able to get good results."
- **Source**: Kickoff transcript (Speaker 3)
- **Confidence**: high
- **Relevant to**: Q4

## Fact 24
- **Claim**: The COVID-19 structural break (2020) is a major modeling challenge explicitly flagged by the BofA team. Options for treatment include: (a) excluding the COVID period from training data, (b) including it with dummy variables to absorb the shock, (c) treating it as a regime shift and modeling pre/post-COVID separately, or (d) winsorizing/trimming extreme observations. The BofA team stated they "regularly ask people doing models, how do you treat the covid period?" -- indicating this is an active debate in the industry.
- **Source**: Kickoff transcript (Speaker 3 and Speaker 2); CLAUDE.md
- **Confidence**: high
- **Relevant to**: Q4

## Fact 25
- **Claim**: Both BUSLOANS and CONSUMER are national-level aggregate series. They do not provide regional, state-level, or sector-level breakdowns. This limits the ability to analyze how climate risks (which are geographically heterogeneous -- e.g., hurricanes affect coastal areas more) differentially affect loan portfolios across regions. The case study acknowledges this with "improved sectoral granularity" listed as an area for refinement.
- **Source**: FRED H.8 release structure; case study PDF (Policy & Risk Insights milestone)
- **Confidence**: high
- **Relevant to**: Q4

## Historical Patterns and Structural Breaks

## Fact 26
- **Claim**: The BUSLOANS series exhibits several notable historical patterns and structural breaks: (1) Steady growth from 1947-1970s, (2) Rapid expansion during the 1980s deregulation era, (3) S&L crisis-related slowdown in early 1990s, (4) Dot-com era expansion and contraction around 2001, (5) Strong growth during the mid-2000s credit boom, (6) Sharp contraction during the 2008-2009 Great Financial Crisis, (7) Slow recovery through the 2010s, (8) Extreme COVID PPP spike in 2020, (9) Post-COVID normalization and recent tightening cycle. Each of these episodes may represent a different lending regime.
- **Source**: FRED BUSLOANS historical data patterns; Federal Reserve publications
- **Confidence**: high
- **Relevant to**: Q4

## Fact 27
- **Claim**: The Great Moderation (roughly 1984-2007) represents a period of reduced macroeconomic volatility that coincides with more stable loan growth patterns. Many econometric models of bank lending perform differently when estimated over the pre-Moderation vs. post-Moderation sample. Starting the training window in the mid-1980s or early 1990s (post-Moderation, post-S&L crisis) is a common choice in applied bank lending models.
- **Source**: Standard macroeconomic literature (Stock & Watson, Bernanke); banking literature
- **Confidence**: high
- **Relevant to**: Q4

## Fact 28
- **Claim**: The 2008 Global Financial Crisis represents the most significant structural break in bank lending data (prior to COVID). C&I loans contracted by approximately 25% from their 2008 peak. Consumer loans also declined significantly. Post-crisis regulatory changes (Dodd-Frank, Basel III capital requirements) permanently altered bank lending behavior, making pre-2008 relationships potentially less informative for current modeling.
- **Source**: FRED data; Federal Reserve publications; banking regulation literature
- **Confidence**: high
- **Relevant to**: Q4

## Commonly Used FRED Series for Bank Lending Models

## Fact 29
- **Claim**: The most commonly used FRED series in academic and industry models of bank lending include: (1) GDP or real GDP growth (GDP, GDPC1), (2) Unemployment rate (UNRATE), (3) Federal Funds Rate (FEDFUNDS), (4) CPI inflation (CPIAUCSL), (5) 10-Year Treasury yield (DGS10), (6) Yield curve spread (T10Y2Y or T10Y3M), (7) Industrial Production (INDPRO), (8) Corporate bond spreads (BAA10Y or BAAFFM), (9) VIX or financial conditions indices (e.g., NFCI from Chicago Fed), and (10) House Price Index (CSUSHPINSA for Case-Shiller).
- **Source**: Standard banking/financial economics literature; Federal Reserve stress testing documentation
- **Confidence**: high
- **Relevant to**: Q3

## Fact 30
- **Claim**: For the specific climate-to-loans modeling task, the most relevant FRED series to serve as "bridge variables" between NGFS climate scenarios and loan outcomes are: GDP growth (directly available in NGFS scenarios), unemployment (can be derived from GDP via Okun's Law), interest rates (can be linked to inflation and central bank reaction functions), and CPI/inflation (linked to energy costs and carbon pricing in NGFS scenarios). These variables create a tractable mapping from NGFS scenario outputs to loan portfolio projections.
- **Source**: Synthesis of case study PDF, kickoff discussion, and standard climate stress testing literature (Acharya et al. 2023)
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Fact 31
- **Claim**: Corporate bond spreads (e.g., FRED: BAA10Y, the Moody's BAA corporate bond yield relative to the 10-year Treasury) serve as a useful indicator of credit conditions and financial stress. Higher spreads indicate tighter credit conditions and higher perceived default risk, which typically correlates with reduced bank lending. This series is available monthly from FRED and could serve as an additional mediating variable between macro conditions and loan portfolios.
- **Source**: Federal Reserve stress testing literature; financial economics
- **Confidence**: medium
- **Relevant to**: Q3

## Fact 32
- **Claim**: The FRED series for bank lending standards -- DRTSCILM (Net Percentage of Domestic Banks Tightening Standards for C&I Loans to Large and Middle-Market Firms) and DRTSCLCC (for credit card loans) -- are derived from the Senior Loan Officer Opinion Survey (SLOOS) and are available quarterly starting from 1990. These capture the supply side of lending (bank willingness to lend), which is influenced by macroeconomic conditions, regulatory pressure, and perceived risk -- all channels through which climate risk could affect loan portfolios.
- **Source**: Federal Reserve SLOOS; FRED data catalog
- **Confidence**: medium
- **Relevant to**: Q3, Q4

## Fact 33
- **Claim**: The course materials (Week 4 summary) demonstrate that the unemployment rate downloaded from FRED for 2000-2024 has an AR(1) coefficient of approximately 0.95, indicating "very, very persistent" dynamics. This high persistence is characteristic of many macroeconomic series that would be used in the climate-loans model, implying near-unit-root behavior that must be addressed through appropriate differencing or cointegration techniques.
- **Source**: /workspaces/forecasting-problemset0/course-materials/lectures/week-04/summary.md (Example 8: Unemployment Rate)
- **Confidence**: high
- **Relevant to**: Q4

## Fact 34
- **Claim**: The Week 5 course materials on Dynamic Causal Effects provide the methodological framework directly applicable to this project: the distributed lag model estimates how a change in X (e.g., a macro variable) affects Y (e.g., loan volumes) over multiple time periods. The course also establishes that HAC (Newey-West) standard errors must be used when modeling such relationships in time series, and that exogeneity of the regressor is required for causal interpretation.
- **Source**: /workspaces/forecasting-problemset0/course-materials/lectures/week-05/summary.md
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Fact 35
- **Claim**: For the climate-to-loans modeling framework, the exogeneity question is important: NGFS climate scenario variables (carbon prices, temperature, emissions) can plausibly be treated as exogenous to U.S. bank lending decisions (banks do not cause climate change, and individual bank lending does not meaningfully affect global carbon prices). However, intermediate macro variables like GDP and interest rates are endogenous with respect to bank lending (lending affects GDP, and the Fed adjusts rates in response to credit conditions), requiring careful modeling -- potentially VAR models that allow for simultaneous determination.
- **Source**: Synthesis of Week 5 course materials on exogeneity with project requirements
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Fact 36
- **Claim**: The Week 5 OJ price data example (dynamic effect of weather on commodity prices) provides a close analogy for the climate-loans project: both involve an exogenous climate/weather variable affecting a financial outcome through a dynamic lag structure. The key lesson from the OJ example is that the effect may be immediate but also persist over multiple periods, and the cumulative multiplier (total effect) may be larger than the impact effect.
- **Source**: /workspaces/forecasting-problemset0/course-materials/lectures/week-05/summary.md (OJ price example)
- **Confidence**: high
- **Relevant to**: Q3, Q5

## Fact 37
- **Claim**: The subsample instability observed in the OJ data (where the effect of freezes on prices changed significantly across decades) is a cautionary tale for the loan modeling project. The relationship between macro variables and bank lending has likely changed over time due to deregulation (1980s), financial innovation, the Great Financial Crisis (2008), and post-crisis regulation. Testing for structural stability across subsamples is essential.
- **Source**: /workspaces/forecasting-problemset0/course-materials/lectures/week-05/summary.md (Example 3: Subsample Instability)
- **Confidence**: high
- **Relevant to**: Q4

## Fact 38
- **Claim**: FRED provides several energy-related series relevant to climate transition risk modeling: crude oil prices (DCOILWTICO for WTI), natural gas prices (DHHNGSP), electricity prices (APU000072610 for average retail electricity), and energy commodity price indices. These can serve as proxies for or supplements to the NGFS energy cost variables, and are available at daily or monthly frequency on FRED.
- **Source**: FRED data catalog; climate risk modeling literature
- **Confidence**: medium
- **Relevant to**: Q3

## Fact 39
- **Claim**: The NGFS scenarios are annual, but the FRED loan data is monthly. A practical approach used in climate stress testing is a "two-stage" framework: (1) Estimate a historical model linking monthly/quarterly loan data to monthly/quarterly macro variables using FRED data, then (2) Feed annual NGFS macro projections (interpolated to quarterly/monthly if needed) into the estimated model to produce scenario-conditional loan forecasts. This approach is consistent with how central banks conduct climate stress tests.
- **Source**: Synthesis of case study requirements, NGFS documentation, and Acharya et al. (2023) methodology
- **Confidence**: high
- **Relevant to**: Q4, Q5

## Fact 40
- **Claim**: The FRED H.8 data (underlying both BUSLOANS and CONSUMER) underwent a methodological revision in March 2010 when the Federal Reserve changed the bank panel composition and restated historical data. Users should be aware that some apparent level shifts around this date may reflect data revision rather than genuine economic changes. The FRED series page typically documents such breaks in the series notes.
- **Source**: Federal Reserve H.8 release documentation
- **Confidence**: medium
- **Relevant to**: Q4
