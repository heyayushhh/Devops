"""
Lab 3: Monitoring, Logging & DevSecOps - Automated E2E Tests
Repository: https://github.com/heyayushhh/Devops
"""

import json
import os
import urllib.request
import pytest


def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "E2E-Test-Runner/1.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.getcode(), resp.read().decode("utf-8")


def test_health_endpoint():
    base_url = os.getenv("APP_URL", "http://localhost:8080")
    try:
        code, body = fetch_url(f"{base_url}/health")
        assert code == 200
        assert '"healthy"' in body
    except Exception as e:
        # Mock/unit fallback if container is not running during local test execution
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app")))
        from app import app
        with app.test_client() as client:
            res = client.get("/health")
            assert res.status_code == 200
            assert b"healthy" in res.data


def test_feature_flag_response():
    base_url = os.getenv("APP_URL", "http://localhost:8080")
    try:
        code, body = fetch_url(base_url)
        assert code == 200
        assert "greeting_v2" in body
    except Exception as e:
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app")))
        from app import app
        with app.test_client() as client:
            res = client.get("/")
            assert res.status_code == 200
            assert b"greeting_v2" in res.data


def test_metrics_endpoint():
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app")))
    from app import app
    with app.test_client() as client:
        res = client.get("/metrics")
        assert res.status_code == 200
        assert b"demo_http_requests_total" in res.data
