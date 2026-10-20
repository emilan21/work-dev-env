-- Loaded after LazyVim's defaults, so these intentionally replace its explorer
-- and horizontal-split mappings without changing the packaged configuration.
vim.keymap.set("n", "<leader>-", function()
  require("oil").open()
end, { desc = "Open parent directory" })

vim.keymap.set("n", "<leader>e", function()
  require("oil").open(vim.uv.cwd())
end, { desc = "Open working directory" })

local function open_cheatsheet()
  local path = vim.fn.stdpath("config") .. "/CHEATSHEET.md"
  local ok, lines = pcall(vim.fn.readfile, path)
  if not ok then
    vim.notify("Neovim cheat sheet not found: " .. path, vim.log.levels.ERROR)
    return
  end

  local buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_lines(buffer, 0, -1, false, lines)
  vim.bo[buffer].filetype = "markdown"
  vim.bo[buffer].modifiable = false

  local width = math.max(1, math.min(100, vim.o.columns - 4))
  local height = math.max(1, math.min(40, vim.o.lines - 4))
  local window = vim.api.nvim_open_win(buffer, true, {
    relative = "editor",
    width = width,
    height = height,
    col = math.floor((vim.o.columns - width) / 2),
    row = math.floor((vim.o.lines - height) / 2),
    style = "minimal",
    border = "rounded",
    title = " Neovim Cheat Sheet ",
    title_pos = "center",
  })

  vim.wo[window].conceallevel = 2
  vim.wo[window].cursorline = true
  vim.wo[window].wrap = false

  local function close()
    if vim.api.nvim_win_is_valid(window) then
      vim.api.nvim_win_close(window, true)
    end
  end

  vim.keymap.set("n", "q", close, { buffer = buffer, nowait = true })
  vim.keymap.set("n", "<Esc>", close, { buffer = buffer, nowait = true })
end

vim.keymap.set("n", "<leader>uc", open_cheatsheet, { desc = "Neovim cheat sheet" })
