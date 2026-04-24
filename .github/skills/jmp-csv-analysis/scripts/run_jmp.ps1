# Runs a JMP JSL script headless via command line
# Usage: .\run_jmp.ps1 -ScriptPath "path\to\script.jsl"
param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptPath
)

$JmpExe = "C:\Program Files\SAS\JMPPRO\17\jmp.exe"

if (-not (Test-Path $JmpExe)) {
    Write-Error "JMP Pro 17 not found at: $JmpExe"
    exit 1
}

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script not found: $ScriptPath"
    exit 1
}

$ScriptPath = Resolve-Path $ScriptPath
Write-Host "Running JMP script: $ScriptPath"
& $JmpExe $ScriptPath
Write-Host "JMP execution completed."
