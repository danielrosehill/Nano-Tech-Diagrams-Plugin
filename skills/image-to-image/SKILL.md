---
name: image-to-image
description: Transform an image into a tech diagram: clean up a whiteboard or notepad sketch, restyle a diagram or Mermaid render, or convert to Mermaid.
---

# Image to image

The main risk is transposition: labels dropped, invented, reworded or wrongly "corrected". So the labels are written down first and the model is told exactly what to write.

## Inputs

- The source: a whiteboard or notepad photo, an existing diagram, a screenshot, or a Mermaid render
- Transformation (below)
- Terms handwriting might garble: product names, acronyms

## Transformations

| Ask | How |
|---|---|
| Clean it up | White background, straight-on view, neat sans-serif, flat colour |
| Keep my handwriting | Same, but "keep the handwriting style, neater and easy to read" |
| Give it a look | Style preset: chalkboard, blueprint, sticky notes, neon, comic |
| Restyle a finished diagram | "Restyle this diagram as ... Do not add, remove, reword or move anything." |
| Make it editable | No image model: write the transcription as Mermaid and use `mermaid-diagram` |
| Translate labels | Transcribe, translate, then pass the translated strings as the exact text |
| Fix or extend it | Apply the change to the transcription, and state it in the prompt |

## Steps

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" status`. If `ready` is false, run `setup-backend`. If `preferences_file` is set, read it: it overrides this skill's defaults.
2. Write down every string, each one's role (title, node, edge label, note) and every arrow as `from -> to`. For a Mermaid render, take them from the `.mmd` file. For a photo, read it closely.
3. For handwriting, show the transcription to the user and ask them to confirm any unclear word. Skip this only if the user said not to check. Don't guess at a name.
4. Write `<name>.prompt.txt` using `references/prompt-recipe.md`. For a photo, state what to remove (frame, pen tray, glare, wall, page edges). Mark titles and notes as plain text, not nodes.
5. Run:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate.py" --image <source> [--model ALIAS] [--provider NAME] [--aspect 4:3] <name>.prompt.txt <name>.png
   ```
   Staging, if configured, happens here without any extra step.
6. Run `verify-diagram` with the transcription as the spec, and compare with the source: nothing dropped.
7. Report the path, the model, and any label you changed and why.

## Notes

The image leaves the machine unless the backend is local. Tell the user first if a board may hold anything private. Omitting `--aspect` lets the provider choose; sizes vary.
