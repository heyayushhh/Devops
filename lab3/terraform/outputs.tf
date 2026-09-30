output "network_id" {
  description = "ID of the created Docker network"
  value       = docker_network.app_network.id
}

output "network_name" {
  description = "Name of the created Docker network"
  value       = docker_network.app_network.name
}

output "replica_count" {
  description = "Current number of provisioned replicas"
  value       = var.replica_count
}

output "container_instances" {
  description = "Details of provisioned container replicas"
  value = [
    for c in docker_container.app_service : {
      id        = c.id
      name      = c.name
      image     = c.image
      ip_address = c.network_data[0].ip_address
      host_port = c.ports[0].external
    }
  ]
}
