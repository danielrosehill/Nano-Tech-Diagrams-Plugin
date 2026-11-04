---
name: setup-backend
description: Set up diagram generation: API keys for fal or Replicate, provider choice, local ComfyUI, custom gateway routes and image staging.
---

# Set up the backend

Use on first run, when a key is missing, in a new environment, or when the user changes how generation runs.

## Steps

1. Check the current state:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" status --check
   ```
   Keys show where they come from (`environment`, `credentials.env`) and whether they work. If the chosen provider is valid, say so and stop.
2. Ask which route the user wants, unless it's already clear:
   - **Hosted API:** fal (default) or Replicate
   - **ComfyUI:** on this machine or a server
   - **Custom route:** a gateway or internal service
3. For a hosted API, sort out the key. Prefer what the user already has:
   - **Secrets manager or shell profile:** have it set `FAL_KEY` or `REPLICATE_API_TOKEN` in the environment the agent runs in. Nothing is saved.
   - **Save it here:** ask the user to run this themselves, so the key never enters the conversation:
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" set-key fal
     ```
   Never ask for a key in chat. If one is pasted anyway, don't repeat it.
4. Save the preference:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" set-provider <name>
   ```
5. For ComfyUI, a custom route or staging, read `references/backends.md` and edit `config.json` in the data directory. Ask for the URL or command; don't invent one.
6. Put anything that isn't a setting in `PREFERENCES.md` in the data directory.
7. Run `status --check` again and report the result.

## Running in another environment

Agent sessions don't always share the user's shell. If `status` shows no key but the user says it's set, the variable isn't reaching this process: check how the agent was launched. A saved key in the data directory works in every session on that machine, but a remote box, container or CI job needs its own setup.

## Data storage

Writes only to the data directory, `configure.py path`, outside the plugin. `credentials.env` is mode 600.
