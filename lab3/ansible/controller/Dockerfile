# Lab 3 — Ansible controller image (Linux)
# Native Windows cannot run the ansible-core controller (no fcntl module on
# Windows), so the controller runs here and manages Docker target nodes
# through the mounted Docker socket via the community.docker connection plugin.
#
# Notes:
# - community.docker >= 3 drives target containers through the docker CLI
#   (not the Python SDK), so the CLI binary is copied from the docker:cli image.
# - Ansible collections are installed from local tarballs (downloaded from
#   galaxy.ansible.com) because the build host's link to Galaxy is slow;
#   pip packages install from PyPI directly.
FROM docker:cli AS docker-cli

FROM python:3.12-slim

# docker CLI for the community.docker connection plugin
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

# ansible-core + Docker SDK (used by verification modules)
RUN pip install --no-cache-dir ansible-core docker

# Collections from local artifacts: dependency first, then community.docker
COPY community-library_inventory_filtering_v1-1.1.5.tar.gz /tmp/
COPY community-docker-5.3.0.tar.gz /tmp/
RUN ansible-galaxy collection install /tmp/community-library_inventory_filtering_v1-1.1.5.tar.gz -p /usr/share/ansible/collections \
    && ansible-galaxy collection install /tmp/community-docker-5.3.0.tar.gz -p /usr/share/ansible/collections \
    && ansible-galaxy collection list | grep -E "community"

WORKDIR /workspace

# The controller is driven by `docker run`; no long-running process needed
CMD ["sleep", "infinity"]
