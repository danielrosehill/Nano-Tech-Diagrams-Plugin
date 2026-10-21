---
name: list-diagram-types
description: Use when the user wants to see available diagram-type presets (network, flowchart, K8s, mind-map, etc.) to guide their description.
---

# List Diagram Types

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


Display all available diagram-type presets. Diagram types guide the model's layout and rendering approach (e.g., network topology, flowchart, Kubernetes cluster, mind-map, data pipeline, entity-relationship, etc.).

## When to use

- User wants to see diagram-type options before describing their diagram
- User is unsure what diagram types are available
- User wants to specify a diagram type when calling `generate-tech-diagram`

## Inputs to gather

None — this is a read-only reference skill.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Call `list_diagram_types` at runtime to fetch the current list.
3. Parse the response. If the MCP returns categories or groupings, format as categorised markdown or table.
4. Include brief descriptions or use-case examples for each type if available from the MCP.
5. Display the list to the user.

## Output / side effects

- User sees a formatted list of available diagram types.
- No files created or modified.

## Safety / constraints

- Never hard-code the diagram-type list — always call the MCP to ensure the list is current.
- If the MCP is unavailable, provide a graceful error and the installation command.
