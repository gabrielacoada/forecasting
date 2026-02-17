# Deep Research Framework — Simplified

A persistent research system built on Claude Code for accumulating knowledge over time.

## Quick Start

```bash
# From your repo root (forecasting-spring2026/)

# Start a new research project
/research "How do NGFS climate scenarios impact banking loan portfolios?"

# Check project status
/status
/status climate-risk-loans
/status climate-risk-loans --facts

# Expand existing research
/extend-research climate-risk-loans
/extend-research climate-risk-loans --add-sources
/extend-research climate-risk-loans --focus "frequency mismatch between NGFS and FRED data"
```

## How It Works

```
Topic → Questions → Sources → Facts → Analysis → Report
  ↑                                                  ↓
  └──────────────── Iterate ────────────────────────┘
```

Each stage is separate and persistent:
- **Questions** are decomposed and stored, not just asked
- **Facts** are extracted and attributed, not just summarized  
- **Analysis** is based on facts, not invented
- **Reports** present analysis, they don't create new claims

## Directory Structure

```
.claude/
├── commands/           # Workflow orchestration
│   ├── research.md     # Full research pipeline
│   ├── extend-research.md  # Expand existing projects
│   └── status.md       # View project state
│
├── agents/             # Specialized workers
│   ├── decomposition.md    # Breaks topics into questions
│   ├── web-research.md     # Extracts facts from web
│   ├── document-research.md # Extracts facts from local docs + course materials
│   └── synthesis.md        # Analysis + report generation
│
└── skills/             # How to do specific tasks
    ├── comprehensive-analysis/  # Full factbase analysis
    ├── gap-analysis/           # Identify what's missing
    └── summary-report/         # Generate summary reports

projects/
└── climate-risk-loans/     # Your first research project
    ├── CLAUDE.md           # Project context (BofA case study details)
    ├── project.yaml        # Metadata
    ├── questions/          # Decomposed research questions
    ├── sources/            # Source registry + local docs
    ├── facts/by-source/    # Extracted facts, organized by source
    ├── analysis/runs/      # Analysis history
    └── artifacts/reports/  # Generated reports
```

## Integration with Course Materials

The document-research agent knows about your course structure:
- It can pull from `course-materials/lectures/` (slides, transcripts, synced notes)
- It can reference `reference/formulas/` for applicable methods
- It connects research findings to course concepts

This means as you add more lecture materials throughout the semester, your research projects get smarter.

## Current State (Phase 1 — Simplified)

### What's implemented:
- 3 commands: `/research`, `/extend-research`, `/status`
- 4 agents: decomposition, web-research, document-research, synthesis
- 3 skills: comprehensive-analysis, gap-analysis, summary-report
- 1 active project: climate-risk-loans

### Phase 2 (to add later):
- Additional analysis skills: contradiction, timeline, comparison
- Additional report skills: executive-brief, detailed-report, fact-sheet, comparison-table, recommendations
- MCP research agent (for tools beyond web search)
- Cross-project knowledge sharing