# Forecasting & Time Series — Spring 2026 (Emory University)

## Course Overview
- **Course**: Forecasting and Time Series, taught by Professor Elena Pesavento
- **University**: Emory University, Department of Economics
- **Semester**: Spring 2026
- **Language**: Python only (course requirement)

## Repository Structure

```
.
├── course-materials/lectures/     # Weekly lecture slides, transcripts, summaries
│   ├── week-01/ through week-06/  # Each has slides PDFs, summary.md, key-concepts.md
│   └── (recordings/ in some weeks with Otter.ai transcripts + alignment data)
├── problem-sets/                  # Homework assignments
│   ├── problem-set-1/             # Complete: BTC returns, MA(1), white noise, volatility
│   └── problem-set-2/             # Complete: ARMA proof, ACF/PACF, oil/GDP, PNFIC1 AR(4)
├── exams/                         # Exam prep (placeholder)
├── projects/                      # Semester research projects
│   └── climate-risk-loans/        # BofA case study (has its own CLAUDE.md)
├── reference/                     # Formula sheets and quick-reference (placeholder)
├── scripts/                       # Automation (align_recording.py, export-notes-pdf.sh)
└── .claude/                       # Framework configuration
    ├── agents/                    # 5 specialized agents
    ├── commands/                  # 4 slash commands
    └── skills/                    # 11 skill definitions
```

## Agents

| Agent | File | Purpose |
|-------|------|---------|
| **Course Knowledge** | `agents/course-knowledge.md` | Builds context briefs from lecture materials for homework; matches professor terminology |
| **Decomposition** | `agents/decomposition.md` | Breaks research topics into structured, prioritized questions |
| **Document Research** | `agents/document-research.md` | Extracts attributed facts from local docs, lectures, papers |
| **Web Research** | `agents/web-research.md` | Searches web for academic/institutional sources, extracts facts |
| **Synthesis** | `agents/synthesis.md` | Analyzes factbase, produces insights, generates reports |

## Commands

| Command | Purpose |
|---------|---------|
| `/research "topic"` | Full research pipeline: questions → sources → facts → analysis → report |
| `/extend-research project-slug` | Expand existing project with new questions/sources/focus |
| `/status [project-slug]` | View project state, facts, questions, sources |
| `/align_recording week-XX` | Align Otter.ai transcript with annotated slides |
| `/hwk_pipeline problem-set-N` | End-to-end homework pipeline (v2, with context brief) |

## Skills

| Skill | Purpose |
|-------|---------|
| **comprehensive-analysis** | Full factbase analysis producing insights per research question |
| **gap-analysis** | Identify missing coverage and recommend next research |
| **summary-report** | Generate 2-4 page report from latest analysis |
| **econometric_analysis** | Statistical tests: Ljung-Box, stationarity, ARMA identification |
| **financial_data** | Fetch data via yfinance, compute returns, export CSV |
| **jupyter_notebook_gen** | Generate structured homework notebooks |
| **lecture_summarization** | Extract key concepts/formulas from slides into study guides |
| **practice_generator** | Create practice problems by type and difficulty |
| **recording_slide_alignment** | Produce timestamped study guides from transcripts + slides |
| **time_series_viz** | Publication-quality time series, ACF/PACF, and volatility plots |
| **docs-with-mermaids** | Create technical documentation with Mermaid diagrams (architecture, flows, schemas, state machines) |

## Homework Pipeline (v2)

The `/hwk_pipeline` command runs 8 steps:
1. **Setup** — Create directory structure
2. **Environment** — Verify Python packages
3. **Context Brief** — Course Knowledge Agent searches lectures for relevant terminology, methods, professor emphasis (writes `context-brief.md`)
4. **Data** — Fetch from FRED/yfinance per problem requirements
5. **Analysis** — Run econometric tests guided by context brief
6. **Visualization** — Generate plots using professor's preferred style
7. **Notebook** — Assemble with discussion sections using professor's framework
8. **Quality Checks** — Verify completeness, terminology alignment, course connections

## Problem Set Conventions

- Each problem set lives in `problem-sets/problem-set-N/`
- Problem statement PDF: `HwkN.pdf`
- Output notebook: `hwkN_analysis.ipynb`
- Data: `data/raw/`
- Figures: `outputs/figures/` (saved at 300 DPI)
- Tables: `outputs/tables/`
- Context brief: `context-brief.md` (from course-knowledge agent)

## Research Project Structure

Each project under `projects/` follows:
```
project-slug/
├── CLAUDE.md          # Project-specific context
├── project.yaml       # Metadata and stats
├── questions/         # Decomposed research questions
├── sources/           # Source manifest
├── facts/by-source/   # Extracted facts per source
├── analysis/runs/     # Dated analysis files
└── artifacts/reports/ # Generated reports
```

## Active Research Project

**climate-risk-loans** — How NGFS climate scenarios affect U.S. banking loan portfolios. Sponsored by Bank of America Treasury. See `projects/climate-risk-loans/CLAUDE.md` for full context.

## Course Topics by Week

- **Week 1**: Introduction to time series, stationarity, white noise
- **Week 2**: Autocorrelation, sample ACF, Ljung-Box test
- **Week 3**: Univariate time series models, AR processes
- **Week 4**: ARMA models, model selection (AIC/BIC), estimation
- **Week 5**: Dynamic causal effects, distributed lag models, HAC standard errors
- **Week 6**: Forecasting with ARMA models, loss functions, optimal forecasts, out-of-sample evaluation

## Key Technical Notes

- FRED API key is stored in notebooks (fredapi library)
- Growth rates: use `100 * ln(Y_t / Y_{t-1})` for log growth (consistent with course convention)
- Standard errors: HC0 for heteroscedasticity-robust, HAC/Newey-West for serial correlation
- Model selection: AIC and BIC grid search for ARMA(p,q)
- Plots use `seaborn-v0_8-darkgrid` style, 150 DPI display / 300 DPI save
