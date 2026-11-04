---
name: illustrate-text
description: Find where a blog post or technical doc needs a diagram, then make, verify and place graphics with alt text and captions.
---

# Illustrate a text

## Inputs

- The post, doc or passage
- Output folder and how images are referenced there
- House style, if any

## Steps

1. Read the text. Find passages a reader would struggle to hold in their head: pipelines, architectures, relationships between parts, before and after. Skip anything a graphic would only decorate.
2. Propose each graphic in one line: where it goes, what it shows, and which route `pick-diagram-route` gives. Two or three is usually enough for a post. Wait for a yes if more than one image will be generated.
3. Take every label, number and name from the text itself. Don't introduce terms the text doesn't use.
4. Make each graphic with the matching skill. Independent graphics can run in parallel.
5. Run `verify-diagram`. The meaning check matters most here: the graphic must agree with the prose.
6. Place each one right after the paragraph that introduces it, with alt text saying what it shows, for example "Five-stage pipeline: record, transcribe, edit, review, publish". Add a caption if the format has them.
7. List the graphics placed, the model used and the total list price.
