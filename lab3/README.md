# Lab 3 — Ansible Configuration & Terraform Infrastructure as Code (IaC)

This directory contains the full implementation, execution logs, evidence screenshots, and technical reports for **Lab 3**:
- **Q1 (5 Marks)**: Configure infrastructure and automate application configuration using Ansible playbooks applied to target nodes.
- **Q2 (5 Marks)**: Provision scalable infrastructure using Terraform (IaC): write configuration files, initialize, plan, apply, and scale infrastructure.

---

## Directory Structure

```
lab3/
├── ansible/
│   ├── ansible.cfg              # Ansible configuration
│   ├── inventory.ini            # Target node inventory with custom vars
│   ├── site.yml                 # Master playbook applying app_config role
│   ├── controller/
│   │   ├── Dockerfile           # Controller container definition
│   │   ├── community-docker-5.3.0.tar.gz
│   │   └── community-library_inventory_filtering_v1-1.1.5.tar.gz
│   ├── roles/
│   │   └── app_config/          # Structured role for lab3app service
│   │       ├── defaults/main.yml
│   │       ├── files/ (app.py, healthcheck.py, lab3app-ctl.sh)
│   │       ├── handlers/main.yml
│   │       ├── tasks/main.yml
│   │       └── templates/app.conf.j2
│   ├── README.md
│   └── commands.txt
├── terraform/
│   ├── main.tf                  # Provider, docker network, image & scalable containers
│   ├── variables.tf             # Input variables & replica validation
│   ├── outputs.tf               # Structured outputs
│   ├── terraform.tfvars         # Configuration variables (replica_count = 4)
│   ├── README.md
│   └── commands.txt
├── tools/
│   ├── terraform.exe            # Terraform v1.13.3 binary
│   └── ansiblew.py              # Windows locale wrapper for ansible CLI
├── screenshots/                 # 17 Evidence screenshots (01 to 17)
├── reports/                     # Formal PDF Technical Reports
│   ├── Lab3_Ansible_Infrastructure_Report.pdf
│   ├── Lab3_Terraform_Infrastructure_Report.pdf
│   └── Lab3_Tools_Documents.pdf
├── commands.txt                 # Master end-to-end command reference
└── Lab3_Tools_Documents.zip     # Complete submission package
```

---

## Summary of Results

### Q1 — Ansible Configuration Automation
- **Controller**: Dockerized `lab3-ansible-controller:latest` with `ansible-core 2.21.4` and `community.docker 5.3.0` communicating via mounted `/var/run/docker.sock`.
- **Target Nodes**: `lab3-ansible-node1` (staging, port 8081) and `lab3-ansible-node2` (production, port 8082).
- **Playbook**: Applied `app_config` role deploying system user/group, directories, Jinja2 config template, Python HTTP microservice, and control script.
- **Execution & Idempotency**: Run 1 applied 7 changes (`ok=10 changed=7`). Run 2 confirmed 100% idempotency (`ok=9 changed=0 failed=0`).

### Q2 — Terraform Scalable Infrastructure (IaC)
- **Engine**: `terraform v1.13.3` with `kreuzwerker/docker v3.0.2` provider.
- **Initial Provisioning**: Created `lab3-tf-net` bridge network, pulled `python:3.12-slim`, and deployed `replica_count = 2` container instances (`lab3-tf-app-1` on port 8181, `lab3-tf-app-2` on port 8182).
- **Dynamic Scaling (2 → 4 Replicas)**: Modified `replica_count = 4`, planned, and applied. Deployed `lab3-tf-app-3` (port 8183) and `lab3-tf-app-4` (port 8184). Verified HTTP 200 responses across all 4 replicas.
