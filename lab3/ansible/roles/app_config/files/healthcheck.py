#!/usr/bin/env python3
"""Health endpoint checker — exits 0 when /etc/lab3app/app.conf exists and
the HTTP port from it answers; non-zero otherwise."""
import json
import sys
import urllib.request

CONF = "/etc/lab3app/app.conf"


def main():
    port = 8080
    with open(CONF, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("listen_port"):
                port = int(line.split("=", 1)[1].strip())
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"OK {data['service']} on port {port} (env={data['environment']})")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
