---
name: cleanup-whiteboard
description: Use when the user has a photo of a whiteboard, paper sketch, or napkin diagram and wants a clean, publishable version.
---

# Cleanup Whiteboard

## Tool names (portable)

Tools are named here by their bare name on the `nano-tech-diagrams` MCP server (e.g. `text_to_image`). Resolve
the callable name once per session:

1. **Local override.** If `config.json` exists in this plugin's data directory
   (`$CLAUDE_USER_DATA/nano-tech-diagrams/`, else `$XDG_DATA_HOME/claude-plugins/nano-tech-diagrams/`, else
   `~/.local/share/claude-plugins/nano-tech-diagrams/`), call `<tool_prefix><name>`. If it also has a
   `tools` map, take `<name>` from it first. A name mapped to `null` has no equivalent on that
   setup: say so and use the fallback that `notes` gives.
2. **Otherwise,** use the loaded tool whose name ends in `nano-tech-diagrams__<name>`. A direct install
   is `mcp__nano-tech-diagrams__<name>`; a proxy or gateway adds its own prefix.
3. **Otherwise** the server isn't connected. Stop and point the user to: the README's "Install the MCP" section (`claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp`, plus `FAL_KEY`).


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
3. Call `whiteboard_cleanup` with source_image, target_style, generate_comparison.
   Local file but the tool needs a URL? Stage it with `cloud-storage:stage-file` (`stage.sh <file>` → presigned URL; delete after). Don't improvise another route. (Gateway tools can't read laptop paths; large base64 fails.)
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
