---
name: verify-diagram
description: Check a generated diagram word by word: exact label text, invented text, arrow direction, legibility and meaning against its spec.
---

# Verify a diagram

## Inputs

- The image
- The spec: the prompt, or the transcription for a sketch
- The source text or original image, if there is one
- Display width, 700 px if unknown

## Steps

1. Read `references/verification.md` in the plugin root.
2. Open the image and run every check.
3. Report the JSON block from that file.
4. On a failure, follow its retry ladder. Regeneration costs money, so stop after three misses.

## Notes

This is a model reading an image. For anything high stakes, ask the user to look too.
