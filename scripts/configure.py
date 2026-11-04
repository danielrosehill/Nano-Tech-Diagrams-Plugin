#!/usr/bin/env python3
"""Set up and check tech-comms-diagrams on this machine.

  configure.py status [--check]      where each key comes from; --check tests them live
  configure.py set-key fal|replicate prompt for a key without echoing, and save it (mode 600)
  configure.py set-provider NAME     save the preferred provider
  configure.py path                  print the data directory

Keys are never printed. Keys in the environment always win over a saved key.
"""
import argparse, getpass, json, os, sys, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcd_common as c

CHECKS = {"fal": ("https://api.fal.ai/v1/models/pricing?endpoint_id=fal-ai/flux/dev", "Key"),
          "replicate": ("https://api.replicate.com/v1/account", "Bearer")}


def probe(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": f"{c.PLUGIN}/2.1", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except OSError as e:
        return f"unreachable: {e}"


def status(check):
    saved, user = c.saved_credentials(), c.user_config()
    custom = user.get("providers", {})
    keys = {}
    for name, var in c.KEY_VARS.items():
        source = "environment" if os.environ.get(var) else "credentials.env" if saved.get(var) else None
        entry = {"variable": var, "source": source}
        if check and source:
            url, scheme = CHECKS[name]
            code = probe(url, {"Authorization": f"{scheme} {os.environ.get(var) or saved[var]}"})
            entry["valid"] = code == 200
            entry["http"] = code
        keys[name] = entry
    backends = {}
    for name, spec in custom.items():
        b = {"type": spec.get("type")}
        if spec.get("type") == "comfyui":
            b["url"] = spec.get("url", "http://127.0.0.1:8188")
            b["workflows"] = spec.get("workflows", {})
            if check:
                b["reachable"] = probe(b["url"].rstrip("/") + "/system_stats") == 200
        backends[name] = b
    prefs = c.data_dir() / "PREFERENCES.md"
    chosen = c.chosen_provider()
    usable = chosen in custom or (chosen in keys and keys[chosen]["source"]) if chosen else any(k["source"] for k in keys.values())
    print(json.dumps({"data_dir": str(c.data_dir()), "provider": chosen or "auto (first with a key)",
                      "ready": bool(usable), "keys": keys, "custom_providers": backends,
                      "image_staging": bool(user.get("image_staging")),
                      "preferences_file": str(prefs) if prefs.exists() else None}, indent=2))


def set_key(name):
    var = c.KEY_VARS[name]
    value = (getpass.getpass(f"{var}: ") if sys.stdin.isatty() else sys.stdin.readline()).strip()
    if not value:
        sys.exit("no key entered; nothing saved")
    creds = {**c.saved_credentials(), var: value}
    path = c.credentials_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.writelines(f"{k}={v}\n" for k, v in creds.items())
    os.chmod(path, 0o600)
    print(f"saved {var} to {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").add_argument("--check", action="store_true")
    sub.add_parser("set-key").add_argument("provider", choices=sorted(c.KEY_VARS))
    sub.add_parser("set-provider").add_argument("name")
    sub.add_parser("path")
    a = ap.parse_args()
    if a.cmd == "status":
        status(a.check)
    elif a.cmd == "set-key":
        set_key(a.provider)
    elif a.cmd == "path":
        print(c.data_dir())
    else:
        cfg = c.user_config()
        if a.name not in c.KEY_VARS and a.name not in cfg.get("providers", {}):
            sys.exit(f"unknown provider {a.name}: use fal, replicate, or add it under providers in config.json")
        c.save_user_config({**cfg, "provider": a.name})
        print(f"provider = {a.name}")


if __name__ == "__main__":
    main()
