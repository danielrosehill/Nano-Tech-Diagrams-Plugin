---
name: restyle-diagram
description: Restyle an existing diagram, screenshot or Mermaid render with an image model, keeping every label and arrow exact (image-to-image).
---

# Restyle a diagram

Changes the look of a diagram that is already right, such as a Mermaid render or an old graphic.

## Steps

1. List every string and arrow in the source. For a Mermaid render, take them from the `.mmd` file rather than from the image.
2. Choose a style from `diagram-prompt-library`.
3. Write `<name>.prompt.txt` from `references/prompt-recipe.md`: "Restyle this diagram as ...", then the exact strings, the arrows, and "Do not add, remove, reword or move anything."
4. Run:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate.py" --image <source.png> [--model ALIAS] <name>.prompt.txt <name>.png
   ```
5. Run `verify-diagram`, comparing with the source. If it keeps failing, keep the source diagram and say so.

## Notes

The source image is uploaded to fal or Replicate.
