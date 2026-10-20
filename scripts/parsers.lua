local parsers = {
  "bash", "c", "diff", "dockerfile", "go", "html", "json", "lua", "luadoc",
  "markdown", "markdown_inline", "odin", "python", "query", "toml", "vim", "vimdoc", "yaml",
}
require("lazy").load({ plugins = { "nvim-treesitter" } })
local ts = require("nvim-treesitter")
ts.install(parsers, { summary = true }):wait(300000)
local installed = ts.get_installed()
for _, name in ipairs(parsers) do
  if not vim.tbl_contains(installed, name) then
    error("Parser install failed: " .. name .. ". Check :TSLog; no TLS bypass is enabled.")
  end
end
