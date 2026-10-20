-- -c normally keeps running after Lua errors; make verification fail explicitly.
local ok, err = xpcall(function()
  dofile(assert(vim.env.WORK_ENV_SCRIPT, "WORK_ENV_SCRIPT is required"))
end, debug.traceback)
if not ok then
  vim.api.nvim_err_writeln(err)
  vim.cmd("cquit 1")
end
