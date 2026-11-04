# Tech Comms Diagrams

Agent skills for making technical diagrams for blog posts, READMEs and documentation.

General image tools optimise for good-looking pictures. A technical diagram has a harder requirement: one misspelt label or backwards arrow makes it wrong. So this plugin only uses models tested for exact text and correct arrows, and checks every result against what was asked for.

## Skills

| Skill | Job |
|---|---|
| `pick-diagram-route` | Choose Mermaid, a generative model, or both |
| `mermaid-diagram` | Write and render Mermaid to SVG or PNG |
| `generate-diagram` | Text to image, with exact labels |
| `image-to-image` | Whiteboard or notepad photo to clean diagram, new look for an existing diagram, or conversion to Mermaid |
| `verify-diagram` | Check labels, invented text, arrows, legibility and meaning |
| `illustrate-text` | Find where a text needs graphics, then make and place them with alt text |
| `diagram-prompt-library` | 28 style presets and 33 diagram-type templates |
| `setup-backend` | API keys, provider choice, ComfyUI, custom routes and image staging |

## How it keeps text accurate

1. **Labels are written down first.** Every string goes in the prompt in quotes. For a sketch, the agent transcribes the photo before any image model runs.
2. **Only tested models are used.** See [`references/model-routing.md`](references/model-routing.md) for the results and how much evidence is behind them.
3. **Every image is read back,** word by word and arrow by arrow, with a retry ladder that ends at Mermaid.

## Backends

| Backend | Set up with |
|---|---|
| fal (default) | `FAL_KEY` |
| Replicate | `REPLICATE_API_TOKEN` |
| ComfyUI, local or on a server | Its URL and your workflows |
| Your own route | Any command that writes an image: a gateway, an internal API |

If your generation runs somewhere that can't read your files, such as a central AI gateway, an optional staging step moves input images to storage you choose first and passes a URL.

The `setup-backend` skill walks through all of this. Keys come from the environment, or from a local file saved without the key entering the conversation.

## Requirements

- Python 3 (standard library only)
- Node, for Mermaid (`mmdc`, or `npx` fetches it)
- One backend above for image generation. Mermaid needs none.

## Installation

```bash
claude plugins install tech-comms-diagrams@danielrosehill
```

## Customising

Your settings live in a data directory outside the plugin, so updates never overwrite them: `~/.claude-user-data/tech-comms-diagrams/` if that root exists, otherwise `${CLAUDE_USER_DATA}` or `${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins/tech-comms-diagrams/`. `TECH_COMMS_DIAGRAMS_DATA` overrides the path.

It holds the provider choice, custom routes and staging (`config.json`), model aliases (`models.json`), house styles (`styles/`), ComfyUI workflows (`workflows/`), and free-text instructions the skills follow (`PREFERENCES.md`). Details: [`references/backends.md`](references/backends.md).

## History

Formerly `nano-tech-diagrams` (Nano-Tech-Diagrams-Plugin), renamed and overhauled in version 2.0.0 on 2026-11-04. It wrapped one model through an MCP server. This version calls its backends directly, adds Mermaid and verification, and needs no MCP server.

## Related

- [Tech-Graphics-Benchmark](https://github.com/danielrosehill/Tech-Graphics-Benchmark): the evaluation behind the model choices
- [Tech-Diagram-Image-Gen-Prompts](https://github.com/danielrosehill/Tech-Diagram-Image-Gen-Prompts): source of the prompt library
- [Sample-Whiteboards](https://github.com/danielrosehill/Sample-Whiteboards): sample inputs

## License

MIT
