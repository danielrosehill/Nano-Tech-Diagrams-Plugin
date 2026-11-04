#!/usr/bin/env bash
# Render Mermaid source to SVG, PNG or PDF. The format comes from the output extension.
# Usage: render-mermaid.sh <input.mmd> <output.svg|png|pdf> [--theme default|neutral|dark|forest] [--bg white|transparent]
# Uses mmdc if installed, else @mermaid-js/mermaid-cli through npx (first run downloads it).
set -euo pipefail
[ $# -ge 2 ] || { echo "usage: $0 <input.mmd> <output.svg|png|pdf> [--theme T] [--bg B]" >&2; exit 2; }
IN="$1"; OUT="$2"; shift 2
THEME=neutral; BG=white
while [ $# -gt 0 ]; do
  case "$1" in
    --theme) THEME="$2"; shift 2 ;;
    --bg) BG="$2"; shift 2 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"
if command -v mmdc >/dev/null; then MMDC=(mmdc); else MMDC=(npx -y -p @mermaid-js/mermaid-cli mmdc); fi
# Chromium's sandbox fails on some Linux hosts, so it is switched off for this local render.
CFG="$(mktemp --suffix=.json)"; trap 'rm -f "$CFG"' EXIT
echo '{"args":["--no-sandbox"]}' > "$CFG"
"${MMDC[@]}" -i "$IN" -o "$OUT" -t "$THEME" -b "$BG" -s 2 -p "$CFG" -q
echo "$OUT"
