---
name: list-diagram-styles
description: Use when the user wants to see available visual style presets (chalkboard, blueprint, pixel-art, neon-sign, etc.) before generating or transforming a diagram.
---

# List Diagram Styles

Display all available visual style presets for diagrams. Styles determine the look and feel of generated diagrams (e.g., chalkboard, blueprint, pixel-art, neon-sign, corporate-clean, retro-fun, technical, etc.).

## When to use

- User is unsure which style to pick before generating a diagram
- User wants to explore the available style options
- User is about to call `generate-tech-diagram` or `restyle-diagram` and wants to see choices first

## Inputs to gather

None — this is a read-only reference skill.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Call `mcp__nano-tech-diagrams__list_styles` at runtime to fetch the current list.
3. Parse the response. If the MCP returns categories (e.g., "creative", "professional", "retro-fun", "technical"), format the output as a categorised table or markdown list.
4. Include 1–2 word descriptions or example use cases for each style if available from the MCP.
5. Display the list to the user.

## Output / side effects

- User sees a formatted list of available styles.
- No files created or modified.

## Safety / constraints

- Never hard-code the style list — always call the MCP to ensure the list is current.
- If the MCP is unavailable, provide a graceful error and the installation command.
