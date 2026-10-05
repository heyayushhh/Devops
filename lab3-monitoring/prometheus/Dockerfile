FROM ubuntu:latest

WORKDIR /etc/prometheus

# Copy and extract prometheus release
COPY downloads/prometheus.tar.gz /tmp/
RUN tar -xzf /tmp/prometheus.tar.gz -C /tmp && \
    cp /tmp/prometheus-2.51.0.linux-amd64/prometheus /bin/ && \
    cp /tmp/prometheus-2.51.0.linux-amd64/promtool /bin/ && \
    mkdir -p /usr/share/prometheus/console_libraries /usr/share/prometheus/consoles /prometheus && \
    cp -r /tmp/prometheus-2.51.0.linux-amd64/console_libraries/* /usr/share/prometheus/console_libraries/ && \
    cp -r /tmp/prometheus-2.51.0.linux-amd64/consoles/* /usr/share/prometheus/consoles/ && \
    rm -rf /tmp/prometheus*

COPY prometheus/prometheus.yml /etc/prometheus/prometheus.yml

EXPOSE 9090

ENTRYPOINT ["/bin/prometheus"]
CMD ["--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus", "--web.enable-lifecycle"]
