# Recording-to-Slide Alignment Skill

## Purpose
Align lecture recordings (audio/video) with PDF slides to produce a timestamped study guide that shows **which slide the professor was discussing at each point in the recording**. Combines the transcript, slide content, and your annotated notes into one comprehensive document.

## Why This Exists
When you record a lecture and annotate slides in Notability, you end up with two disconnected artifacts: a recording with no slide context, and annotated slides with no timing information. This skill bridges that gap so you can:
- Jump to the exact recording timestamp for any slide
- See what the professor said while on a particular slide
- Merge your handwritten annotations with the spoken explanation
- Create rich, timestamped study notes automatically

## Core Capabilities
- Transcribe lecture recordings (audio or video) with word-level timestamps
- Extract text content from each slide in a PDF
- Align transcript segments to slides using content matching + temporal progression
- Produce a timestamped markdown guide: `timestamp → slide number → transcript + notes`
- Handle the natural flow of lectures (professor starts at slide 1, progresses forward)

## When to Use
- After each lecture: Upload recording + slides → get timestamped study guide
- Before exams: Revisit specific topics by jumping to the right timestamp
- When reviewing: Cross-reference what the professor emphasized vs. what's on the slide
- Catching up: If you missed part of a lecture, find exactly where a topic was covered

## Required Tools & Dependencies

### Python Packages
```bash
pip install openai-whisper    # Speech-to-text transcription (local, free)
pip install pdfplumber        # Extract text from PDF slides
pip install pdf2image         # Convert slides to images for visual comparison
pip install scikit-learn      # TF-IDF similarity for content matching
```

### System Dependencies
```bash
# For whisper (audio processing)
sudo apt-get install ffmpeg

# For pdf2image (PDF rendering)
sudo apt-get install poppler-utils
```

### Model Sizes (whisper)
| Model  | Size   | Speed   | Accuracy | Recommended For          |
|--------|--------|---------|----------|--------------------------|
| tiny   | 39 MB  | ~10x RT | Good     | Quick drafts             |
| base   | 74 MB  | ~7x RT  | Better   | **Default (good balance)** |
| small  | 244 MB | ~4x RT  | Great    | Important lectures       |
| medium | 769 MB | ~2x RT  | Excellent| Exam-critical material   |

## How the Alignment Works

### Algorithm Overview
The alignment uses a **content-matching + monotonic temporal constraint** approach:

1. **Transcribe** the recording with timestamps (whisper produces segment-level timestamps)
2. **Extract text** from each slide in the PDF
3. **Compute similarity** between each transcript segment and each slide using TF-IDF cosine similarity
4. **Apply monotonic constraint**: slides generally progress forward (the professor doesn't jump from slide 30 back to slide 5)
5. **Detect transitions**: look for topic shifts, pauses, or explicit cues ("next slide", "moving on")
6. **Refine**: use temporal heuristic as a prior — early recording ≈ early slides, late recording ≈ late slides

### Key Assumptions
- The professor generally progresses through slides in order (with possible brief revisits to a recent slide)
- The recording starts roughly when the professor starts the slide deck
- Content overlap between what's spoken and what's on the slide is the strongest signal
- Keyword matching (technical terms, formula names, example names) is more reliable than generic words

### Handling Edge Cases
- **Professor skips slides**: Some slides get no transcript segments — that's fine, they're marked as "skipped or briefly shown"
- **Professor revisits a slide**: The monotonic constraint allows small backward jumps (up to 3 slides back)
- **Tangents/digressions**: Segments with low similarity to any slide are marked as "off-slide discussion"
- **Q&A sections**: Typically at slide boundaries, detected by question-like patterns in transcript

## File Organization

### Input Files (per week)
```
course-materials/lectures/week-XX/
├── slides-original.pdf          # Professor's unmodified slides
├── slides-annotated.pdf         # Your Notability export with handwritten notes
├── recording.m4a                # Audio recording (or .mp3, .wav, .mp4)
└── my-notes.md                  # (Optional) typed notes to supplement
```

### Output Files (generated)
```
course-materials/lectures/week-XX/
├── transcript.md                # Full timestamped transcript
├── slide-alignment.md           # Timestamped slide-by-slide guide (MAIN OUTPUT)
├── alignment-data.json          # Machine-readable alignment data
└── enriched-summary.md          # Combined: slides + transcript + your notes
```

## Output Format

### slide-alignment.md (Main Output)
```markdown
# Week 5: Lecture Recording Alignment
**Recording:** recording.m4a (1h 15m)
**Slides:** Dynamics+Causal+Effects.pdf (42 slides)
**Generated:** 2026-02-10

---

## Slide 1 (00:00 – 02:15) — Title Slide
**Slide text:** "Dynamic Causal Effects, Chapter 13"
**Professor said:**
> "Alright, so today we're going to talk about dynamic causal effects.
> This is chapter 13 in Stock and Watson. The key question is: when X
> changes, how does the effect on Y unfold over time?"

**Your annotations:** [None on this slide]

---

## Slide 2 (02:15 – 05:40) — Motivation: Why Dynamic Effects?
**Slide text:** "Static vs Dynamic: cigarette tax example..."
**Professor said:**
> "Think about what happens if you raise the cigarette tax. The immediate
> effect might be small — people don't quit overnight. But over months
> and years, consumption drops significantly..."

**Your annotations:** "Key: effects unfold over TIME, not instant"

---
[... continues for all slides ...]
```

### enriched-summary.md
Combines the existing `summary.md` format with recording insights:
- Which concepts the professor spent the most time on (by timestamp duration)
- Verbal emphasis markers ("this is really important", "this will be on the exam")
- Examples the professor gave verbally that aren't on slides
- Q&A exchanges captured in the recording

## Usage

### Quick Start (Single Command)
```bash
# From repo root:
claude "Align the week 5 recording with slides. Recording is at
course-materials/lectures/week-05/recording.m4a and slides are
Dynamics+Causal+Effects.pdf"
```

### Using the Script Directly
```bash
python scripts/align_recording.py \
  --recording course-materials/lectures/week-05/recording.m4a \
  --slides course-materials/lectures/week-05/Dynamics+Causal+Effects.pdf \
  --output-dir course-materials/lectures/week-05/ \
  --whisper-model base \
  --annotated-slides course-materials/lectures/week-05/slides-annotated.pdf \
  --notes course-materials/lectures/week-05/my-notes.md
```

### Using the Claude Command
```bash
# Easy invocation via slash command:
/align_recording week-05
```

## Integration with Other Skills

### With lecture_summarization
After alignment, the enriched summary feeds into the lecture summarization skill:
```bash
claude "Using the slide-alignment.md and enriched-summary.md from week 5,
create an improved summary.md that highlights what the professor
emphasized most (by time spent and verbal cues)"
```

### With practice_generator
Generate practice problems weighted by professor emphasis:
```bash
claude "Based on the week 5 alignment, the professor spent 15 minutes on
HAC standard errors. Generate 5 practice problems focused on that topic."
```

### With hwk_pipeline
Cross-reference homework problems with lecture coverage:
```bash
claude "Which slides from week 5 are most relevant to Problem Set 2?
Use the alignment to find where the professor discussed those concepts."
```

## Professor Emphasis Detection

The alignment skill also identifies **what the professor emphasized**, which is invaluable for exam prep:

### Emphasis Signals
- **Time spent**: If 3 slides take 20 minutes, that topic matters
- **Verbal cues**: "This is important", "You need to know this", "This will come up again"
- **Repetition**: Professor revisits a concept or re-explains it
- **Examples**: Extended worked examples signal key application areas
- **Warnings**: "Students often get this wrong", "Common mistake is..."

### Output: Emphasis Report
```markdown
## Professor Emphasis Analysis

### High Emphasis Topics (most time + verbal cues)
1. **HAC Standard Errors** — 18 min, 4 verbal emphasis markers
   - Slides 25-31
   - "You absolutely need to understand why OLS SEs are wrong here"
2. **Exogeneity Assessment** — 12 min, 3 verbal cues
   - Slides 18-22
   - "This is the key assumption. If this fails, everything falls apart"

### Medium Emphasis
3. **Distributed Lag Model** — 8 min
4. **OJ Price Example** — 7 min (used as running illustration)

### Briefly Covered
5. **GLS/Strict Exogeneity** — 2 min ("Section 13.5, you can skip this")
```

## Tuning & Configuration

### Whisper Model Selection
- Use `base` for weekly processing (fast, good enough)
- Use `small` or `medium` for exam-critical lectures
- Use `tiny` for quick tests or when you just need rough alignment

### Similarity Threshold
- Default: 0.15 (cosine similarity) — a segment must match a slide at least this well
- Lower (0.10): More permissive, assigns more segments to slides
- Higher (0.20): More conservative, more segments marked as "off-slide"

### Transition Detection Sensitivity
- Keywords like "next slide", "moving on", "let's look at" trigger slide transitions
- Pauses > 3 seconds at segment boundaries suggest transitions
- Configurable via `--transition-sensitivity` (low/medium/high)

## Tips for Best Results

### Recording Quality
- Record from a consistent position (front of class is best)
- External microphone improves transcription accuracy significantly
- Avoid recording in noisy environments when possible
- M4A or WAV format preferred over MP3 for quality

### Slide Preparation
- Upload the **original** slides PDF (cleaner text extraction)
- If available, also provide **annotated** slides for note integration
- Ensure slides are text-based PDFs (not scanned images) for best text extraction

### Post-Processing
- Review the alignment output — fix any obvious misalignments manually
- Add your own notes to sections where the transcript was unclear
- Use the enriched summary as your primary study document

## Limitations
- Whisper may struggle with heavy accents, very fast speech, or poor audio quality
- Slides that are mostly images/graphs have less text to match against
- The alignment is approximate — expect ~85-90% accuracy for slide boundaries
- Very long tangents or discussions may be hard to assign to specific slides
- Handwritten annotations on slides can't be read automatically (type key ones in my-notes.md)
