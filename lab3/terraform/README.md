# Lab 3 — Q2: Scalable Infrastructure Provisioning with Terraform (IaC)

## Objective
Provision scalable infrastructure using Terraform (Infrastructure as Code): write configuration files, initialize, plan, and apply the infrastructure, demonstrating dynamic scaling from 2 to 4 replicas.

## Architecture
- **Provider**: `kreuzwerker/docker` (version `~> 3.0.2`) interacting with the local Docker Engine on Windows via named pipe `npipe:////./pipe/docker_engine`.
- **Network**: Dedicated Docker bridge network (`lab3-tf-net`).
- **Scalable Workload**: Python HTTP service container instances (`lab3-tf-app-1`, `lab3-tf-app-2`, `lab3-tf-app-3`, `lab3-tf-app-4`) mapped to host ports `8181`, `8182`, `8183`, and `8184`.
- **Scaling Mechanism**: Dynamic `count = var.replica_count` with input validation (`1 <= replica_count <= 10`).

## File Structure
- `main.tf`: Defines the required Terraform and Docker provider version, `docker_network`, `docker_image`, and scalable `docker_container` resources.
- `variables.tf`: Defines configurable variables (`docker_host`, `network_name`, `image_name`, `container_name_prefix`, `replica_count`, `base_host_port`, `environment`) with strict validation rules.
- `outputs.tf`: Exports structured network information, active replica counts, and container instance IP and port metadata.
- `terraform.tfvars`: Input variable definitions setting `replica_count = 4`.

## Execution Lifecycle
1. **Initialize (`terraform init`)**: Installed the `kreuzwerker/docker` provider plugin and generated `.terraform.lock.hcl`.
2. **Validate (`terraform validate`)**: Validated syntax, provider block constraints, and schema conformance.
3. **Plan 1 (`terraform plan`)**: Evaluated initial creation plan for 2 replicas (4 resources to add).
4. **Apply 1 (`terraform apply -auto-approve`)**: Successfully provisioned `lab3-tf-net`, image, and 2 containers.
5. **Scale Plan & Apply (2 → 4)**: Updated `replica_count = 4` in `terraform.tfvars`, planned and applied infrastructure expansion to 4 container replicas.
6. **State & Endpoint Validation**: Validated all 4 running containers and confirmed HTTP 200 responses across ports `8181`, `8182`, `8183`, `8184`.
