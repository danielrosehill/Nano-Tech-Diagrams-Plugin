#!/usr/bin/env python3
"""Generate or edit one diagram image on fal or Replicate. Standard library only.

  generate.py [--model ALIAS] [--provider auto|fal|replicate] [--aspect 16:9]
              [--image IN ...] [--dry-run] PROMPT_FILE OUT.png

With --image the run is an edit (image-to-image); without it, text-to-image.
Needs FAL_KEY and/or REPLICATE_API_TOKEN. Writes OUT.png and OUT.png.json (model,
provider, request, list price), so a graphic can be traced and regenerated.
"""
import argparse, base64, json, mimetypes, os, sys, time, uuid
import urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

PLUGIN = "tech-comms-diagrams"
# Replicate's edge returns 403 to the default Python-urllib User-Agent.
UA = f"{PLUGIN}/2.0"


def die(msg):
    sys.exit(f"ERROR: {msg}")


def data_dir():
    if os.environ.get("TECH_COMMS_DIAGRAMS_DATA"):
        return Path(os.environ["TECH_COMMS_DIAGRAMS_DATA"])
    if os.environ.get("CLAUDE_USER_DATA"):
        return Path(os.environ["CLAUDE_USER_DATA"]) / PLUGIN
    xdg = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local/share")
    return Path(xdg) / "claude-plugins" / PLUGIN


def load_config():
    cfg = json.loads((Path(__file__).resolve().parent.parent / "models.json").read_text())
    overlay = data_dir() / "models.json"
    if overlay.exists():
        o = json.loads(overlay.read_text())
        cfg["models"].update(o.get("models", {}))
        cfg["default"].update(o.get("default", {}))
        cfg["provider_order"] = o.get("provider_order", cfg["provider_order"])
    return cfg


def http(url, headers=None, body=None, timeout=300):
    req = urllib.request.Request(url, data=body, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        die(f"{url} returned {e.code}: {e.read()[:600].decode('utf-8', 'replace')}")


def post_json(url, headers, payload):
    raw = http(url, {**headers, "Content-Type": "application/json"}, json.dumps(payload).encode())
    return json.loads(raw)


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(Path(path).read_bytes()).decode()}"


def replicate_upload(path, auth):
    """Files API, because large data URIs in a prediction input are unreliable."""
    b = uuid.uuid4().hex
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    body = (f'--{b}\r\nContent-Disposition: form-data; name="content"; '
            f'filename="{Path(path).name}"\r\nContent-Type: {mime}\r\n\r\n').encode()
    body += Path(path).read_bytes() + f"\r\n--{b}--\r\n".encode()
    raw = http("https://api.replicate.com/v1/files",
               {**auth, "Content-Type": f"multipart/form-data; boundary={b}"}, body)
    return json.loads(raw)["urls"]["get"]


def run_fal(endpoint, payload):
    res = post_json(f"https://fal.run/{endpoint}", {"Authorization": f"Key {os.environ['FAL_KEY']}"}, payload)
    images = res.get("images") or []
    if not images:
        die(f"no image in fal response: {json.dumps(res)[:600]}")
    return images[0]["url"], {}, {k: v for k, v in res.items() if k != "images"}


def run_replicate(model, payload):
    auth = {"Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}"}
    p = post_json(f"https://api.replicate.com/v1/models/{model}/predictions",
                  {**auth, "Prefer": "wait=60"}, {"input": payload})
    deadline = time.time() + 300
    while p.get("status") not in ("succeeded", "failed", "canceled"):
        if time.time() > deadline:
            die(f"Replicate prediction {p.get('id')} still {p.get('status')} after 5 minutes")
        time.sleep(3)
        p = json.loads(http(p["urls"]["get"], auth))
    if p["status"] != "succeeded":
        die(f"Replicate prediction {p['status']}: {p.get('error')}")
    out = p["output"]
    return (out[0] if isinstance(out, list) else out), auth, {"id": p["id"], "metrics": p.get("metrics")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt_file")
    ap.add_argument("out")
    ap.add_argument("--model")
    ap.add_argument("--provider", default="auto", choices=["auto", "fal", "replicate"])
    ap.add_argument("--aspect")
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg = load_config()
    mode = "edit" if a.image else "t2i"
    alias = a.model or cfg["default"][mode]
    model = cfg["models"].get(alias) or die(f"unknown model {alias}; have {sorted(cfg['models'])}")
    keys = {"fal": "FAL_KEY", "replicate": "REPLICATE_API_TOKEN"}

    if a.provider == "auto":
        hosts = [p for p in cfg["provider_order"] if p in model]
        ready = [p for p in hosts if os.environ.get(keys[p])]
        if not ready and not a.dry_run:
            die(f"{alias} runs on {hosts}; set {' or '.join(keys[p] for p in hosts)}")
        provider = (ready or hosts)[0]
    else:
        provider = a.provider
        if provider not in model:
            die(f"{alias} is not configured on {provider}")
        if not os.environ.get(keys[provider]) and not a.dry_run:
            die(f"{keys[provider]} is not set")

    spec = model[provider]
    endpoint = spec.get(mode) or die(f"{alias} has no {mode} endpoint on {provider}")
    for path in a.image:
        if not Path(path).is_file():
            die(f"input image not found: {path}")

    payload = {"prompt": Path(a.prompt_file).read_text().strip(), **spec.get("args", {})}
    aspect = a.aspect or ("16:9" if mode == "t2i" else None)
    if aspect:
        table = spec["aspect"].get("map")
        if table and aspect not in table:
            die(f"{alias} on {provider} supports aspects {sorted(table)}")
        payload[spec["aspect"]["param"]] = table[aspect] if table else aspect

    usd = spec.get("usd", {}).get(mode)
    logged = dict(payload)
    if a.image:
        logged[spec["image_param"]] = [str(p) for p in a.image]
    if a.dry_run:
        print(json.dumps({"provider": provider, "endpoint": endpoint, "usd_list": usd, "request": logged}, indent=2))
        return

    if a.image:
        if provider == "fal":
            payload[spec["image_param"]] = [data_uri(p) for p in a.image]
        else:
            auth = {"Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}"}
            payload[spec["image_param"]] = [replicate_upload(p, auth) for p in a.image]

    url, dl_headers, meta = (run_fal if provider == "fal" else run_replicate)(endpoint, payload)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(http(url, dl_headers))
    Path(f"{out}.json").write_text(json.dumps({
        "model": alias, "label": model.get("label"), "provider": provider, "endpoint": endpoint,
        "mode": mode, "usd_list": usd, "created": datetime.now(timezone.utc).isoformat(),
        "request": logged, "response": meta}, indent=2))
    print(out)
    price = f"~${usd}" if usd is not None else "price not recorded"
    print(f">>> {alias} on {provider} ({endpoint}), {price}", file=sys.stderr)


if __name__ == "__main__":
    main()
