# Climate Risk Impact on Banking Loan Portfolios: Summary Report (v2)

Date: 2026-02-12
Project: climate-risk-loans
Factbase: ~401 facts from 9 sources (including 162 directly from PDF papers with page citations)

## Overview

This research investigates how NGFS climate scenarios impact U.S. banking loan portfolios, focusing on aggregate commercial loans (BUSLOANS) and consumer loans (CONSUMER) from FRED. The updated analysis integrates 162 facts extracted directly from Acharya et al. (2023, SR 1059, 85 facts) and Jung et al. (2024, SR 1058, 77 facts) with page-level attribution, alongside facts from the BofA case study, kickoff transcript, course materials (Weeks 3-5), NGFS documentation, stress testing literature, and FRED data characteristics. The key finding: **disorderly transition poses the greatest short-term financial risk to banks**, but even extreme stress scenarios produce C&I loan exposure losses bounded at ~14% of portfolios (sr1058 p. 3). A two-stage conditional forecasting model — historical macro-to-loan estimation, then NGFS scenario projection — is the recommended approach.

## Key Findings

### Finding 1: Quantified GDP Impacts Across Scenarios
NGFS scenarios produce differentiated GDP impacts (sr1059 p. 10): Net Zero 2050 causes -1.97% world GDP (chronic physical risk), Delayed Transition -2.86%, Current Policies -5.66%. Cross-jurisdictional: BoE projects UK GDP -1.4% (Early Action) to -7.8% (No Action) by 2050 (sr1059 p. 45); Fed pilot projects U.S. GDP ~$24,030B (Current) vs. ~$23,574B (Net Zero) by 2030 with carbon prices $17/ton vs. $162/ton (sr1059 p. 46).

### Finding 2: Bank Exposure Bounds from Three GE Models
Jung et al. use three general equilibrium models producing meaningfully different exposure estimates (sr1058 pp. 9-17):

| Model | Industries | Avg Bank Exposure | Key Insight |
|-------|-----------|-------------------|-------------|
| Jorgenson/IGEM | 36 | 0.5%-3.5% | Revenue recycling policy dominates |
| Goulder/E3 | 35 | -1% to 1% | Corporate tax cut makes exposure *negative* |
| G-Cubed | 12-20 | 2%-6.4% | Highest exposures; only annual path model |

Maximum exposure does not exceed 14% under any scenario/model/stress combination (sr1058 p. 3).

### Finding 3: CRISK Market-Based Climate Risk
Acharya et al. estimate that a 50% decline in the stranded asset factor would increase CRISK of the top 4 U.S. banks by **$425 billion** (~47% of market capitalization) (sr1059 p. 30). Climate beta is estimated from a stranded asset portfolio: 30% XLE + 70% KOL, short SPY.

### Finding 4: Delayed Transition Is the Riskiest Scenario
Consistent across all exercises: ECB ~70B EUR combined losses under disorderly (sr1059 p. 26); BoE Late Action 30% higher losses than Early Action (sr1059 p. 26); carbon prices jump from $0 to $31.52/ton in 2030 under Delayed Transition, reaching $121.97 by 2050 (sr1058 p. 16). Policy uncertainty itself is a source of financial risk.

### Finding 5: C&I vs. Consumer Loan Asymmetry
Jung et al. is **exclusively C&I-focused** — consumer loan exposure "cannot be estimated with their methodology because general equilibrium models do not provide household-level effects" (sr1058 p. 8). C&I loans face direct industry-specific transition risk; consumer loans are affected only through indirect macro channels (unemployment, inflation). Carbon emissions explain at most 60% of bank transition risk; 40%+ is driven by other factors captured only by forward-looking GE models (sr1058 pp. 4, 29).

### Finding 6: No Historical Precedent
"No historical precedent exists for either extreme physical or transition risk realizations" (sr1059 p. 8), limiting purely statistical approaches. Transition risks may materialize "more quickly" than physical risks because carbon taxes could be introduced at any moment (sr1059 p. 18). Average U.S. bank loan maturity is 3-5 years (sr1059 p. 17), meaning long-horizon physical risks may not directly impair current loan books.

## Detailed Results

### Q1: NGFS Scenarios and Variables — **Strong confidence**
Six scenarios, three IAM families, three model types (climate impact, transition pathway, economic impact — sr1059 p. 10). NiGEM provides U.S.-specific GDP, unemployment, CPI, interest rates. G-Cubed carbon prices: Current Policy $3.72→$26.50/ton; Orderly $16.75→$119.14/ton; Disorderly $0→$31.52 (2030)→$121.97/ton (2050) (sr1058 p. 16). NGFS scenarios "aim at exploring the bookends of plausible futures" — not forecasts (sr1059 p. 9).

### Q2: Transmission Mechanism — **Strong confidence**
Three channels: credit risk, market risk, liquidity risk (sr1059 p. 16). Physical risk materializes at longer horizons (sea-level-rise priced only in bonds >20yr maturity — sr1059 p. 18). Transition risk materializes faster (carbon taxes can be introduced immediately). Important nuance: disaster loan losses may be offset by increased loan demand, with "insignificant or small effects on bank stability" (sr1059 p. 19). Banks already respond — charging higher rates for exposed properties, shortening maturities.

### Q3: Mediating Variables — **Strong confidence**
Primary: GDP growth, unemployment, interest rates, CPI. Revenue recycling policy can swing exposures by 2-3 percentage points (sr1058 pp. 14-15). The cascade: NGFS scenarios → NiGEM macro paths → estimated loan models → conditional forecasts. Key FRED series: GDPC1, UNRATE, FEDFUNDS, DGS10, CPIAUCSL.

### Q4: Data Challenges — **Strong confidence**
Frequency mismatch (NGFS annual vs. FRED monthly); non-stationarity; COVID PPP spike; training window selection; IAM model differences. Y-14Q covers 42 banks (2012-2023) with 1.2-6.9% loan drop rates from NAICS matching (sr1058 pp. 8-9). Exposures have fallen ~3 percentage points since 2014 due to portfolio shifts toward services (sr1058 p. 8).

### Q5: Forecasting Frameworks — **Strong confidence**
Two-stage conditional forecasting: VAR or ADL trained on FRED, conditioned on NGFS paths. Pesavento Box-Jenkins recipe for model selection. Transparency required (no black-box ML). Contextualize against PDF benchmarks: 0.5%-6.4% baseline exposures, 14% maximum. CRISK as conceptual complement for market-based risk.

### Q6: Regulatory Approaches — **Strong confidence**
ECB 2022 (104 banks, 70B EUR disorderly losses); BoE CBES (30% higher Late vs. Early Action); Fed CSA pilot (6 banks, rescinded 2025); Banque de France (15.8 vs. 17.2 bps orderly vs. sudden); ECB 2023 expected losses 0.7-0.9% of exposure across all scenarios (sr1058 pp. 3, 5-6). NGFS has 121 members and 19 observers (sr1059 p. 4).

### Q7: Scenario Comparisons — **Moderate confidence**
Delayed Transition produces highest short-term losses across all jurisdictions and methodologies. G-Cubed exposure: 6.4% (disorderly) vs. 2.0% (orderly) for average bank (sr1058 p. 17). Net-Zero Alliance signatories pushed risky borrowers to non-signatory banks — risk migration rather than risk reduction (sr1058 p. 8).

### Q8: Financial Stability — **Moderate confidence**
System-wide: climate risks do not yet pose existential threat, but caveats are substantial (sr1059 p. 26). Concentrated banks face material pressure. Fire-sale amplification creates systemic risk beyond direct exposure. Orderly transition is less destabilizing — the key strategic insight for executives.

## Methodology Notes

**PDF-sourced facts** (162 total) provide page-level attribution and specific quantitative claims. **Web-sourced facts** (~170) are from training knowledge — directionally reliable but should be verified against cited URLs. **Course materials** (48 facts) provide the methodological toolkit. All claims in the analysis trace to specific numbered facts.

**Applicable course methods**: Unit root tests (ADF/KPSS) → AR baseline → ADL or VAR with macro regressors → HAC standard errors → AIC/BIC model comparison → scenario-conditional forecasting.

## Open Questions

1. **NGFS NiGEM U.S. data** not yet downloaded — most urgent gap
2. **BUSLOANS/CONSUMER** empirical properties not yet tested
3. **Frequency alignment** method not yet decided
4. **COVID treatment** — BofA flagged as key question with no industry consensus
5. **Consumer loan exposure gap** — Jung et al. C&I-only; no GE model for household effects
6. **Parameter stability** across regimes (pre/post-2008, pre/post-COVID)

## Next Steps

**Before Feb 20 Q&A:**
1. Download NGFS NiGEM data; filter for U.S. GDP, unemployment, CPI, interest rates across GCAM + REMIND
2. Download FRED series; compute growth rates; run unit root tests; plot ACF/PACF
3. Build univariate AR baseline
4. Prepare Q&A questions: COVID treatment, modeling frequency, consumer loan approach, which IAM to prioritize

**Modeling Phase (Feb 20 - March):**
5. Estimate ADL or VAR; start large, eliminate per Pesavento recipe
6. Address frequency mismatch; test sensitivity
7. Generate scenario-conditional forecasts under 3+ NGFS scenarios
8. Contextualize against PDF benchmarks (0.5-6.4% baseline, 14% max, $425B CRISK)

**Presentation Phase (March - April 9):**
9. Lead with "act early" finding — orderly beats disorderly everywhere
10. Present ranges not point estimates (three GE models give -1% to 6.4%)
11. Discuss consumer loan gap honestly; frame as refinement area
12. Reference limitations with page citations (sr1059 p. 8, sr1058 p. 8, p. 11)

## Sources

### Local Documents (directly extracted)
- Emory Time Series Climate Case Study (PDF) — BofA project document
- Kickoff transcript — Feb 12, 2026 meeting recording
- **Acharya et al. (2023) "Climate Stress Testing" — NY Fed SR 1059 (85 facts, page-cited)**
- **Jung et al. (2024) "U.S. Banks' Exposures to Climate Transition Risks" — NY Fed SR 1058 (77 facts, page-cited)**

### Course Materials
- Week 3: Univariate Time Series (stationarity, transformations, ACF/PACF)
- Week 4: ARMA Models & Cycles (AR identification, Box-Jenkins, model selection)
- Week 5: Dynamic Causal Effects (distributed lags, HAC errors, ADL, VAR preview)

### Web Research (training-knowledge-based, pending verification)
- NGFS Phase IV documentation and IIASA data portal
- ECB 2022 Climate Stress Test; Bank of England CBES 2022
- Federal Reserve CSA pilot 2023-2024
- IMF GFSR 2022; BIS Working Papers
- FRED series documentation (BUSLOANS, CONSUMER, macro variables)
