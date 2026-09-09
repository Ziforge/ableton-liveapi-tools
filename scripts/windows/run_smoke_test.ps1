param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$TargetHost = "127.0.0.1",
    [int]$Port = 9004,
    [string]$PythonLauncher = "py",
    [string]$LogFile = ""
)

$ErrorActionPreference = "Stop"

$clientPath = Join-Path $RepoRoot "scripts\poc\smoke_test_client.py"
$logsDir = Join-Path $RepoRoot "logs"

if (-not (Test-Path $clientPath)) {
    throw "Smoke test client not found: $clientPath"
}

if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

if (-not $LogFile) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $LogFile = Join-Path $logsDir "smoke-test-$timestamp.txt"
}

Write-Host "Checking Windows listener state on port $Port..."
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
    Format-Table -AutoSize LocalAddress, LocalPort, State, OwningProcess

Write-Host ""
Write-Host "Running smoke test client..."
& $PythonLauncher -3 $clientPath --host $TargetHost --port $Port --log-file $LogFile

Write-Host ""
Write-Host "Raw request/response capture saved to $LogFile"
