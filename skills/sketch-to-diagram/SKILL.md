---
name: sketch-to-diagram
description: Turn a whiteboard photo or notepad sketch into a clean publishable diagram, restyled, kept handwritten, or converted to Mermaid.
---

# Sketch to diagram (image to image)

The main risk is transposition: labels dropped, invented, reworded or wrongly "corrected". So the labels are transcribed first and the model is told exactly what to write.

## Inputs

- Photo of the whiteboard or notepad page
- Transformation (below)
- Terms the handwriting might garble: product names, acronyms

## Transformations

| Ask | How |
|---|---|
| Clean it up | White background, straight-on view, neat sans-serif, flat colour |
| Keep my handwriting | Same, but "keep the handwriting style, neater and easy to read" |
| Give it a look | Style preset: chalkboard, blueprint, sticky notes, neon, comic |
| Make it editable | No image model: write the transcription as Mermaid and use `mermaid-diagram` |
| Translate labels | Transcribe, translate, then pass the translated strings as the exact text |
| Fix or extend it | Apply the change to the transcription, and state it in the prompt |

## Steps

1. Open the photo and transcribe it: every string, each one's role (title, node, edge label, note), and every arrow as `from -> to`.
2. Show the transcription to the user and ask them to confirm any word the handwriting left unclear. Skip this only if the user said not to check. Don't guess at a name.
3. Write `<name>.prompt.txt` using `references/prompt-recipe.md`. State what to remove (frame, pen tray, glare, wall, page edges), and mark titles and notes as plain text, not nodes.
4. Run with the photo as input:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate.py" --image <photo> [--model ALIAS] [--aspect 4:3] <name>.prompt.txt <name>.png
   ```
5. Run `verify-diagram` with the transcription as the spec. Also compare with the photo: nothing dropped.
6. Report the path, the model, and any label you changed and why.

## Notes

The photo is uploaded to fal or Replicate. Tell the user first if the board may hold anything private. Omitting `--aspect` lets the provider choose; sizes vary.
