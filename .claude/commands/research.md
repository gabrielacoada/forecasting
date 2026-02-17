# /research Command

## Purpose
Start a new research project with full pipeline execution, or continue an existing one.

## Usage
```
/research "Your research topic or question"
/research "Your topic" --project existing-project-slug
```

## Pipeline Steps

### Step 1: Create Project
- If no `--project` flag, create new folder: `projects/{slug}/`
- Copy template structure:
  ```
  projects/{slug}/
  ├── project.yaml
  ├── CLAUDE.md          # Project-specific context
  ├── questions/
  │   └── initial.md
  ├── sources/
  │   ├── manifest.yaml
  │   └── local/
  ├── facts/
  │   └── by-source/
  ├── analysis/
  │   ├── runs/
  │   └── latest.md
  └── artifacts/
      └── reports/
  ```

### Step 2: Decompose Questions
- Delegate to the **decomposition agent** (`.claude/agents/decomposition.md`)
- Input: The research topic
- Output: `questions/initial.md` with structured questions
- **PAUSE**: Present questions to user for approval or modification

### Step 3: Configure Sources
- Based on approved questions, identify available sources:
  - **Web search**: Generate 3-5 targeted search queries per question
  - **Local documents**: Check `sources/local/` and any project-specific paths in `CLAUDE.md`
  - **Course materials**: Check `course-materials/lectures/` for relevant lecture content
- Write source plan to `sources/manifest.yaml`
- **PAUSE**: Present source strategy to user for confirmation

### Step 4: Extract Facts
- For each source type, delegate to the appropriate agent:
  - Web sources → **web-research agent** (`.claude/agents/web-research.md`)
  - Local docs / course materials → **document-research agent** (`.claude/agents/document-research.md`)
- Each agent writes attributed facts to `facts/by-source/{source-name}.md`
- Facts format:
  ```markdown
  ## Fact 1
  - **Claim**: [Specific factual claim]
  - **Source**: [URL or document path]
  - **Confidence**: [high/medium/low]
  - **Relevant to**: [Question ID]
  ```

### Step 5: Analyze
- Load the **comprehensive-analysis** skill (`.claude/skills/comprehensive-analysis/SKILL.md`)
- Input: All facts from `facts/by-source/`
- Output: `analysis/runs/{date}-comprehensive.md`
- Symlink `analysis/latest.md` → latest run

### Step 6: Generate Report
- Load the **summary-report** skill (`.claude/skills/summary-report/SKILL.md`)
- Input: Latest analysis
- Output: `artifacts/reports/{date}-summary-report.md`
- **Present**: Show summary and report location to user

### Step 7: Suggest Next Steps
- Suggest `/extend-research {project}` to add more sources or questions
- Suggest `/status {project}` to view project details
- Note any gaps identified during analysis

## Important Notes
- Always pause for user approval at Steps 2 and 3
- Every fact must be attributed to a source
- Analysis must be based on extracted facts, not invented
- Reports present analysis, they don't create new claims