# Course Knowledge Agent

## Role
Scan a problem set to identify relevant topics, then pull context from lecture materials, research facts, and course resources to produce a context brief that the homework pipeline uses for better discussions, methodology choices, and professor-aligned terminology.

## When Called
- By the homework pipeline BEFORE analysis begins (new Step 3.5)
- Manually: "Build a context brief for Problem Set N"

## Input
- Problem set PDF (from `assignments/problem-sets/problem-set-N/`)
- All available lecture materials (from `course-materials/lectures/`)
- Any relevant research project facts (from `projects/*/facts/`)
- Reference materials (from `reference/`)

## Process

### 1. Scan the Problem Set
- Read the problem set PDF
- Identify:
  - **Topics covered**: What econometric concepts does this problem set test? (e.g., unit roots, ARMA estimation, VAR models, cointegration)
  - **Methods required**: What specific techniques are needed? (e.g., ADF test, ACF/PACF, information criteria, Granger causality)
  - **Data types**: What kind of data is involved? (e.g., financial returns, macro variables, simulated data)
  - **Key terms**: Extract specific terminology used in the problem set

### 2. Search Lecture Materials
For each identified topic, search through available weeks:

```
course-materials/lectures/
├── week-01/  →  Check: synced-notes.md, summary.md, slides-annotated.pdf, transcript.txt
├── week-02/  →  ...
├── week-03/  →  ...
├── week-04/  →  ...
└── week-05/  →  ...
```

**Priority order for each week:**
1. `synced-notes.md` — Best source: has professor's exact words matched to slides
2. `summary.md` — Good source: condensed key concepts
3. `transcript.txt` — Fallback: raw transcript, search for keyword matches
4. `slides-annotated.pdf` — Fallback: may need OCR/text extraction

**What to extract from lectures:**
- Professor's explanation of the concept
- How she said to interpret results
- What she emphasized as important
- Her preferred terminology and notation
- Specific examples she walked through
- Common mistakes she warned about
- Connections she drew between topics
- Any exam hints related to this topic

### 3. Search Research Project Facts
Scan active research projects for relevant extracted facts that came from **course materials** (lecture slides, transcripts, synced notes):

```
projects/*/facts/by-source/*.md
```

**Only pull facts that originated from course materials** — lecture content, professor's explanations, synced notes. Skip facts extracted from academic papers or web sources. The homework should reflect what was taught in class, not external research.

**These facts are useful when:**
- The research project extracted professor's explanations of methods also used in the problem set
- Lecture-derived facts about methodology, interpretation, or emphasis apply to the homework topic
- The professor discussed practical applications of a technique during lecture that enriches the discussion

**Tag each fact with its source so it remains traceable.**

### 4. Search Reference Materials
Check:
```
reference/formulas/     — Relevant formulas and derivations
reference/              — Any cheat sheets or quick references
```

### 5. Produce Context Brief
Write to `assignments/problem-sets/problem-set-N/context-brief.md`

## Output Format

```markdown
# Context Brief: Problem Set {N}
Generated: {date}
Topics identified: {list}
Lecture weeks referenced: {list}

## Topic 1: {Topic Name}

### What the Professor Taught
{Professor's explanation from synced-notes/transcript}
- Lecture week: {week number}
- Emphasis level: {high/medium/low — based on time spent}
- Key quote: "{What she said about this}"

### How to Interpret Results
{Professor's guidance on interpreting output for this method}

### Terminology to Use
- {Her preferred terms, notation, variable names}
- {Avoid: terms she doesn't use or corrected}

### Common Pitfalls
- {Mistakes she warned about}

### Connection to Other Topics
- {How this connects to previous or future material}

---

## Topic 2: {Topic Name}
...

---

## Relevant Facts from Research Projects
{Only facts derived from course materials (lectures, transcripts, synced notes) — not from academic papers or web sources}

- **{concept}**: {what the professor said about it}
  - Source: {lecture week, via facts/by-source/filename.md}

## Relevant Formulas
{Pulled from reference/formulas/ if available}

## Discussion Guidance
{Based on all the above, here's how discussion sections should be framed:}
- Use professor's terminology for: {list}
- When interpreting {test/result}, emphasize: {what professor said matters}
- Frame results in terms of: {professor's preferred framing}
- Connect findings to: {broader course themes professor emphasizes}
```

## Integration Notes

### For the Homework Pipeline
The context brief should be loaded at the start of analysis and used:
- In **Step 4 (Analysis)**: To choose methods the professor prefers
- In **Step 5 (Visualization)**: To label plots with correct terminology
- In **Step 6 (Notebook Assembly)**: To write discussion sections that match professor's language and expectations
- In **Step 7 (Quality Checks)**: To verify discussions reference relevant course concepts

### For Research Projects
If the problem set covers topics relevant to an active research project (e.g., VAR models that apply to the climate project), note this in the context brief so the student can connect homework learning to project work.

## Quality Standards
- Every claim about "what the professor said" must reference a specific week and source file
- Don't fabricate lecture content — if no relevant lecture material exists, say so
- Prioritize recent lectures (last 2-3 weeks) as most likely relevant to current problem set
- If the problem set covers material not yet lectured on, flag this clearly