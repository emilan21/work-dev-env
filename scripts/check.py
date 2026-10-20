#!/usr/bin/env python3
"""Check checked-in assets without using the developer's live configuration."""
import json
from pathlib import Path
import subprocess
import tomllib

root = Path(__file__).resolve().parents[1]
for name in ('install', 'bootstrap', 'bin/tmux-sessionizer'):
    compile((root / name).read_text(), name, 'exec')
for path in root.rglob('*.json'):
    if '.local' not in path.parts:
        json.loads(path.read_text())
tomllib.loads((root / 'config/alacritty/alacritty.toml').read_text())
for path in (root / 'config/nvim').rglob('*.lua'):
    subprocess.run(['nvim', '--clean', '--headless', '-l', str(root / 'scripts/syntax.lua'), str(path)], check=True)
print('Python, JSON, TOML, and Lua checks passed.')

lock = json.loads((root / "config/nvim/lazy-lock.json").read_text())
pins = json.loads((root / "plugins.json").read_text())
for name in ("lazy.nvim", "LazyVim"):
    assert pins[name]["commit"] == lock[name]["commit"], f"Inconsistent pin: {name}"
for name in ("mason.nvim", "mason-lspconfig.nvim", "copilot.lua", "copilot.vim", "avante.nvim", "codecompanion.nvim", "99"):
    assert name not in lock, f"Unexpected plugin in lock: {name}"
