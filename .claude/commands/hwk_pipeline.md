# Homework Pipeline Workflow (v2)

## Purpose
Automated end-to-end workflow for completing econometrics problem sets, enhanced with course-knowledge integration. This command orchestrates context gathering, data fetching, analysis, visualization, and notebook generation.

## Usage
```bash
# From repo root, use Claude Code:
# "Run the homework pipeline for Problem Set 3"
```

## Workflow Steps

### Step 1: Project Setup
```bash
# Ensure directory structure exists
mkdir -p assignments/problem-sets/problem-set-{N}/data/raw
mkdir -p assignments/problem-sets/problem-set-{N}/outputs/figures
mkdir -p assignments/problem-sets/problem-set-{N}/outputs/tables
```

### Step 2: Environment Check
```python
# Verify all required packages are installed
required_packages = [
    'pandas', 'numpy', 'matplotlib', 'seaborn',
    'statsmodels', 'scipy', 'yfinance',
    'nbformat', 'jupyter'
]

import subprocess, sys
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
```

### Step 3: Build Context Brief ← NEW
```
Delegate to: .claude/agents/course-knowledge.md

1. Read the problem set PDF
2. Identify topics and methods required
3. Search lecture materials (course-materials/lectures/week-01 through latest)
4. Search research project facts (projects/*/facts/by-source/)
5. Search reference materials (reference/formulas/)
6. Write context-brief.md to the problem set directory

Output: assignments/problem-sets/problem-set-{N}/context-brief.md
```

**This step is critical.** The context brief ensures that:
- Discussion sections use the professor's terminology
- Methods are applied the way she taught them
- Interpretations match her expectations
- Connections to course themes are explicit

### Step 4: Data Acquisition
```python
# Read skills/financial_data/SKILL.md
# Execute data fetching based on problem requirements
# Save to data/raw/
```

### Step 5: Analysis Execution
```python
# Read skills/econometric_analysis/SKILL.md
# ALSO READ: context-brief.md for methodology guidance
#
# The context brief tells you:
# - Which methods the professor prefers for this type of problem
# - How she expects results to be interpreted
# - What specific tests or checks she emphasized
#
# Execute statistical tests and computations accordingly
```

### Step 6: Visualization Generation
```python
# Read skills/time_series_viz/SKILL.md
# ALSO READ: context-brief.md for terminology
#
# Use the professor's preferred:
# - Variable names and labels
# - Plot formatting conventions shown in class
# - Annotation style
```

### Step 7: Notebook Assembly
```python
# Read skills/jupyter_notebook_gen/SKILL.md
# ALSO READ: context-brief.md for discussion writing
#
# For each discussion section:
# 1. State the result
# 2. Interpret using professor's framework and terminology
# 3. Connect to course concepts she emphasized
# 4. Note any caveats she mentioned in lectures
# 5. If relevant, connect to broader themes (e.g., climate project)
```

### Step 8: Quality Checks
```python
def run_quality_checks():
    checks = {
        'All figures saved': True,
        'All problems addressed': True,
        'Code runs without errors': True,
        'Discussion sections complete': True,
        'Professional formatting': True,
        'Context brief generated': True,              # NEW
        'Discussions use professor terminology': True, # NEW
        'Course concepts referenced': True,            # NEW
    }
    # ... verification logic
```

## Complete Pipeline Function

```python
def run_homework_pipeline(problem_set_num):
    """
    Master function to run entire homework pipeline.
    
    Parameters:
    -----------
    problem_set_num : int
        Problem set number (1, 2, 3, ...)
    """
    
    print("=" * 70)
    print(f"HOMEWORK PIPELINE v2: Problem Set {problem_set_num}")
    print("=" * 70)
    
    # Step 1: Setup
    print("\n[1/8] Setting up project structure...")
    setup_project_structure(problem_set_num)
    
    # Step 2: Environment
    print("\n[2/8] Checking environment...")
    check_environment()
    
    # Step 3: Context Brief (NEW)
    print("\n[3/8] Building context brief from lecture materials...")
    context = build_context_brief(problem_set_num)
    # → Reads problem set PDF
    # → Searches lectures weeks 1-N for relevant content
    # → Searches research project facts
    # → Writes context-brief.md
    
    # Step 4: Data
    print("\n[4/8] Fetching data...")
    data = fetch_data(problem_set_num)
    
    # Step 5: Analysis
    print("\n[5/8] Running analysis (using context brief)...")
    results = run_analysis(problem_set_num, data, context)
    
    # Step 6: Visualization
    print("\n[6/8] Generating plots...")
    plots = generate_plots(problem_set_num, data, results)
    
    # Step 7: Notebook
    print("\n[7/8] Assembling notebook (using context brief)...")
    notebook_path = assemble_notebook(problem_set_num, data, results, plots, context)
    
    # Step 8: Quality checks
    print("\n[8/8] Running quality checks...")
    quality_ok = run_quality_checks(problem_set_num)
    
    print("\n" + "=" * 70)
    if quality_ok:
        print("✓ PIPELINE COMPLETE!")
        print(f"  Context brief: assignments/problem-sets/problem-set-{problem_set_num}/context-brief.md")
        print(f"  Notebook: {notebook_path}")
    else:
        print("⚠ PIPELINE COMPLETE WITH WARNINGS")
    print("=" * 70)
    
    return notebook_path
```

## Integration with Claude Code

When using Claude Code, you can say:
- "Run the homework pipeline for Problem Set 3"
  → Runs full pipeline including context brief
- "Build a context brief for Problem Set 3"
  → Just runs Step 3 (useful for reviewing before full pipeline)
- "Update Problem Set 3 discussions using lecture notes"
  → Rebuilds context brief and rewrites discussion sections only

## Extensibility

The pipeline is now topic-agnostic. For any new problem set:
1. Place the problem set PDF in `assignments/problem-sets/problem-set-N/`
2. Run the pipeline
3. The course-knowledge agent automatically finds relevant lectures
4. No problem-set-specific functions needed (generic analysis driven by context)