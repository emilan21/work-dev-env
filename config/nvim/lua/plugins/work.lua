return {
  { "mason-org/mason.nvim", enabled = false },
  { "mason-org/mason-lspconfig.nvim", enabled = false },
  { "LazyVim/LazyVim", opts = { colorscheme = "tokyonight-night" } },
  { "folke/tokyonight.nvim", opts = { style = "night", on_colors = function(c)
    c.bg = "#202124"
    c.fg = "#b0aea8"
  end } },
  { "neovim/nvim-lspconfig", opts = {
    servers = {
      clangd = { mason = false },
      gopls = { mason = false },
      lua_ls = { mason = false },
      ols = { mason = false },
      pyright = { mason = false },
    },
  } },
  { "stevearc/conform.nvim", opts = { formatters_by_ft = {
    c = { "clang_format" }, cpp = { "clang_format" },
    go = { "gofmt" }, lua = { "stylua" },
    python = { "ruff_format" }, sh = { "shfmt" },
  } } },
  -- Install parsers explicitly through ./bootstrap, never on file open.
  { "nvim-treesitter/nvim-treesitter", opts = function(_, opts)
    opts.ensure_installed = {}
  end },
  -- Use Lua fuzzy matching; avoid blink's prebuilt-binary download.
  { "saghen/blink.cmp", opts = { fuzzy = { implementation = "lua" } } },
}
