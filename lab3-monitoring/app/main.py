import http.server
import json
import time
import socketserver
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST

PORT = 8000
START_TIME = time.time()

# Prometheus Metrics Definitions
HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total count of HTTP requests processed',
    ['method', 'endpoint', 'status']
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)

APP_UPTIME_SECONDS = Gauge(
    'app_uptime_seconds',
    'Total uptime of the application in seconds'
)
APP_UPTIME_SECONDS.set_function(lambda: time.time() - START_TIME)

APP_INFO = Info('app_info', 'Application metadata and build information')
APP_INFO.info({
    'app_name': 'devops-lab3-monitoring-app',
    'version': '1.0.0',
    'environment': 'production',
    'maintainer': 'heyayushhh'
})


class MonitoringRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        req_start = time.time()
        path = self.path.split('?')[0]
        
        if path == '/':
            status_code = 200
            response_body = json.dumps({
                "status": "ok",
                "message": "DevOps Lab 3 Target Application",
                "version": "1.0.0",
                "endpoints": ["/", "/health", "/metrics", "/api/data", "/api/error"]
            }).encode('utf-8')
            content_type = "application/json"
            
        elif path == '/health':
            status_code = 200
            uptime = round(time.time() - START_TIME, 2)
            response_body = json.dumps({
                "status": "healthy",
                "uptime_seconds": uptime,
                "service": "devops-lab3-monitoring-app"
            }).encode('utf-8')
            content_type = "application/json"
            
        elif path == '/metrics':
            status_code = 200
            response_body = generate_latest()
            content_type = CONTENT_TYPE_LATEST
            
        elif path == '/api/data':
            status_code = 200
            response_body = json.dumps({
                "status": "success",
                "data": [
                    {"id": 1, "metric": "cpu_utilization", "value": 42.5},
                    {"id": 2, "metric": "memory_usage", "value": 78.1},
                    {"id": 3, "metric": "disk_io", "value": 12.3}
                ]
            }).encode('utf-8')
            content_type = "application/json"
            
        elif path == '/api/error':
            status_code = 500
            response_body = json.dumps({
                "status": "error",
                "message": "Simulated Internal Server Error for metric testing"
            }).encode('utf-8')
            content_type = "application/json"
            
        else:
            status_code = 404
            response_body = json.dumps({
                "status": "error",
                "message": "Endpoint not found"
            }).encode('utf-8')
            content_type = "application/json"

        # Record metrics
        HTTP_REQUESTS_TOTAL.labels(method='GET', endpoint=path, status=str(status_code)).inc()
        duration = time.time() - req_start
        HTTP_REQUEST_DURATION_SECONDS.labels(method='GET', endpoint=path).observe(duration)

        # Send response
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def do_POST(self):
        req_start = time.time()
        path = self.path.split('?')[0]
        status_code = 201
        response_body = json.dumps({
            "status": "created",
            "message": "Resource created successfully"
        }).encode('utf-8')
        content_type = "application/json"

        HTTP_REQUESTS_TOTAL.labels(method='POST', endpoint=path, status=str(status_code)).inc()
        duration = time.time() - req_start
        HTTP_REQUEST_DURATION_SECONDS.labels(method='POST', endpoint=path).observe(duration)

        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        # Override to suppress default console logging spam or format cleanly
        pass


def run_server():
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, MonitoringRequestHandler)
    print(f"Target Application running on port {PORT} with /metrics enabled...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
