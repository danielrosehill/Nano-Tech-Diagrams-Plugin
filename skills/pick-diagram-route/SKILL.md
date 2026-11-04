---
name: pick-diagram-route
description: Choose Mermaid, a generative image model, or both for a tech diagram in a blog post, README or doc. Use on "what kind of diagram".
---

# Pick a diagram route

Decide how to make a technical graphic before making it. State the choice in one line and carry on; ask only if the user's goal is unclear.

| The graphic needs | Route | Skill |
|---|---|---|
| Accuracy above all, many nodes, or edits in version control | Mermaid | `mermaid-diagram` |
| Docs or a README where the source should stay editable | Mermaid | `mermaid-diagram` |
| Colour, style or personality, 8 nodes or fewer, short labels | Generative | `generate-diagram` |
| A hand-drawn whiteboard or notepad sketch as the input | Image to image | `image-to-image` |
| An existing diagram or screenshot that needs a new look | Image to image | `image-to-image` |
| Correct structure and a designed look | Mermaid first, then restyle | `mermaid-diagram`, then `image-to-image` |
| Prose that needs a graphic, type not yet known | Start from the text | `illustrate-text` |
| Charts of real numbers | Neither: plot the data in code | none |

Never send real data to an image model to draw as a chart: bar lengths and values can't be trusted.

Non-Latin text, Hebrew especially, goes to Mermaid unless the user accepts the risk: most image models fail at right-to-left text.
