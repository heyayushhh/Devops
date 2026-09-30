#!/usr/bin/env python3
"""Lab 3 demo application.

A tiny deterministic HTTP service used as the managed workload for the
Ansible (Q1) and Terraform (Q2) experiments. It serves a JSON payload built
from /etc/lab3app/app.conf and prints a startup/heartbeat line to stdout.
"""
import json
import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIG_PATH = "/etc/lab3app/app.conf"


def load_conf(path=CONFIG_PATH):
    conf = {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                conf[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return conf


def main():
    conf = load_conf()
    port = int(conf.get("listen_port") or os.environ.get("APP_PORT", "8080"))
    host = "0.0.0.0"

    httpd = HTTPServer((host, port), Handler)
    print(f"[{conf.get('node', socket.gethostname())}] lab3app listening on {host}:{port} "
          f"(env={conf.get('environment', 'unknown')})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        conf = load_conf()
        payload = {
            "service": conf.get("app_name", "lab3app"),
            "node": conf.get("node", socket.gethostname()),
            "environment": conf.get("environment", "unknown"),
            "greeting": conf.get("greeting", "Hello from Lab 3"),
            "listen_port": conf.get("listen_port"),
        }
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # keep request log lines on stdout
        sys.stdout.write(f"{self.address_string()} - {fmt % args}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
