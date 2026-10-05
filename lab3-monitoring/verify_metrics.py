import urllib.request
import urllib.parse
import json

def query_prom(expr):
    url = 'http://127.0.0.1:9090/api/v1/query?' + urllib.parse.urlencode({'query': expr})
    req = urllib.request.urlopen(url)
    res = json.loads(req.read().decode('utf-8'))
    print(f"=== Query: {expr} ===")
    for r in res['data']['result']:
        print(f"Metric: {r.get('metric')} | Value: {r.get('value')}")
    print()

def main():
    print("[+] Querying Prometheus for Lab 3 Application Metrics:\n")
    query_prom('up{job="lab3-monitoring-app"}')
    query_prom('sum(http_requests_total{job="lab3-monitoring-app"})')
    query_prom('sum(http_requests_total{job="lab3-monitoring-app"}) by (endpoint)')
    query_prom('sum(http_requests_total{job="lab3-monitoring-app"}) by (status)')
    query_prom('app_uptime_seconds{job="lab3-monitoring-app"}')

if __name__ == '__main__':
    main()
