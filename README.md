# work-dev-env

A standalone macOS development environment for Alacritty, tmux, tmux-sessionizer,
and Neovim 0.12+ (LazyVim). Uses Homebrew and macOS zsh. Includes C, Go, Lua, Odin, and
Python tooling. No personal desktop assets, Linux configuration, or AI integrations.

## Install on the Mac

Homebrew must already be installed and available in your shell. Apple Command Line
Tools are required (`xcode-select -p` checks them; `xcode-select --install` installs
them if your employer permits it). Use your approved GitHub authentication method;
no tokens or Git identity are included in this repository.

```sh
mkdir -p ~/Work
cd ~/Work
git clone https://github.com/emilan21/work-dev-env.git
cd work-dev-env
brew bundle --file Brewfile
./install --dry-run
./install
```

Add this line to your existing `~/.zshrc`, after Homebrew's `shellenv` setup:

```sh
source "$HOME/.config/work-dev-env/work-env.zsh"
```

Then finish setup:

```sh
source ~/.zshrc
./bootstrap
```

Keep the checkout in place: the installer links configuration files to it. It
backs up existing targets and prints the backup location. It does not replace
`.zshrc`, Git identity, login shells, or unrelated configuration. It replaces the
Neovim config directory as a unit so previous plugins do not leak into this setup.
Use the standard XDG locations under your home directory; custom XDG paths and
`NVIM_APPNAME` are not supported by this installer.

The Brewfile includes JetBrains Mono Nerd Font, Neovim, tmux, fzf,
ripgrep, fd, LazyGit, parser build tools, language servers, and formatters. LLVM's
keg-only `bin` directory is added by the shell snippet using `brew --prefix llvm`,
which works on Apple Silicon and Intel. Go and Odin toolchains are included;
project-specific dependencies remain project-owned. Homebrew's support for your
macOS version/architecture determines binary availability and possible source builds.

`./bootstrap` explicitly downloads pinned tmux plugins, lazy.nvim, LazyVim, and
locked editor plugins, then builds syntax parsers. It needs GitHub access plus
Homebrew's usual download hosts for the Brew step. Parser builds use upstream
archives identified by the pinned nvim-treesitter revision. Normal editing does
not install missing plugins, language servers, parsers, or completion binaries,
and periodic update checks are disabled. TLS/proxy failures stop setup: use your
company's approved certificate/proxy configuration rather than disabling checks.
There are no background update services or login agents.

Alacritty must be installed separately through an employer-approved source.
As of 2026-10-20, [Homebrew disables its Alacritty cask](https://formulae.brew.sh/api/cask/alacritty.json)
because it fails Gatekeeper checks. The Brewfile deliberately excludes that cask.
This repository does not remove quarantine flags or bypass Gatekeeper. You can
finish setup and use tmux/Neovim from macOS Terminal while arranging an approved
Alacritty installation. If approved Alacritty is installed only as an application,
its command-line executable is `/Applications/Alacritty.app/Contents/MacOS/alacritty`.

## Everyday use

- `ts`: select a project or existing tmux session with fzf.
- `ts /path/to/project`: open a project directly. Spaces and quotes are supported.
- `Ctrl+A`, then `f`: open the sessionizer inside tmux.
- New project sessions have `editor` (Neovim) and `terminal` windows.
- `Ctrl+A`, then `h/j/k/l`: move between panes; `v` and `s` split panes.
- `Ctrl+A`, then `[`: copy mode; `v` selects and `y` copies using macOS `pbcopy`.
- `Ctrl+A`, then `Ctrl+S` / `Ctrl+R`: save / restore sessions manually.
- `Space e` or `Space -` in Neovim opens Oil; `Space u c` opens its cheat sheet.
- Alacritty uses Command+C/V for clipboard and left Option as Alt.

Project search defaults to `~/Work` and `~/Projects`, two directory levels deep.
Hidden directories, `node_modules`, and `vendor` are skipped. Session names include
a short hash of the canonical directory path so projects with the same basename
remain separate. Cancelling fzf does nothing. Per-project executable hydration
hooks and project scaffolding are intentionally absent.

Neovim uses your familiar LazyVim mappings, Oil, and an initial vertical split
when launched without files. Project `.editorconfig` files take precedence over
editor defaults. LSPs use Homebrew executables: `clangd`, `gopls`, `lua-language-server`,
`ols`, and `pyright`. Formatting uses clang-format, gofmt, StyLua, Ruff, and shfmt,
with LSP formatting as fallback. No AI extras are enabled. LazyVim's `mini.ai`
plugin implements local Vim text objects; it is not an AI service.

## Automatic session recovery

Tmux continuum checks its lightweight status-line hook while tmux is active and
saves every 15 minutes. Resurrect restores when the first tmux server starts.
There is no automatic login launch. The sessionizer waits for restore before
creating a new project session. If restore does not finish within 20 seconds,
it reports an error instead of creating competing sessions; use `tmux attach`
and manual restore to inspect the saved environment. Continuum may skip automatic
restore when another tmux server is running.

Restore recreates windows, pane layouts, working directories, and Neovim processes.
It does **not** recover arbitrary programs or unsaved edits. LazyVim's separate
editor-session feature can restore saved editor layouts through `Space q s`.
Pane scrollback/content capture is off, and only Neovim is eligible for process
restart. Snapshots can still contain work paths and command arguments: they stay
in `~/.local/state/work-dev-env/resurrect`, outside Git, with a private directory.
Snapshot retention is seven days, cleaned on subsequent saves. Workstation backup
or sync policies still apply to this local data.

Zscaler and CrowdStrike remain untouched. No exclusions, bypasses, or endpoint
configuration changes are required by this repo. Employer policy determines
whether the software and its ordinary process inspection/downloads are allowed;
this configuration cannot guarantee an absence of endpoint alerts.

## Local customization, updates, and rollback

Local files are outside the checkout and are never uploaded by this repo:

- `~/.config/tmux/local.conf` for tmux overrides.
- `~/.config/tmux-sessionizer/local.json` for `search_paths` and `max_depth` overrides.
- `~/.config/work-dev-env/nvim-local.lua` for editor options.

For example, sessionizer's local JSON can be:

```json
{"search_paths": ["~/Work", "~/Projects"], "max_depth": 3}
```

Work-approved Copilot customization can be added on the Mac later. This repo
contains no agent tooling or authentication and imposes no prohibition on your
later approved additions. Keep work code, credentials, editor state, and generated
snapshots out of this configuration repository.

After reviewing upstream changes, `git pull --ff-only`, run `make check`, and run
`./bootstrap` to apply the committed plugin pins. Brew updates are a separate,
explicit decision. Updating Neovim plugin versions with `:Lazy update` changes the
tracked lockfile; review and commit it deliberately. If updating LazyVim or lazy.nvim,
update the corresponding `plugins.json` commit to match `config/nvim/lazy-lock.json`.
Tmux plugin updates are reviewed commit changes in `plugins.json`. No package
manager automatically commits or pushes changes.

To roll back configuration, use the backup printed by `./install`:

```sh
./install --dry-run --restore ~/.local/state/work-dev-env/backups/<timestamp>
./install --restore ~/.local/state/work-dev-env/backups/<timestamp>
```

Restore refuses to overwrite targets changed since installation. Move such files
aside before restoring. Restoring does not uninstall Brew packages or plugin/state
directories, and does not edit your manually added zsh source line; remove that
line if you are uninstalling. Restart the affected applications after restore.

## Validation

`make check` runs isolated installer/sessionizer tests plus Lua, Python, TOML, and
JSON checks. The GitHub Actions macOS job installs the Brewfile, bootstraps in a
temporary home, checks the editor dependency graph, validates Alacritty TOML,
and exercises tmux save/restore on a disposable socket. Native Alacritty validation
runs if its executable is available; the real Mac still needs the rendering check. No work project content
or credentials are used in CI.

After installing on the actual Mac:

1. Open Alacritty; check font rendering, Option shortcuts, and Command+C/V.
2. Run `ts` on a disposable project and check editor/terminal windows and clipboard.
3. Run `:LazyHealth` and `:checkhealth vim.lsp`; open a file in each needed language
   and confirm attachment with `:LspInfo`. Project dependencies may be needed.
4. Save a test tmux session, exit its server when safe, and start tmux again to
   verify automatic recovery on your machine. Keep real work saved beforehand.
5. Check that no download or certificate errors appear on the corporate network.

The repository starts with fresh history and has no connection to the original
personal repo's remotes or deployment tooling. The copied custom configuration
and scripts carry no repository-wide license; upstream plugins retain their own
licenses and are downloaded separately.
