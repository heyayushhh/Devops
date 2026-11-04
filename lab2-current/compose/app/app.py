import os
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import redis

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Attempt Redis connection
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True, socket_connect_timeout=2)
except Exception as e:
    r = None

class ComposeAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        redis_status = "DISCONNECTED"
        hit_count = 0
        error_msg = None
        
        if r:
            try:
                hit_count = r.incr('page_hits')
                redis_status = "CONNECTED"
            except Exception as e:
                redis_status = "ERROR"
                error_msg = str(e)

        data = {
            "status": "success",
            "service": "lab2-compose-app",
            "message": "Docker Compose Multi-Container Application Operational",
            "redis_status": redis_status,
            "redis_host": REDIS_HOST,
            "redis_port": REDIS_PORT,
            "total_visits": hit_count,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if error_msg:
            data["redis_error"] = error_msg

        response_body = json.dumps(data, indent=2).encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        print(f"[Compose-App] {self.address_string()} - {format % args}")

def run(server_class=HTTPServer, handler_class=ComposeAppHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[*] Starting Lab 2 Compose App on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
