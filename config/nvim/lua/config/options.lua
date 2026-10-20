vim.g.ai_cmp = false
vim.g.snacks_animate = false
vim.opt.exrc = false
-- Honor .editorconfig; filetype defaults come from Neovim and LazyVim.
vim.g.editorconfig = true
-- Machine-specific settings belong outside the Git checkout.
local path = vim.fn.expand("~/.config/work-dev-env/nvim-local.lua")
if vim.uv.fs_stat(path) then dofile(path) end
