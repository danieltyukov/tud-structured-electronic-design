[CmdletBinding()]
param(
    [switch]$Dry
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Design knobs (same defaults as run.sh)
$N_RI = "0.2"
$R_I = "5000"
$MOS_TYPE_GMCISS = "P"
$N_M = "0.5"
$MOS_TYPE_WLID = "P"
$W_FINGER = "10"
$CHANNEL_LENGTH = "0.18"
$MOS_TYPE_CTRL = "P"

$venvPython = Join-Path (Join-Path (Split-Path -Parent $PSScriptRoot) ".venv") "Scripts\python.exe"

function Get-Runner {
    if (Test-Path $venvPython) {
        return @{ Name = $venvPython; Args = @() }
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @{ Name = "py"; Args = @("-3") }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{ Name = "python"; Args = @() }
    }
    throw "Python not found. Run .\setup_windows_slicap.ps1 first."
}

$runner = Get-Runner

if ($Dry) {
    Write-Host "=== Design Knob Parameters ==="
    Write-Host ""
    Write-Host "  Step 5: n_Ri           = $N_RI"
    Write-Host "  Step 5: R_i            = $R_I Ohm"
    Write-Host "  Step 7: mosType        = $MOS_TYPE_GMCISS"
    Write-Host "  Step 7: n_M            = $N_M"
    Write-Host "  Step 8: mosType        = $MOS_TYPE_WLID"
    Write-Host "  Step 8: W_finger       = $W_FINGER um"
    Write-Host "  Step 8: Channel length = $CHANNEL_LENGTH um"
    Write-Host "  Step 9: mosType        = $MOS_TYPE_CTRL"
    Write-Host ""
    $budget = ([double]$N_RI + [double]$N_M + 0.02)
    Write-Host ("  Noise budget: n_SRC(~0.02) + {0} + {1} = {2}" -f $N_RI, $N_M, $budget)
    Write-Host ""
    Write-Host "Would run: $($runner.Name) $($runner.Args -join ' ') hlr_main.py (with piped inputs)"
    exit 0
}

Write-Host "=== Hearing Loop Receiver - EE4109 Design Pipeline (Windows) ==="
Write-Host ""
Write-Host "Design knobs:"
Write-Host "  n_Ri           = $N_RI"
Write-Host "  R_i            = $R_I Ohm"
Write-Host "  mosType        = $MOS_TYPE_GMCISS"
Write-Host "  n_M            = $N_M"
Write-Host "  W_finger       = $W_FINGER um"
Write-Host "  Channel length = $CHANNEL_LENGTH um"
Write-Host ""
Write-Host "Running pipeline..."
Write-Host ""

$inputs = @(
    $N_RI,
    $R_I,
    $MOS_TYPE_GMCISS,
    $N_M,
    $MOS_TYPE_WLID,
    $W_FINGER,
    $CHANNEL_LENGTH,
    $MOS_TYPE_CTRL
)

$stdinPayload = ($inputs -join [Environment]::NewLine) + [Environment]::NewLine
$stdinPayload | & $runner.Name @($runner.Args + "hlr_main.py")

if ($LASTEXITCODE -ne 0) {
    throw "Pipeline failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=== Pipeline complete ==="
Write-Host "Open html\index.html to view results."
