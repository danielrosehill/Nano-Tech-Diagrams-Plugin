---
name: list-diagram-types
description: Use when the user wants to see available diagram-type presets (network, flowchart, K8s, mind-map, etc.) to guide their description.
---

# List Diagram Types

Display all available diagram-type presets. Diagram types guide the model's layout and rendering approach (e.g., network topology, flowchart, Kubernetes cluster, mind-map, data pipeline, entity-relationship, etc.).

## When to use

- User wants to see diagram-type options before describing their diagram
- User is unsure what diagram types are available
- User wants to specify a diagram type when calling `generate-tech-diagram`

## Inputs to gather

None — this is a read-only reference skill.

## Procedure

1. If the MCP is not installed, show the user: `claude mcp add nano-tech-diagrams -- npx -y nano-tech-diagrams-mcp` and stop.
2. Call `mcp__nano-tech-diagrams__list_diagram_types` at runtime to fetch the current list.
3. Parse the response. If the MCP returns categories or groupings, format as categorised markdown or table.
4. Include brief descriptions or use-case examples for each type if available from the MCP.
5. Display the list to the user.

## Output / side effects

- User sees a formatted list of available diagram types.
- No files created or modified.

## Safety / constraints

- Never hard-code the diagram-type list — always call the MCP to ensure the list is current.
- If the MCP is unavailable, provide a graceful error and the installation command.
