# Enable WSL feature on Windows if not already enabled
wsl --install

# Install WSL (if not already installed)
if (!(Get-Command wsl -ErrorAction SilentlyContinue)) {
    Write-Host "WSL is not installed, installing WSL..."
    Invoke-WebRequest -Uri "https://aka.ms/wsl-install" -OutFile "wsl_install.ps1"
    powershell -ExecutionPolicy Bypass -File "wsl_install.ps1"
}

# Install Ubuntu 22.04 LTS if not installed already
$ubuntuInstalled = wsl -l --verbose | Select-String -Pattern "Ubuntu-22.04"
if (-not $ubuntuInstalled) {
    Write-Host "Installing Ubuntu 22.04 LTS..."
    wsl --install -d Ubuntu-22.04
}

# Set Ubuntu 22.04 as the default distribution
wsl --set-default Ubuntu-22.04

# Ensure WSL version 2 is being used for Ubuntu
wsl --set-version Ubuntu-22.04 2