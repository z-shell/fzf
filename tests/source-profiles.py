#!/usr/bin/env python3
"""Exercise all source hooks with a controlled compiler and an isolated prefix."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

profiles = json.loads((Path(__file__).resolve().parents[1] / "package.json").read_text())["zsh-data"]["zi-ices"]
for name in ("default", "default+keys", "bgn", "bgn+keys"):
    profile = profiles[name]
    with tempfile.TemporaryDirectory(prefix="fzf-source-") as directory:
        root = Path(directory)
        for folder in ("bin", "shell", "man/man1"):
            (root / folder).mkdir(parents=True)
        for filename in ("bin/fzf", "bin/fzf-tmux", "man/man1/fzf.1", "man/man1/fzf-tmux.1"):
            (root / filename).write_text("fixture\n")
        (root / "shell/completion.zsh").write_text("typeset -g completion_loaded=yes\n")
        (root / "shell/key-bindings.zsh").write_text('[[ $completion_loaded == yes ]] || return 8; typeset -g keys_loaded=yes\n')
        prefix = root / "prefix with spaces"
        env = dict(os.environ, HOME=directory, ZDOTDIR=directory, ZPFX=str(prefix))
        hook = profile["atclone"]
        def run(make_result):
            script = '() { builtin emulate -L zsh; make() { [[ $GOTOOLCHAIN == local && $1 == install ]] || return 9; return ' + str(make_result) + '; }; ' + hook + '; }'
            return subprocess.run(["zsh", "-dfc", script], cwd=root, env=env, capture_output=True, text=True)
        failed = run(7)
        assert failed.returncode == 7, (name, failed.stderr)
        assert not prefix.exists(), name
        passed = run(0)
        assert passed.returncode == 0, (name, passed.stderr)
        assert (prefix / "man/man1/fzf.1").is_file(), name
        assert not (root / "_fzf_completion").exists(), name
        sources = profile.get("multisrc", profile.get("src", "")).split()
        script = '; '.join('source "' + filename + '"' for filename in sources)
        script += '; [[ $completion_loaded == yes ]]'
        script += ' && [[ ${keys_loaded-no} == ' + ('yes' if name.endswith('+keys') else 'no') + ' ]]'
        subprocess.run(["zsh", "-dfc", script], cwd=root, env=env, check=True)
        assert profile["atpull"] == "%atclone"
print("ok - four source profiles preserve build failures, use the local compiler and load intended integration")
