#!/usr/bin/env python3
"""
Recording-to-Slide Alignment Script

Aligns lecture recordings with PDF slides to produce a timestamped study guide.
Uses whisper for transcription, pdfplumber for slide text extraction, and
TF-IDF cosine similarity for content matching with a monotonic temporal constraint.

Usage:
    python scripts/align_recording.py \
        --recording course-materials/lectures/week-05/recording.m4a \
        --slides course-materials/lectures/week-05/Dynamics+Causal+Effects.pdf \
        --output-dir course-materials/lectures/week-05/ \
        --whisper-model base
"""

import argparse
import json
import re
import sys
from pathlib import Path


def check_dependencies():
    """Check and report missing dependencies."""
    missing = []
    for pkg, import_name in [
        ("openai-whisper", "whisper"),
        ("pdfplumber", "pdfplumber"),
        ("scikit-learn", "sklearn"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Missing dependencies. Install with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def transcribe_recording(recording_path, model_name="base"):
    """Transcribe audio/video using whisper, returning timestamped segments."""
    import whisper

    print(f"Loading whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Transcribing {recording_path}...")
    result = model.transcribe(
        str(recording_path),
        verbose=False,
        word_timestamps=True,
    )

    segments = []
    for seg in result["segments"]:
        segments.append({
            "id": seg["id"],
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })

    print(f"  Transcribed {len(segments)} segments, "
          f"total duration: {format_timestamp(segments[-1]['end'])}")
    return segments


def extract_slide_texts(slides_path):
    """Extract text content from each page/slide of a PDF."""
    import pdfplumber

    print(f"Extracting text from {slides_path}...")
    slides = []
    with pdfplumber.open(str(slides_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            slides.append({
                "slide_number": i + 1,
                "text": text.strip(),
                "word_count": len(text.split()),
            })

    print(f"  Extracted text from {len(slides)} slides")
    return slides


def compute_similarity_matrix(segments, slides):
    """Compute TF-IDF cosine similarity between transcript segments and slides."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    segment_texts = [s["text"] for s in segments]
    slide_texts = [s["text"] for s in slides]

    # Build TF-IDF on combined corpus (slides first, then segments)
    all_texts = slide_texts + segment_texts
    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=1,
        max_df=0.95,
        ngram_range=(1, 2),
    )
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    slide_vectors = tfidf_matrix[: len(slides)]
    segment_vectors = tfidf_matrix[len(slides):]

    similarity = cosine_similarity(segment_vectors, slide_vectors)
    return similarity


def detect_transition_cues(text):
    """Check if a transcript segment contains slide transition cues."""
    cues = [
        r"\bnext slide\b",
        r"\bmoving on\b",
        r"\blet'?s look at\b",
        r"\blet'?s move\b",
        r"\bnow let'?s\b",
        r"\bturning to\b",
        r"\bon this slide\b",
        r"\bas you can see\b",
        r"\blooking at this\b",
        r"\bso now\b",
    ]
    lower = text.lower()
    return any(re.search(cue, lower) for cue in cues)


def align_segments_to_slides(segments, slides, similarity_matrix,
                              similarity_threshold=0.15, max_backtrack=3):
    """
    Assign each transcript segment to a slide using content similarity
    with a monotonic temporal constraint.

    The algorithm:
    1. For each segment, find the best-matching slide by cosine similarity
    2. Apply a monotonic constraint: the assigned slide can only move forward
       or backtrack by at most max_backtrack slides from the current position
    3. Use temporal prior: weight similarity by proximity to expected position
       (early recording -> early slides)
    4. Detect transition cues to trigger slide advancement
    """
    import numpy as np

    n_segments = len(segments)
    n_slides = len(slides)
    assignments = []
    current_slide_idx = 0

    total_duration = segments[-1]["end"] if segments else 1.0

    for i, seg in enumerate(segments):
        # Temporal prior: expected slide position based on time progress
        time_progress = seg["start"] / total_duration
        expected_slide_idx = int(time_progress * n_slides)

        # Allowed slide range: current position to a bit ahead, with small backtrack
        min_slide = max(0, current_slide_idx - max_backtrack)
        max_slide = min(n_slides - 1, current_slide_idx + max(5, n_slides // 4))

        # Get similarities for allowed range
        sims = similarity_matrix[i].copy()

        # Zero out slides outside allowed range
        mask = np.zeros(n_slides)
        mask[min_slide: max_slide + 1] = 1.0
        sims = sims * mask

        # Add temporal prior bonus (small gaussian centered on expected position)
        for j in range(n_slides):
            temporal_bonus = np.exp(-0.5 * ((j - expected_slide_idx) / max(n_slides * 0.15, 1)) ** 2)
            sims[j] += 0.05 * temporal_bonus

        # Check for transition cues
        has_transition = detect_transition_cues(seg["text"])

        best_slide_idx = int(np.argmax(sims))
        best_sim = similarity_matrix[i][best_slide_idx]

        # If similarity is too low, keep current slide (professor is elaborating)
        if best_sim < similarity_threshold and not has_transition:
            best_slide_idx = current_slide_idx

        # If transition cue detected and we haven't moved, nudge forward
        if has_transition and best_slide_idx <= current_slide_idx:
            best_slide_idx = min(current_slide_idx + 1, n_slides - 1)

        assignments.append({
            "segment_id": seg["id"],
            "slide_number": slides[best_slide_idx]["slide_number"],
            "slide_index": best_slide_idx,
            "similarity": float(best_sim),
            "has_transition_cue": has_transition,
        })

        current_slide_idx = best_slide_idx

    return assignments


def merge_into_slide_blocks(segments, slides, assignments):
    """Group consecutive segments assigned to the same slide into blocks."""
    blocks = []
    current_block = None

    for seg, assign in zip(segments, assignments):
        slide_num = assign["slide_number"]

        if current_block is None or current_block["slide_number"] != slide_num:
            if current_block is not None:
                blocks.append(current_block)
            current_block = {
                "slide_number": slide_num,
                "slide_text": slides[assign["slide_index"]]["text"],
                "start_time": seg["start"],
                "end_time": seg["end"],
                "transcript_segments": [seg["text"]],
                "avg_similarity": assign["similarity"],
                "n_segments": 1,
            }
        else:
            current_block["end_time"] = seg["end"]
            current_block["transcript_segments"].append(seg["text"])
            current_block["avg_similarity"] = (
                (current_block["avg_similarity"] * current_block["n_segments"]
                 + assign["similarity"])
                / (current_block["n_segments"] + 1)
            )
            current_block["n_segments"] += 1

    if current_block is not None:
        blocks.append(current_block)

    return blocks


def detect_emphasis(blocks):
    """Analyze blocks to detect professor emphasis signals."""
    emphasis_cues = [
        (r"\b(?:this is (?:really |very )?important)\b", "important"),
        (r"\b(?:you need to know|you should know)\b", "need to know"),
        (r"\b(?:this will (?:come up|be on))\b", "exam hint"),
        (r"\b(?:key (?:point|idea|concept|takeaway))\b", "key point"),
        (r"\b(?:common mistake|students often)\b", "common mistake"),
        (r"\b(?:remember this|don'?t forget)\b", "remember"),
        (r"\b(?:pay attention|note that)\b", "attention"),
    ]

    emphasis_report = []
    for block in blocks:
        full_text = " ".join(block["transcript_segments"]).lower()
        duration = block["end_time"] - block["start_time"]
        cues_found = []

        for pattern, label in emphasis_cues:
            if re.search(pattern, full_text):
                cues_found.append(label)

        emphasis_report.append({
            "slide_number": block["slide_number"],
            "duration_seconds": round(duration, 1),
            "emphasis_cues": cues_found,
            "emphasis_score": len(cues_found) + (duration / 120),  # cues + time weight
        })

    return emphasis_report


def load_notes(notes_path):
    """Load optional typed notes file."""
    if notes_path and Path(notes_path).exists():
        return Path(notes_path).read_text(encoding="utf-8")
    return None


def format_timestamp(seconds):
    """Format seconds as HH:MM:SS or MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def generate_slide_alignment_md(blocks, emphasis, recording_name, slides_name,
                                 total_slides, notes_text=None):
    """Generate the main slide-alignment.md output."""
    total_duration = blocks[-1]["end_time"] if blocks else 0

    lines = [
        f"# Lecture Recording Alignment",
        f"**Recording:** {recording_name} ({format_timestamp(total_duration)})",
        f"**Slides:** {slides_name} ({total_slides} slides)",
        f"",
        f"---",
        f"",
    ]

    for block in blocks:
        start = format_timestamp(block["start_time"])
        end = format_timestamp(block["end_time"])
        slide_num = block["slide_number"]
        duration = block["end_time"] - block["start_time"]

        # Find emphasis info for this block
        emph = next((e for e in emphasis if e["slide_number"] == slide_num), None)
        emphasis_markers = ""
        if emph and emph["emphasis_cues"]:
            markers = ", ".join(emph["emphasis_cues"])
            emphasis_markers = f" **[{markers}]**"

        lines.append(f"## Slide {slide_num} ({start} - {end}) [{format_duration(duration)}]{emphasis_markers}")
        lines.append(f"")

        # Slide text (truncated if very long)
        slide_text = block["slide_text"]
        if len(slide_text) > 500:
            slide_text = slide_text[:500] + "..."
        if slide_text:
            lines.append(f"**Slide content:**")
            lines.append(f"> {slide_text[:200]}")
            lines.append(f"")

        # Transcript
        transcript = " ".join(block["transcript_segments"])
        lines.append(f"**Professor said:**")
        lines.append(f"> {transcript}")
        lines.append(f"")

        # Similarity confidence
        confidence = "high" if block["avg_similarity"] > 0.3 else \
                     "medium" if block["avg_similarity"] > 0.15 else "low"
        lines.append(f"*Alignment confidence: {confidence}*")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    return "\n".join(lines)


def generate_emphasis_report_md(emphasis, slides):
    """Generate the emphasis analysis section."""
    sorted_emph = sorted(emphasis, key=lambda x: x["emphasis_score"], reverse=True)

    lines = [
        "## Professor Emphasis Analysis",
        "",
        "### High Emphasis Topics (most time + verbal cues)",
        "",
    ]

    rank = 1
    for e in sorted_emph[:5]:
        slide = next((s for s in slides if s["slide_number"] == e["slide_number"]), None)
        slide_preview = (slide["text"][:80] + "...") if slide and slide["text"] else "No text"
        cues = ", ".join(e["emphasis_cues"]) if e["emphasis_cues"] else "time-based"
        duration = format_duration(e["duration_seconds"])
        lines.append(f"{rank}. **Slide {e['slide_number']}** - {duration}, cues: {cues}")
        lines.append(f"   - Preview: {slide_preview}")
        lines.append(f"")
        rank += 1

    lines.append("### All Slides by Time Spent")
    lines.append("")
    lines.append("| Slide | Duration | Emphasis Cues |")
    lines.append("|-------|----------|---------------|")
    for e in sorted(emphasis, key=lambda x: x["slide_number"]):
        cues = ", ".join(e["emphasis_cues"]) if e["emphasis_cues"] else "-"
        lines.append(f"| {e['slide_number']} | {format_duration(e['duration_seconds'])} | {cues} |")

    return "\n".join(lines)


def generate_transcript_md(segments, recording_name):
    """Generate the full transcript with timestamps."""
    lines = [
        f"# Full Transcript: {recording_name}",
        f"",
    ]

    for seg in segments:
        ts = format_timestamp(seg["start"])
        lines.append(f"**[{ts}]** {seg['text']}")
        lines.append(f"")

    return "\n".join(lines)


def generate_enriched_summary_md(blocks, emphasis, slides, notes_text=None):
    """Generate an enriched summary combining slides, transcript, and notes."""
    lines = [
        "# Enriched Lecture Summary",
        "",
        "This summary combines slide content, what the professor said, "
        "and your annotations into a single study document.",
        "",
        "---",
        "",
    ]

    # Add emphasis report
    lines.append(generate_emphasis_report_md(emphasis, slides))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Main content by slide
    lines.append("## Slide-by-Slide Breakdown")
    lines.append("")

    for block in blocks:
        slide_num = block["slide_number"]
        duration = block["end_time"] - block["start_time"]
        start = format_timestamp(block["start_time"])

        lines.append(f"### Slide {slide_num} (at {start}, {format_duration(duration)})")
        lines.append("")

        if block["slide_text"]:
            lines.append(f"**On the slide:**")
            lines.append(f"{block['slide_text'][:300]}")
            lines.append("")

        transcript = " ".join(block["transcript_segments"])
        lines.append(f"**Professor explained:**")
        lines.append(f"{transcript}")
        lines.append("")

    # Append user notes if provided
    if notes_text:
        lines.append("---")
        lines.append("")
        lines.append("## Your Typed Notes")
        lines.append("")
        lines.append(notes_text)

    return "\n".join(lines)


def format_duration(seconds):
    """Format duration nicely."""
    if seconds < 60:
        return f"{int(seconds)}s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s}s"


def save_alignment_data(output_dir, blocks, assignments, emphasis):
    """Save machine-readable alignment data as JSON."""
    data = {
        "blocks": blocks,
        "segment_assignments": assignments,
        "emphasis": emphasis,
    }
    output_path = Path(output_dir) / "alignment-data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Align lecture recording with PDF slides"
    )
    parser.add_argument(
        "--recording", required=True,
        help="Path to recording file (m4a, mp3, wav, mp4)"
    )
    parser.add_argument(
        "--slides", required=True,
        help="Path to slides PDF"
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Directory to write output files"
    )
    parser.add_argument(
        "--whisper-model", default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    parser.add_argument(
        "--annotated-slides", default=None,
        help="Path to annotated slides PDF (optional)"
    )
    parser.add_argument(
        "--notes", default=None,
        help="Path to typed notes file (optional)"
    )
    parser.add_argument(
        "--similarity-threshold", type=float, default=0.15,
        help="Minimum cosine similarity for slide assignment (default: 0.15)"
    )
    parser.add_argument(
        "--max-backtrack", type=int, default=3,
        help="Max slides to backtrack in alignment (default: 3)"
    )
    args = parser.parse_args()

    # Validate inputs
    recording_path = Path(args.recording)
    slides_path = Path(args.slides)
    output_dir = Path(args.output_dir)

    if not recording_path.exists():
        print(f"Error: Recording not found: {recording_path}")
        sys.exit(1)
    if not slides_path.exists():
        print(f"Error: Slides not found: {slides_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    check_dependencies()

    # Step 1: Transcribe
    print("\n[1/5] Transcribing recording...")
    segments = transcribe_recording(recording_path, args.whisper_model)

    # Step 2: Extract slide text
    print("\n[2/5] Extracting slide text...")
    slides = extract_slide_texts(slides_path)

    # Step 3: Compute similarity and align
    print("\n[3/5] Computing alignment...")
    similarity_matrix = compute_similarity_matrix(segments, slides)
    assignments = align_segments_to_slides(
        segments, slides, similarity_matrix,
        similarity_threshold=args.similarity_threshold,
        max_backtrack=args.max_backtrack,
    )

    # Step 4: Merge into slide blocks and analyze emphasis
    print("\n[4/5] Merging and analyzing emphasis...")
    blocks = merge_into_slide_blocks(segments, slides, assignments)
    emphasis = detect_emphasis(blocks)

    # Step 5: Generate outputs
    print("\n[5/5] Generating output files...")

    notes_text = load_notes(args.notes)
    recording_name = recording_path.name
    slides_name = slides_path.name

    # Main alignment file
    alignment_md = generate_slide_alignment_md(
        blocks, emphasis, recording_name, slides_name, len(slides), notes_text
    )
    alignment_path = output_dir / "slide-alignment.md"
    alignment_path.write_text(alignment_md, encoding="utf-8")
    print(f"  Saved: {alignment_path}")

    # Full transcript
    transcript_md = generate_transcript_md(segments, recording_name)
    transcript_path = output_dir / "transcript.md"
    transcript_path.write_text(transcript_md, encoding="utf-8")
    print(f"  Saved: {transcript_path}")

    # Enriched summary
    enriched_md = generate_enriched_summary_md(blocks, emphasis, slides, notes_text)
    enriched_path = output_dir / "enriched-summary.md"
    enriched_path.write_text(enriched_md, encoding="utf-8")
    print(f"  Saved: {enriched_path}")

    # Machine-readable JSON
    save_alignment_data(output_dir, blocks, assignments, emphasis)

    # Summary
    print("\n" + "=" * 60)
    print("ALIGNMENT COMPLETE")
    print("=" * 60)
    print(f"  Recording:  {recording_name}")
    print(f"  Slides:     {slides_name} ({len(slides)} slides)")
    print(f"  Segments:   {len(segments)} transcript segments")
    print(f"  Blocks:     {len(blocks)} slide blocks")
    print(f"  Duration:   {format_timestamp(segments[-1]['end'])}")
    print(f"\nOutputs:")
    print(f"  {alignment_path}     <- Main timestamped guide")
    print(f"  {transcript_path}        <- Full transcript")
    print(f"  {enriched_path}   <- Combined study document")
    print(f"  {output_dir / 'alignment-data.json'}  <- Machine-readable data")
    print("=" * 60)


if __name__ == "__main__":
    main()
