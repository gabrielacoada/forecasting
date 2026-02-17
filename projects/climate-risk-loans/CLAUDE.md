# Project: Climate Risk Impact on Banking Loan Portfolios

## Domain Context

This is a semester-long case study project for Professor Pesavento's Forecasting and Time Series course (Spring 2026) at Emory University, sponsored by Bank of America's Treasury Quantitative Analytics team.

### The Core Question
How does climate change/climate risk impact commercial and consumer loan portfolios in the banking industry?

### Two Types of Climate Risk
- **Physical risk**: Immediate effects — more powerful storms, storm surges, property damage
- **Transition risk**: How humanity reacts — carbon taxes, regulatory changes, policy shifts, GDP impacts, interest rate changes

### Project Sponsors
- Bank of America Treasury team (4 people)
- They do NOT currently work on climate risk for the bank — this is exploratory
- Contact: `emory_climate_case_study@bofa.com` (underscores between words)
- Keep analysis industry-level, NOT specific to Bank of America

### Key Evaluation Criteria (from kickoff + Q&A)

**Methodology & Modeling Decisions**
- Variable/feature selection WITH justification
- Forecasting framework design given NGFS + FRED data
- Handling uncertainty, missing data, different frequencies, regions, imperfect data

**Transparency & Explainability**
- Models must be transparent, explainable, defensible — NOT black-box ML
- Must justify each modeling choice logically and in business terms

**Critical Thinking & Framing**
- This is ambiguous with no single correct answer — they know that
- They care about: problem framing, framework trade-offs, sample period decisions, COVID treatment, business cycle coverage, training/test split design

**Communication & Presentation Quality**
- Translate technical work into high-level insights for non-technical decision-makers
- Strategic implications (financial stability, portfolio risk)
- Clear, compelling visualizations
- Don't fill 5 pages just to fill them — concise and clear communication wins

**What they explicitly said they do NOT care about:**
- Raw model accuracy
- Code syntax or coding details
- Perfect results

### Deliverables
1. **Presentation** (30 min): High-level insights, strategic decisions, visualizations. At least some BofA team in person.
2. **Technical report** (max 5 pages): Methodology, variable selection reasoning, limitations, refinements. Concise > long.
3. **Code**: NOT required for grading. Professor grades report + presentation.

### Timeline
- Feb 12: Kickoff (completed)
- Feb 20: First Q&A session (30 min, same Teams format, ~2:30-3:00 PM) — PREPARE STRONG QUESTIONS
- Throughout semester: Up to 2 optional Q&A sessions per team (on demand, business hours)
- April 9: Final presentations (30 min per team, likely in person at Emory, Rich building)

### Class Integration
- Professor Pesavento grades based on report + presentation
- Technical report uploaded to Canvas
- Two teams competing — rubric TBD, winner gets a prize (TBD)
- Team names required (creativity = bonus points)
- Tuesday class will discuss team logistics

## Data Sources

### Primary
- **BUSLOANS** (FRED): Commercial & Industrial loans — explicitly specified as the main target
- **CONSUMER** (FRED): Consumer loans — confirmed in Q&A (ticker is "CONSUMER", uppercase)
  - Teams can do C&I only, consumer only, or BOTH (doing both is "an even more interesting challenge")
- **NGFS climate scenarios**: https://data.ene.iiasa.ac.at/ngfs/#/downloads
  - Downloaded as zip file with multiple model outputs
  - Multiple model families: GCAM, REMIND, MESSAGEix
  - Variables: carbon prices, GDP, temperature, CO2 emissions, energy costs
  - Scenarios: Net Zero 2050, Delayed Transition, Current Policies, etc.
  - Note: macro variables will differ slightly depending on whether modeling commercial vs consumer loans

### Supporting
- FRED macroeconomic data: unemployment, CPI, interest rates, GDP
- Historical economic data for model training
- FRED data goes back to 1940s in some series, 1990s in others

### Known Data Challenges
- NGFS scenarios are **annual** frequency
- FRED loan data is **monthly/quarterly**
- Frequency mismatch must be addressed (interpolation vs. aggregation)
- Different NGFS model families may give different results
- Regional vs. national granularity questions

### Training Window & COVID (from Q&A)
- Training window is YOUR DESIGN CHOICE — part of the modeling process
- Must cover enough **business cycles** for good results
- **COVID structural break** is a major question they actively discuss at BofA
  - How do you treat the COVID shock period?
  - How different is it from historical patterns?
  - This is something they regularly ask modelers — good topic for presentation
- Need to think about training/test split design

## Constraints
- Python only (course requirement)
- Models must be transparent and explainable — no black-box ML
- Analysis must be industry-level, not bank-specific
- Focus on time series / forecasting methods from the course
- Open-ended question — no single correct answer

## Applicable Course Methods
- Time series forecasting (AR, ARMA, ARIMA)
- VAR models (for multivariate relationships)
- Unit root testing (ADF, PP, KPSS) for stationarity
- Information Criteria for model selection
- Trend analysis and structural breaks
- Scenario-based forecasting

## Source Preferences
- Prioritize: NGFS documentation, Fed staff reports, academic papers on climate stress testing
- Key papers cited in project doc:
  - Acharya et al., "Climate Stress Testing" (2023): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1059.pdf
  - Jung et al., "U.S. Banks' Exposures to Climate Transition Risks" (2024): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1058.pdf
- Also useful: NGFS scenario portal documentation, European Banking Authority climate risk publications

## Analysis Priorities
1. Understanding what NGFS scenarios contain and how to use them
2. Establishing the link between macro/climate variables and loan portfolios
3. Choosing and justifying the right forecasting framework
4. Feature selection with economic rationale
5. Clear scenario comparison and visualization
6. Honest discussion of limitations and uncertainty

## Research Phases
- **Phase 1** (Now - Feb 20): Understand NGFS data, explore FRED series, formulate framework ideas, prepare Q&A questions
- **Phase 2** (Feb 20 - March): Build models, iterate on feature selection
- **Phase 3** (March - April): Refine, visualize, prepare presentation