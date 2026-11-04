#!/usr/bin/env python3
"""Generate or edit one diagram image. Standard library only.

  generate.py [--model ALIAS] [--provider NAME] [--aspect 16:9]
              [--image IN ...] [--dry-run] PROMPT_FILE OUT.png

With --image the run is an edit (image-to-image); without it, text-to-image.
Providers: fal, replicate, or any entry under "providers" in the user's config.json
(type "comfyui" or "command"). Choice order: --provider, TECH_COMMS_DIAGRAMS_PROVIDER,
config.json "provider", then the model's provider_order. An "image_staging" entry in
config.json moves input images first and passes URLs. See references/backends.md.

Writes OUT.png and OUT.png.json (model, provider, request, list price).
"""
import argparse, base64, json, mimetypes, os, random, subprocess, sys, time, uuid
import urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcd_common as c

# Replicate's edge returns 403 to the default Python-urllib User-Agent.
UA = f"{c.PLUGIN}/2.1"


def die(msg):
    sys.exit(f"ERROR: {msg}")


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
    b, body = multipart("content", path)
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


def multipart(field, path):
    b = uuid.uuid4().hex
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    body = (f'--{b}\r\nContent-Disposition: form-data; name="{field}"; '
            f'filename="{Path(path).name}"\r\nContent-Type: {mime}\r\n\r\n').encode()
    return b, body + Path(path).read_bytes() + f"\r\n--{b}--\r\n".encode()


def fill(node, values):
    """Replace {{placeholders}} in a ComfyUI workflow. A lone {{seed}} becomes a number."""
    if isinstance(node, dict):
        return {k: fill(v, values) for k, v in node.items()}
    if isinstance(node, list):
        return [fill(v, values) for v in node]
    if isinstance(node, str):
        if node == "{{seed}}":
            return values["seed"]
        for k, v in values.items():
            node = node.replace("{{" + k + "}}", str(v))
    return node


def run_comfyui(spec, mode, prompt, images):
    base = spec.get("url", "http://127.0.0.1:8188").rstrip("/")
    rel = (spec.get("workflows") or {}).get(mode) or die(f"no ComfyUI workflow set for {mode}: see references/backends.md")
    path = Path(rel).expanduser()
    path = path if path.is_absolute() else c.data_dir() / path
    if not path.is_file():
        die(f"ComfyUI workflow not found: {path}")
    values = {"prompt": prompt, "seed": random.randint(1, 2**31)}
    for i, img in enumerate(images):
        b, body = multipart("image", img)
        up = json.loads(http(f"{base}/upload/image", {"Content-Type": f"multipart/form-data; boundary={b}"}, body))
        name = f"{up['subfolder']}/{up['name']}" if up.get("subfolder") else up["name"]
        values["image" if i == 0 else f"image{i + 1}"] = name
    workflow = fill(json.loads(path.read_text()), values)
    pid = post_json(f"{base}/prompt", {}, {"prompt": workflow, "client_id": uuid.uuid4().hex})["prompt_id"]
    deadline = time.time() + int(spec.get("timeout", 600))
    while time.time() < deadline:
        h = json.loads(http(f"{base}/history/{pid}")).get(pid)
        if h:
            if (h.get("status") or {}).get("status_str") == "error":
                die(f"ComfyUI run failed: {json.dumps(h['status'])[:600]}")
            for out in h.get("outputs", {}).values():
                for im in out.get("images", []):
                    q = urllib.parse.urlencode({k: im.get(k, "") for k in ("filename", "subfolder", "type")})
                    return f"{base}/view?{q}", {}, {"prompt_id": pid, "workflow": str(path)}
            die("ComfyUI finished without an output image")
        time.sleep(2)
    die(f"ComfyUI prompt {pid} did not finish in time")


def run_command(spec, env):
    cmd = [os.path.expanduser(x) for x in spec.get("command") or die("custom provider has no command")]
    r = subprocess.run(cmd, env={**os.environ, **env})
    if r.returncode:
        die(f"provider command exited {r.returncode}")
    if not Path(env["TCD_OUT"]).is_file():
        die("provider command did not write the output file")


def stage(staging, path):
    """Run the user's staging command. Its last stdout line is a URL or a JSON object with url."""
    cmd = [os.path.expanduser(x).replace("{file}", str(path)) for x in staging["command"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    if r.returncode or not lines:
        die(f"image staging failed: {r.stderr.strip()[:400]}")
    try:
        fields = json.loads(r.stdout)
    except ValueError:
        fields = {"url": lines[-1].strip()}
    if not str(fields.get("url", "")).startswith("http"):
        die("image staging did not return a URL")
    return {**fields, "file": str(path)}


def unstage(staging, staged):
    cmd = staging.get("cleanup_command")
    for item in staged if cmd else []:
        args = [os.path.expanduser(x) for x in cmd]
        for k, v in item.items():
            args = [x.replace("{" + k + "}", str(v)) for x in args]
        if subprocess.run(args, capture_output=True).returncode:
            print(f"warning: could not clean up staged copy of {item['file']}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt_file")
    ap.add_argument("out")
    ap.add_argument("--model")
    ap.add_argument("--provider")
    ap.add_argument("--aspect")
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    c.load_credentials()
    cfg, user = c.load_models(), c.user_config()
    custom = user.get("providers", {})
    mode = "edit" if a.image else "t2i"
    for path in a.image:
        if not Path(path).is_file():
            die(f"input image not found: {path}")
    prompt = Path(a.prompt_file).read_text().strip()
    provider = c.chosen_provider(a.provider)
    aspect = a.aspect or ("16:9" if mode == "t2i" else None)
    staging = user.get("image_staging")

    if provider in custom:
        spec = custom[provider]
        kind, alias, endpoint, usd = spec.get("type"), a.model, provider, None
        if kind not in ("comfyui", "command"):
            die(f"provider {provider} needs type comfyui or command")
        payload = {"prompt": prompt, "aspect": aspect}
        label = None
    else:
        alias = a.model or cfg["default"][mode]
        model = cfg["models"].get(alias) or die(f"unknown model {alias}; have {sorted(cfg['models'])}")
        kind, label = "hosted", model.get("label")
        hosts = [p for p in cfg["provider_order"] if p in model]
        if provider and provider not in model:
            die(f"{alias} is not configured on {provider}; it runs on {hosts}, and custom providers are {sorted(custom)}")
        if not provider:
            ready = [p for p in hosts if os.environ.get(c.KEY_VARS[p])]
            if not ready and not a.dry_run:
                die(f"no API key for {alias}: run the setup-backend skill, or set {' or '.join(c.KEY_VARS[p] for p in hosts)}")
            provider = (ready or hosts)[0]
        if not os.environ.get(c.KEY_VARS[provider]) and not a.dry_run:
            die(f"{c.KEY_VARS[provider]} is not set: run the setup-backend skill")
        spec = model[provider]
        endpoint = spec.get(mode) or die(f"{alias} has no {mode} endpoint on {provider}")
        usd = spec.get("usd", {}).get(mode)
        payload = {"prompt": prompt, **spec.get("args", {})}
        if aspect:
            table = spec["aspect"].get("map")
            if table and aspect not in table:
                die(f"{alias} on {provider} supports aspects {sorted(table)}")
            payload[spec["aspect"]["param"]] = table[aspect] if table else aspect

    logged = dict(payload)
    use_staging = bool(a.image and staging and kind != "comfyui" and provider in staging.get("for", [provider]))
    if a.image:
        logged[spec.get("image_param", "images")] = [str(p) for p in a.image]
    if a.dry_run:
        print(json.dumps({"provider": provider, "type": kind, "endpoint": endpoint, "usd_list": usd,
                          "image_staging": use_staging, "request": logged}, indent=2))
        return

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    staged = [stage(staging, p) for p in a.image] if use_staging else []
    try:
        if kind == "command":
            refs = [s["url"] for s in staged] or [str(Path(p).resolve()) for p in a.image]
            run_command(spec, {"TCD_PROMPT_FILE": str(Path(a.prompt_file).resolve()), "TCD_OUT": str(out.resolve()),
                               "TCD_MODE": mode, "TCD_ASPECT": aspect or "", "TCD_MODEL": alias or "",
                               "TCD_IMAGES": "\n".join(refs)})
            meta = {}
        else:
            if kind == "comfyui":
                url, headers, meta = run_comfyui(spec, mode, prompt, a.image)
            else:
                if staged:
                    payload[spec["image_param"]] = [s["url"] for s in staged]
                elif a.image and provider == "fal":
                    payload[spec["image_param"]] = [data_uri(p) for p in a.image]
                elif a.image:
                    auth = {"Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}"}
                    payload[spec["image_param"]] = [replicate_upload(p, auth) for p in a.image]
                url, headers, meta = (run_fal if provider == "fal" else run_replicate)(endpoint, payload)
            out.write_bytes(http(url, headers))
    finally:
        if staged:
            unstage(staging, staged)

    Path(f"{out}.json").write_text(json.dumps({
        "model": alias, "label": label, "provider": provider, "type": kind, "endpoint": endpoint,
        "mode": mode, "usd_list": usd, "image_staged": use_staging,
        "created": datetime.now(timezone.utc).isoformat(), "request": logged, "response": meta}, indent=2))
    print(out)
    price = f"~${usd}" if usd is not None else "price not recorded"
    print(f">>> {alias or kind} on {provider}, {price}", file=sys.stderr)


if __name__ == "__main__":
    main()
