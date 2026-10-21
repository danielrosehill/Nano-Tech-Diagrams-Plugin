---
name: generate-tech-diagram
description: Use when the user wants to generate a tech diagram from a text description (network topology, architecture, flowchart, mind map, K8s cluster, etc.).
---

# Generate Tech Diagram

## Tool names (portable)

Tools are named here by their bare name on the `nano-tech-diagrams` MCP server (e.g. `text_to_image`). Resolve
the callable name once per session:

1. **Local override.** If `config.json` exists in this plugin's data directory
   (`$CLAUDE_USER_DATA/nano-tech-diagrams/`, else `$XDG_DATA_HOME/claude-plugins/nano-tech-diagrams/`, else
   `~/.local/share/claude-plugins/nano-tech-diagrams/`), call `<tool_prefix><name>`. If it also has a
   `tools` map, take `<name>` from it first. A name mapped to `null` has no equivalent on that
   setup: say so and use the fallback that `notes` gives.
2. **Otherwise,** use the loaded tool whose name ends in `nano-tech-diagrams__<name>`. A direct install
   is `mcp__nano-tech-diagrams__<name>`; a proxy or gateway adds its own prefix.
3. **Otherwise** the server isn't connected. Stop and point the user to: the README's "Install the MCP" section (`claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp`, plus `FAL_KEY`).


Generate a diagram from a text description using the Nano Banana 2 model. The MCP tool `text_to_image` accepts a description, optional diagram-type preset (network, flowchart, K8s, mind-map, etc.), and visual style preset (chalkboard, blueprint, pixel-art, neon-sign, corporate-clean, etc.).

## When to use

- User describes a diagram idea in words (e.g., "draw a 3-tier microservice architecture")
- User wants to visualize a system topology, flowchart, data pipeline, or conceptual model
- User wants to experiment with different visual styles for the same diagram

## Inputs to gather

- **Description** (required) — free-text description of what the diagram should show
- **Diagram type** (optional) — preset from `list-diagram-types` (e.g. `network`, `flowchart`, `kubernetes`, `mind-map`). If not provided, the model infers from description.
- **Style preset** (optional) — preset from `list-diagram-styles` (e.g. `blueprint`, `pixel-art`, `corporate-clean`). Default: `corporate-clean`. Offer to run `list-diagram-styles` if user is unsure.
- **Aspect ratio** (optional) — e.g. `16:9`, `1:1`, `4:3`. Default: `16:9`.
- **Output path** (optional) — where to save the PNG. Default: `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/diagrams/<slug>-<timestamp>.png`

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Call `list-diagram-types` silently to validate the diagram-type preset (if provided); skip if user is confident.
3. Call `text_to_image` with description, diagram_type, style, aspect_ratio.
4. The MCP returns a fal.media URL and base64 PNG data. Extract the base64.
5. Compute output path (use default if not specified), ensuring parent directories exist.
6. Write the base64 as PNG to disk.
7. Report the file path and the fal.media URL to the user.

## Output / side effects

- PNG saved to disk at the computed output path.
- User sees the local path and a fal.media URL (for preview/sharing).

## Safety / constraints

- Never dump raw base64 into the chat — always write to disk first.
- If the MCP call fails, offer to retry with a simpler description or suggest `list-diagram-styles` to pick a more stable style preset.
