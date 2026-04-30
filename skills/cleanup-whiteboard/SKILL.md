---
name: cleanup-whiteboard
description: Use when the user has a photo of a whiteboard, paper sketch, or napkin diagram and wants a clean, publishable version.
---

# Cleanup Whiteboard

Transform a messy whiteboard photo, paper sketch, or napkin diagram into a clean, polished diagram. The MCP tool `whiteboard_cleanup` extracts the content, vectorizes, and applies a visual style.

## When to use

- User has a photo of a whiteboard drawing and needs a clean version
- User has a paper sketch or napkin diagram to digitize
- User wants a publishable diagram from a quick hand-drawn rough sketch
- User wants side-by-side before/after comparison

## Inputs to gather

- **Source photo path** (required) — absolute path to the whiteboard/paper photo
- **Target style preset** (optional) — preset from `list-diagram-styles`. Default: `corporate-clean`. Offer to run `list-diagram-styles` if unsure.
- **Output path** (optional) — where to save cleaned diagram. Default: `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/diagrams/<slug>-cleaned-<timestamp>.png`
- **Side-by-side comparison** (optional) — boolean flag. If true, also generate a comparison image with original and cleaned versions side-by-side.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Validate that the source photo path is readable; fail with a clear message if not found.
3. Call `mcp__nano-tech-diagrams__whiteboard_cleanup` with source_image, target_style, generate_comparison.
4. Extract base64 PNG(s) from the response.
5. Compute output path(s), ensuring parent directories exist.
6. Write cleaned diagram to disk.
7. If comparison was requested, write comparison image to disk (e.g., `<slug>-comparison-<timestamp>.png`).
8. Report file paths and fal.media URLs.

## Output / side effects

- Cleaned PNG saved to disk.
- Optional comparison image saved if requested.
- User sees local paths and fal.media URLs.

## Safety / constraints

- Never dump raw base64 into the chat — always write to disk first.
- If the cleanup produces poor results, suggest retrying with a different style preset.
