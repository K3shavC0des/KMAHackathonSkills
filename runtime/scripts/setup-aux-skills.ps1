[CmdletBinding()]
param([switch]$SkipDownloads, [string]$Actor)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$tools = Join-Path $root '.tools'
$downloads = Join-Path $tools 'downloads'
$nodeVersion = '24.15.0'
$nodeDir = Join-Path $tools "node-v$nodeVersion-win-x64"
$bunDir = Join-Path $tools 'bun-windows-x64'
$runtime = Join-Path $tools 'runtime'

New-Item -ItemType Directory -Force $downloads | Out-Null

function Get-Archive($url, $file, $destination) {
    $archive = Join-Path $downloads $file
    if (-not (Test-Path $destination)) {
        if (-not (Test-Path $archive)) { Invoke-WebRequest $url -OutFile $archive -UseBasicParsing }
        Expand-Archive $archive -DestinationPath $tools -Force
    }
}

if (-not $SkipDownloads) {
    Get-Archive "https://nodejs.org/dist/v$nodeVersion/node-v$nodeVersion-win-x64.zip" "node-$nodeVersion.zip" $nodeDir
    Get-Archive 'https://github.com/oven-sh/bun/releases/latest/download/bun-windows-x64.zip' 'bun-windows-x64.zip' $bunDir
}

$node = Join-Path $nodeDir 'node.exe'
$npm = Join-Path $nodeDir 'npm.cmd'
if (-not (Test-Path $node) -or -not (Test-Path $npm)) { throw "Node.js runtime missing. Rerun without -SkipDownloads." }
$env:Path = "$nodeDir;$bunDir;$env:Path"

if (-not (Test-Path (Join-Path $runtime 'node_modules/claude-mem'))) {
    & $npm install --prefix $runtime claude-mem@15.18.3 --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'Claude Mem installation failed.' }
}

$uvCache = Join-Path $tools 'uv-cache'
$uvTools = Join-Path $tools 'uv-tools'
$uvPython = Join-Path $tools 'uv-python'
$env:UV_CACHE_DIR = $uvCache
$env:UV_TOOL_DIR = $uvTools
$env:UV_PYTHON_INSTALL_DIR = $uvPython
$uv = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uv -and -not $SkipDownloads) {
    Get-Archive 'https://github.com/astral-sh/uv/releases/download/0.9.17/uv-x86_64-pc-windows-msvc.zip' 'uv-windows.zip' (Join-Path $tools 'uv.exe')
}
$uvBinary = if ($uv) { $uv.Source } else { Join-Path $tools 'uv.exe' }
if (Test-Path $uvBinary) {
    & $uvBinary python install 3.13
    if ($LASTEXITCODE -ne 0) { throw 'Python installation failed.' }
    & $uvBinary tool install --python 3.13 'headroom-ai[all]==0.44.0'
    if ($LASTEXITCODE -ne 0) { throw 'Headroom installation failed.' }
    & $uvBinary tool install --python 3.13 graphifyy==0.9.108
    if ($LASTEXITCODE -ne 0) { throw 'Graphify installation failed.' }
} else { throw 'uv is missing. Rerun without -SkipDownloads.' }

New-Item -ItemType Directory -Force (Join-Path $root '.local/claude-mem') | Out-Null
if ($Actor) {
    $request = @{ actor = $Actor; action = 'init' } | ConvertTo-Json -Compress
    $request | & $node (Join-Path $root '.agents/skills/hackathon-autopilot/scripts/board.mjs')
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Hackathon board initialization failed; rerun with -Actor.' }
}
Write-Host ''
Write-Host 'Auxiliary skills are ready for this project.' -ForegroundColor Green
Write-Host 'Packages installed; recording hooks and live model requests require separate verification.'
Write-Host 'Start memory: .\scripts\memory.ps1 start'
Write-Host 'Check memory: .\scripts\memory.ps1 status'
Write-Host 'Codex MCP config: .codex\config.toml'
Write-Host 'Provider sign-in: run codex login if Codex is not authenticated.'
Write-Host 'Optional team board: .\scripts\setup-aux-skills.ps1 -SkipDownloads -Actor your-handle'
