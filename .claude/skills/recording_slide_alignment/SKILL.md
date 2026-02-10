# Recording-to-Slide Alignment Skill

## Purpose
Align lecture recording transcripts with PDF slides to produce a timestamped study guide that shows **which slide the professor was discussing at each point in the recording**. Combines the transcript, slide content, and your annotated notes into one comprehensive document.

## Why This Exists
When you record a lecture and annotate slides in Notability, you end up with two disconnected artifacts: a transcript with no slide context, and annotated slides with no timing information. This skill bridges that gap so you can:
- Jump to the exact recording timestamp for any slide
- See what the professor said while on a particular slide
- Merge your handwritten annotations with the spoken explanation
- Create rich, timestamped study notes automatically

## Input: Otter.ai Text Transcripts

The primary input is a **pre-transcribed text file** from Otter.ai (not raw audio). This means:
- **No Whisper/ffmpeg needed** — the transcription is already done
- Transcripts live in `course-materials/lectures/week-XX/recordings/` as `.txt` files
- The annotated PDF (Notability export) serves as both the slides and the annotation source

### Otter.ai Transcript Format
```
Speaker 1  0:00
Text of what was said in this segment...

Speaker 1  1:37
Next segment of text...

Unknown Speaker  2:56
Another speaker's text...
```

Each segment has:
- A speaker label (`Speaker 1`, `Speaker 2`, `Unknown Speaker`, etc.)
- A timestamp in `M:SS` or `MM:SS` format
- Transcript text on the following line(s)
- Segments separated by blank lines

### Segment Splitting
Otter.ai segments are often very long (full speaker turns spanning multiple slides). The alignment script automatically splits them into ~30-second chunks by sentence boundaries, distributing timestamps proportionally. This produces granularity closer to what Whisper would give (~10-30s segments).

## Core Capabilities
- Parse Otter.ai transcript files into timestamped segments with automatic chunking
- Extract text content from each slide in a PDF
- Analyze annotation density on slides (ink objects: lines, curves, rects)
- Align transcript segments to slides using content matching + temporal progression
- Produce a timestamped markdown guide: `timestamp → slide number → transcript + notes`
- Handle the natural flow of lectures (professor starts at slide 1, progresses forward)

## When to Use
- After each lecture: Upload transcript + annotated slides → get timestamped study guide
- Before exams: Revisit specific topics by jumping to the right timestamp
- When reviewing: Cross-reference what the professor emphasized vs. what's on the slide
- Catching up: If you missed part of a lecture, find exactly where a topic was covered

## Required Tools & Dependencies

### Python Packages
```bash
pip install pdfplumber        # Extract text from PDF slides
pip install scikit-learn      # TF-IDF similarity for content matching
```

### Not Required
- ~~openai-whisper~~ — transcription is done by Otter.ai
- ~~ffmpeg~~ — no audio processing needed
- ~~pdf2image / poppler-utils~~ — not needed for text extraction

## How the Alignment Works

### Algorithm Overview
The alignment uses a **content-matching + monotonic temporal constraint** approach:

1. **Parse** the Otter.ai transcript into timestamped segments (~30s chunks)
2. **Extract text** from each slide in the PDF
3. **Compute similarity** between each transcript segment and each slide using TF-IDF cosine similarity
4. **Apply monotonic constraint**: slides generally progress forward (the professor doesn't jump from slide 30 back to slide 5)
5. **Detect transitions**: look for topic shifts or explicit cues ("next slide", "moving on")
6. **Refine**: use temporal heuristic as a prior — early recording ≈ early slides, late recording ≈ late slides

### Similarity Challenges with Text Transcripts
Text transcripts from Otter.ai produce **lower similarity scores** than Whisper because:
- **Math notation mismatch**: Slides contain symbols (ω, β, σ²) while the professor says "omega", "beta", "sigma squared"
- **Verbal filler**: Transcripts include "right?", "okay", "you know" that dilute keyword matching
- **Transcription artifacts**: Otter.ai mishears technical terms (e.g., "hack" for "HAC", "Coada" for "coda")
- **Coarser segments**: Even after splitting, chunks may span slide boundaries

**Recommended settings for text transcripts:**
- `--similarity-threshold 0.08` (lower than default 0.15)
- `--max-backtrack 2`
- Expected coverage: ~70-80% of slides, with low-medium confidence scores

### Key Assumptions
- The professor generally progresses through slides in order (with possible brief revisits to a recent slide)
- The recording starts roughly when the professor starts the slide deck
- Content overlap between what's spoken and what's on the slide is the strongest signal
- Keyword matching (technical terms, formula names, example names) is more reliable than generic words
- **Annotations are ground truth**: If you wrote on or annotated a slide, the professor was actively on that slide at that time. Annotated slides are confirmed "active" slides and should be weighted heavily in alignment

### Using Your Annotations as Alignment Anchors

Your handwritten annotations on slides (from Notability) are the **strongest signal** for alignment — stronger than transcript-to-slide text matching. The reasoning is simple: you only write on a slide while the professor is talking about it.

**How this works:**
1. When a separate **original slides PDF** is available, compare it to the **annotated slides PDF** page by page to detect annotations added on top
2. When only the annotated PDF is available (the common case), analyze **ink density** per page using pdfplumber — pages with many lines, curves, and rects have heavy annotations
3. Slides with **more annotation content** (heavier writing, more ink) likely had the professor on them for longer
4. Slides with **no annotations** were either skipped, shown briefly, or the professor talked without you needing to write
5. These annotation anchors constrain the alignment — transcript segments near an annotated slide are strongly pulled toward it

**Annotation density as a time proxy:**
- Heavy annotations (lots of writing, diagrams, underlines) → professor spent significant time here
- Light annotations (a checkmark, one word) → briefly discussed or a quick note to yourself
- No annotations → possibly skipped, or pure listening (Q&A, verbal-only explanation)

**Ink score heuristic** (when only annotated PDF is available):
```
ink_score = len(lines) * 5 + len(curves) * 3
```
- Pages with ink_score > 200: heavily annotated (board work, detailed notes)
- Pages with ink_score > 100: moderately annotated
- Pages with ink_score < 20: minimal or no annotations (just slide template elements)
- Pages with ink_score > 0 but no extractable text: **board-note pages** (inserted blank pages)

**This means:** Even if the transcript text poorly matches a slide's content (e.g., the professor went on a verbal tangent while on slide 15), the annotation on slide 15 confirms the professor was there. The alignment should trust annotation evidence over text-matching scores when they conflict.

### Inserted "Board Note" Pages

You sometimes add extra blank pages to the annotated PDF to write down what the professor draws or writes on the board (content that isn't on any slide). This means the annotated PDF can have **more pages** than the original slides PDF.

**How the system handles this:**
1. Pages are matched by **text content similarity** (not by index), so inserted pages don't break the alignment
2. Each annotated page is compared to all original slides — if it matches one well, it's that slide with annotations
3. Pages that **don't match any original slide** are detected as **board note pages**
4. Board note pages are associated with the **nearest preceding matched slide** (the professor was on that slide when they started writing on the board)
5. Board notes **boost the emphasis score** of their associated slide — if the professor went to the board to explain something, that topic is clearly important
6. Board note content (text or "handwritten/diagram") is included in the alignment output under the associated slide

**When only the annotated PDF is available:** Board-note pages are detected as pages with high ink scores but no extractable text (empty text, lots of curves/lines).

**Example:** If the original PDF has 30 slides and your annotated PDF has 34 pages, the system detects 4 inserted board-note pages, matches the other 30 to original slides, and shows each board note under the slide it belongs to.

### Handling Edge Cases
- **Professor skips slides**: Some slides get no transcript segments — that's fine, they're marked as "skipped or briefly shown"
- **Professor revisits a slide**: The monotonic constraint allows small backward jumps (up to `max_backtrack` slides back)
- **Tangents/digressions**: Segments with low similarity to any slide stay on the current slide
- **Q&A sections**: Typically at slide boundaries, detected by question-like patterns in transcript
- **Inserted pages (board notes)**: Extra pages you added to write board content are detected and associated with the slide the professor was on
- **Page count mismatch**: If annotated PDF has more pages than original, pages are matched by content similarity — not by index — so everything stays aligned
- **Long Otter.ai segments**: Automatically split into ~30s chunks by sentence to improve alignment granularity

## File Organization

### Input Files (per week)
```
course-materials/lectures/week-XX/
├── recordings/
│   └── feb-10-topicname.txt     # Otter.ai transcript (primary input)
├── Topic+Name.pdf                # Annotated slides from Notability
├── slides-original.pdf           # (Optional) unannotated slides for annotation comparison
├── summary.md                    # (Optional) existing summary to enrich
└── my-notes.md                   # (Optional) typed notes to supplement
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
# Lecture Recording Alignment
**Recording:** feb-10-dynamiccausaleeffects.txt (58:54)
**Slides:** Dynamics+Causal+Effects.pdf (39 slides)

---

## Slide 3 (00:00 – 00:40) [40s]
**Slide content:** "Dynamic Causal Effects — A dynamic causal effect is..."
**Professor said:**
> "Economics, because now we have time, and we can even ask
> different questions, right? We can ask that, what is the
> effect of a shock now to today, but also maybe five years..."

*Alignment confidence: low*

---

## Slide 4 (01:11 – 02:47) [1m 35s]
**Slide content:** "The Orange Juice Data..."
**Professor said:**
> "And I have the prices. I also have the percentage change..."

*Alignment confidence: medium*

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
# From repo root, using the slash command:
/align_recording week-05
```

### Using the Script Directly
```bash
python scripts/align_recording.py \
  --transcript course-materials/lectures/week-05/recordings/feb-10-dynamiccausaleeffects.txt \
  --slides course-materials/lectures/week-05/Dynamics+Causal+Effects.pdf \
  --output-dir course-materials/lectures/week-05/ \
  --similarity-threshold 0.08 \
  --max-backtrack 2
```

### With Separate Original Slides (for annotation comparison)
```bash
python scripts/align_recording.py \
  --transcript course-materials/lectures/week-05/recordings/feb-10-dynamiccausaleeffects.txt \
  --slides course-materials/lectures/week-05/slides-original.pdf \
  --output-dir course-materials/lectures/week-05/ \
  --annotated-slides course-materials/lectures/week-05/Dynamics+Causal+Effects.pdf \
  --similarity-threshold 0.08
```

### Legacy: Using Audio Recording (if available)
```bash
# Only if you have the actual audio file and Whisper installed:
python scripts/align_recording.py \
  --recording course-materials/lectures/week-05/recording.m4a \
  --slides course-materials/lectures/week-05/slides.pdf \
  --output-dir course-materials/lectures/week-05/ \
  --whisper-model base
```

## Integration with Other Skills

### With lecture_summarization
After alignment, enrich the existing summary with recording and annotation insights:
```bash
claude "Using the slide-alignment.md, enriched-summary.md, and annotation
density data from week 5, enrich summary.md with:
- Time allocation table (how long on each topic)
- Heaviest annotations (which slides you wrote on most)
- Key things the professor said that aren't on slides
- Midterm hints from Q&A"
```

### With practice_generator
Generate practice problems weighted by professor emphasis:
```bash
claude "Based on the week 5 alignment, the professor spent 13 minutes on
exogeneity examples. Generate 5 practice problems focused on that topic."
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
- **Your annotations**: If you wrote on a slide, the professor was actively discussing it — annotated slides are confirmed important
- **Annotation density**: Slides with heavy annotations (lots of writing, diagrams, underlines) received the most professor attention
- **Board-note pages**: Inserted blank pages with ink = professor went to the board = topic is clearly important
- **Time spent**: If 3 slides take 20 minutes, that topic matters
- **Verbal cues**: "This is important", "You need to know this", "This will come up again"
- **Repetition**: Professor revisits a concept or re-explains it
- **Examples**: Extended worked examples signal key application areas
- **Warnings**: "Students often get this wrong", "Common mistake is..."

### Output: Emphasis Report
```markdown
## Professor Emphasis Analysis

### High Emphasis Topics (most time + verbal cues + annotations)
1. **Exogeneity examples** — ~13 min, "super important", heavy annotations on slides 34-36
2. **HAC Standard Errors** — ~12 min, board derivation (page 19 board note), "remember this"
   - Board note page 19: variance derivation with serial correlation
   - Board note page 31: multiplier graphic interpretation

### Medium Emphasis
3. **OJ estimation results** — ~12 min (slides 24-33)
4. **Distributed lag model** — ~5 min, annotated on slides 8, 12

### Briefly Covered
5. **GLS/Strict Exogeneity** — mentioned briefly, no annotations
```

## Tuning & Configuration

### Similarity Threshold
- Default: 0.15 — **too high for text transcripts**, use 0.08 instead
- 0.08: Good for Otter.ai transcripts with math-heavy slides
- 0.05: Very permissive, may produce noisy assignments
- 0.15+: Only appropriate for Whisper transcripts or text-light slides

### Max Backtrack
- Default: 3 — how many slides backward the algorithm can look
- 2: Better for Otter.ai transcripts (reduces oscillation between slides)
- 1: Very strict forward-only progression

### Segment Target Duration
- The transcript parser splits long Otter.ai turns into ~30s chunks by default
- This is hardcoded in `parse_transcript_file()` but can be adjusted if needed

## Tips for Best Results

### Transcript Quality
- Export from Otter.ai as plain text (not rich text or PDF)
- Review and fix any critical transcription errors before running alignment (optional but helpful)
- Otter.ai works best when the professor uses a microphone
- Speaker labels don't need to be accurate — the alignment uses text content, not speaker identity

### Slide Preparation
- The annotated PDF (Notability export) is the primary input
- If you also have the original unannotated slides, provide them via `--annotated-slides` for better annotation detection
- Ensure slides are text-based PDFs (not scanned images) for best text extraction

### Post-Processing
- Review the alignment output — fix any obvious misalignments manually
- Add your own notes to sections where the transcript was unclear
- Use the enriched summary as your primary study document
- When enriching summary.md, include direct quotes from the professor for verbal insights not on slides

## Limitations
- Otter.ai may struggle with heavy accents, very fast speech, or overlapping speakers
- Math-heavy slides have low text-matching similarity with spoken words (the biggest accuracy challenge)
- Slides that are mostly images/graphs have less text to match against
- The alignment is approximate — expect ~70-80% accuracy for slide boundaries with text transcripts
- Very long tangents or discussions may be hard to assign to specific slides
- Handwritten annotations on slides can't be read automatically (type key ones in my-notes.md)
- Without a separate original PDF, annotation detection relies on ink density heuristics rather than precise comparison
