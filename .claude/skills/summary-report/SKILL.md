---
name: summary-report
description: Generate a 2-4 page summary report from the latest analysis
---

# Summary Report Skill

## Instructions for the Artifact Agent

Generate a clear, well-structured summary report suitable for review and reference.

## Input
- Latest analysis from `analysis/latest.md`
- Project context from `CLAUDE.md`

## Output Format

```markdown
# {Project Title}: Summary Report
Date: {date}
Project: {project-slug}

## Overview
{1 paragraph: what was researched, why, and key takeaway}

## Key Findings

### Finding 1: {Title}
{2-3 sentences summarizing the finding}
- Evidence: {Brief attribution}

### Finding 2: {Title}
...

## Detailed Results
{For each research question: the answer, confidence level, and key supporting evidence}

## Methodology Notes
{What sources were used, how facts were gathered, any limitations in the research process}

## Open Questions
{What remains unanswered or uncertain}

## Next Steps
{Recommended actions based on findings}

## Sources
{List of all sources consulted with links/paths}
```

## Guidelines
- Keep to 2-4 pages equivalent in markdown
- Lead with the most important findings
- Write for someone who hasn't read the full analysis
- Use clear, direct language
- Include enough attribution that claims are verifiable
- For course projects: note which course concepts are applicable
- Do NOT introduce new claims not in the analysis