[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $repoRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

function Get-PythonCommand {
    $candidates = @(
        @{ Name = "py"; Args = @("-3.12") },
        @{ Name = "py"; Args = @("-3.11") },
        @{ Name = "py"; Args = @("-3.10") },
        @{ Name = "py"; Args = @("-3") },
        @{ Name = "python"; Args = @() }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Name -ErrorAction SilentlyContinue)) {
            continue
        }
        try {
            & $candidate.Name @($candidate.Args + "--version") | Out-Null
            if ($LASTEXITCODE -eq 0) {
                return $candidate
            }
        } catch {
        }
    }

    return $null
}

$python = Get-PythonCommand
if (-not $python) {
    throw "Python is not installed (or not on PATH). Install Python 3.10+ first, then rerun this script."
}

if ((Test-Path $venvPath) -and -not $Force) {
    Write-Host "Using existing virtual environment: $venvPath"
} else {
    if (Test-Path $venvPath) {
        Write-Host "Recreating virtual environment: $venvPath"
        Remove-Item -Recurse -Force $venvPath
    } else {
        Write-Host "Creating virtual environment: $venvPath"
    }

    & $python.Name @($python.Args + "-m" + "venv" + $venvPath)
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create virtual environment."
    }
}

if (-not (Test-Path $venvPython)) {
    throw "Virtual environment python not found at $venvPython"
}

Write-Host "Upgrading pip/setuptools/wheel..."
& $venvPython -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upgrade pip tooling."
}

Write-Host "Installing SLiCAP + required scientific packages..."
& $venvPython -m pip install SLiCAP sympy numpy scipy
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install SLiCAP dependencies."
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "Next run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\run.ps1"
