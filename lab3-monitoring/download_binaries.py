import urllib.request
import os

os.makedirs("lab3-monitoring/downloads", exist_ok=True)

urls = [
    ("lab3-monitoring/downloads/prometheus.tar.gz", "https://github.com/prometheus/prometheus/releases/download/v2.51.0/prometheus-2.51.0.linux-amd64.tar.gz"),
    ("lab3-monitoring/downloads/grafana.tar.gz", "https://dl.grafana.com/oss/release/grafana-10.4.1.linux-amd64.tar.gz")
]

for target, url in urls:
    if os.path.exists(target) and os.path.getsize(target) > 1000000:
        print(f"[+] Already downloaded: {target} ({os.path.getsize(target)} bytes)")
        continue
    print(f"[*] Downloading {url} -> {target}...")
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, target)
    print(f"[+] Downloaded {target} ({os.path.getsize(target)} bytes)")
