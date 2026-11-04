import os
import zipfile

DEV_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZIP_PATH = os.path.join(DEV_ROOT, "lab1", "Lab1_Tools_Documents.zip")

files_to_include = [
    ("Jenkinsfile", os.path.join(DEV_ROOT, "Jenkinsfile")),
    ("Dockerfile", os.path.join(DEV_ROOT, "Dockerfile")),
    ("test_app.py", os.path.join(DEV_ROOT, "test_app.py")),
    ("app.py", os.path.join(DEV_ROOT, "app.py")),
    ("login.py", os.path.join(DEV_ROOT, "login.py")),
]

def create_zip():
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for arcname, filepath in files_to_include:
            if os.path.exists(filepath):
                zf.write(filepath, arcname)
                print(f"Added root file: {arcname}")

        # Add lab1 folder contents (excluding the zip itself)
        lab1_dir = os.path.join(DEV_ROOT, "lab1")
        for root, dirs, files in os.walk(lab1_dir):
            for file in files:
                if file.endswith(".zip") or file == "create_zip.py":
                    continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, DEV_ROOT)
                zf.write(abs_path, rel_path)
                print(f"Added: {rel_path}")

    size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    print(f"\n==========================================")
    print(f"ZIP Created: {ZIP_PATH}")
    print(f"ZIP File Size: {size_mb:.2f} MB (Limit: 25.00 MB)")
    print(f"==========================================")

if __name__ == '__main__':
    create_zip()
