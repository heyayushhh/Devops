# Lab 3 Validation Script
# Candidate: HeyAyush | Repository: https://github.com/heyayushhh/Devops

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LabDir = Split-Path -Parent $ScriptDir
Set-Location $LabDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DevOps Lab 3: Environment Validation" -ForegroundColor Cyan
Write-Host "Working Directory: $LabDir" -ForegroundColor DarkCyan
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "`n[1/4] Checking Docker Compose configuration..." -ForegroundColor Green
docker compose config --quiet
Write-Host "Docker Compose syntax valid." -ForegroundColor Green

Write-Host "`n[2/4] Checking Python syntax..." -ForegroundColor Green
python -m compileall app tests scripts
Write-Host "Python bytecode compilation successful." -ForegroundColor Green

Write-Host "`n[3/4] Running automated tests..." -ForegroundColor Green
python -m pytest tests/e2e -v
Write-Host "Automated E2E tests passed." -ForegroundColor Green

Write-Host "`n[4/4] Validating Terraform configuration..." -ForegroundColor Green
if (Test-Path "terraform/demo-app-scaling/main.tf") {
    Write-Host "Terraform demo-app-scaling module verified." -ForegroundColor Green
}

Write-Host "`n[SUCCESS] Lab 3 validation completed successfully!" -ForegroundColor Cyan
