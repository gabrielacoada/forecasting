#!/usr/bin/env bash
#
# export-notes-pdf.sh — Convert lecture markdown notes to PDF with Mermaid diagrams
#
# Usage:
#   ./scripts/export-notes-pdf.sh                    # Export all lecture notes
#   ./scripts/export-notes-pdf.sh week-03            # Export a specific week
#   ./scripts/export-notes-pdf.sh week-04 summary    # Export a specific file (summary or key-concepts)
#
# Output goes to course-materials/lectures/<week>/pdf/
#
# Requirements: Node.js (npx will auto-install md-to-pdf and @mermaid-js/mermaid-cli on first run)
#
# How it works:
#   1. Extracts ```mermaid code blocks from markdown
#   2. Renders each diagram to PNG using mermaid-cli (mmdc)
#   3. Embeds diagrams as base64 inline images in a processed markdown
#   4. Converts to PDF using md-to-pdf (Puppeteer/Chromium)
#   5. Cleans up temporary files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LECTURES_DIR="$REPO_ROOT/course-materials/lectures"

# md-to-pdf stylesheet for clean academic output
CSS='
body {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 12px;
  line-height: 1.6;
  max-width: 100%;
  color: #1a1a1a;
}
h1 { font-size: 22px; border-bottom: 2px solid #333; padding-bottom: 6px; margin-top: 30px; }
h2 { font-size: 18px; border-bottom: 1px solid #999; padding-bottom: 4px; margin-top: 24px; }
h3 { font-size: 15px; margin-top: 18px; }
h4 { font-size: 13px; margin-top: 14px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 11px; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background-color: #f5f5f5; font-weight: bold; }
code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-size: 11px; }
pre { background: #f8f8f8; padding: 12px; border-radius: 4px; overflow-x: auto; }
blockquote { border-left: 3px solid #666; padding-left: 12px; color: #555; margin: 12px 0; }
strong { color: #000; }
img { max-width: 100%; height: auto; display: block; margin: 12px auto; }
'

# Mermaid rendering config
MMDC_CONFIG='{
  "theme": "default",
  "themeVariables": {
    "fontSize": "14px"
  }
}'

preprocess_mermaid() {
  local md_file="$1"
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  local processed="$tmp_dir/processed.md"
  local diagram_idx=0
  local in_mermaid=0
  local mermaid_buf=""

  # Write mmdc config once
  echo "$MMDC_CONFIG" > "$tmp_dir/mmdc-config.json"

  while IFS= read -r line || [ -n "$line" ]; do
    if [ "$in_mermaid" -eq 0 ]; then
      if echo "$line" | grep -qE '^\s*```mermaid\s*$'; then
        in_mermaid=1
        mermaid_buf=""
      else
        echo "$line" >> "$processed"
      fi
    else
      if echo "$line" | grep -qE '^\s*```\s*$'; then
        in_mermaid=0
        diagram_idx=$((diagram_idx + 1))
        local mmd_file="$tmp_dir/diagram_${diagram_idx}.mmd"
        local png_file="$tmp_dir/diagram_${diagram_idx}.png"

        echo "$mermaid_buf" > "$mmd_file"

        if npx --yes @mermaid-js/mermaid-cli \
            -i "$mmd_file" \
            -o "$png_file" \
            -c "$tmp_dir/mmdc-config.json" \
            -w 800 \
            -b white \
            -q 2>/dev/null; then
          # Base64 encode and embed inline
          local b64
          b64="$(base64 -w 0 "$png_file")"
          echo "![diagram](data:image/png;base64,${b64})" >> "$processed"
        else
          echo '```' >> "$processed"
          echo "$mermaid_buf" >> "$processed"
          echo '```' >> "$processed"
          echo "    Warning: Failed to render diagram $diagram_idx" >&2
        fi
      else
        if [ -z "$mermaid_buf" ]; then
          mermaid_buf="$line"
        else
          mermaid_buf="$mermaid_buf
$line"
        fi
      fi
    fi
  done < "$md_file"

  echo "$tmp_dir"
}

export_file() {
  local md_file="$1"
  local week_dir
  week_dir="$(dirname "$md_file")"
  local pdf_dir="$week_dir/pdf"
  local basename
  basename="$(basename "$md_file" .md)"
  local pdf_file="$pdf_dir/${basename}.pdf"

  mkdir -p "$pdf_dir"

  echo "  Converting: $(basename "$week_dir")/$basename.md → pdf/$basename.pdf"

  # Step 1: Pre-render mermaid diagrams
  echo "    Rendering Mermaid diagrams..."
  local tmp_dir
  tmp_dir="$(preprocess_mermaid "$md_file")"
  local processed_md="$tmp_dir/processed.md"

  # Step 2: Convert processed markdown to PDF
  echo "    Generating PDF..."
  local css_file="$tmp_dir/style.css"
  echo "$CSS" > "$css_file"

  npx --yes md-to-pdf \
    --stylesheet "$css_file" \
    --pdf-options '{"format":"Letter","margin":{"top":"0.75in","bottom":"0.75in","left":"0.75in","right":"0.75in"}}' \
    "$processed_md" 2>/dev/null

  local default_output="$tmp_dir/processed.pdf"
  if [ -f "$default_output" ]; then
    mv "$default_output" "$pdf_file"
  fi

  # Cleanup
  rm -rf "$tmp_dir"

  if [ -f "$pdf_file" ]; then
    local size
    size="$(du -h "$pdf_file" | cut -f1)"
    echo "  ✓ Created: pdf/$basename.pdf ($size)"
  else
    echo "  ✗ Failed: $pdf_file" >&2
    return 1
  fi
}

export_week() {
  local week="$1"
  local file_filter="${2:-}"
  local week_dir="$LECTURES_DIR/$week"

  if [ ! -d "$week_dir" ]; then
    echo "Error: Directory not found: $week_dir" >&2
    exit 1
  fi

  echo "Exporting $week..."

  local found=0
  for md_file in "$week_dir"/*.md; do
    [ -f "$md_file" ] || continue

    local basename
    basename="$(basename "$md_file" .md)"

    if [ -n "$file_filter" ] && [ "$basename" != "$file_filter" ]; then
      continue
    fi

    export_file "$md_file"
    found=1
  done

  if [ "$found" -eq 0 ]; then
    if [ -n "$file_filter" ]; then
      echo "  No file matching '$file_filter.md' found in $week"
    else
      echo "  No .md files found in $week"
    fi
  fi
}

main() {
  local week_filter="${1:-}"
  local file_filter="${2:-}"

  echo "=== Lecture Notes PDF Export ==="
  echo ""

  if ! command -v npx &>/dev/null; then
    echo "Error: npx not found. Install Node.js first." >&2
    exit 1
  fi

  if [ -n "$week_filter" ]; then
    export_week "$week_filter" "$file_filter"
  else
    for week_dir in "$LECTURES_DIR"/week-*/; do
      [ -d "$week_dir" ] || continue
      local week
      week="$(basename "$week_dir")"

      if ls "$week_dir"/*.md &>/dev/null 2>&1; then
        export_week "$week" ""
      fi
    done
  fi

  echo ""
  echo "=== Done ==="
}

main "$@"
