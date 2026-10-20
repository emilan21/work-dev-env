local path = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(path) then
  error("Dependencies missing: run ./bootstrap from the work-dev-env checkout")
end
vim.opt.rtp:prepend(path)
require("lazy").setup({
  spec = {
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },
    { import = "plugins" },
  },
  defaults = { lazy = false, version = false },
  install = { missing = vim.env.WORK_ENV_BOOTSTRAP == "1", colorscheme = { "habamax" } },
  checker = { enabled = false },
  change_detection = { notify = false },
})
