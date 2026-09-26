import time
import socket
import os
import app
import login

def main():
    hostname = socket.gethostname()
    print(f"==================================================")
    print(f"[Lab 2 Orchestration] Initializing Container Workload")
    print(f"Host / Pod Name : {hostname}")
    print(f"Environment     : {os.environ.get('APP_ENV', 'local')}")
    print(f"==================================================")
    
    # Execute existing application logic
    login.login()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Core application loaded successfully.")
    
    count = 1
    while True:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [Pod: {hostname}] Heartbeat #{count} - Application is healthy and serving.")
        count += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
