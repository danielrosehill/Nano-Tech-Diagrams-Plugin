---
name: mermaid-diagram
description: Write and render a Mermaid diagram (flowchart, sequence, ER, state, C4) to SVG or PNG for a tech blog, README or documentation.
---

# Mermaid diagram

## Inputs

- What the diagram explains: prose, code, or a list of steps
- Destination: GitHub Markdown renders a fenced `mermaid` block natively, so keep it as source there; blogs and slides need a file
- Format: `svg` by default, `png` for platforms that reject SVG

## Steps

1. Pick the diagram type for the job: `flowchart` for processes, `sequenceDiagram` for calls between systems, `erDiagram` for schemas, `stateDiagram-v2` for lifecycles.
2. Write `<name>.mmd`. Quote any label containing punctuation: `A["Clean (v2)"]`. Keep to about 12 nodes; split larger diagrams in two.
3. Render:
   ```bash
   "${CLAUDE_PLUGIN_ROOT}/scripts/render-mermaid.sh" <name>.mmd <name>.svg --theme neutral
   ```
   A non-zero exit means a syntax error. Fix the source from the message.
4. Open a PNG render and check the layout: crossing edges, clipped labels, text too small at display width. Change the direction (`LR` or `TD`) or split the diagram if needed.
5. Keep the `.mmd` beside the output so it can be edited later.
6. If the user wants a designed look, hand the PNG to `image-to-image`.

## Notes

The first run downloads `@mermaid-js/mermaid-cli` through `npx` unless `mmdc` is installed. It needs Node and runs locally: nothing leaves the machine.
