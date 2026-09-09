param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$AbletonScriptsRoot = "C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts",
    [switch]$BackupExisting
)

$ErrorActionPreference = "Stop"

$source = Join-Path $RepoRoot "ClaudeMCP_Remote"
$destination = Join-Path $AbletonScriptsRoot "ClaudeMCP_Remote"

if (-not (Test-Path $source)) {
    throw "Source control surface not found: $source"
}

if (-not (Test-Path $AbletonScriptsRoot)) {
    throw "Ableton MIDI Remote Scripts directory not found: $AbletonScriptsRoot"
}

if ($BackupExisting -and (Test-Path $destination)) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "${destination}.backup.$timestamp"
    Move-Item -Path $destination -Destination $backupPath
    Write-Host "Backed up existing installation to $backupPath"
}
elseif (Test-Path $destination) {
    Remove-Item -Recurse -Force $destination
}

Copy-Item -Recurse -Force $source $destination

Write-Host "Installed ClaudeMCP_Remote to $destination"
Write-Host "Next step: restart Ableton Live and select ClaudeMCP_Remote as a Control Surface."
