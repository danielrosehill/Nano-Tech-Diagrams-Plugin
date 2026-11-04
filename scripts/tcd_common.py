"""Shared paths and settings for tech-comms-diagrams. Standard library only.

User settings live in the data dir, outside the plugin, so plugin updates never touch them:
  config.json       provider choice, custom providers, image staging
  models.json       model aliases, merged over the built-in file
  credentials.env   API keys saved by configure.py (mode 600)
  PREFERENCES.md    free-text instructions that the skills read and follow
  styles/           house styles
  workflows/        ComfyUI workflows
"""
import json, os
from pathlib import Path

PLUGIN = "tech-comms-diagrams"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
KEY_VARS = {"fal": "FAL_KEY", "replicate": "REPLICATE_API_TOKEN"}


def data_dir():
    if os.environ.get("TECH_COMMS_DIAGRAMS_DATA"):
        return Path(os.environ["TECH_COMMS_DIAGRAMS_DATA"]).expanduser()
    if os.environ.get("CLAUDE_USER_DATA"):
        return Path(os.environ["CLAUDE_USER_DATA"]).expanduser() / PLUGIN
    root = Path.home() / ".claude-user-data"
    if root.is_dir():
        return root / PLUGIN
    xdg = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local/share")
    return Path(xdg) / "claude-plugins" / PLUGIN


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def user_config():
    return read_json(data_dir() / "config.json", {})


def save_user_config(cfg):
    d = data_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / "config.json").write_text(json.dumps(cfg, indent=2) + "\n")


def load_models():
    cfg = json.loads((PLUGIN_ROOT / "models.json").read_text())
    overlay = read_json(data_dir() / "models.json", {})
    cfg["models"].update(overlay.get("models", {}))
    cfg["default"].update(overlay.get("default", {}))
    cfg["provider_order"] = overlay.get("provider_order", cfg["provider_order"])
    return cfg


def credentials_file():
    return data_dir() / "credentials.env"


def saved_credentials():
    path, out = credentials_file(), {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


def load_credentials():
    """Environment wins: a saved key only fills a variable that isn't set."""
    for k, v in saved_credentials().items():
        if not os.environ.get(k):
            os.environ[k] = v


def chosen_provider(flag=None):
    """Flag, then environment, then the saved preference. None means use provider_order."""
    return flag or os.environ.get("TECH_COMMS_DIAGRAMS_PROVIDER") or user_config().get("provider")
