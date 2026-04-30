---
name: whiteboard-to-publishable
description: Use when the user wants the full pipeline: take a whiteboard photo, pick a style, clean it up, and save the result as a publishable diagram with optional comparison.
---

# Whiteboard to Publishable

End-to-end orchestration skill that transforms a whiteboard photo into a polished, publishable diagram. Optionally generates a side-by-side comparison and drafts a one-line caption.

## When to use

- User has a whiteboard photo and wants a finished, production-ready diagram
- User wants to document a quick whiteboard session with a polished output
- User wants side-by-side before/after comparison for context
- User wants the full workflow in one invocation

## Inputs to gather

- **Source photo path** (required) — absolute path to whiteboard/paper photo
- **Project name** (optional) — used to scaffold output as `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/projects/<name>/`. If not provided, uses default `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/diagrams/`.
- **Style preset** (optional) — preset from `list-diagram-styles`. Default: `corporate-clean`. Offer to run `list-diagram-styles` if unsure.
- **Generate comparison** (optional) — boolean flag to also produce side-by-side before/after. Default: `false`.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Invoke `cleanup-whiteboard` with the source photo, style preset, and comparison flag.
3. Collect the cleaned diagram path and (if enabled) comparison image path from the `cleanup-whiteboard` output.
4. Draft a one-line caption based on the visible content in the cleaned diagram (e.g., "Architecture diagram showing 3-tier microservice topology with API gateway, business logic, and database layers").
5. If a project name was provided, move/organize files under `projects/<name>/` and create a simple index or metadata file.
6. Report final file paths, fal.media URLs, and the drafted caption to the user.

## Output / side effects

- Cleaned diagram PNG saved to disk.
- Optional comparison image saved if requested.
- Drafted one-line caption provided in the chat.
- Optionally organized under `projects/<name>/` if project name was provided.

## Safety / constraints

- Never dump raw base64 into the chat — always write to disk first.
- The caption is a draft suggestion; user may refine it.
- If cleanup produces poor results, fall back to the `cleanup-whiteboard` skill's troubleshooting suggestions.
