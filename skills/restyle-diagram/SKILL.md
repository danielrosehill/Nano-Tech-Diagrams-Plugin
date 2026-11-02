---
name: restyle-diagram
description: Use when the user has an existing diagram or screenshot and wants to transform it into a different visual style or polish the rendering.
---

# Restyle Diagram

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


Transform an existing diagram, screenshot, or sketch into a new visual style. The MCP tool `image_to_image` accepts a source image, target style (preset or free-text brief), and optional preservation directives.

## When to use

- User has a diagram created elsewhere and wants to apply a new visual style
- User wants to polish a screenshot or rough sketch into a polished diagram
- User wants to experiment with multiple styles on the same diagram
- User needs to preserve specific labels or topology while changing the look

## Inputs to gather

- **Source image path** (required) — absolute path to the image file to transform
- **Target style** (optional) — preset from `list-diagram-styles` (e.g. `blueprint`, `pixel-art`, `neon-sign`) OR free-text style brief (e.g. "clean, minimalist, flat design"). Default: `corporate-clean`. Offer to run `list-diagram-styles` if unsure.
- **Preservation directives** (optional) — free-text notes like "keep all labels" or "preserve network topology" to guide the transformation
- **Output path** (optional) — where to save the result. Default: `${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/nano-tech-diagrams/diagrams/<slug>-<timestamp>.png`

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Validate that the source image path is readable; fail with a clear message if not found.
3. Call `image_to_image` with source_image (base64 or URL), target_style, preservation_directives.
   Local file but the tool needs a URL? Stage it with `cloud-storage:stage-file` (`stage.sh <file>` → presigned URL; delete after). Don't improvise another route. (Gateway tools can't read laptop paths; large base64 fails.)
4. Extract the base64 PNG from the response.
5. Compute output path (use default if not specified), ensuring parent directories exist.
6. Write the base64 as PNG to disk.
7. Report the file path and fal.media URL.

## Output / side effects

- Transformed PNG saved to disk.
- User sees local path and fal.media URL.

## Safety / constraints

- Never dump raw base64 into the chat — always write to disk first.
- If preservation directives are vague, offer to refine them before retrying.
