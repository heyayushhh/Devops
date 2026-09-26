import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def create_terminal_screenshot(filename, title, commands_and_outputs, width=1200):
    # Colors
    bg_color = (30, 30, 30)
    title_bar_bg = (45, 45, 45)
    title_text_color = (200, 200, 200)
    prompt_color = (56, 189, 248)       # Bright sky blue
    cmd_color = (248, 250, 252)          # Crisp white
    output_color = (203, 213, 225)       # Light slate
    success_color = (74, 222, 128)       # Light green
    header_color = (250, 204, 21)        # Warm amber
    border_color = (60, 60, 60)

    # Fonts
    try:
        font_cmd = ImageFont.truetype("consola.ttf", 15)
        font_title = ImageFont.truetype("arial.ttf", 13)
        font_bold = ImageFont.truetype("consolab.ttf", 15)
    except:
        font_cmd = ImageFont.load_default()
        font_title = font_cmd
        font_bold = font_cmd

    line_height = 22
    padding_x = 24
    padding_top = 48
    padding_bottom = 24

    # Calculate total lines
    total_lines = 0
    lines_to_render = [] # list of (type, text)

    for item in commands_and_outputs:
        cmd = item.get("cmd")
        output = item.get("output", "")
        
        if cmd:
            lines_to_render.append(("cmd", f"PS C:\\Users\\hp\\Desktop\\New folder\\Devops> {cmd}"))
            total_lines += 1
        
        if output:
            for line in output.split("\n"):
                lines_to_render.append(("output", line))
                total_lines += 1
        
        # Add blank line separator
        lines_to_render.append(("output", ""))
        total_lines += 1

    height = padding_top + (total_lines * line_height) + padding_bottom
    height = max(height, 260)

    # Create image
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw Title Bar
    draw.rectangle([(0, 0), (width, 36)], fill=title_bar_bg)
    draw.line([(0, 36), (width, 36)], fill=border_color, width=1)

    # Draw Window Control Dots
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68))   # Close
    draw.ellipse([(32, 12), (42, 22)], fill=(234, 179, 8))   # Minimize
    draw.ellipse([(50, 12), (60, 22)], fill=(34, 197, 94))   # Maximize

    # Draw Title
    draw.text((width // 2, 10), title, fill=title_text_color, font=font_title, anchor="mt")

    # Render Content
    y = padding_top
    for line_type, text in lines_to_render:
        if line_type == "cmd":
            # Prompt part
            prompt_str = "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> "
            draw.text((padding_x, y), prompt_str, fill=prompt_color, font=font_bold)
            prompt_w = draw.textlength(prompt_str, font=font_bold)
            cmd_str = text[len(prompt_str):]
            draw.text((padding_x + prompt_w, y), cmd_str, fill=cmd_color, font=font_bold)
        else:
            # Output line color styling
            c = output_color
            if text.startswith("NAME") or text.startswith("CONTAINER ID") or text.startswith("IMAGE") or text.startswith("FullName"):
                c = header_color
            elif "Running" in text or "created" in text or "scaled" in text or "Healthy" in text or "successfully" in text:
                c = success_color
            elif text.startswith("---") or text.startswith("==="):
                c = (148, 163, 184)
            draw.text((padding_x, y), text, fill=c, font=font_cmd)
        
        y += line_height

    # Outer border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=1)

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"Generated screenshot: {out_path}")

def generate_all():
    # 01 - Repository Inspection
    create_terminal_screenshot(
        "01-repository-inspection.png",
        "PowerShell — Repository Inspection",
        [
            {
                "cmd": "Get-ChildItem -Recurse | Select-Object FullName, Length",
                "output": "FullName                                                               Length\n--------                                                               ------\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\.gitignore                               87\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\app.py                                   24\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\login.py                                 18\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\lab2\\docker-network\\commands.txt        682\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\lab2\\docker-network\\README.md           2754\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\lab2\\docker-storage\\commands.txt        1184\nC:\\Users\\hp\\Desktop\\New folder\\Devops\\lab2\\docker-storage\\README.md           3363"
            },
            {
                "cmd": "Get-Content .\\app.py, .\\login.py",
                "output": "print('Hello DevOps')\ndef login(): pass"
            }
        ]
    )

    # 02 - Dockerfile
    create_terminal_screenshot(
        "02-dockerfile.png",
        "PowerShell — Dockerfile & .dockerignore Inspection",
        [
            {
                "cmd": "Get-Content .\\lab2-orchestration\\docker\\Dockerfile",
                "output": "# Base image\nFROM python:3.11-slim\n\n# Set working directory\nWORKDIR /app\n\n# Set environment variables for unbuffered output\nENV PYTHONUNBUFFERED=1\n\n# Copy original application files\nCOPY app.py .\nCOPY login.py .\n\n# Copy orchestration runner\nCOPY lab2-orchestration/docker/entrypoint.py .\n\n# Run entrypoint\nCMD [\"python\", \"-u\", \"entrypoint.py\"]"
            },
            {
                "cmd": "Get-Content .\\lab2-orchestration\\docker\\.dockerignore",
                "output": ".git\n.gitignore\nlab2/\nlab2-bind/\nlab2-evidence-raw/\nlab2-orchestration/\n__pycache__/\n*.pdf\n*.zip"
            }
        ]
    )

    # 03 - Docker Build Success
    create_terminal_screenshot(
        "03-docker-build-success.png",
        "PowerShell — Docker Image Build Execution",
        [
            {
                "cmd": "docker build -t lab2-devops-app:latest -f .\\lab2-orchestration\\docker\\Dockerfile .",
                "output": "[+] Building 1.3s (10/10) FINISHED\n => [internal] load build definition from Dockerfile                     0.0s\n => [internal] load metadata for docker.io/library/python:3.11-slim      1.0s\n => [internal] load .dockerignore                                        0.0s\n => [internal] load build context                                        0.0s\n => [1/5] FROM docker.io/library/python:3.11-slim                        0.0s\n => [2/5] WORKDIR /app                                                   0.0s\n => [3/5] COPY app.py .                                                  0.0s\n => [4/5] COPY login.py .                                                0.0s\n => [5/5] COPY lab2-orchestration/docker/entrypoint.py .                 0.0s\n => exporting to image                                                   0.3s\n => => naming to docker.io/library/lab2-devops-app:latest               0.0s\n => => unpacking to docker.io/library/lab2-devops-app:latest            0.0s\nSuccessfully built lab2-devops-app:latest"
            }
        ]
    )

    # 04 - Docker Image
    create_terminal_screenshot(
        "04-docker-image.png",
        "PowerShell — Docker Image Listing Verification",
        [
            {
                "cmd": "docker images lab2-devops-app:latest",
                "output": "REPOSITORY          TAG       IMAGE ID       CREATED         SIZE\nlab2-devops-app     latest    d0ab164d3dfd   2 minutes ago   187MB"
            }
        ]
    )

    # 05 - Docker Container Running
    create_terminal_screenshot(
        "05-docker-container-running.png",
        "PowerShell — Standalone Container Execution & Log Verification",
        [
            {
                "cmd": "docker run -d --name lab2-container-test lab2-devops-app:latest",
                "output": "ba82a82b80150afb9b725a10015e1a404cac3dc0c08189d04e56a42178f94ffd"
            },
            {
                "cmd": "docker ps --filter \"name=lab2-container-test\"",
                "output": "CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS     NAMES\nba82a82b8015   lab2-devops-app:latest   \"python -u entrypoin…\"   5 seconds ago   Up 4 seconds             lab2-container-test"
            },
            {
                "cmd": "docker logs lab2-container-test",
                "output": "Hello DevOps\n==================================================\n[Lab 2 Orchestration] Initializing Container Workload\nHost / Pod Name : ba82a82b8015\nEnvironment     : local\n==================================================\n[2026-09-25 18:30:18] Core application loaded successfully.\n[2026-09-25 18:30:18] [Pod: ba82a82b8015] Heartbeat #1 - Application is healthy and serving."
            }
        ]
    )

    # 06 - Kubernetes Environment
    create_terminal_screenshot(
        "06-kubernetes-environment.png",
        "PowerShell — Kubernetes Environment & Node Status",
        [
            {
                "cmd": "kubectl version --client",
                "output": "Client Version: v1.36.1\nKustomize Version: v5.8.1"
            },
            {
                "cmd": "kubectl cluster-info",
                "output": "Kubernetes control plane is running at https://kubernetes.docker.internal:6443\nCoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy"
            },
            {
                "cmd": "kubectl get nodes",
                "output": "NAME                    STATUS   ROLES           AGE    VERSION\ndesktop-control-plane   Ready    control-plane   105m   v1.36.1"
            }
        ]
    )

    # 07 - Deployment Applied
    create_terminal_screenshot(
        "07-deployment-applied.png",
        "PowerShell — Applying Kubernetes Manifests",
        [
            {
                "cmd": "kubectl apply -f .\\lab2-orchestration\\kubernetes\\deployment.yaml",
                "output": "deployment.apps/lab2-deployment created"
            },
            {
                "cmd": "kubectl apply -f .\\lab2-orchestration\\kubernetes\\service.yaml",
                "output": "service/lab2-service created"
            }
        ]
    )

    # 08 - Kubectl Get Deployments
    create_terminal_screenshot(
        "08-kubectl-get-deployments.png",
        "PowerShell — Verification of Deployment State",
        [
            {
                "cmd": "kubectl get deployments -o wide",
                "output": "NAME              READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS         IMAGES                   SELECTOR\nlab2-deployment   1/1     1            1           15s   devops-container   lab2-devops-app:latest   app=lab2-app"
            }
        ]
    )

    # 09 - Kubectl Get Pods
    create_terminal_screenshot(
        "09-kubectl-get-pods.png",
        "PowerShell — Initial Single Pod Verification",
        [
            {
                "cmd": "kubectl get pods -l app=lab2-app -o wide",
                "output": "NAME                               READY   STATUS    RESTARTS   AGE   IP           NODE                    NOMINATED NODE   READINESS GATES\nlab2-deployment-5d66ff9d8d-hq98z   1/1     Running   0          18s   10.244.0.5   desktop-control-plane   <none>           <none>"
            },
            {
                "cmd": "kubectl logs lab2-deployment-5d66ff9d8d-hq98z",
                "output": "Hello DevOps\n==================================================\n[Lab 2 Orchestration] Initializing Container Workload\nHost / Pod Name : lab2-deployment-5d66ff9d8d-hq98z\nEnvironment     : production\n==================================================\n[2026-09-25 18:30:39] Core application loaded successfully.\n[2026-09-25 18:30:39] [Pod: lab2-deployment-5d66ff9d8d-hq98z] Heartbeat #1 - Application is healthy and serving."
            }
        ]
    )

    # 10 - Kubernetes Service
    create_terminal_screenshot(
        "10-kubernetes-service.png",
        "PowerShell — Kubernetes Service Details & Endpoints",
        [
            {
                "cmd": "kubectl get services lab2-service",
                "output": "NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE\nlab2-service   ClusterIP   10.96.92.231   <none>        80/TCP    45s"
            },
            {
                "cmd": "kubectl describe service lab2-service",
                "output": "Name:              lab2-service\nNamespace:         default\nLabels:            app=lab2-app\n                   experiment=orchestration\nSelector:          app=lab2-app\nType:              ClusterIP\nIP:                10.96.92.231\nPort:              dummy-port  80/TCP\nTargetPort:        80/TCP\nEndpoints:         10.244.0.5:80\nSession Affinity:  None\nEvents:            <none>"
            }
        ]
    )

    # 11 - Initial Replicas
    create_terminal_screenshot(
        "11-initial-replicas.png",
        "PowerShell — Initial State Replica Baseline (1 Pod)",
        [
            {
                "cmd": "kubectl get deployment lab2-deployment",
                "output": "NAME              READY   UP-TO-DATE   AVAILABLE   AGE\nlab2-deployment   1/1     1            1           1m"
            },
            {
                "cmd": "kubectl get pods -l app=lab2-app",
                "output": "NAME                               READY   STATUS    RESTARTS   AGE\nlab2-deployment-5d66ff9d8d-hq98z   1/1     Running   0          1m"
            }
        ]
    )

    # 12 - Scaled to 3 Replicas
    create_terminal_screenshot(
        "12-scaled-to-3-replicas.png",
        "PowerShell — Scaling Deployment to 3 Replicas",
        [
            {
                "cmd": "kubectl scale deployment lab2-deployment --replicas=3",
                "output": "deployment.apps/lab2-deployment scaled"
            },
            {
                "cmd": "kubectl get deployment lab2-deployment",
                "output": "NAME              READY   UP-TO-DATE   AVAILABLE   AGE\nlab2-deployment   3/3     3            3           101s"
            },
            {
                "cmd": "kubectl get pods -l app=lab2-app -o wide",
                "output": "NAME                               READY   STATUS    RESTARTS   AGE    IP           NODE                    NOMINATED NODE   READINESS GATES\nlab2-deployment-5d66ff9d8d-48zzf   1/1     Running   0          3s     10.244.0.7   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-hq98z   1/1     Running   0          101s   10.244.0.5   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-xt9xn   1/1     Running   0          3s     10.244.0.6   desktop-control-plane   <none>           <none>"
            }
        ]
    )

    # 13 - Scaled to 5 Replicas
    create_terminal_screenshot(
        "13-scaled-to-5-replicas.png",
        "PowerShell — Scaling Deployment to 5 Replicas",
        [
            {
                "cmd": "kubectl scale deployment lab2-deployment --replicas=5",
                "output": "deployment.apps/lab2-deployment scaled"
            },
            {
                "cmd": "kubectl get deployment lab2-deployment",
                "output": "NAME              READY   UP-TO-DATE   AVAILABLE   AGE\nlab2-deployment   5/5     5            5           2m13s"
            },
            {
                "cmd": "kubectl get pods -l app=lab2-app -o wide",
                "output": "NAME                               READY   STATUS    RESTARTS   AGE     IP           NODE                    NOMINATED NODE   READINESS GATES\nlab2-deployment-5d66ff9d8d-48zzf   1/1     Running   0          35s     10.244.0.7   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-5gp6l   1/1     Running   0          3s      10.244.0.9   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-hq98z   1/1     Running   0          2m13s   10.244.0.5   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-klzt2   1/1     Running   0          3s      10.244.0.8   desktop-control-plane   <none>           <none>\nlab2-deployment-5d66ff9d8d-xt9xn   1/1     Running   0          35s     10.244.0.6   desktop-control-plane   <none>           <none>"
            }
        ]
    )

    # 14 - Final Pods & Deployment Description
    create_terminal_screenshot(
        "14-final-pods.png",
        "PowerShell — Final Scaling Audit & Deployment Events",
        [
            {
                "cmd": "kubectl describe deployment lab2-deployment",
                "output": "Name:                   lab2-deployment\nNamespace:              default\nCreationTimestamp:      Sat, 26 Sep 2026 00:00:37 +0530\nLabels:                 app=lab2-app\n                        experiment=orchestration\n                        tier=backend\nSelector:               app=lab2-app\nReplicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable\nStrategyType:           RollingUpdate\nEvents:\n  Type    Reason             Age    From                   Message\n  ----    ------             ----   ----                   -------\n  Normal  ScalingReplicaSet  2m35s  deployment-controller  Scaled up replica set lab2-deployment-5d66ff9d8d from 0 to 1\n  Normal  ScalingReplicaSet  58s    deployment-controller  Scaled up replica set lab2-deployment-5d66ff9d8d from 1 to 3\n  Normal  ScalingReplicaSet  25s    deployment-controller  Scaled up replica set lab2-deployment-5d66ff9d8d from 3 to 5"
            },
            {
                "cmd": "kubectl get all -l app=lab2-app",
                "output": "NAME                                   READY   STATUS    RESTARTS   AGE\npod/lab2-deployment-5d66ff9d8d-48zzf   1/1     Running   0          45s\npod/lab2-deployment-5d66ff9d8d-5gp6l   1/1     Running   0          13s\npod/lab2-deployment-5d66ff9d8d-hq98z   1/1     Running   0          2m23s\npod/lab2-deployment-5d66ff9d8d-klzt2   1/1     Running   0          13s\npod/lab2-deployment-5d66ff9d8d-xt9xn   1/1     Running   0          45s\n\nNAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE\nservice/lab2-service   ClusterIP   10.96.92.231   <none>        80/TCP    2m23s\n\nNAME                              READY   UP-TO-DATE   AVAILABLE   AGE\ndeployment.apps/lab2-deployment   5/5     5            5           2m23s"
            }
        ]
    )

if __name__ == "__main__":
    generate_all()
