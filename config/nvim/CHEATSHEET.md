# Neovim Cheat Sheet

`<leader>` is `Space`. Press `Space` and pause to browse commands with WhichKey.

## Essential Vim

| Keys | Action |
| --- | --- |
| `i` / `a` | Insert before / after the cursor |
| `Esc` | Return to Normal mode |
| `h j k l` | Move left, down, up, right |
| `w` / `b` | Next / previous word |
| `0` / `^` / `$` | Line start / first text / line end |
| `gg` / `G` | First / last line |
| `{` / `}` | Previous / next paragraph |
| `Ctrl-u` / `Ctrl-d` | Scroll half a page up / down |
| `%` | Jump between matching brackets |
| `zz` | Center the current line |
| `u` / `Ctrl-r` | Undo / redo |
| `.` | Repeat the last change |

## Editing

| Keys | Action |
| --- | --- |
| `x` | Delete character |
| `dd` / `D` | Delete line / to end of line |
| `yy` / `Y` | Copy line / to end of line |
| `p` / `P` | Paste after / before |
| `cw` / `ciw` | Change word / change inside word |
| `ci"` / `ci(` | Change inside quotes / parentheses |
| `di{` / `da{` | Delete inside / around braces |
| `>` / `<` in Visual mode | Indent / outdent selection |
| `gcc` | Toggle comment on the current line |
| `gc` with a motion | Toggle comment over a motion |

## Search and Navigation

| Keys | Action |
| --- | --- |
| `/text` | Search forward |
| `n` / `N` | Next / previous search match |
| `*` / `#` | Search word under cursor forward / backward |
| `s` | Flash jump to visible text |
| `<leader><space>` | Find files from project root |
| `<leader>ff` | Find files from project root |
| `<leader>fF` | Find files from working directory |
| `<leader>fg` | Find Git-tracked files |
| `<leader>sg` | Search project text with grep |
| `<leader>sw` | Search word under cursor |
| `<leader>sk` | Search keymaps |
| `<leader>:` | Command history |

## Oil File Explorer

| Keys | Action |
| --- | --- |
| `<leader>-` | Open the current file's directory |
| `<leader>e` | Open the working directory |
| `-` in Oil | Go to the parent directory |
| `Enter` | Open file or directory |
| `Ctrl-s` / `Ctrl-h` | Open in vertical / horizontal split |
| `Ctrl-t` | Open in a new tab page |
| `g.` | Toggle hidden files |
| `g?` | Show Oil help |
| `q` | Close Oil |

In Oil, edit filenames like normal text, then write with `:w` to apply file
operations. Review the confirmation before accepting deletes or moves.

## Buffers, Windows, and Tabs

| Keys | Action |
| --- | --- |
| `Shift-h` / `Shift-l` | Previous / next buffer |
| `[b` / `]b` | Previous / next buffer |
| `<leader>bb` | Switch to the other buffer |
| `<leader>bd` | Delete current buffer |
| `<leader>bo` | Delete other buffers |
| `<leader>\|` | Split window to the right |
| `Ctrl-h/j/k/l` | Focus the window left/down/up/right |
| `Ctrl-Up/Down/Left/Right` | Resize the current window |
| `<leader><Tab><Tab>` | Create a tab page |
| `<leader><Tab>[/]` | Previous / next tab page |
| `<leader><Tab>d` | Close current tab page |

The labels across the top are normally buffers. Neovim tab pages are separate
window layouts and use the `<leader><Tab>` group.

## LSP and Code

| Keys | Action |
| --- | --- |
| `gd` | Go to definition |
| `gD` | Go to declaration |
| `gr` | Show references |
| `gI` | Go to implementation |
| `K` | Show documentation for symbol |
| `<leader>ca` | Code actions |
| `<leader>cr` | Rename symbol |
| `<leader>cf` | Format file or selection |
| `]d` / `[d` | Next / previous diagnostic |
| `<leader>cd` | Show diagnostic details |
| `<leader>cs` | Document symbols |
| `<leader>cS` | Workspace symbols |

## Git, Terminal, and Sessions

| Keys | Action |
| --- | --- |
| `<leader>gg` | Open LazyGit |
| `]h` / `[h` | Next / previous changed hunk |
| `<leader>ghp` | Preview changed hunk |
| `<leader>ghs` | Stage changed hunk |
| `<leader>ghr` | Reset changed hunk |
| `Ctrl-/` | Toggle terminal |
| `<leader>qs` | Restore the last session |
| `<leader>ql` | Restore the current directory's session |

## Commands Worth Remembering

| Command | Action |
| --- | --- |
| `:w` / `:q` / `:wq` | Save / quit / save and quit |
| `:qa` / `:qa!` | Quit all / quit all without saving |
| `:checkhealth` | Diagnose Neovim and plugin setup |
| `:Lazy` | Plugin manager |
| `:LazyHealth` | Check editor setup |
| `:LspInfo` | Inspect attached language servers |

Open this sheet inside Neovim with `<leader>uc`, with `nvim ~/.config/nvim/CHEATSHEET.md`.
