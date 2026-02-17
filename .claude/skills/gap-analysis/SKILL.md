---
name: gap-analysis
description: Identify gaps in the current factbase and recommend what to research next
---

# Gap Analysis Skill

## Instructions for the Synthesis Agent

Evaluate the current factbase to identify what's missing, weak, or needs deeper investigation.

## Process

1. **Coverage audit**: For each question, count facts and assess source diversity
2. **Confidence assessment**: Which answers rely on single sources or low-confidence facts?
3. **Missing perspectives**: What viewpoints or source types are absent?
4. **Data gaps**: What quantitative data is needed but not yet found?
5. **Prioritize**: Rank gaps by importance to the project

## Output Format

```markdown
# Gap Analysis: {Project Name}
Date: {date}

## Coverage Summary
| Question | Facts | Sources | Confidence | Gap Level |
|----------|-------|---------|------------|-----------|
| Q1       | 5     | 3       | strong     | low       |
| Q2       | 1     | 1       | weak       | HIGH      |
| ...      |       |         |            |           |

## Critical Gaps (must address)
### Gap 1: {Description}
- Affects questions: {Q list}
- What's needed: {Specific data, source, or analysis}
- Suggested action: {Search query, document to read, etc.}

## Moderate Gaps (should address)
...

## Minor Gaps (nice to have)
...

## Recommended Next Steps
1. {Highest priority action}
2. {Second priority}
3. ...

## Suggested Search Queries
- "{query 1}" — to fill Gap 1
- "{query 2}" — to fill Gap 2
```