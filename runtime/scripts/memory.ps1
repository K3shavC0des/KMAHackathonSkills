param([ValidateSet('start','stop','status','mcp')][string]$Action = 'status')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$env:CLAUDE_MEM_DATA_DIR = Join-Path $projectRoot '.local/claude-mem'
$env:CLAUDE_MEM_WORKER_PORT = '37778'
$env:CLAUDE_MEM_PROVIDER = 'codex'
$env:DO_NOT_TRACK = '1'
$env:Path = "$projectRoot/.tools/node-v24.15.0-win-x64;$projectRoot/.tools/bun-windows-x64;$env:Path"
$codexBinary = Get-ChildItem "$env:USERPROFILE/.codex/packages/standalone/releases/*/bin/codex.exe" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($codexBinary) { $env:CLAUDE_MEM_CODEX_PATH = $codexBinary.FullName }
$runtime = Join-Path $projectRoot '.tools/runtime/node_modules/claude-mem/plugin/scripts'
if ($Action -eq 'mcp') {
    & "$projectRoot/.tools/node-v24.15.0-win-x64/node.exe" "$runtime/mcp-server.cjs"
} else {
    & "$projectRoot/.tools/bun-windows-x64/bun.exe" "$runtime/worker-service.cjs" $Action
}
exit $LASTEXITCODE
