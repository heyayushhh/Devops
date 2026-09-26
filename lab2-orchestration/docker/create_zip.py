import os
import zipfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZIP_PATH = os.path.join(BASE_DIR, "Lab2_Tools_Documents.zip")

files_to_include = [
    ("docker/Dockerfile", "docker/Dockerfile"),
    ("docker/.dockerignore", "docker/.dockerignore"),
    ("docker/entrypoint.py", "docker/entrypoint.py"),
    ("kubernetes/deployment.yaml", "kubernetes/deployment.yaml"),
    ("kubernetes/service.yaml", "kubernetes/service.yaml"),
    ("commands.txt", "commands.txt"),
    ("README.md", "README.md"),
    ("Lab2_Containerization_Orchestration_Report.pdf", "Lab2_Containerization_Orchestration_Report.pdf"),
    ("Lab2_Tools_Documents.pdf", "Lab2_Tools_Documents.pdf"),
]

# Add screenshots
screenshots_dir = os.path.join(BASE_DIR, "screenshots")
for f in sorted(os.listdir(screenshots_dir)):
    if f.endswith(".png"):
        files_to_include.append((os.path.join("screenshots", f), os.path.join("screenshots", f)))

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for rel_path, arc_name in files_to_include:
        full_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(full_path):
            zipf.write(full_path, arcname=os.path.join("Lab2_Tools_Documents", arc_name))
            print(f"Added to zip: {arc_name}")

print(f"Created ZIP package successfully: {ZIP_PATH} ({os.path.getsize(ZIP_PATH)} bytes)")
