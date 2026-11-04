# Model routing

Defaults come from [Tech-Graphics-Benchmark](https://github.com/danielrosehill/Tech-Graphics-Benchmark), which tests exact text and correct arrows rather than general image quality. Aliases live in `models.json`.

| Job | First | Then | Then |
|---|---|---|---|
| Text to image | `flare` | `nano` | Mermaid |
| Image to image, labels listed in the prompt | `flare` | `nano` | Mermaid |
| Image to image, labels not listed | Don't: transcribe first | | |

`klein` is the cheapest option, for simple diagrams only.

## Evidence (as of 2026-11-04)

Pass = text exact, structure right and legible. These are agent reads of 5 images per model, not human ratings, so treat them as a first look.

| Model | Diagrams, tables, charts | Whiteboards, labels not listed | List price |
|---|---|---|---|
| GPT Image 2.5 Flare (`flare`) | 5/5 | 0/5 | $0.012 / $0.015 edit |
| Nano Banana 2.1 (`nano`) | 5/5 | 3/5 | $0.04 / $0.044 edit |
| Ideogram V4.5 | 3/5 | not tested | $0.03 |
| FLUX.3 Klein (`klein`) | 2/5 | 0/5 | $0.009 |
| Qwen-Image 3 | 0/5 | 0/5 | $0.04 |
| Seedream 5 Flash | not tested | 0/5 | $0.027 |

Listing the labels changes the whiteboard result. In follow-up tests on 2026-11-04, `flare` got every string exact on a 7-string board (fal and Replicate) and a 15-string board, and `nano` matched it on the 15-string board. That is three Flare images and one Nano image. Structure was not fully right on the 15-string board: both models turned bullets into arrows.

Without listed labels, the failures were handwriting copied as written, misreads ("META MCP" to "MCF"), dropped labels and invented arrows.

## Providers

`flare` and `nano` run on fal and Replicate; `klein` is configured on fal only. The benchmark ran on fal. On Replicate only `flare` has been tested, and its prices aren't recorded here, so check the model page. Without a saved preference, the first of them with a key set is used. See `backends.md` for choosing a provider, ComfyUI and custom routes.

To add or override a model, put a `models.json` with the same shape in the data directory. It's merged over the built-in file by alias.
