[CmdletBinding()]
param(
    [switch]$Dry
)

$ErrorActionPreference = "Stop"

# hlr_main.py already imports all simulation modules in the correct order.
$argsForRun = @()
if ($Dry) {
    $argsForRun += "-Dry"
}

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "run.ps1") @argsForRun
exit $LASTEXITCODE
