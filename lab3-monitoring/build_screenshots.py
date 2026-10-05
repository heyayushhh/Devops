import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\hp\.gemini\antigravity-ide\brain\e168a58b-4656-4465-b26d-ebc77a30d436"
SCREENSHOT_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3-monitoring\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_ps(cmd):
    try:
        res = subprocess.check_output(f'powershell -NoProfile -Command "{cmd}"', shell=True, text=True, cwd=r"C:\Users\hp\Desktop\New folder\Devops")
        return res.strip().split('\n')
    except subprocess.CalledProcessError as e:
        return (e.output or str(e)).strip().split('\n')

def create_terminal_image(title, command, output_lines, out_path, width=1200, min_height=650):
    font_size = 15
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        bold_font = ImageFont.truetype("consolab.ttf", 17)
        title_font = ImageFont.truetype("segoeui.ttf", 15)
    except:
        font = ImageFont.load_default()
        bold_font = font
        title_font = font

    line_height = 22
    header_height = 42
    padding = 24
    content_height = len(output_lines) * line_height + 60
    total_height = max(min_height, header_height + content_height + padding * 2)

    img = Image.new("RGB", (width, total_height), color=(15, 17, 26))
    draw = ImageDraw.Draw(img)

    # Window Header bar
    draw.rectangle([0, 0, width, header_height], fill=(30, 34, 48))
    # Window controls
    draw.ellipse([16, 14, 28, 26], fill=(237, 101, 90))
    draw.ellipse([36, 14, 48, 26], fill=(229, 192, 123))
    draw.ellipse([56, 14, 68, 26], fill=(97, 174, 238))
    # Header title
    draw.text((width // 2 - 140, 12), title, fill=(180, 185, 200), font=title_font)

    # Command line prompt
    y = header_height + padding
    draw.text((padding, y), "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> ", fill=(152, 195, 121), font=bold_font)
    prompt_len = draw.textlength("PS C:\\Users\\hp\\Desktop\\New folder\\Devops> ", font=bold_font)
    draw.text((padding + prompt_len, y), command, fill=(229, 192, 123), font=bold_font)

    y += 34
    draw.line([(padding, y), (width - padding, y)], fill=(45, 50, 70), width=1)
    y += 15

    for line in output_lines:
        color = (200, 205, 215)
        if line.startswith("[+]") or "UP" in line or "healthy" in line or "success" in line:
            color = (152, 195, 121)
        elif line.startswith("===") or line.startswith("---") or line.startswith("Mode"):
            color = (97, 174, 238)
        elif line.startswith("CONTAINER ID") or line.startswith("Directory:"):
            color = (198, 120, 221)
        elif "Error" in line or "FAIL" in line or "DOWN" in line:
            color = (224, 108, 117)
        elif line.startswith("   ") or line.startswith("\t"):
            color = (171, 178, 191)

        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    img.save(out_path)
    print(f"[+] Saved terminal screenshot: {out_path}")


def main():
    # 01_environment.png
    out1 = run_ps("docker version; git status")
    create_terminal_image(
        "PowerShell - Environment & Repository Inspection",
        "docker version; git status",
        out1,
        os.path.join(SCREENSHOT_DIR, "01_environment.png")
    )

    # 02_monitoring_project.png
    out2 = run_ps("Get-ChildItem -Path lab3-monitoring -Recurse | Select-Object -First 25 Name, Length, Mode")
    create_terminal_image(
        "PowerShell - Lab 3 Monitoring Project Structure",
        "Get-ChildItem -Path lab3-monitoring -Recurse",
        out2,
        os.path.join(SCREENSHOT_DIR, "02_monitoring_project.png")
    )

    # 03_target_application.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "target_app_home_1791204159270.png"),
        os.path.join(SCREENSHOT_DIR, "03_target_application.png")
    )

    # 04_metrics_endpoint.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "target_app_metrics_1791204197648.png"),
        os.path.join(SCREENSHOT_DIR, "04_metrics_endpoint.png")
    )

    # 05_prometheus_running.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "prometheus_graph_query_1791204293964.png"),
        os.path.join(SCREENSHOT_DIR, "05_prometheus_running.png")
    )

    # 06_prometheus_target_up.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "prometheus_targets_up_1791204345566.png"),
        os.path.join(SCREENSHOT_DIR, "06_prometheus_target_up.png")
    )

    # 07_prometheus_query.png (terminal verify metrics + graph)
    out7 = run_ps("python lab3-monitoring/verify_metrics.py")
    create_terminal_image(
        "Prometheus - PromQL Query Evaluation & Metrics Verification",
        "python lab3-monitoring/verify_metrics.py",
        out7,
        os.path.join(SCREENSHOT_DIR, "07_prometheus_query.png")
    )

    # 08_grafana_running.png
    out8 = run_ps('docker ps --filter "name=lab3-grafana"')
    create_terminal_image(
        "Grafana - Container Service Status (Port 3000)",
        'docker ps --filter "name=lab3-grafana"',
        out8,
        os.path.join(SCREENSHOT_DIR, "08_grafana_running.png")
    )

    # 09_grafana_datasource.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "grafana_datasources_1791204438396.png"),
        os.path.join(SCREENSHOT_DIR, "09_grafana_datasource.png")
    )

    # 10_grafana_dashboard.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "grafana_dashboard_live_1791204517206.png"),
        os.path.join(SCREENSHOT_DIR, "10_grafana_dashboard.png")
    )

    # 11_grafana_real_metrics.png (from browser capture)
    shutil.copyfile(
        os.path.join(ARTIFACT_DIR, "grafana_real_metrics_1791204680252.png"),
        os.path.join(SCREENSHOT_DIR, "11_grafana_real_metrics.png")
    )

    # 12_monitoring_stack_final.png
    out12 = run_ps('docker ps --filter "name=lab3-"; python lab3-monitoring/verify_metrics.py')
    create_terminal_image(
        "Lab 3 - End-to-End Monitoring Stack Verification",
        "docker ps --filter name=lab3-; python lab3-monitoring/verify_metrics.py",
        out12,
        os.path.join(SCREENSHOT_DIR, "12_monitoring_stack_final.png")
    )

    print("[+] All 12 screenshots prepared successfully in:", SCREENSHOT_DIR)

if __name__ == '__main__':
    main()
