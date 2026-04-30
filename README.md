# Nano-Tech-Diagrams Plugin

Generate, transform, and clean up tech diagrams and whiteboard photos via Fal AI's Nano Banana 2 model. Wraps the `nano-tech-diagrams` MCP server with seven skills and a curated prompt library across 5 diagram families and 28+ visual styles.

## Skills

- `generate-tech-diagram` — text-to-image diagram generation (network, flowchart, K8s, mind map, etc.)
- `restyle-diagram` — transform an existing image into a different visual style
- `cleanup-whiteboard` — turn whiteboard / sketch photos into polished diagrams
- `list-diagram-styles` — browse the 28+ visual style presets
- `list-diagram-types` — browse the diagram-type presets
- `diagram-prompt-library` — curated, known-good prompt templates by family and style
- `whiteboard-to-publishable` — full pipeline: photo → cleaned diagram → comparison + caption

## Requirements

This plugin is a wrapper. The actual generation runs through the `nano-tech-diagrams` MCP server, which must be installed and configured with a Fal AI API key.

### 1. Install the MCP

```bash
claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp
```

Or pin via npm globally and reference the binary directly. See [nano-tech-diagrams-mcp on GitHub](https://github.com/danielrosehill/Nano-Tech-Diagrams-MCP).

### 2. Set the Fal AI API key

Export `FAL_KEY` (or `FAL_AI_API_KEY`) in the environment Claude Code launches the MCP from.

### 3. (Optional) Install the `image-annotation` plugin

The `whiteboard-to-publishable` orchestrator can optionally use it for side-by-side comparison images and redaction. Without it, the orchestrator degrades gracefully.

## Installation

```bash
# User scope (always available):
claude plugins install nano-tech-diagrams@danielrosehill

# Or project scope (run inside the target repo):
claude plugins install nano-tech-diagrams@danielrosehill --scope project
```

## Data storage

Generated images and projects default to:

```
${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/
```

You can always pass an explicit output path to any generation skill.

## Credits

- Generation engine: [Nano-Tech-Diagrams-MCP](https://github.com/danielrosehill/Nano-Tech-Diagrams-MCP)
- Prompt library substrate: [Tech-Diagram-Image-Gen-Prompts](https://github.com/danielrosehill/Tech-Diagram-Image-Gen-Prompts) (vendored snapshot)
- Sample corpus: [Sample-Whiteboards](https://github.com/danielrosehill/Sample-Whiteboards)
- Underlying model: Fal AI's [Nano Banana 2](https://fal.ai/models/fal-ai/nano-banana-2)

## License

MIT
