# Facts: Feb 20, 2026 Q&A Session with BofA Treasury Team

Source: `sources/local/feb20q+a.txt`
Extracted: 2026-02-20

## COVID Treatment
- F1: BofA confirmed dummy variables are the standard approach for COVID. "That's the way a lot of people have been doing it." [line 62]
- F2: During COVID (2021-2022), BofA internally found it "muddled the back test data points" — those observations were unusable. [line 62-65]
- F3: COVID must be excluded from out-of-sample evaluation periods. "If you're giving us your out-of-sample period, make sure you have it out." [line 65]

## Outcome Variable
- F4: Outcome variable is open-ended — cumulative balance, growth rates, or any transformation are all acceptable. [line 80-83]
- F5: Must justify the variable transformation choice. "It really depends on what you think your model will be able to predict best, and be able to justify why you did that variable transformation." [line 83]
- F6: Final insights must translate clearly regardless of transformation. "If your final conclusion is 'we see the industry dropping' or 'the growth rate is negative,' how are you going to explain your final conclusion?" [line 92]

## Training Window
- F7: Training window should include at least 3 decades (1990s+) to capture enough business cycles. [line 104]
- F8: Must include: 2008 GFC, 2001 tech bubble, 1990s effects. [line 104]
- F9: More historical data does not necessarily improve performance. "What matters more is that your historical data captures relevant business cycles." [line 107]
- F10: Some variables may not go back as far as others — this is a modeling trade-off to discuss. [line 107]

## Frequency Mismatch
- F11: Frequency handling is an open modeling decision. "You could just give it a try with different frequencies and see what makes your model perform the best." [line 119]
- F12: Different NGFS models may have different frequencies; fit data structure to comparison goals. [line 124-125]
- F13: BofA encouraged creativity: "Be creative with your approach to solving these kind of data questions, data problems." [line 119]
- F14: Professor Pesavento will teach MIDAS (mixed-frequency data analysis) earlier than planned to help with this. [line 128]

## Consumer Loan Approach
- F15: Indirect macro channel approach (climate → unemployment/rates → consumer loans) was approved. "I think that makes sense." [line 149]
- F16: BofA pushed for more thorough consumer drivers beyond unemployment and rates. "Are there other aspects of it that matter to consumers?" [line 152-155]
- F17: Suggested additional consumer drivers: house prices, disposable income, consumer confidence (implied by "other aspects"). [line 152-155]

## Fed Paper Benchmarks
- F18: The 14% max exposure from Jung et al. is "interesting context" and a "guideline" only. [line 134]
- F19: BofA does not expect replication of those results — papers use bank-specific balance sheet data and regional segmentation not available to us. [line 134-137]

## Industry Granularity
- F20: Do NOT go to firm level. "We don't want you to go to the firm level — like, do you want to make it about America or Citi? That's not something we want." [line 176]
- F21: Core analysis should be aggregate US industry-level. [line 176-182]
- F22: Sector-level exploration is fine for additional interest but not required. [line 182]
- F23: Going granular creates a driver-matching problem: "If you start to break out the sectors or the regions, then do you need region specific unemployment?" [line 194]

## Scenarios & Time Horizon
- F24: No preference on which NGFS scenarios to use — "Any or all?" [line 203]
- F25: No preference on forecast horizon. "As long as you have your model, you can just plug in the numbers." [line 212]

## Confidence Intervals & Uncertainty
- F26: BofA explicitly wants confidence bands. "A lot of times there's a lot of value from the confidence bands around the estimate." [line 242]
- F27: "It is about how comfortable we are with the number within certain bounds." [line 242]

## Scenario Visualization
- F28: BofA wants to see robust understanding of scenario narratives. "Show a robust understanding of what different data sets are telling you." [line 245-248]
- F29: Visualize how scenarios differ in terms of both climate and economic variables. [line 248]
- F30: "Really try to show that you thought about what these variables mean, the story they're telling you, and how they're applicable to your forecasting model." [line 248]

## Actionable Insights
- F31: Go beyond point estimates. "Can you dig into that number? Answer some important policy questions or systemic risk questions?" [line 227]
- F32: Frame for executive decision-making: "If you're going to present this to an executive making strategic decisions about increasing loan exposures, you want to be able to derive granular suggestions." [line 233]
- F33: Different modeling approaches (interpolation methods, variable choices, segmentation) will tell different stories — use that. [line 236]

## Leading vs. Lagging Indicators
- F34: Critical warning: "Make sure you understand which ones are leading and which ones are lagging." [line 164]
- F35: GDP is lagged — a GDP print covers the previous quarter, not the current one. [line 164]
- F36: "The one thing you don't want to do when you're building a forecast is accidentally include a future point in your time series." [line 167]
- F37: BofA has seen this mistake in practice: "Your model ends up being so good, and you just don't realize that you ended up using the close of day value in the morning." [line 167]

## Timeline & Logistics
- F38: Midterm is March 5; spring break is March 10-12. [line 341]
- F39: Next possible Q&A session around March 3 (before spring break). [line 350]
- F40: Team names confirmed: "Too Big to Melt" and "Green Horizon". [line 23-32]
- F41: BofA expressed interest in meeting in person for Q&A sessions or presentation. [line 338]

## BofA Meta-Commentary
- F42: BofA praised the quality of questions: "These are the things like this is like taking the technical into the domain... these are the kinds of discussions we have on the data." [line 197]
- F43: Multiple modeling approaches and sensitivity analysis are valued even if outputs are similar: "They'll tell you very different stories. So try to use that." [line 236]
