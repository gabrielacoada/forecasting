# Q&A Session 2 Takeaways — March 3, 2026


## BofA Validated Our Approach

- **Satellite model confirmed.** They said it "sounds like the right approach" and is "industry standard for stress testing." Zero pushback.
- **Two-model structure approved.** Satellite for forecasting + VAR for causality/explainability. They said: "try to explain why" you use both.

## Presentation Guidance (Critical)

### Structure
1. **Lead with the visual story.** Direct quote: "Start with a nice visual story — fan charts, this is what loans look like in the future, you have a certain degree of confidence because... then talk about drivers and modeling decisions."
2. **30 minutes confirmed** for the final presentation (April 9).
3. **Start with results, not the timeline.** Don't walk through the chronological journey of models tried. Focus on the story and results. The process goes in the written report.

### Slide Design
- **Graphs > text > numbers.** They want slides that are mostly graphs, very little text.
- "Three to four numbers" max per slide.
- Technical details go in the appendix with hyperlinked slides — only show if someone asks.
- **No code on slides.** Professor confirmed code stays completely separate (Jupyter notebooks submitted to her independently).

### Content Priorities (in order of emphasis)
1. **Fan charts / visual scenario forecasts** — the hook
2. **Driver explainability** — WHY each driver matters, in plain English
3. **Data decisions** — frequency choices, NGFS model comparison, interpolation approach
4. **COVID treatment** — show the impact, not just the method
5. **Model benchmarking** — they're "pretty interested in how you benchmark your models"
6. **Technical tests** — appendix only (DM tests, Granger, etc.)

### Communication Style
- Plain English first. "If you were able to explain something in plain English, it shows you that you really have a deep understanding of it."
- Visualizations are paramount. "It's just so much easier to pay attention."
- Technical appendix with linked slides for deep dives — "save on the back pocket if people ask."

---

## Consumer Loans Direction

- **Consumer driver null result is fine to present.** No pushback on reporting that house prices, income, and sentiment didn't improve the model. They didn't suggest other drivers to try.
- **Sub-models / loan segmentation is interesting but NOT required.** They mentioned splitting consumer into auto/credit cards/student and said "a lot of insight to be gained" but followed with "prioritize trying other model frameworks if you have time." Don't chase this.
- **Delinquency rates / credit quality as alternative dependent variable** — they said it's "fair game" (FRED has this data) but again not a directive.
- **Can focus on one loan type.** They said "focus on one first, way more in depth" is acceptable. But doing both is fine if we have the bandwidth. Not required to do both.

---

## Strategic Insights Guidance

- **C&I vs Consumer divergence is expected.** "Makes sense that this feature can act differently for C&I vs consumer." Present the difference and explain the economic intuition (businesses vs individuals spend differently, different cycle sensitivities).
- **Transition risk vs physical risk decomposition** — they specifically asked "whether you think you're capturing more transition or physical risk." Be ready to discuss this.
- **Tell a story someone can act on.** "If you're thinking of the US economy, which one matters more and why? If you're looking at all banks, which do they care more about?"
- **Banks use simplified frameworks.** "A lot of what they do is linear regression. Sometimes they break up the problem into more digestible pieces — sub-models." Our satellite approach aligns perfectly.

---

## Specific BofA Requests

1. **"I'd like to see more detail on what your satellite model looks like."** — Show the equation, coefficients, significance levels.
2. **"What macro variables were the most significant, by how much?"** — Coefficient magnitudes + economic intuition.
3. **"Why does that make logical sense? Unemployment is a big driver — tell me why."** — Economic narrative for every driver.
4. **"Be sure that the variable you use can be mapped to the scenario."** — Every regressor must have an NGFS counterpart for scenario conditioning.
5. **"I'd like to see more explanation on how COVID impacted your modeling."** — Show the dummy's effect quantitatively.
6. **"Comparing the multiple scenarios or different models available from NGFS — there's a lot of value in doing that analysis."** — NGFS exploration / model comparison section in the presentation.

---

## Other Notes

- **Fan charts preferred for confidence intervals.** When we asked about parametric vs cross-IAM vs combined, they leaned toward whatever "looks better from a visualization point of view" and "gives the message." Fan charts with scenario spread seem ideal.
- **AI/agentic tools — fine to show off.** Professor said if we want to showcase AI tooling, we can do that separately. BofA seemed mildly interested but it's not a requirement.
- **Next Q&A possible** late March / early April before the April 9 presentation.
- **Presentation date: April 9** (or possibly April 12 — slight confusion but negligible difference).

---

## Action Items

| Priority | Action | Owner |
|----------|--------|-------|
| **HIGH** | Build fan chart visualizations as the presentation lead-in | Gabriela |
| **HIGH** | Prepare plain-English economic intuition for every driver (unemployment, Fed Funds, CPI, GDP, DGS10) | Gabriela + Econ Narrative |
| **HIGH** | Show COVID dummy impact explicitly (before/after or coefficient interpretation) | Gabriela |
| **HIGH** | Add NGFS data exploration / scenario comparison section early in presentation | Presentation Lead |
| **HIGH** | Show satellite model equation + coefficient detail | Gabriela |
| **MEDIUM** | Discuss transition vs physical risk decomposition | Econ Narrative |
| **MEDIUM** | Explain C&I vs consumer divergence with economic reasoning | Econ Narrative |
| **MEDIUM** | Explore other model frameworks for one loan type (if time permits) | Gabriela |
| **LOW** | Explore sub-models / loan segmentation (auto, credit cards, etc.) | Gabriela (stretch) |
| **LOW** | Look into delinquency rates / credit quality as alternative DV | Gabriela (stretch) |

---

## Key Differences from Q&A 1

| Topic | Q&A 1 (Feb 20) | Q&A 2 (Mar 3) |
|-------|----------------|----------------|
| Model direction | Open-ended, try things | Satellite confirmed, VAR for causality |
| Consumer drivers | "Look beyond unemployment and rates" | Null result accepted, no new suggestions |
| Presentation style | Not discussed | Visuals first, plain English, minimal text |
| Confidence bands | "A lot of value" (vague) | Fan charts preferred |
| Loan types | Do both if possible | Can focus on one, go deep |
| Benchmark framing | Not discussed | Don't frame AR as a ceiling — explain the "why" |
