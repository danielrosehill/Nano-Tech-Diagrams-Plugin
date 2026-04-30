---
name: diagram-prompt-library
description: Use when the user wants a curated, known-good prompt template to start from, organised by diagram family and style category.
---

# Diagram Prompt Library

Browse a curated library of diagram prompt templates organized by diagram family (conceptual, data-viz, infrastructure, process, software) and style category (creative, language, professional, retro-fun, technical). Prompts are vendored from `danielrosehill/Tech-Diagram-Image-Gen-Prompts` and live under `${plugin_root}/skills/diagram-prompt-library/prompts/`.

## When to use

- User wants a starting template instead of writing a description from scratch
- User wants to see example diagram descriptions organized by use case
- User is exploring what types of diagrams are possible

## Inputs to gather

- **Diagram family** (optional) — e.g. `conceptual`, `data-viz`, `infrastructure`, `process`, or `software`
- **Style category** (optional) — e.g. `creative`, `language`, `professional`, `retro-fun`, or `technical`
- User may ask for all prompts, or filter by family, style, or both

## Procedure

1. If the prompt files are not present under `${plugin_root}/skills/diagram-prompt-library/prompts/`, explain to the user that this skill requires the prompt library to be vendored first and suggest cloning from the source repo.
2. List available prompt files, optionally filtered by the user's family/style preferences.
3. Display the selected prompt(s) as formatted text with headers showing family, style, and a brief title.
4. Encourage the user to customize the prompt or use it as-is, then hand off to `generate-tech-diagram` with the description.

## Output / side effects

- User sees formatted prompt text(s) in the chat.
- No files created or modified.

## Safety / constraints

- This is a reference/curation skill — no MCP calls, no image generation.
- If prompts are missing, provide a clear message about manual setup rather than trying to fetch from the remote.
