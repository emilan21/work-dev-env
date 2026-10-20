local config = require("lazy.core.config")
for _, name in ipairs({ "LazyVim", "oil.nvim", "nvim-lspconfig", "conform.nvim", "blink.cmp" }) do
  assert(config.plugins[name], "Missing editor plugin: " .. name)
  assert(vim.uv.fs_stat(config.plugins[name].dir), "Plugin not installed: " .. name)
end
for _, name in ipairs({ "mason.nvim", "mason-lspconfig.nvim", "copilot.lua", "copilot.vim",
  "avante.nvim", "codecompanion.nvim", "99", "neo-tree.nvim" }) do
  assert(not config.plugins[name], "Unexpected plugin enabled: " .. name)
end
assert(config.options.checker.enabled == false)
assert(config.options.install.missing == false)
require("lazy").load({ plugins = { "nvim-lspconfig", "conform.nvim", "blink.cmp" } })
for _, server in ipairs({ "clangd", "gopls", "lua_ls", "ols", "pyright" }) do
  assert(vim.lsp.config[server], "Missing LSP configuration: " .. server)
end
local servers = LazyVim.opts("nvim-lspconfig").servers
for _, server in ipairs({ "clangd", "gopls", "lua_ls", "ols", "pyright" }) do
  assert(servers[server].mason == false)
end
assert(LazyVim.opts("blink.cmp").fuzzy.implementation == "lua")
assert(#LazyVim.opts("nvim-treesitter").ensure_installed == 0)

local lock = vim.json.decode(table.concat(vim.fn.readfile(vim.fn.stdpath("config") .. "/lazy-lock.json"), "\n"))
for name, plugin in pairs(config.plugins) do
  if plugin.url then
    assert(vim.uv.fs_stat(plugin.dir), "Plugin not installed: " .. name)
    assert(lock[name], "Missing lock entry: " .. name)
    local commit = vim.fn.system({ "git", "-C", plugin.dir, "rev-parse", "HEAD" }):gsub("%s+$", "")
    assert(commit == lock[name].commit, "Plugin does not match lockfile: " .. name)
  end
end
print("Standalone editor smoke checks passed")
