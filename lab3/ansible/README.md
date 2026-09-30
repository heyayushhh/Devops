# Lab 3 — Q1: Infrastructure Configuration Automation with Ansible

## Objective
Configure infrastructure and automate application configuration using Ansible by writing playbooks and applying them to target nodes.

## Architecture
- **Ansible Controller**: Containerized controller (`lab3-ansible-controller:latest`) based on `python:3.12-slim` with `ansible-core 2.21.4`, Docker CLI, and `community.docker 5.3.0` collection. Communicates directly with target nodes over Docker socket `/var/run/docker.sock`.
- **Target Nodes**: `lab3-ansible-node1` (staging) and `lab3-ansible-node2` (production) running on `lab3-net`.
- **Managed Application**: `lab3app` — lightweight Python HTTP microservice configured dynamically via Jinja2 template (`app.conf.j2`), managed via a pidfile service control script (`ctl.sh`), and verified via automated healthchecks (`healthcheck.py`).

## File Structure
- `ansible.cfg`: Controller configuration setting inventory path and disabling deprecation warnings.
- `inventory.ini`: Host inventory declaring target node connection parameters (`community.docker.docker`), port allocations, and environment tiers.
- `site.yml`: Top-level orchestration playbook importing the `app_config` role with post-task verification.
- `roles/app_config/`:
  - `defaults/main.yml`: Default application parameters.
  - `tasks/main.yml`: Tasks creating user/group, directories (`/opt/lab3app`, `/etc/lab3app`, `/var/log/lab3app`), templating `app.conf`, deploying python scripts, and ensuring service start.
  - `handlers/main.yml`: Handler to restart the service on configuration or code changes.
  - `templates/app.conf.j2`: Jinja2 template for `/etc/lab3app/app.conf`.
  - `files/`: `lab3app.py`, `healthcheck.py`, and `lab3app-ctl.sh`.

## Verification & Idempotency
- **First Execution**: All tasks executed, resulting in `ok=10 changed=7 failed=0`.
- **Second Execution**: Executed immediately after to demonstrate idempotency, resulting in `ok=9 changed=0 failed=0`.
- **State Validation**: Directly validated process status and healthcheck endpoints inside both target nodes.
