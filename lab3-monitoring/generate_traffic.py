import time
import random
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

def make_request(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = data.encode('utf-8')
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def generate_traffic(cycles=30, delay=0.2):
    print(f"[*] Generating realistic traffic against {BASE_URL} for {cycles} cycles...")
    endpoints = [
        ('/', 'GET', None, 40),          # 40% home
        ('/health', 'GET', None, 25),    # 25% health
        ('/api/data', 'GET', None, 20),  # 20% data API
        ('/api/error', 'GET', None, 5),  # 5% simulated errors
        ('/notfound', 'GET', None, 5),   # 5% 404 not found
        ('/api/data', 'POST', '{"action": "create", "value": 100}', 5) # 5% POST
    ]
    
    total = 0
    for cycle in range(1, cycles + 1):
        # Choose endpoint based on weights
        r = random.uniform(0, 100)
        cum = 0
        chosen = endpoints[0]
        for ep in endpoints:
            cum += ep[3]
            if r <= cum:
                chosen = ep
                break
        
        path, method, body, _ = chosen
        status, resp = make_request(path, method, body)
        total += 1
        if cycle % 5 == 0 or cycle == cycles:
            print(f"[{cycle}/{cycles}] {method} {path} -> HTTP {status} (Total: {total})")
        time.sleep(delay)
        
    print(f"[+] Traffic generation complete. Sent {total} requests.")

if __name__ == '__main__':
    generate_traffic(cycles=60, delay=0.1)
