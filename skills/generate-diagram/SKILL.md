---
name: generate-diagram
description: Generate a tech diagram or infographic from a text description with an image model that renders exact labels and arrows (text-to-image).
---

# Generate a diagram (text to image)

## Inputs

- What it must explain, and the exact labels
- Style: a preset from `diagram-prompt-library`, or the user's house style
- Aspect ratio: 16:9 by default
- Output path

## Steps

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" status`. If `ready` is false, run `setup-backend`. If `preferences_file` is set, read it: it overrides this skill's defaults.
2. Read `references/prompt-recipe.md` in the plugin root and write `<name>.prompt.txt` following all six parts.
3. Choose the model from `references/model-routing.md`, or omit `--model` for the default.
4. Generate:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate.py" [--model ALIAS] [--provider NAME] [--aspect 16:9] <name>.prompt.txt <name>.png
   ```
   This writes `<name>.png` and `<name>.png.json` (model, request, list price). Keep both, plus the prompt.
5. Run `verify-diagram`. Do not skip this: a clean-looking image can carry invented text.
6. Report the path, model and list price.

## Notes

Sends the prompt to the configured backend. Hosted calls cost money, usually cents; use `--dry-run` to see the request and price first.
