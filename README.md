# Tech Comms Diagrams

Agent skills for making technical diagrams for blog posts, READMEs and documentation.

General image tools optimise for good-looking pictures. A technical diagram has a harder requirement: one misspelt label or backwards arrow makes it wrong. So this plugin only uses models tested for exact text and correct arrows, and checks every result against what was asked for.

## Skills

| Skill | Job |
|---|---|
| `pick-diagram-route` | Choose Mermaid, a generative model, or both |
| `mermaid-diagram` | Write and render Mermaid to SVG or PNG |
| `generate-diagram` | Text to image, with exact labels |
| `sketch-to-diagram` | Whiteboard or notepad photo to clean diagram, restyled image, or Mermaid |
| `restyle-diagram` | New look for an existing diagram or Mermaid render |
| `verify-diagram` | Check labels, invented text, arrows, legibility and meaning |
| `illustrate-text` | Find where a text needs graphics, then make and place them with alt text |
| `diagram-prompt-library` | 28 style presets and 33 diagram-type templates |

## How it keeps text accurate

1. **Labels are written down first.** Every string goes in the prompt in quotes. For a sketch, the agent transcribes the photo before any image model runs.
2. **Only tested models are used.** See [`references/model-routing.md`](references/model-routing.md) for the results and how much evidence is behind them.
3. **Every image is read back,** word by word and arrow by arrow, with a retry ladder that ends at Mermaid.

## Requirements

- Python 3 (standard library only)
- Node, for Mermaid (`mmdc`, or `npx` fetches it)
- `FAL_KEY` and/or `REPLICATE_API_TOKEN` for generation. Mermaid needs neither.

## Installation

```bash
claude plugins install tech-comms-diagrams@danielrosehill
```

## Customising

Your own settings go in the data directory, `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/tech-comms-diagrams/`. `TECH_COMMS_DIAGRAMS_DATA` overrides that path.

- `models.json`: add or override model aliases, defaults and provider order
- `styles/<name>.prompty`: add a house style, or replace a built-in of the same name

Built-ins are read from the plugin, so they keep getting updates.

## History

Formerly `nano-tech-diagrams` (Nano-Tech-Diagrams-Plugin), renamed and overhauled in version 2.0.0 on 2026-11-04. It wrapped one model through an MCP server. This version calls fal and Replicate directly, adds Mermaid and verification, and no longer needs the MCP server.

## Related

- [Tech-Graphics-Benchmark](https://github.com/danielrosehill/Tech-Graphics-Benchmark): the evaluation behind the model choices
- [Tech-Diagram-Image-Gen-Prompts](https://github.com/danielrosehill/Tech-Diagram-Image-Gen-Prompts): source of the prompt library
- [Sample-Whiteboards](https://github.com/danielrosehill/Sample-Whiteboards): sample inputs

## License

MIT
