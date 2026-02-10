# Align Lecture Recording with Slides

## Purpose
Align a lecture recording with its PDF slides to produce a timestamped study guide showing which slide the professor was discussing at each point in the recording.

## Usage
```
/align_recording week-05
```

## Workflow

When the user invokes this command with a week number (e.g., `week-05`):

### 1. Locate Files
Find the recording and slides in `course-materials/lectures/week-XX/`:
- **Recording**: Look for `.m4a`, `.mp3`, `.wav`, or `.mp4` files
- **Slides**: Look for the original PDF slides (not annotated)
- **Annotated slides** (optional): Look for `slides-annotated.pdf` or Notability exports
- **Notes** (optional): Look for `my-notes.md` or similar

If files are missing, tell the user what's needed and where to put them.

### 2. Check Dependencies
Ensure required packages are installed:
```bash
pip install openai-whisper pdfplumber scikit-learn
```
Also verify `ffmpeg` is available (needed by whisper).

### 3. Run Alignment
Execute the alignment script:
```bash
python scripts/align_recording.py \
  --recording course-materials/lectures/week-XX/[recording file] \
  --slides course-materials/lectures/week-XX/[slides PDF] \
  --output-dir course-materials/lectures/week-XX/ \
  --whisper-model base \
  [--annotated-slides path/if/available] \
  [--notes path/if/available]
```

### 4. Review Output
After the script runs, review the generated files:
- `slide-alignment.md` — The main timestamped guide (timestamp → slide → transcript)
- `transcript.md` — Full transcript with timestamps
- `enriched-summary.md` — Combined slides + transcript + notes
- `alignment-data.json` — Machine-readable alignment data

### 5. Enhance Summary
If a `summary.md` already exists for this week, offer to enrich it with insights from the recording:
- Which topics the professor spent the most time on
- Verbal emphasis markers ("this is important", "this will be on the exam")
- Examples given verbally that aren't on the slides
- Q&A exchanges captured in the recording

Read the `lecture_summarization` and `recording_slide_alignment` skills from `.claude/skills/` for detailed guidance.

## Model Selection Guide
- Use `--whisper-model tiny` for quick tests
- Use `--whisper-model base` for weekly processing (default, good balance)
- Use `--whisper-model small` for important or exam-critical lectures
- Use `--whisper-model medium` for maximum accuracy (slower)

## Example
```
User: /align_recording week-05
Claude: I'll align your week 5 recording with the slides...
  - Found recording: recording.m4a
  - Found slides: Dynamics+Causal+Effects.pdf
  - Running alignment with whisper base model...
  [... processing ...]
  - Generated slide-alignment.md (42 slides mapped)
  - Generated transcript.md
  - Generated enriched-summary.md
  - The professor spent the most time on slides 25-31 (HAC Standard Errors)
```
