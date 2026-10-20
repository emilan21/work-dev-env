# Add this line to ~/.zshrc after Homebrew's shellenv setup:
# source "$HOME/.config/work-dev-env/work-env.zsh"
export PATH="$HOME/.local/bin:$PATH"
# LLVM is keg-only; clangd needs this addition on either Mac architecture.
if command -v brew >/dev/null 2>&1; then
  export PATH="$(brew --prefix llvm)/bin:$PATH"
fi
