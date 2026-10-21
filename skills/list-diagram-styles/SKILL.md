---
name: list-diagram-styles
description: Use when the user wants to see available visual style presets (chalkboard, blueprint, pixel-art, neon-sign, etc.) before generating or transforming a diagram.
---

# List Diagram Styles

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


Display all available visual style presets for diagrams. Styles determine the look and feel of generated diagrams (e.g., chalkboard, blueprint, pixel-art, neon-sign, corporate-clean, retro-fun, technical, etc.).

## When to use

- User is unsure which style to pick before generating a diagram
- User wants to explore the available style options
- User is about to call `generate-tech-diagram` or `restyle-diagram` and wants to see choices first

## Inputs to gather

None — this is a read-only reference skill.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Call `list_styles` at runtime to fetch the current list.
3. Parse the response. If the MCP returns categories (e.g., "creative", "professional", "retro-fun", "technical"), format the output as a categorised table or markdown list.
4. Include 1–2 word descriptions or example use cases for each style if available from the MCP.
5. Display the list to the user.

## Output / side effects

- User sees a formatted list of available styles.
- No files created or modified.

## Safety / constraints

- Never hard-code the style list — always call the MCP to ensure the list is current.
- If the MCP is unavailable, provide a graceful error and the installation command.
