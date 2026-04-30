# Tech Diagram Image-Gen Prompts

A library of prompts for generating and transforming technical diagrams with image-generation models (Nano Banana 2, Gemini, GPT-Image, etc.). Extracted from [Tech-Diagram-Maker](https://github.com/danielrosehill/Tech-Diagram-Maker) for standalone reuse.

## Format

Prompts use the [**`.prompty`**](https://prompty.ai) format — markdown with YAML frontmatter. It's the closest thing to an emerging standard for portable prompt files (Microsoft, VS Code extension, Python/JS runtimes), and stays fully human-readable on GitHub.

```yaml
---
name: Prompt Name
description: One-line summary
tags: [whiteboard, cleanup]
inputs:
  subject:
    type: string
    default: system architecture
---
The prompt body, with {{subject}} variable injection.
```

Variables use `{{double_braces}}` (Jinja-style), the prompty convention.

## Layout

```
whiteboard/         Whiteboard photo cleanup prompts
styles/             28 visual style presets
  professional/   creative/   technical/   retro-fun/   language/
diagram-types/      33 diagram-type prompts (what to draw)
  infrastructure/ software/   process/     conceptual/  data-viz/
builders/           Composite prompts that combine style + diagram-type + user input
```

## Usage

The prompts are designed to compose:

- **Text-to-image**: pick a `diagram-types/` prompt + a `styles/` prompt, fill in the variable for your subject.
- **Image-to-image**: feed an existing image plus a `styles/` prompt to restyle it, or a `diagram-types/` prompt to reinterpret it.
- **Whiteboard cleanup**: use `whiteboard/cleanup.prompty` plus a `styles/` prompt of your choice.

The `builders/` directory contains the meta-templates that show how the original tool stitches these together.

## Source

Extracted from `src/nano_tech_diagrams/core.py` in danielrosehill/Tech-Diagram-Maker.
