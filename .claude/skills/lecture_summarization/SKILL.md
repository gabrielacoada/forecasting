# Lecture Summarization Skill

## Purpose
Extract key concepts, formulas, and examples from lecture slides (including annotated PDFs from Notability) to create concise study materials.

## Core Capabilities
- Read PDF slides (original or annotated)
- Extract main concepts and definitions
- Identify important formulas
- Create structured summaries
- Generate study questions
- Link to relevant problem sets

## When to Use
- After each lecture: Create summary.md
- Before problem sets: Review relevant lecture concepts
- Exam preparation: Compile multi-week summaries
- Clarification needed: Generate targeted explanations

## Best Practices

### 1. Single Lecture Summary
```bash
# After Week 3 lecture
cd course-materials/lectures/week-03-arma-models

claude "Read slides-annotated.pdf and create a structured summary in summary.md covering:
- Main topic and learning objectives
- Key concepts and definitions
- Important formulas with explanations
- Examples demonstrated
- Connection to previous weeks
- What to review for next week"
```

### 2. Extract Key Concepts
```markdown
## Output Format for summary.md

# Week 3: ARMA Models

## Main Topic
[One-sentence description]

## Key Concepts

### 1. [Concept Name]
**Definition:** [Clear definition]
**Intuition:** [Why it matters]
**Example:** [Simple example]

### 2. [Next Concept]
[Same structure]

## Important Formulas

### [Formula Name]
$$[LaTeX formula]$$

**When to use:** [Application]
**Interpretation:** [What it means]

## Examples from Class

### Example 1: [Description]
- **Setup:** [Problem context]
- **Solution:** [Key steps]
- **Takeaway:** [Lesson learned]

## Connections
- **Builds on:** Week 1-2 concepts of [...]
- **Related to:** Problem Set 2, Questions 1-3
- **Prerequisite for:** Next week's topic on [...]

## Questions to Consider
1. [Thought-provoking question]
2. [Application question]
3. [Conceptual question]

## Review Checklist
- [ ] Understand [key concept 1]
- [ ] Can derive [formula 1]
- [ ] Can identify [pattern/test]
```

### 3. Multi-Week Compilation
```bash
# Before midterm
claude "Compile summaries from weeks 1-7 into exam/study-guide.md, organizing by:
1. Core concepts (stationarity, processes, testing)
2. Key formulas (grouped by topic)
3. Common patterns and procedures
4. Example problems by type"
```

### 4. Concept Deep-Dive
```bash
claude "I'm confused about invertibility in MA processes. Read week-3 slides and explain:
- What invertibility means
- Why it matters
- How to check it
- Examples from slides"
```

### 5. Extract Formulas
```bash
claude "Extract all formulas from week-3 slides and:
1. Add them to reference/formulas/arma-processes.md
2. Include conditions and interpretations
3. Cross-reference with textbook formulas if applicable"
```

## Working with Annotated PDFs

### Your Notability Exports
Since you annotate slides with Apple Pencil in Notability:

**Claude can:**
- ✅ Read the underlying slide text
- ✅ Identify structure (headers, equations)
- ✅ Extract formulas
- ⚠️ May or may not capture your handwritten notes accurately

**Workaround for handwritten notes:**
If your annotations are important:
```bash
# Option 1: Tell Claude what you wrote
claude "In addition to the slide content, I noted: [your handwritten insights]. Incorporate this into the summary."

# Option 2: Type key annotations
# Create: week-03/my-notes.md with your key handwritten observations
# Then: claude "Combine slides-annotated.pdf and my-notes.md into comprehensive summary"
```

## Use Cases by Timing

### After Each Lecture (5-10 min)
```bash
# Immediate summary while fresh
claude "Summarize today's lecture from week-X slides. Focus on concepts I'll need for the problem set."
```

### Before Problem Sets (15 min)
```bash
# Review relevant lectures
cd assignments/problem-set-2
claude "What concepts from weeks 2-4 lectures are relevant to this problem set? Create a quick reference guide."
```

### Weekly Review (20 min)
```bash
# Friday review of the week
claude "Compare week 3 lecture with problem set 2. What did I understand well? What needs more review?"
```

### Exam Preparation (2-3 hours)
```bash
# Comprehensive compilation
claude "Create master study guide from all lectures covering:
- Every key concept with examples
- All formulas organized by topic
- Common problem types
- Connections between topics"
```

## Integration with Other Materials

### Link to Problem Sets
```bash
claude "In week-3 summary, add references to which problem set questions use each concept"
```

### Link to Reference Formulas
```bash
claude "Ensure formulas in week-3 summary match reference/formulas/arma-processes.md. Update if needed."
```

### Connect to Exam Prep
```bash
claude "Based on week-3 summary, generate 5 potential exam questions and add to exam/practice-problems/"
```

## Quality Checks

Good summaries should:
- ✅ Be 2-4 pages (not too long, not too brief)
- ✅ Include all major concepts from lecture
- ✅ Have formulas with context (not just equations)
- ✅ Show examples or applications
- ✅ Connect to broader course narrative
- ✅ Be understandable 2 weeks later

Ask Claude to verify:
```bash
claude "Review my week-3 summary.md. Is anything missing? Is it clear and complete?"
```

## Advanced: Comparative Analysis

### Compare Lecture vs Problem Set
```bash
claude "Compare week-3 lecture concepts with problem set 2 questions. What was emphasized in lecture but not tested? What was tested but not heavily covered?"
```

### Track Professor's Emphasis
```bash
claude "Across weeks 1-5, which concepts has Prof. Pesavento spent the most time on? These are likely exam priorities."
```

## Time-Saving Tips

### Batch Processing
```bash
# If you get behind on summaries
claude "Create summaries for weeks 2, 3, and 4 all at once from their slides"
```

### Template Reuse
```bash
# After first few summaries, create template
claude "Based on my week-1 and week-2 summaries, create a template structure I should use for all future weeks"
```

### Incremental Updates
```bash
# Don't start from scratch each time
claude "Update week-3 summary with insights from problem set 2 solutions"
```

## Common Patterns

### For Theory-Heavy Lectures
Focus on:
- Definitions and assumptions
- Theorem statements (no full proofs unless required)
- Intuition and interpretation
- When to apply each result

### For Applied/Computational Lectures
Focus on:
- Procedures and steps
- Code examples
- Interpretation of outputs
- Common pitfalls

### For Mixed Lectures
- Theory section
- Application section
- How theory informs practice

## Exam Season Optimization

2 weeks before exam:
```bash
# Generate comprehensive guide
claude "Create ultimate study guide from ALL lecture summaries, organized for efficient review"
```

1 week before:
```bash
# Quick reference
claude "Distill all lecture summaries into a 5-page formula sheet + key concepts only"
```

Night before:
```bash
# Final review
claude "What are the 10 most important concepts from all lectures? Create flashcard-style review."
```