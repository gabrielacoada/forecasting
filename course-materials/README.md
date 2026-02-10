# Course Materials

This directory contains all learning materials for the Forecasting & Time Series course.

## Organization

### lectures/
Weekly lecture materials organized by week number.

**For each week:**
```
week-XX-topic-name/
├── slides-original.pdf       # Prof's slides (as uploaded to Canvas/email)
├── slides-annotated.pdf      # Your Notability export with handwritten notes
├── recording.m4a             # Lecture recording (audio or video)
├── summary.md                # AI-generated or manual summary
├── key-concepts.md           # Main takeaways
├── code-examples.ipynb       # Any code from class
├── slide-alignment.md        # (Generated) Timestamped recording-to-slide guide
├── transcript.md             # (Generated) Full lecture transcript
├── enriched-summary.md       # (Generated) Slides + transcript + your notes
└── alignment-data.json       # (Generated) Machine-readable alignment data
```

**Naming convention:**
- `week-01-introduction/`
- `week-02-stationarity/`
- `week-03-arma-models/`
- etc.

**Workflow:**
1. After each lecture, export annotated slides from Notability to PDF
2. Save to `week-XX/slides-annotated.pdf`
3. Save your lecture recording to `week-XX/recording.m4a` (or .mp3/.mp4)
4. Run `/align_recording week-XX` to generate timestamped slide alignment
5. Optionally: Ask Claude to summarize key points
6. Optionally: Type up important concepts in `key-concepts.md`

### resources/
External materials referenced in class.

```
resources/
├── papers/              # Research papers discussed
│   └── paper-name.pdf
├── tutorials/           # External tutorials/guides
└── useful-links.md      # Bookmarked websites
```

## Using AI for Study

### Align Recording with Slides
```bash
# After uploading recording + slides to the week folder:
/align_recording week-05

# This generates:
#   slide-alignment.md   — timestamped guide (which slide at which time)
#   transcript.md        — full lecture transcript
#   enriched-summary.md  — combined slides + transcript + your notes
```

### Summarize Lecture
```bash
cd course-materials/lectures/week-03-arma-models
claude "Read slides-annotated.pdf and extract the key concepts into summary.md"
```

### Generate Practice Problems
```bash
claude "Based on week 3 lectures, generate 5 ARMA identification problems with solutions"
```

### Connect to Problem Sets
```bash
claude "Problem Set 2 is on ARMA models. What from week 3-4 lectures is most relevant?"
```

### Before Midterm
```bash
claude "Create a comprehensive study guide from all lectures in weeks 1-7"
```

## Tips

### Managing PDF Annotations
- **Original slides**: Save professor's unmodified slides as `slides-original.pdf`
- **Your notes**: Export your annotated version as `slides-annotated.pdf`
- **Why both**: Original is useful if you want to re-annotate or share clean slides

### Converting Notes to Text
If you want searchable notes:
```bash
claude "Extract text and your handwritten notes from slides-annotated.pdf into notes.md"
```

### Linking to Problem Sets
When working on homework, reference relevant lectures:
```bash
cd assignments/problem-set-2
claude "Use concepts from course-materials/lectures/week-03 to help solve this problem set"
```

## Week-by-Week Topics

Will be filled in as course progresses:

- **Week 1**: [Topic]
- **Week 2**: [Topic]
- **Week 3**: [Topic]
- **Week 4**: [Topic]
- **Week 5**: [Topic]
- **Week 6**: [Topic]
- **Week 7**: Midterm Review
- **Week 8**: Midterm
- **Week 9**: [Topic]
- **Week 10**: [Topic]
- **Week 11**: [Topic]
- **Week 12**: [Topic]
- **Week 13**: [Topic]
- **Week 14**: [Topic]
- **Week 15**: Final Review

(Update this as syllabus becomes clear)