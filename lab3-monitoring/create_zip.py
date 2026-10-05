import os
import zipfile

ZIP_PATH = r"C:\Users\hp\Desktop\New folder\Devops\lab3-monitoring\Lab3_Monitoring_Tools_Documents.zip"
BASE_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3-monitoring"

files_and_dirs = [
    "app",
    "prometheus",
    "grafana",
    "docker-compose.yml",
    "generate_traffic.py",
    "verify_metrics.py",
    "README.md",
    "commands.txt",
    "screenshots",
    "Lab3_Monitoring_Prometheus_Grafana_Report.pdf"
]

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for item in files_and_dirs:
        full_path = os.path.join(BASE_DIR, item)
        if os.path.isfile(full_path):
            zipf.write(full_path, arcname=item)
            print(f"[+] Added file: {item}")
        elif os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path):
                # Exclude downloads or cache
                if "downloads" in root or "__pycache__" in root:
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, BASE_DIR)
                    zipf.write(file_path, arcname=arcname)
                    print(f"[+] Added: {arcname}")

print(f"\n[+] Created ZIP Archive: {ZIP_PATH} ({os.path.getsize(ZIP_PATH)} bytes / {round(os.path.getsize(ZIP_PATH)/1024/1024, 2)} MB)")
