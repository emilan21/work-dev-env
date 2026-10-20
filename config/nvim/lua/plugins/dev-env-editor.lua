local startup_group = vim.api.nvim_create_augroup("DevEnvStartupLayout", { clear = true })

vim.api.nvim_create_autocmd("VimEnter", {
  group = startup_group,
  once = true,
  callback = function()
    if vim.fn.argc(-1) ~= 0 or #vim.api.nvim_list_uis() == 0 or #vim.api.nvim_list_wins() ~= 1 then
      return
    end

    -- Give a bare Neovim session two distinct, side-by-side editing buffers.
    vim.cmd("vnew")
  end,
})

return {
  {
    "nvim-neo-tree/neo-tree.nvim",
    enabled = false,
  },
  {
    "stevearc/oil.nvim",
    lazy = false,
    dependencies = {
      { "nvim-mini/mini.icons", opts = {} },
    },
    opts = {
      default_file_explorer = true,
      view_options = {
        show_hidden = true,
      },
    },
  },
}
