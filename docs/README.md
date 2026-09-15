<table align="center"><tr><td>
<h1 align="center">
<a target="_self" href="https://github.com/z-shell/zi/">
  <p>
  <img align="center" src="https://raw.githubusercontent.com/z-shell/wiki/main/static/img/logo.png" alt="Zi Logo" width="60px" height="60px" />
  </a>
  ❮ Zi package - fzf ❯
  </p>
  </h1>
  <h2 align="center"><p> A command-line fuzzy finder </p></h2>
<h3 align="center">
<table>
    <tr>
        <td><b>Package source:</b></td>
        <td>Source Tarball</td>
        <td>Binary</td>
        <td>Git</td>
        <td>Node</td>
        <td>Gem</td>
    </tr>
    <tr>
        <td><b>Status:</b></td>
        <td>✔️ (default)</td>
        <td>✔️</td>
        <td>✔️</td>
        <td>❌</td>
        <td>❌</td>
    </tr>
</table></h3>
<p><img align="center" src="img/fzf-example-preview.png" alt="zi package fzf" width="100%" height="auto" /><p>
</td></tr></table><hr />

## 💡 Wiki: [packages](https://wiki.zshell.dev/ecosystem/category/-packages) | [annexes](https://wiki.zshell.dev/ecosystem/category/-annexes)

## Available `pack''` invocations

```zsh
# Download the package with the default ice list
zi pack for fzf
```

```zsh
# Download the package with the default ice list + setting up the key bindings
zi pack"default+keys" for fzf
```

```zsh
# Download the package with the bin-gem-node annex-utilizing ice list
zi pack"bgn" for fzf
```

```zsh
# Download the package with the bin-gem-node annex-utilizing ice list
# + setting up the key bindings. The "+keys" variants are available for each profile
zi pack"bgn+keys" for fzf
```

```zsh
# Download with the bin-gem-node annex-utilizing ice list FROM GIT REPOSITORY
zi pack"bgn" git for fzf
```

```zsh
# Download the binary from the Github releases (like from'gh-r' ice)
zi pack"binary" for fzf
```

```zsh
# Download the binary from the Github releases and install via Bin-Gem-Node shims
zi pack"bgn-binary" for fzf
```

## Default Profile

Provides the fuzzy finder via Makefile-installation of the `fzf` binary under `$ZPFX/bin`.

```zsh
zi lucid as=program pick="$ZPFX/bin/fzf(|-tmux)" src="shell/completion.zsh" \
  atclone='GOTOOLCHAIN=local PREFIX=$ZPFX make install && cp -vf bin/fzf(|-tmux) "$ZPFX/bin"' \
    …
```

The `default+keys` profile loads `shell/key-bindings.zsh` after the completion.

## `bin-gem-node` Profile

Provides the fuzzy finder via _shims_, i.e.: automatic forwarder scripts created under `$ZPFX/bin` (which is added to the `$PATH` by default). It needs the [bin-gem-node](https://github.com/z-shell/z-a-bin-gem-node) annex.

```zsh
zi lucid as=null src="shell/completion.zsh" \
  atclone='GOTOOLCHAIN=local PREFIX=$ZPFX make install' \
  sbin="bin/fzf*" \
  …
```

The `bgn+keys` profile loads `shell/key-bindings.zsh` after the completion.

---

> This repository compatible with [Zi](https://github.com/z-shell/zi)

The [junegunn/fzf](https://github.com/junegunn/fzf) zsh package. Zi's package support reads its `package.json` to automatically:

- get the plugin's Git repository OR release-package URL,
- get the list of the recommended ices for the plugin,
  - there can be multiple lists of ices,
  - the ice lists are stored in _profiles_; there's at least one profile, _default_,
  - the ices can be selectively overridden.

## Native binary and shell integration

```zsh
zi pack'native+keys' for fzf
```

This profile loads the release executable through Zi's native program support.
At install/update it caches `fzf --zsh` output and fetches `fzf-tmux` from the
matching release tag. Loading sources the cached integration without a new
generator process. The binary, shell integration, and tmux helper stay paired.
No bin-gem-node or patch-dl annex is required for this profile.

The upstream completion and keybinding defaults apply. Set `FZF_CTRL_T_COMMAND`,
`FZF_ALT_C_COMMAND`, or `FZF_CTRL_R_COMMAND` to an empty string before loading
to disable the corresponding binding. Existing profiles remain available.

The source profiles (`default`, `default+keys`, `bgn`, `bgn+keys`) require an
existing Go compiler compatible with upstream's `go.mod`, plus make and Git.
Builds use `GOTOOLCHAIN=local` so an incompatible compiler fails without
automatically downloading another Go toolchain. Dependencies still download
through Go's normal module mechanism. Source profiles load their checked-out
completion integration directly; `+keys` additionally loads the keybindings.
