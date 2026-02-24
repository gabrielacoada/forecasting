# /checkpoint Command

## Purpose
Snapshot the current state of a project after a work session so future sessions have full context. Run this at the end of every work session.

## Usage
```
/checkpoint climate-risk-loans
/checkpoint climate-risk-loans "Finished downloading all NGFS data and FRED series"
```

## What It Does

### 1. Scan Project Directory
- List all files in `projects/{slug}/data/` (if it exists)
- List all files in `projects/{slug}/facts/by-source/`
- List all files in `projects/{slug}/analysis/runs/`
- List all files in `projects/{slug}/artifacts/reports/`
- Check `projects/{slug}/questions/` for question status

### 2. Scan Related Directories
- Check `assignments/problem-sets/` for any problem sets with context briefs linking to this project
- Check `course-materials/lectures/` for which weeks have materials

### 3. Update project.yaml
Update the stats section with current counts:
```yaml
stats:
  questions: {count}
  sources: {count}
  facts: {count}
  analysis_runs: {count}
  reports: {count}
last_checkpoint: {date}
```

### 4. Write Current State to CLAUDE.md
Append or update a `## Current State` section at the bottom of the project's `CLAUDE.md`:

```markdown
## Current State (checkpoint {date})

### Data
- {For each file/directory in data/}: {filename} — {size, row count if CSV}
- Status: {downloaded / cleaned / not started}

### Facts
- {N} facts across {M} source files
- Latest extraction: {date of newest fact file}

### Analysis
- {N} analysis runs
- Latest: {filename}

### Reports
- {N} reports generated
- Latest: {filename}

### Questions
- {N} answered, {M} partial, {K} unanswered

### What Was Done This Session
{User's description if provided, otherwise summarize git diff or recent file changes}

### What's Next
{Based on gap analysis or project phase, what are the immediate next steps}
```

### 5. Confirm
Print a summary:
```
✓ Checkpoint saved for climate-risk-loans
  Data files: 12
  Facts: 444 across 10 sources
  Last analysis: 2026-02-20
  Session note: "Finished downloading all NGFS data and FRED series"
```

## When to Run
- End of every work session
- After downloading new data
- After running analysis or generating reports
- After adding new source documents
- Before starting a new session (to verify state)