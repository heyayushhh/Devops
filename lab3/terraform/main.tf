terraform {
  required_version = ">= 1.0.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

# Dedicated bridge network for Terraform-managed infrastructure
resource "docker_network" "app_network" {
  name   = var.network_name
  driver = "bridge"
  labels {
    label = "managed_by"
    value = "terraform"
  }
}

# Pull/use base container image
resource "docker_image" "app_image" {
  name         = var.image_name
  keep_locally = true
}

# Scalable container resources managed by count
resource "docker_container" "app_service" {
  count = var.replica_count

  name  = "${var.container_name_prefix}-${count.index + 1}"
  image = docker_image.app_image.image_id

  command = [
    "python", "-m", "http.server", "8080"
  ]

  env = [
    "APP_ENV=${var.environment}",
    "INSTANCE_ID=${count.index + 1}",
    "MANAGED_BY=terraform"
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }

  ports {
    internal = 8080
    external = var.base_host_port + count.index
  }

  labels {
    label = "managed_by"
    value = "terraform"
  }

  labels {
    label = "tier"
    value = "application"
  }
}
