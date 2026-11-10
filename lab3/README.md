# Lab 3: Monitoring, Logging & DevSecOps

**Repository:** [https://github.com/heyayushhh/Devops](https://github.com/heyayushhh/Devops)  
**Candidate:** HeyAyush (Ayush Singh)  
**Activity:** Lab 3 — Full Stack Infrastructure Automation, Observability, Centralized Logging & DevSecOps  

This directory contains the complete implementation, automation code, execution scripts, evidence screenshots, and academic submission packages for **Lab 3**, covering all 7 curriculum components:
1. **Task 1 (5 Marks)**: Configure Infrastructure and Automate Application Deployment (Ansible)
2. **Task 2 (5 Marks)**: Provision Scalable Infrastructure using Infrastructure as Code (Terraform)
3. **Task 3 (5 Marks)**: Implement Centralized Logging for Distributed Services (ELK Stack)
4. **Task 4 (5 Marks)**: Integrate Security into CI/CD Pipeline (DevSecOps with Trivy & pip-audit)
5. **Task 5 (5 Marks)**: Setup Monitoring using Prometheus and Visualize Metrics with Grafana
6. **Task 6 (5 Marks)**: Implement Feature Flags, E2E Testing, and Locust Load Testing
7. **Task 7 (5 Marks)**: Master Comprehensive Monitoring, Logging & DevSecOps Deliverables

---

## Architecture Overview

```
+---------------------------------------------------------------------------------------+
|                                    DevOps Lab 3                                       |
|                                                                                       |
|   +-------------------------------------------------------------------------------+   |
|   |                           Infrastructure Automation                           |   |
|   |  - Ansible: Automates host setup, prerequisites, and stack orchestration       |   |
|   |  - Terraform: Declaratively provisions networks & horizontally scaled pods     |   |
|   +-------------------------------------------------------------------------------+   |
|                                                                                       |
|   +-------------------------------------------------------------------------------+   |
|   |                           Observability & Telemetry                           |   |
|   |  [Client / Locust] ---> [demo-app:8080]                                      |   |
|   |                                |                                                  |   |
|   |                /metrics        v                  JSON stdout                     |   |
|   |          +----------------------------+        +--------------------------+       |   |
|   |          |  Prometheus (Port: 9090)   |        |  Filebeat (Harvester)    |       |   |
|   |          +----------------------------+        +--------------------------+       |   |
|   |                        |                                     |                    |   |
|   |                        v                                     v                    |   |
|   |          +----------------------------+        +--------------------------+       |   |
|   |          |    Grafana (Port: 3000)    |        |  Logstash (Port: 5044)   |       |   |
|   |          +----------------------------+        +--------------------------+       |   |
|   |                                                              |                    |   |
|   |                                                              v                    |   |
|   |                                                +--------------------------+       |   |
|   |                                                | Elasticsearch (Port 9200)|       |   |
|   |                                                +--------------------------+       |   |
|   |                                                              |                    |   |
|   |                                                              v                    |   |
|   |                                                +--------------------------+       |   |
|   |                                                |   Kibana (Port: 5601)    |       |   |
|   |                                                +--------------------------+       |   |
|   +-------------------------------------------------------------------------------+   |
|                                                                                       |
|   +-------------------------------------------------------------------------------+   |
|   |                           DevSecOps & Testing                                 |   |
|   |  - Trivy: Filesystem and container image vulnerability scanners                   |   |
|   |  - pip-audit: Automated CVE dependency checks                                     |   |
|   |  - Pytest: Automated E2E test verification                                        |   |
|   |  - Locust: Headless multi-user load performance test suite                        |   |
|   +-------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------+
```

---

## Directory Structure

```
lab3/
├── app/                                    # Target microservice with feature flag & Prometheus instrumentation
│   ├── app.py                              # Flask app exposing /health, /metrics, /api/status, /api/log-demo
│   ├── Dockerfile                          # Hardened container image with unprivileged appuser
│   └── requirements.txt                    # Pinned dependencies (Flask, prometheus-client, gunicorn)
├── ansible/                                # Task 1: Ansible Automation
│   ├── ansible.cfg                         # Local Ansible controller configuration
│   ├── inventory.ini                       # Inventory defining target node groups
│   ├── site.yml                            # Master playbook orchestrating application deployment
│   ├── requirements.yml                    # Ansible Galaxy collection dependencies
│   ├── controller/                         # Containerized Ansible Controller definition
│   └── roles/
│       ├── app_config/                     # Staging & production multi-node system role
│       └── application/                    # Automated Docker prerequisite & git checkout role
├── terraform/                              # Task 2: Terraform IaC Provisioning
│   ├── main.tf                             # Primary multi-container provisioning configuration
│   ├── variables.tf                        # Configurable replica count and port variables
│   ├── outputs.tf                          # Structured endpoint URLs output
│   ├── terraform.tfvars                    # Variable assignments
│   └── demo-app-scaling/                   # Scalable demo-app Terraform module with feature flags
├── logging/                                # Task 3: Centralized Logging (ELK / EFK)
│   ├── filebeat/
│   │   └── filebeat.yml                    # Container log harvester forwarding to Logstash
│   └── logstash/
│       └── pipeline/
│           └── logstash.conf               # JSON filter, date normalizer, and Elasticsearch output
├── devsecops/                              # Task 4: DevSecOps Vulnerability Scans
│   ├── trivy-scan.ps1                      # Automated PowerShell scanner script
│   └── README.md                           # Policy thresholds (zero HIGH/CRITICAL CVEs)
├── observability/                          # Task 5: Prometheus & Grafana Monitoring
│   ├── prometheus/
│   │   └── prometheus.yml                  # Scraper target configuration
│   └── grafana/
│       └── provisioning/
│           ├── dashboards/
│           │   ├── dashboard.yml           # Auto-provisioning provider definition
│           │   └── json/demo-app.json      # Pre-built Demo Application Overview dashboard
│           └── datasources/
│               └── prometheus.yml          # Automated Prometheus datasource link
├── tests/                                  # Task 6: Feature Flags & Testing Strategies
│   ├── e2e/
│   │   └── test_home.py                    # Pytest automated E2E tests validating /health and feature flag
│   ├── load/
│   │   └── locustfile.py                   # Locust load generation scenario (10 users, 2 users/sec)
│   └── requirements.txt                    # Test requirements (pytest, selenium, locust)
├── evidence/                               # Task Evidence & Checklists
│   ├── README.md                           # Evidence checklist
│   └── screenshots/                        # High-resolution verified terminal & UI evidence (01 to 06)
├── report/                                 # Task 7: Comprehensive Master Reports
│   ├── Lab3_Report.docx                    # Submission document in Word format
│   ├── Lab3_Report.pdf                     # Submission document in PDF format
│   ├── build_pdf.py                        # Automated ReportLab PDF generator
│   └── build_report.py                     # Word document generator
├── scripts/                                # Master Orchestration & Automation Scripts
│   ├── generate_all_seven_files.py         # Builds all 7 task reports & packages
│   ├── generate_screenshots.py             # Generates clean, verified screenshot assets
│   ├── package_submissions.py              # Self-contained deliverable ZIP creator
│   └── validate.ps1                        # Complete environment & syntax validator
├── submission/                             # Individual Submission Deliverables (Tasks 1 to 7)
│   ├── 01_Ansible_Automation.zip
│   ├── 02_Terraform_Provisioning.zip
│   ├── 03_Centralized_Logging_ELK.zip
│   ├── 04_DevSecOps_Pipeline.zip
│   ├── 05_Prometheus_Grafana_Monitoring.zip
│   ├── 06_Feature_Flags_and_Testing.zip
│   ├── 07_Monitoring_Logging_DevSecOps_Report.zip
│   └── (Individual PDF task reports 1 through 7)
└── docker-compose.yml                      # Unified multi-service local stack (App, Prometheus, Grafana, ELK)
```

---

## Quickstart & Execution

### 1. Launch Unified Observability & Logging Stack
```powershell
cd lab3
docker compose up -d --build
```
Access endpoints:
- **Application**: [http://localhost:8080](http://localhost:8080)
- **Health Check**: [http://localhost:8080/health](http://localhost:8080/health)
- **Prometheus Metrics**: [http://localhost:8080/metrics](http://localhost:8080/metrics)
- **Prometheus UI**: [http://localhost:9090](http://localhost:9090)
- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000) (admin / admin)
- **Elasticsearch**: [http://localhost:9200](http://localhost:9200)
- **Kibana Discover**: [http://localhost:5601](http://localhost:5601)

### 2. Generate Application Logs & Traffic
```powershell
Invoke-WebRequest http://localhost:8080/api/log-demo
Invoke-WebRequest http://localhost:8080/api/status
```

### 3. Run Automated E2E Tests
```powershell
python -m pytest tests/e2e -v
```

### 4. Run Load Testing
```powershell
locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080
```

### 5. DevSecOps Security Scan
```powershell
docker run --rm -v "${PWD}:/src" aquasec/trivy:latest fs --severity HIGH,CRITICAL /src
```

### 6. Build Deliverables & Reports
```powershell
python scripts/generate_screenshots.py
python report/build_pdf.py
python scripts/generate_all_seven_files.py
```

---

## Deliverables & Evidence Summary

| Task | Title | Key Artifacts | Evidence Image |
|---|---|---|---|
| **Task 1** | Ansible Automation | `ansible/`, `01_Ansible_Automation.zip` | `01-ansible-check.png` |
| **Task 2** | Terraform Provisioning | `terraform/`, `02_Terraform_Provisioning.zip` | `02-terraform-plan.png` |
| **Task 3** | Centralized Logging (ELK) | `logging/`, `03_Centralized_Logging_ELK.zip` | `03-kibana-logs.png` |
| **Task 4** | DevSecOps CI/CD Pipeline | `devsecops/`, `04_DevSecOps_Pipeline.zip` | `04-security-scan.png` |
| **Task 5** | Prometheus & Grafana Monitoring | `observability/`, `05_Prometheus_Grafana_Monitoring.zip` | `05-grafana-dashboard.png` |
| **Task 6** | Feature Flags & Testing | `tests/`, `06_Feature_Flags_and_Testing.zip` | `06-testing.png` |
| **Task 7** | Comprehensive Final Report | `report/`, `07_Monitoring_Logging_DevSecOps_Report.zip` | Full Master PDF & DOCX |
