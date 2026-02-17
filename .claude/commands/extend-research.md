# /extend-research Command

## Purpose
Expand an existing research project with new questions, sources, or focused investigation.

## Usage
```
/extend-research {project-slug}
/extend-research {project-slug} --add-sources
/extend-research {project-slug} --add-questions
/extend-research {project-slug} --focus "specific subtopic"
```

## Modes

### Default (Interactive)
1. Read `project.yaml` and `analysis/latest.md`
2. Present current state to user
3. Ask what to expand: new questions, new sources, or deeper dive on existing questions
4. Execute chosen expansion
5. Re-run analysis and update report

### --add-sources
1. Read existing `sources/manifest.yaml`
2. Suggest new sources based on gaps in current factbase
3. User can also provide new local documents (place in `sources/local/`)
4. Extract facts from new sources only
5. Re-run analysis with full factbase (old + new facts)

### --add-questions
1. Read existing `questions/initial.md`
2. Propose additional questions based on analysis gaps
3. User approves/modifies
4. Append to questions file
5. Research new questions using existing + new sources
6. Re-run analysis

### --focus "subtopic"
1. Generate focused sub-questions on the subtopic
2. Search for sources specific to this subtopic
3. Extract facts
4. Run analysis specifically on this subtopic
5. Save as separate analysis run: `analysis/runs/{date}-focus-{subtopic}.md`

## Re-analysis Rules
- After any extension, always re-run analysis with the FULL factbase
- New analysis runs get new timestamps
- Update `analysis/latest.md` symlink
- Optionally regenerate report if user wants

## Integration with Course Materials
When extending research for course-related projects:
- Check if new lecture materials have been added since last research run
- Scan `course-materials/lectures/` for relevant new content
- Prompt user: "New lecture materials found in week-XX. Include in research?"