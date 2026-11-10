# DevSecOps Security Scan Script (PowerShell)
# Repository: https://github.com/heyayushhh/Devops

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DevOps Lab 3: DevSecOps Vulnerability Scan" -ForegroundColor Cyan
Write-Host "Candidate: HeyAyush | Repo: heyayushhh/Devops" -ForegroundColor DarkCyan
Write-Host "==========================================" -ForegroundColor Cyan

$RepoRoot = (Resolve-Path "$PSScriptRoot\..").Path
Write-Host "[INFO] Scanning workspace directory: $RepoRoot" -ForegroundColor Yellow

# 1. Run Trivy Filesystem Scan
Write-Host "`n[STEP 1] Running Trivy Filesystem Scan (Severity: HIGH, CRITICAL)..." -ForegroundColor Green
docker run --rm -v "${RepoRoot}:/src" aquasec/trivy:latest fs --severity HIGH,CRITICAL --scanners vuln,secret,misconfig /src

# 2. Run Trivy Image Scan (if image exists)
$ImageName = "lab3-demo-app:latest"
$imageExists = docker images -q $ImageName
if ($imageExists) {
    Write-Host "`n[STEP 2] Running Trivy Image Scan for $ImageName..." -ForegroundColor Green
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL $ImageName
} else {
    Write-Host "`n[NOTICE] Image $ImageName not built locally yet; skipping image scan." -ForegroundColor DarkYellow
}

Write-Host "`n[SUCCESS] DevSecOps security assessment pipeline completed." -ForegroundColor Cyan
