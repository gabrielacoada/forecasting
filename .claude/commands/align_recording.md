# Align Lecture Recording with Slides

## Purpose
Align a lecture recording transcript with its PDF slides to produce a timestamped study guide showing which slide the professor was discussing at each point in the recording.

## Usage
```
/align_recording week-05
```

The user will typically also describe which files to use, e.g.:
```
/align_recording week 05 recording of todays lecture with the annotated pdf
```

## Workflow

When the user invokes this command with a week number (e.g., `week-05`):

### 1. Locate Files
Find the transcript and slides in `course-materials/lectures/week-XX/`:
- **Transcript**: Look in `recordings/` subdirectory for `.txt` files (Otter.ai export format)
- **Slides (annotated PDF)**: Look for `.pdf` files in the week directory — this is the user's Notability-annotated export, which serves as both the slides and the source of annotation data
- **Original slides** (optional): If a separate unannotated PDF exists, it can be compared against the annotated PDF to detect annotation density
- **Notes** (optional): Look for `my-notes.md` or similar

**Typical file layout:**
```
course-materials/lectures/week-XX/
├── recordings/
│   └── feb-10-topicname.txt          # Otter.ai transcript (primary input)
├── Topic+Name.pdf                     # Annotated slides PDF from Notability
├── summary.md                         # Existing summary (may be enriched)
└── my-notes.md                        # (Optional) typed notes
```

If files are missing, tell the user what's needed and where to put them.

### 2. Transcript Format
The transcript files are **Otter.ai exports** with this format:
```
Speaker 1  0:00
Text of what was said in this segment...

Speaker 1  1:37
Next segment of text...

Unknown Speaker  2:56
Another speaker's text...
```

Each segment has a speaker label and timestamp (`M:SS` or `MM:SS`), followed by the transcript text on the next line(s), separated by blank lines.

### 3. Check Dependencies
Ensure required packages are installed:
```bash
pip install pdfplumber scikit-learn
```
Note: Whisper and ffmpeg are **not** needed since we work with pre-transcribed text.

### 4. Run Alignment
Execute the alignment script with `--transcript` (not `--recording`):
```bash
python scripts/align_recording.py \
  --transcript course-materials/lectures/week-XX/recordings/[transcript.txt] \
  --slides course-materials/lectures/week-XX/[slides PDF] \
  --output-dir course-materials/lectures/week-XX/ \
  --similarity-threshold 0.08 \
  --max-backtrack 2 \
  [--annotated-slides path/if/separate/annotated/pdf/exists] \
  [--notes path/if/available]
```

**Important tuning for text transcripts:** Use `--similarity-threshold 0.08` (lower than the default 0.15) because Otter.ai transcripts have more verbal filler and the slides contain math notation that doesn't match spoken words well.

### 5. Analyze Annotations
Even without a separate original PDF for comparison, inspect the annotated PDF for ink density per page using pdfplumber (lines, curves, rects). Pages with high ink scores indicate heavy annotation — these are the slides where the professor spent the most time and the student was actively writing.

Blank pages with ink but no text are **board-note pages** — inserted pages where the student wrote down what the professor drew on the board.

### 6. Review Output
After the script runs, review the generated files:
- `slide-alignment.md` — The main timestamped guide (timestamp -> slide -> transcript)
- `transcript.md` — Full transcript with timestamps
- `enriched-summary.md` — Combined slides + transcript + notes + emphasis analysis
- `alignment-data.json` — Machine-readable alignment data

### 7. Enhance Summary
If a `summary.md` already exists for this week, offer to enrich it with insights from the recording and annotations:
- Time allocation: which topics the professor spent the most time on
- Annotation density: which slides were annotated most heavily
- Verbal emphasis markers ("this is important", "this will be on the exam")
- Examples and explanations given verbally that aren't on the slides
- Q&A exchanges captured in the recording
- Midterm/exam hints from Q&A sections

Read the `lecture_summarization` and `recording_slide_alignment` skills from `.claude/skills/` for detailed guidance.

## Alignment Quality Notes
Text transcripts from Otter.ai produce lower similarity scores than Whisper because:
- Otter.ai segments are coarser (full speaker turns vs Whisper's ~10-30s segments) — the script splits these into ~30s chunks automatically
- Math notation in slides (omega, beta, sigma) doesn't match spoken words
- More transcription artifacts and filler words

Expected: ~70-80% of slides covered, with low-medium confidence scores. The overall lecture flow (topic progression) should still be captured correctly.

## Example
```
User: /align_recording week 05 recording with the annotated pdf Dynamic Causal Effects
Claude: I'll align your week 5 transcript with the annotated slides...
  - Found transcript: recordings/feb-10-dynamiccausaleeffects.txt (58:54)
  - Found slides: Dynamics+Causal+Effects.pdf (39 pages)
  - Running alignment...
  - Generated slide-alignment.md (28 blocks, 21 slides covered)
  - Generated transcript.md (178 segments)
  - Generated enriched-summary.md
  - Heaviest annotations: pages 19, 8, 31 (board notes + OJ regression + multiplier graphic)
  - Professor spent the most time on exogeneity (~13 min) and HAC standard errors (~12 min)
```
