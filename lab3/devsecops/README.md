# Task 4: DevSecOps — Security Vulnerability Scanning & Policy Enforcement

## Overview
DevSecOps embeds security analysis directly into the CI/CD pipeline lifecycle rather than treating security as an isolated post-build activity. In this task, container filesystem scanning, dependency vulnerability analysis, and image vulnerability auditing are automated using **Aqua Security Trivy**.

---

## Security Scanning Architecture

```
+--------------------------------------------------------------------------------+
|                             DevSecOps Pipeline                                 |
|                                                                                |
|  +--------------------+        +---------------------+        +-------------+  |
|  | Application Source | -----> | Trivy Filesystem    | -----> | Security    |  |
|  | & Dockerfile       |        | Vulnerability Scan  |        | Findings    |  |
|  +--------------------+        +---------------------+        | Pass / Fail |  |
|                                                               +-------------+  |
|  +--------------------+        +---------------------+               |         |
|  | Built Docker Image | -----> | Trivy Container     | --------------+         |
|  | lab3-demo-app:v1   |        | Image Scanning      |                         |
|  +--------------------+        +---------------------+                         |
+--------------------------------------------------------------------------------+
```

---

## Automated Security Commands

### 1. Filesystem Vulnerability Scan (PowerShell)
```powershell
docker run --rm -v "${PWD}:/src" aquasec/trivy:latest fs --severity HIGH,CRITICAL /src
```

### 2. Built Container Image Scan
```powershell
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL lab3-demo-app:latest
```

### 3. Dependency Audit (pip-audit / safety)
```powershell
python -m pip install pip-audit
pip-audit -r ../app/requirements.txt
```

---

## Severity Enforcement Policy
- **CRITICAL**: Fails build pipeline immediately.
- **HIGH**: Requires mitigation ticket and approved exception.
- **MEDIUM / LOW**: Logged for scheduled remediation cycles.

---

## Verification Evidence
The security scan verification screenshot is recorded in `lab3/evidence/screenshots/04-security-scan.png`.
