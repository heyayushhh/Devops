FROM ubuntu:latest

WORKDIR /usr/share/grafana

# Copy and extract Grafana release
COPY downloads/grafana.tar.gz /tmp/
RUN tar -xzf /tmp/grafana.tar.gz -C /tmp && \
    cp -r /tmp/grafana-v10.4.1/* /usr/share/grafana/ && \
    mkdir -p /var/lib/grafana /var/log/grafana /etc/grafana/provisioning /var/lib/grafana/dashboards && \
    rm -rf /tmp/grafana*

ENV GF_PATHS_PROVISIONING=/etc/grafana/provisioning \
    GF_PATHS_CONFIG=/usr/share/grafana/conf/defaults.ini \
    GF_PATHS_DATA=/var/lib/grafana \
    GF_PATHS_LOGS=/var/log/grafana \
    GF_PATHS_PLUGINS=/var/lib/grafana/plugins \
    GF_SECURITY_ADMIN_USER=admin \
    GF_SECURITY_ADMIN_PASSWORD=admin \
    GF_USERS_ALLOW_SIGN_UP=false \
    GF_AUTH_ANONYMOUS_ENABLED=true \
    GF_AUTH_ANONYMOUS_ORG_ROLE=Admin

COPY grafana/provisioning /etc/grafana/provisioning
COPY grafana/dashboards /var/lib/grafana/dashboards

EXPOSE 3000

ENTRYPOINT ["/usr/share/grafana/bin/grafana-server", "--homepath=/usr/share/grafana"]
