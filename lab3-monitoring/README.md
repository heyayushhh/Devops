# Lab 3: Monitoring & Observability with Prometheus and Grafana

## 1. Objective
The primary objective of this laboratory assignment is to design, deploy, and verify an end-to-end cloud-native monitoring and observability pipeline. A target Python HTTP microservice exposes real application metrics in Prometheus exposition format. Prometheus is configured to scrape and store time-series telemetry, and Grafana is integrated as a visualization platform providing real-time operational intelligence across critical system health and performance indicators.

---

## 2. Architecture & Pipeline

```
+-------------------------------------------------------------------------------+
|                                Docker Host                                    |
|                                                                               |
|  +---------------------+      /metrics       +-----------------------------+  |
|  | Target Application  | -----------------> |         Prometheus          |  |
|  | (Python Microserv)  |    (Scrape: 5s)    |     (Time-Series TSDB)      |  |
|  |  Port: 8000         |                    |         Port: 9090          |  |
|  +---------------------+                    +-----------------------------+  |
|            ^                                               |                 |
|            | Traffic                                       | PromQL Queries  |
|            |                                               v                 |
|  +---------------------+                    +-----------------------------+  |
|  | Traffic Generator   |                    |           Grafana           |  |
|  | (Load & Test Suite) |                    |     (Visual Dashboards)     |  |
|  +---------------------+                    |         Port: 3000          |  |
|                                             +-----------------------------+  |
|                     Isolated Network: lab3-monitoring-net                     |
+-------------------------------------------------------------------------------+
```

The data flow operates continuously through four distinct stages:
1. **Target Application (`lab3-monitoring-app:8000`)**: Processes client requests and updates thread-safe Prometheus counters, histograms, and gauges.
2. **Metrics Exposition (`/metrics`)**: Formats live telemetry according to the standard Prometheus text-based exposition protocol.
3. **Prometheus Scraper (`lab3-prometheus:9090`)**: Periodically polls the target service at 5-second scrape intervals and ingests data into its local TSDB.
4. **Grafana Analytics (`lab3-grafana:3000`)**: Evaluates PromQL queries via proxy datasource to render dynamic visual panels and dashboards.

---

## 3. System Components

| Component | Container Name | Base Image / Version | Host Port | Network | Role |
|---|---|---|---|---|---|
| **Target App** | `lab3-monitoring-app` | `python:3.12-slim` | `8000:8000` | `lab3-monitoring-net` | Production HTTP service exposing `/metrics` |
| **Prometheus** | `lab3-prometheus` | `prom/prometheus v2.51.0` | `9090:9090` | `lab3-monitoring-net` | Metrics collection engine, TSDB, & PromQL evaluator |
| **Grafana** | `lab3-grafana` | `grafana/grafana v10.4.1` | `3000:3000` | `lab3-monitoring-net` | Visualization server & interactive dashboards |

---

## 4. Target Application Design
The target microservice is implemented in Python using the official `prometheus_client` library. It exposes several endpoints:
- `GET /`: Returns JSON service status and endpoints list (`HTTP 200`).
- `GET /health`: Returns service health and uptime in seconds (`HTTP 200`).
- `GET /metrics`: Returns standard Prometheus text-based exposition metrics (`HTTP 200`).
- `GET /api/data`: Returns business payload for operational simulation (`HTTP 200`).
- `POST /api/data`: Creates new data records for method testing (`HTTP 201`).
- `GET /api/error`: Simulates server exceptions for error monitoring (`HTTP 500`).
- `* /notfound`: Handles invalid routes (`HTTP 404`).

---

## 5. Metrics Exposed

| Metric Name | Type | Labels | Description |
|---|---|---|---|
| `http_requests_total` | Counter | `method`, `endpoint`, `status` | Cumulative count of all HTTP requests processed by endpoint and status. |
| `http_request_duration_seconds` | Histogram | `method`, `endpoint` | Request execution latency distribution in seconds across buckets. |
| `app_uptime_seconds` | Gauge | — | Total continuous uptime of the application process in seconds. |
| `app_info` | Info | `app_name`, `version`, `environment`, `maintainer` | Static application metadata and release version. |
| `up` | Gauge (Standard) | `job`, `instance` | Standard Prometheus liveness probe (1 = UP, 0 = DOWN). |

---

## 6. Prometheus Configuration (`prometheus.yml`)
```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'lab3-monitoring-app'
    scrape_interval: 5s
    metrics_path: '/metrics'
    static_configs:
      - targets: ['lab3-monitoring-app:8000']
```

---

## 7. Grafana Provisioning
Grafana is fully automated using infrastructure-as-code provisioning:
- **Datasource Provisioning (`prometheus-datasource.yml`)**: Automatically establishes `http://lab3-prometheus:9090` as the default Prometheus data source.
- **Dashboard Provisioning (`dashboard-provider.yml`)**: Automatically loads dashboards from `/var/lib/grafana/dashboards`.

---

## 8. Dashboard Design & PromQL Queries

The dashboard `Lab 3 — Application Monitoring` includes 8 specialized monitoring panels:

1. **Application Availability**:
   - PromQL: `up{job="lab3-monitoring-app"}`
   - Type: Stat Panel with Value Mappings (`1 -> UP (Healthy)`, `0 -> DOWN`).
2. **Total HTTP Requests**:
   - PromQL: `sum(http_requests_total{job="lab3-monitoring-app"})`
   - Type: Stat Panel with trend sparkline.
3. **Application Uptime**:
   - PromQL: `app_uptime_seconds{job="lab3-monitoring-app"}`
   - Type: Stat Panel formatted in seconds.
4. **Current Request Rate**:
   - PromQL: `sum(rate(http_requests_total{job="lab3-monitoring-app"}[1m]))`
   - Type: Stat Panel formatted in req/sec.
5. **HTTP Request Rate by Endpoint**:
   - PromQL: `sum(rate(http_requests_total{job="lab3-monitoring-app"}[1m])) by (endpoint)`
   - Type: Time Series graph.
6. **Cumulative Requests by Endpoint**:
   - PromQL: `sum(http_requests_total{job="lab3-monitoring-app"}) by (endpoint)`
   - Type: Bar Chart grouped by route.
7. **Requests Breakdown by HTTP Status Code**:
   - PromQL: `sum(http_requests_total{job="lab3-monitoring-app"}) by (status)`
   - Type: Donut Pie Chart displaying distribution of 200, 201, 404, and 500 status codes.
8. **Average Request Latency**:
   - PromQL: `sum(rate(http_request_duration_seconds_sum{job="lab3-monitoring-app"}[1m])) by (endpoint) / sum(rate(http_request_duration_seconds_count{job="lab3-monitoring-app"}[1m])) by (endpoint)`
   - Type: Time Series latency tracker.

---

## 9. Deployment Steps

```powershell
# 1. Navigate to lab directory
cd lab3-monitoring

# 2. Build and launch the stack
docker compose up --build -d

# 3. Verify container statuses
docker ps --filter "name=lab3-"

# 4. Generate realistic traffic
python generate_traffic.py

# 5. Verify Prometheus scraped metrics
python verify_metrics.py
```

---

## 10. Verification & Evidence

All 12 verification screenshots are archived under `lab3-monitoring/screenshots/`:
- `01_environment.png`: Repository & Docker environment check
- `02_monitoring_project.png`: Project directory tree
- `03_target_application.png`: Application home & health JSON response
- `04_metrics_endpoint.png`: `/metrics` Prometheus exposition format
- `05_prometheus_running.png`: Prometheus web UI
- `06_prometheus_target_up.png`: Prometheus Targets showing target status as `UP`
- `07_prometheus_query.png`: PromQL query execution output
- `08_grafana_running.png`: Grafana container running on port 3000
- `09_grafana_datasource.png`: Grafana Prometheus datasource verification
- `10_grafana_dashboard.png`: Grafana dashboard overview
- `11_grafana_real_metrics.png`: Grafana live multi-panel visualization with real metrics
- `12_monitoring_stack_final.png`: End-to-end health audit

---

## 11. Observations
- **Low Latency & Fast Scraping**: At a 5-second scrape interval, Prometheus captured endpoint traffic within one collection cycle.
- **Granular Error Detection**: Labeling metrics by HTTP status code (`status="500"`) allowed immediate visual isolation of service errors in Grafana without inspecting raw log files.
- **Dynamic Provisioning**: Automated provisioning allowed Grafana to start instantly configured with Prometheus datasources and dashboards without manual browser clicks.

---

## 12. Conclusion
The Prometheus and Grafana monitoring stack was successfully designed, implemented, and verified. The target application exposes real Prometheus metrics that are collected by Prometheus and rendered through dynamic, multi-panel Grafana dashboards, fulfilling all requirements for DevOps Lab 3.
