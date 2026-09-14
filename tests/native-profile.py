#!/usr/bin/env python3
"""Check package hooks offline: version pairing, refresh and failed downloads."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

profile = json.loads((Path(__file__).resolve().parents[1] / "package.json").read_text())["zsh-data"]["zi-ices"]["native+keys"]
with tempfile.TemporaryDirectory(prefix="fzf-profile-") as directory:
    root = Path(directory)
    binary = root / "fzf"
    binary.write_text("#!/bin/sh\ncase $1 in\n--version) echo '0.74.4 (fixture)' ;;\n--zsh) echo 'typeset -g fixture_integration=ready' ;;\nesac\n")
    binary.chmod(0o755)
    env = dict(os.environ, HOME=directory, ZDOTDIR=directory)
    hook = profile["atclone"]
    subprocess.run(["zsh", "-n", "-c", hook], check=True, env=env)
    def run(download):
        script = "() { builtin emulate -L zsh; " + download + "; " + hook + "; }"
        return subprocess.run(["zsh", "-dfc", script], cwd=root, env=env, capture_output=True, text=True)
    good = '.zi-download-file-stdout() { [[ $1 == https://raw.githubusercontent.com/junegunn/fzf/v0.74.4/bin/fzf-tmux ]] || return 9; print -r -- helper; }'
    assert run(good).returncode == 0
    integration = (root / "fzf.zsh").read_bytes()
    helper = (root / "fzf-tmux").read_bytes()
    assert b"fixture_integration=ready" in integration
    assert helper == b"helper\n" and os.access(root / "fzf-tmux", os.X_OK)
    assert profile["atpull"] == "%atclone"
    assert run('.zi-download-file-stdout() { return 7; }').returncode == 7
    assert (root / "fzf.zsh").read_bytes() == integration
    assert (root / "fzf-tmux").read_bytes() == helper
    assert run(good.replace("-- helper", "-- refreshed")).returncode == 0
    assert (root / "fzf-tmux").read_bytes() == b"refreshed\n"
print("ok - native package generates paired integration, refreshes it and preserves caches on download failure")
