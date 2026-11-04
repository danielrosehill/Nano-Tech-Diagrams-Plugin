# Verification checks

A generated diagram is unverified until every check below passes. One wrong label is worse than no diagram.

Open the image and read it word by word, not at a glance. Check against the spec (the quoted strings and layout from the prompt), not against what looks plausible.

| Check | Pass means |
|---|---|
| Text exact | Every required string is present and spelled exactly |
| Nothing invented | No extra words, sample content, stray letters or pseudo-text anywhere, including inside illustrations |
| Structure | Node count and order are right; each arrow is checked one at a time: start, end, direction |
| Legible | Readable at the display width (a blog column is about 700 px), with no warped or cramped lettering |
| Meaning | A reader takes away what the source text says: counts, names, versions and flows agree with it |

Spelling can be perfect while the meaning is wrong, for example a box whose number doesn't match the arrows flowing into it. Check the arithmetic and direction of any flow against the source.

## On a failure

1. Regenerate once with the same model, stating the fix: "the arrow from Clean goes down to Label speakers".
2. Move to the next model in `references/model-routing.md`.
3. After three misses, shorten the labels, cut nodes, or switch to Mermaid, and say so.

Never hand over an image that failed a check without saying which check it failed.

Report in this form:

```json
{"file": "out.png", "text_exact": true, "nothing_invented": false, "structure": true,
 "legible": true, "meaning": true, "errors": ["invented: 'Client' inside card 1"]}
```
