# Practice Problem Generator Skill

## Purpose
Generate custom practice problems with solutions based on lecture content, problem sets, and exam preparation needs. Problems are tailored to your learning progress and exam format.

## Core Capabilities
- Generate problems by topic
- Create exam-style questions
- Vary difficulty levels
- Provide detailed solutions
- Explain common mistakes
- Connect to course concepts

## When to Use
- After completing problem sets (practice variations)
- During exam preparation (mock problems)
- When stuck on concepts (targeted practice)
- For group study (share problems with classmates)

## Problem Types

### 1. Concept Check (Easy)
**Purpose:** Verify understanding of definitions and basic properties

**Example request:**
```bash
claude "Generate 5 concept-check problems on ARMA model identification:
- MA(q) vs AR(p) properties
- ACF/PACF patterns
- Stationarity conditions
Include short-answer solutions."
```

### 2. Computational (Medium)
**Purpose:** Practice calculations and procedures

**Example request:**
```bash
claude "Generate 3 computational problems:
1. Calculating ACF for given MA(1) with θ=0.6
2. Testing for unit root with given data
3. Computing h-step ahead forecast
Include step-by-step solutions."
```

### 3. Applied Analysis (Hard)
**Purpose:** Analyze realistic data scenarios

**Example request:**
```bash
claude "Generate 2 applied problems using Bitcoin or S&P 500 data:
- Identify appropriate ARMA model
- Test for structural breaks
- Evaluate forecast accuracy
Include Python code and interpretation."
```

### 4. Theoretical (Very Hard)
**Purpose:** Prove relationships or derive formulas

**Example request:**
```bash
claude "Generate 2 theoretical problems:
1. Prove MA(1) autocorrelation bound
2. Derive Wold decomposition for given process
Include detailed proofs."
```

## Problem Templates

### Standard Format
```markdown
## Problem [N]: [Topic]

**Type:** [Conceptual / Computational / Applied / Theoretical]
**Difficulty:** [Easy / Medium / Hard]
**Topic:** [Specific topic from lectures]
**Related:** Week [X] lecture, Problem Set [Y]

### Question
[Problem statement]

**Given:**
- [Information provided]

**Find:**
- [What to determine]

**Hint:** [Optional hint if needed]

---

### Solution

**Step 1:** [First step with explanation]
[Calculations or reasoning]

**Step 2:** [Next step]
[More work]

**Final Answer:**
[Conclusion]

**Common Mistakes:**
- [Pitfall 1]
- [Pitfall 2]

**Key Insight:**
[What this problem teaches]
```

## Usage Patterns

### After Lecture
```bash
# Immediate practice
claude "Based on today's week-5 lecture on unit roots, generate 3 problems:
- 1 easy (identify unit root processes)
- 1 medium (conduct ADF test)
- 1 hard (interpret test results with structural break)"
```

### Before Problem Set Due
```bash
# Practice similar problems
cd assignments/problem-set-2
claude "Generate 5 practice problems similar to PS2 questions but with different data/parameters"
```

### Exam Preparation
```bash
# Mock exam
claude "Generate a 10-problem practice midterm covering weeks 1-7:
- 3 concept checks (5 min each)
- 4 computational (10 min each)
- 2 applied (20 min each)
- 1 theoretical (15 min)
Total: 120 minutes like real exam"
```

### Topic Deep Dive
```bash
# Focus on weak area
claude "I struggled with invertibility on PS2. Generate 10 problems specifically on:
- Checking invertibility conditions
- Converting to invertible form
- Understanding why it matters
Gradually increase difficulty."
```

### Group Study
```bash
# Share with classmates
claude "Generate 15 mixed problems for study group:
- Each person gets 3 problems
- Cover all midterm topics
- Include answer key separately"
```

## Difficulty Calibration

### Easy (5-10 minutes)
- Direct application of definition
- Single formula
- Clear-cut answer
- Example: "Is process yt = 0.5yt-1 + εt stationary?"

### Medium (15-20 minutes)
- Multiple steps
- Requires choosing approach
- Some interpretation needed
- Example: "Given ACF values, identify ARMA order and explain reasoning"

### Hard (30-45 minutes)
- Multi-part problem
- Requires analysis of real data
- Interpretation and judgment calls
- Example: "Analyze this dataset for unit roots, choose transformation, estimate model, evaluate forecasts"

### Very Hard (45-60 minutes)
- Proof or derivation
- Novel combination of concepts
- Research-paper style
- Example: "Derive asymptotic distribution under alternative hypothesis"

## Problem Sources

### Based on Lectures
```bash
claude "Review week-3 lecture slides and generate problems testing each major concept covered"
```

### Based on Problem Sets
```bash
claude "Create variations of Problem Set 2, Question 3 with:
- Different ARMA orders
- Different datasets
- Additional parts asking for interpretation"
```

### Based on Past Exams
```bash
# If available
claude "Based on 2025 midterm problems, generate similar questions with different numbers/contexts"
```

### Novel Combinations
```bash
claude "Generate problems that combine concepts from weeks 2 and 4 in ways not seen in problem sets"
```

## Solution Quality

Good solutions include:

### 1. Step-by-Step Work
- ✅ Show all calculations
- ✅ Explain reasoning at each step
- ✅ Label intermediate results

### 2. Interpretation
- ✅ Explain what numbers mean
- ✅ Connect to economic intuition
- ✅ State practical implications

### 3. Common Mistakes
- ✅ Warn about typical errors
- ✅ Explain why wrong approaches fail
- ✅ Show how to avoid pitfalls

### 4. Extensions
- ✅ "What if we changed X?"
- ✅ "How would this apply to Y?"
- ✅ Deepen understanding

## Organization

### By Topic
```
exam/practice-problems/
├── stationarity/
│   ├── easy-problems.md
│   ├── medium-problems.md
│   └── hard-problems.md
├── arma-models/
│   └── [same structure]
└── unit-roots/
    └── [same structure]
```

### By Difficulty
```
exam/practice-problems/
├── concept-checks.md        # All easy problems
├── computational.md         # Medium problems
└── comprehensive.md         # Hard problems
```

### By Timing
```
exam/practice-problems/
├── week-3-practice.md       # Generated after week 3
├── week-4-practice.md
├── midterm-review.md        # Compiled before exam
└── mock-exams/
    ├── mock-exam-1.md
    └── mock-exam-2.md
```

## Advanced Features

### Adaptive Difficulty
```bash
claude "Generate 5 problems on MA processes. If I get the first 3 right, make last 2 harder. If I struggle, keep them at medium level."
```

### Explain-Your-Work Problems
```bash
claude "Generate problems that require written explanations, like:
- 'Explain why this test result suggests...'
- 'Interpret the economic meaning of...'
- 'Justify your choice of model...'"
```

### Code-Based Problems
```bash
claude "Generate problems requiring Python code:
- Simulate AR(2) process
- Estimate ARMA model
- Create diagnostic plots
Include expected code and output"
```

### Multiple Choice
```bash
claude "Generate 10 multiple choice questions on unit root testing with:
- 1 correct answer
- 3 plausible distractors
- Explanation of why each choice is right/wrong"
```

## Quality Control

### Verify Problem Quality
```bash
# After generating problems
claude "Review the problems I just generated. Are they:
- At the right difficulty level?
- Clear and unambiguous?
- Representative of exam style?
- Well-connected to course material?"
```

### Test Yourself
```bash
# Work through without looking at solutions
# Then check:
claude "I solved problem 3 and got [answer]. Is this correct? If not, where did I go wrong?"
```

## Integration with Study Plan

### Week-by-Week
- After each lecture: 3-5 practice problems
- After each problem set: 5-10 variations
- Weekly review: 10-15 mixed problems

### Exam Preparation
- 2 weeks before: 50+ problems covering all topics
- 1 week before: 2-3 full mock exams
- 3 days before: 20 concept-check problems
- Night before: Quick review of most-missed problems

## Time Management

### Problem Set Recommendations
```
Easy problems: 5-10 minutes each
→ Do 10-15 for quick review
→ Total: 60-90 minutes

Medium problems: 15-20 minutes each
→ Do 5-8 for solid practice
→ Total: 90-120 minutes

Hard problems: 30-45 minutes each
→ Do 2-4 for deep practice
→ Total: 90-120 minutes
```

## Sharing with Study Group

### Generate Group Problems
```bash
claude "Create 12 problems (4 per person) for 3-person study group:
- Mixed difficulty
- All midterm topics
- Include solutions (share after working independently)"
```

### Problem Exchange
```bash
# Each person generates problems for others
claude "I'll solve problems from classmates. Generate 5 problems I can give them in exchange."
```