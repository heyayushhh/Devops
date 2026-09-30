docker_host           = "npipe:////./pipe/docker_engine"
network_name          = "lab3-tf-net"
image_name            = "python:3.12-slim"
container_name_prefix = "lab3-tf-app"
replica_count         = 4
base_host_port        = 8181
environment           = "production"
