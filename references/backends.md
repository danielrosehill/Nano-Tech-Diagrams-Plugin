# Backends, staging and preferences

Everything here is user configuration. It lives in the data directory, outside the plugin, so updates never overwrite it. Find the directory with `scripts/configure.py path`.

| File | Holds |
|---|---|
| `config.json` | Provider choice, custom providers, image staging |
| `credentials.env` | API keys saved with `configure.py set-key` (mode 600) |
| `PREFERENCES.md` | Free-text instructions the skills read and follow |
| `models.json` | Extra or changed model aliases |
| `styles/` | House styles |
| `workflows/` | ComfyUI workflows |

The folder can be its own private git repo. Keep `credentials.env` out of it.

## Choosing a provider

Order: `--provider`, then `TECH_COMMS_DIAGRAMS_PROVIDER`, then `provider` in `config.json`, then the first of `fal`, `replicate` with a key set.

## API keys

`FAL_KEY` and `REPLICATE_API_TOKEN`. A key in the environment wins over a saved key, so a secrets manager that injects variables needs no setup here.

## ComfyUI (local or on a server)

```json
{
  "provider": "comfy",
  "providers": {
    "comfy": {
      "type": "comfyui",
      "url": "http://127.0.0.1:8188",
      "workflows": {"t2i": "workflows/t2i.json", "edit": "workflows/edit.json"}
    }
  }
}
```

Export each workflow from ComfyUI with **Save (API Format)**, then put these placeholders in its input values: `{{prompt}}`, `{{seed}}`, and for edits `{{image}}` (`{{image2}}` and so on for more inputs). The script uploads input images through ComfyUI's own API, so a remote server needs no staging. Add `"timeout": 900` for slow hardware.

`--model` has no effect here: the workflow decides the model. The benchmark results don't cover local models, so `verify-diagram` matters more, and many open models render text poorly.

## Custom command provider

Any route the plugin doesn't know: an internal API, a gateway, a different vendor.

```json
{
  "provider": "my-route",
  "providers": {"my-route": {"type": "command", "command": ["~/bin/make-diagram.sh"]}}
}
```

The command gets these variables, must write the image to `TCD_OUT`, and exits 0 on success:

| Variable | Value |
|---|---|
| `TCD_PROMPT_FILE` | Path to the prompt |
| `TCD_OUT` | Where to write the image |
| `TCD_MODE` | `t2i` or `edit` |
| `TCD_ASPECT` | For example `16:9`; may be empty |
| `TCD_MODEL` | The `--model` value; may be empty |
| `TCD_IMAGES` | Input images, one per line: staged URLs if staging applies, otherwise paths |

## Image staging

For setups where the machine doing the generation can't read the client's files, such as a central AI gateway: move the input to shared storage first and pass a URL.

```json
{
  "image_staging": {
    "command": ["~/bin/stage.sh", "{file}"],
    "cleanup_command": ["~/bin/stage.sh", "--rm", "{key}"],
    "for": ["my-route"]
  }
}
```

- `command` prints a URL on its last line, or one JSON object with a `url` field.
- `cleanup_command` is optional and runs after generation. It can use `{url}`, `{file}` and any field from that JSON object.
- `for` is optional and limits staging to named providers. Without it, staging applies to every provider except ComfyUI.

Any storage works: S3, MinIO, an SSH copy, a file server. The URL must be reachable by whatever fetches it, so a hosted provider needs a URL open to the internet.

## PREFERENCES.md

For anything that doesn't fit a setting. Skills read it before generating, and it overrides their defaults.

```markdown
- Default style: our house style, `styles/acme.prompty`.
- Always ask before uploading whiteboard photos from work projects.
- Save diagrams to `assets/diagrams/` in the current repo.
```
