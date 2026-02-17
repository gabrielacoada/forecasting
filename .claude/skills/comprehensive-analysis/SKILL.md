---
name: comprehensive-analysis
description: Full analysis of all extracted facts to produce insights and conclusions
---

# Comprehensive Analysis Skill

## Instructions for the Synthesis Agent

Produce a thorough analysis that answers each research question using the extracted factbase.

## Process

1. **Summarize the factbase**: How many facts, from how many sources, covering which questions
2. **Answer each question**: For each question in `questions/initial.md`:
   - Gather all relevant facts
   - Synthesize an answer
   - Rate answer confidence (strong/moderate/weak)
   - Note supporting and contradicting evidence
3. **Cross-cutting themes**: Identify patterns that span multiple questions
4. **Gaps and limitations**: What couldn't be answered? What needs more research?
5. **Recommendations**: Based on the analysis, what should be done next?

## Output Format

```markdown
# Comprehensive Analysis: {Project Name}
Date: {date}
Factbase: {N} facts from {M} sources

## Executive Summary
{2-3 paragraph overview of key findings}

## Question-by-Question Analysis

### Q1: {Question text}
**Answer confidence**: {strong/moderate/weak}

{Analysis paragraph(s)}

**Supporting evidence**:
- Fact X from {source}: "{claim}" 
- Fact Y from {source}: "{claim}"

**Contradicting or qualifying evidence**:
- {If any}

---

### Q2: {Question text}
...

## Cross-Cutting Themes
{Patterns and connections across questions}

## Knowledge Gaps
- {Gap 1}: {What's missing and why it matters}
- {Gap 2}: ...

## Methodological Notes
{For course-related projects: which forecasting methods are applicable and why}

## Recommendations
{Next steps, further research, or action items}

## Fact Attribution Index
{List of all facts used, grouped by source}
```

## Quality Guidelines
- Every claim in the analysis must reference a specific fact
- Clearly separate what the evidence shows from your interpretation
- When facts conflict, present both sides
- Be specific about what "confidence" means in each case
- For course projects, connect recommendations to applicable course methods