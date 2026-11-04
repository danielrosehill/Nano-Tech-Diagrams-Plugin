# Prompt recipe for diagrams with exact text

Every generated diagram prompt has these parts, in this order.

1. **Format and type.** "A 16:9 pipeline diagram for a technical blog post."
2. **Style.** One preset from `skills/diagram-prompt-library/styles/`, or the user's house style.
3. **Layout, explicitly.** How many cards and rows, the reading order, which way each arrow points and what it joins.
4. **Every string in double quotes**, exactly as it must appear, in reading order, each with its role: title, card label, edge label, caption.
5. **Containment rule.** "Each card contains only its label: no sample content, mini-diagrams, screenshots or example text inside it."
6. **Closing rule.** "No other text, logos or watermarks anywhere."

## Rules that come from observed failures

- **Card names invite illustration.** A card called "Whiteboard photo" got a drawn whiteboard with invented labels ("Client", "Option A") on both fal and Replicate, even with the closing rule in the prompt (tested 2026-11-04). Adding part 5 removed it in a retest (one image, Flare on fal).
- **Say which strings are not nodes.** A title and subtitle from a sketch became boxes joined by arrows when the prompt listed them only as strings. Write: `Title, top left, plain text, no box and no arrow: "..."`.
- **Say what isn't an arrow.** Bullets under a heading came back as arrows from both Flare and Nano. Write: `Plain bulleted list under "Agent 2:", no arrows.`
- **Whiteboards: always list the labels.** With no list, Flare passed 0 of 5 boards. With one, it got every string exact. See `model-routing.md`.
- **Keep labels short:** about five words or fewer, and eight cards or fewer. Past that, text errors climb.
- **Switch off prompt expansion** wherever a model has it, or the model rewrites the exact strings. `models.json` does this for the built-in aliases.
- **Style alone is not a brief.** A correct diagram in a childish style still fails: pick styles a reader of a technical post would take seriously.

## Output size

Providers return different sizes for the same request (Flare, 16:9: 1088x608 on fal, 2048x1152 on Replicate). Check the size against where the image is going, and read the text at that display width.
