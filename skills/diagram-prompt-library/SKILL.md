---
name: diagram-prompt-library
description: Browse visual style presets and diagram-type templates for tech diagrams (blueprint, chalkboard, flowchart, K8s, network topology).
---

# Diagram prompt library

Style and diagram-type snippets to drop into a prompt built with `references/prompt-recipe.md`. Files are `.prompty`: YAML frontmatter, then the prompt text. `PROMPTS.md` explains the format.

- `styles/<category>/`: `professional`, `technical`, `creative`, `retro-fun`, `language`
- `diagram-types/<family>/`: `conceptual`, `data-viz`, `infrastructure`, `process`, `software`

## Steps

1. List files in the category that fits, filtered by the user's request. For a technical audience start with `professional` and `technical`.
2. Check the overlay first: a file in `<data dir>/styles/` with the same name replaces the built-in, and a new name adds a house style.
3. Use the body as part 2 (style) or part 3 (layout) of the recipe. Add the exact strings yourself: the templates don't carry them.

The data dir is `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/tech-comms-diagrams/`.

`diagram-types/data-viz/` covers the look of a chart only. Charts of real numbers should be plotted in code.
