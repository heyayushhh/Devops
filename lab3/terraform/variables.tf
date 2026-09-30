variable "docker_host" {
  description = "Docker daemon connection URI (npipe on Windows, unix socket on Linux)"
  type        = string
  default     = "npipe:////./pipe/docker_engine"
}

variable "network_name" {
  description = "Name of the bridge network to create"
  type        = string
  default     = "lab3-tf-net"
}

variable "image_name" {
  description = "Docker image to deploy"
  type        = string
  default     = "python:3.12-slim"
}

variable "container_name_prefix" {
  description = "Prefix for container names"
  type        = string
  default     = "lab3-tf-app"
}

variable "replica_count" {
  description = "Number of scalable application container instances"
  type        = number
  default     = 2

  validation {
    condition     = var.replica_count >= 1 && var.replica_count <= 10
    error_message = "Replica count must be between 1 and 10."
  }
}

variable "base_host_port" {
  description = "Base host port for container port forwarding"
  type        = number
  default     = 8181
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "production"
}
