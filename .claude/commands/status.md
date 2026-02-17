# /status Command

## Purpose
View project state, progress, and details.

## Usage
```
/status                          # List all projects
/status {project-slug}           # Details for specific project
/status {project-slug} --facts   # Show fact summary
/status {project-slug} --questions  # Show question tree with status
/status {project-slug} --sources    # Show source details
```

## Output Format

### List All Projects
```
Research Projects:
─────────────────
1. climate-risk-loans (active)
   Last updated: 2026-02-12
   Facts: 24 | Sources: 6 | Questions: 8
   
2. arma-model-selection (complete)
   Last updated: 2026-02-08
   Facts: 12 | Sources: 3 | Questions: 4
```

### Project Details
```
Project: climate-risk-loans
Status: active
Created: 2026-02-12
Last updated: 2026-02-12

Questions: 8 (6 answered, 2 open)
Sources: 6 (3 web, 2 local docs, 1 course material)
Facts: 24 extracted
Analysis runs: 2
Reports: 1

Latest analysis: analysis/runs/2026-02-12-comprehensive.md
Latest report: artifacts/reports/2026-02-12-summary-report.md
```

### --facts Flag
Show fact count per source and sample facts.

### --questions Flag
Show full question tree with answered/unanswered status.

### --sources Flag
Show source manifest with extraction status.

## Implementation
1. Read `project.yaml` for metadata
2. Count files in `facts/by-source/` for fact counts
3. Parse `questions/initial.md` for question status
4. Read `sources/manifest.yaml` for source details
5. List `analysis/runs/` and `artifacts/reports/` for history