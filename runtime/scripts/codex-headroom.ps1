$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$headroom = Join-Path $projectRoot '.tools/uv-tools/headroom-ai/Scripts/headroom.exe'
if (-not (Test-Path $headroom)) { throw 'Run scripts/setup-aux-skills.ps1 first.' }
$codex = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codex) {
    $binary = Get-ChildItem "$env:USERPROFILE/.codex/packages/standalone/releases/*/bin/codex.exe" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $binary) { throw 'Install the Codex CLI or add it to PATH first.' }
    $env:Path = "$($binary.DirectoryName);$env:Path"
}
$env:HEADROOM_OFFLINE = '1'
Push-Location $projectRoot
try { & $headroom wrap codex @args; $result = $LASTEXITCODE }
finally { Pop-Location }
exit $result
