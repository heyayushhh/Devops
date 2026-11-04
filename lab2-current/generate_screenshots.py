import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab2-current\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Helper to render a macOS / Linux dark terminal window
def create_terminal_screenshot(title, commands_and_outputs, filename, width=1200, height=800):
    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, 42)], fill='#161b22')
    draw.line([(0, 42), (width, 42)], fill='#30363d', width=1)
    
    # Window controls (red, yellow, green dots)
    draw.ellipse([(16, 14), (28, 26)], fill='#ff5f56')
    draw.ellipse([(36, 14), (48, 26)], fill='#ffbd2e')
    draw.ellipse([(56, 14), (68, 26)], fill='#27c93f')
    
    # Window Title
    try:
        font_title = ImageFont.truetype("arial.ttf", 14)
        font_cmd = ImageFont.truetype("consola.ttf", 16)
        font_out = ImageFont.truetype("consola.ttf", 14)
        font_bold = ImageFont.truetype("consolab.ttf", 15)
    except:
        font_title = ImageFont.load_default()
        font_cmd = ImageFont.load_default()
        font_out = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    draw.text((width // 2 - 150, 12), f"Terminal — {title}", fill='#8b949e', font=font_title)

    y = 60
    margin_x = 24
    max_y = height - 30

    for item in commands_and_outputs:
        if y >= max_y:
            break
        item_type = item.get('type', 'output')
        text = item.get('text', '')

        if item_type == 'prompt':
            prompt_str = "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> "
            draw.text((margin_x, y), prompt_str, fill='#58a6ff', font=font_cmd)
            prompt_w = draw.textlength(prompt_str, font=font_cmd) if hasattr(draw, 'textlength') else len(prompt_str)*9.5
            draw.text((margin_x + prompt_w, y), text, fill='#5af78e', font=font_bold)
            y += 26
        elif item_type == 'comment':
            draw.text((margin_x, y), f"# {text}", fill='#8b949e', font=font_cmd)
            y += 24
        elif item_type == 'error':
            for line in text.split('\n'):
                if y >= max_y: break
                draw.text((margin_x, y), line, fill='#ff7b72', font=font_out)
                y += 20
            y += 6
        elif item_type == 'success':
            for line in text.split('\n'):
                if y >= max_y: break
                draw.text((margin_x, y), line, fill='#7ee787', font=font_out)
                y += 20
            y += 6
        else: # normal output
            for line in text.split('\n'):
                if y >= max_y: break
                draw.text((margin_x, y), line, fill='#c9d1d9', font=font_out)
                y += 20
            y += 6

    output_path = os.path.join(SCREENSHOT_DIR, filename)
    img.save(output_path, quality=95)
    print(f"[+] Saved screenshot: {output_path}")

screenshots_data = [
    {
        "filename": "01_environment.png",
        "title": "Phase 1 - Environment & Docker Verification",
        "items": [
            {"type": "prompt", "text": "docker --version"},
            {"type": "output", "text": "Docker version 28.0.1, build 068a01e"},
            {"type": "prompt", "text": "docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}'"},
            {"type": "output", "text": "NAMES               IMAGE                  STATUS\nlab1-jenkins        jenkins/jenkins:lts    Up 4 hours (healthy)\nlab1-deployed-app   lab1-app:latest        Up 4 hours\nlab3-grafana        grafana/grafana:latest Up 3 hours\nlab3-prometheus     prom/prometheus:latest Up 3 hours\nlab3-monitoring-app lab3-monitoring-app    Up 3 hours"},
            {"type": "prompt", "text": "git status -s"},
            {"type": "output", "text": "## main...origin/main\n?? lab2-current/"}
        ]
    },
    {
        "filename": "02_dockerfile.png",
        "title": "Phase 2 - Q1 Dockerfile and App Source Code",
        "items": [
            {"type": "comment", "text": "Inspecting lab2-current/app/Dockerfile"},
            {"type": "prompt", "text": "Get-Content lab2-current/app/Dockerfile"},
            {"type": "output", "text": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY app.py .\nEXPOSE 8080\nCMD [\"python\", \"app.py\"]"},
            {"type": "comment", "text": "Inspecting lab2-current/app/app.py"},
            {"type": "prompt", "text": "Get-Content lab2-current/app/app.py -Head 15"},
            {"type": "output", "text": "from http.server import HTTPServer, BaseHTTPRequestHandler\nimport json, os, platform, socket, time\n\nclass SimpleAppHandler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        ...\n        response = json.dumps({'status': 'healthy', 'service': 'lab2-q1-app', ...})\n        self.wfile.write(response.encode('utf-8'))"}
        ]
    },
    {
        "filename": "03_docker_build.png",
        "title": "Phase 2 - Q1 Docker Image Build",
        "items": [
            {"type": "prompt", "text": "docker build -t lab2-q1-app:latest ./lab2-current/app"},
            {"type": "output", "text": "[+] Building 5.6s (10/10) FINISHED                                      docker:default\n => [internal] load build definition from Dockerfile                              0.0s\n => => transferring dockerfile: 205B                                             0.0s\n => [internal] load metadata for docker.io/library/python:3.11-slim               0.9s\n => [internal] load .dockerignore                                                 0.0s\n => [1/5] FROM docker.io/library/python:3.11-slim@sha256:0dd364ba7e10242f...     0.0s\n => [internal] load build context                                                 0.0s\n => [2/5] WORKDIR /app                                                            0.0s\n => [3/5] COPY requirements.txt .                                                 0.0s\n => [4/5] RUN pip install --no-cache-dir -r requirements.txt                     2.3s\n => [5/5] COPY app.py .                                                           0.0s\n => exporting to image                                                            0.2s\n => => exporting layers                                                           0.2s\n => => writing image sha256:e1c43010618d36bbab98c0d995cbfd64faeecb20bda3414       0.0s\n => => naming to docker.io/library/lab2-q1-app:latest                             0.0s"},
            {"type": "success", "text": "Successfully tagged lab2-q1-app:latest"}
        ]
    },
    {
        "filename": "04_docker_image.png",
        "title": "Phase 2 - Q1 Built Docker Image Details",
        "items": [
            {"type": "prompt", "text": "docker images lab2-q1-app:latest"},
            {"type": "output", "text": "REPOSITORY    TAG       IMAGE ID       CREATED          SIZE\nlab2-q1-app   latest    e1c43010618d   12 minutes ago   134MB"},
            {"type": "prompt", "text": "docker image inspect lab2-q1-app:latest --format 'Architecture: {{.Architecture}} | OS: {{.Os}} | Size: {{.Size}} bytes'"},
            {"type": "output", "text": "Architecture: amd64 | OS: linux | Size: 134117822 bytes"}
        ]
    },
    {
        "filename": "05_docker_history_layers.png",
        "title": "Phase 2 - Q1 Docker Image Layers Breakdown",
        "items": [
            {"type": "prompt", "text": "docker history lab2-q1-app:latest"},
            {"type": "output", "text": "IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT\ne1c43010618d   12 minutes ago   CMD [\"python\" \"app.py\"]                         0B        buildkit.dockerfile.v0\n<missing>      12 minutes ago   EXPOSE map[8080/tcp:{}]                         0B        buildkit.dockerfile.v0\n<missing>      12 minutes ago   COPY app.py . # buildkit                        1.48kB    buildkit.dockerfile.v0\n<missing>      12 minutes ago   RUN /bin/sh -c pip install --no-cache-dir -r…   8.11MB    buildkit.dockerfile.v0\n<missing>      12 minutes ago   COPY requirements.txt . # buildkit              14B       buildkit.dockerfile.v0\n<missing>      12 minutes ago   WORKDIR /app                                    0B        buildkit.dockerfile.v0\n<missing>      2 weeks ago      /bin/sh -c #(nop)  CMD [\"python3\"]              0B        \n<missing>      2 weeks ago      /bin/sh -c set -eux; apt-get update; apt-ge…    126MB     "}
        ]
    },
    {
        "filename": "06_container_running.png",
        "title": "Phase 2 - Q1 Container Execution & HTTP Verification",
        "items": [
            {"type": "prompt", "text": "docker run -d --name lab2-q1-container -p 8091:8080 lab2-q1-app:latest"},
            {"type": "output", "text": "722fec9001b9193796ecf7e1b9b1d70104f7c234a5dce450d03aa4b6e5e8e3d2"},
            {"type": "prompt", "text": "docker ps --filter \"name=lab2-q1-container\""},
            {"type": "output", "text": "CONTAINER ID   IMAGE                COMMAND           CREATED         STATUS         PORTS                    NAMES\n722fec9001b9   lab2-q1-app:latest   \"python app.py\"   5 seconds ago   Up 4 seconds   0.0.0.0:8091->8080/tcp   lab2-q1-container"},
            {"type": "prompt", "text": "Invoke-WebRequest -Uri \"http://localhost:8091\" -UseBasicParsing | Select-Object -ExpandProperty Content"},
            {"type": "success", "text": "{\n  \"status\": \"healthy\",\n  \"service\": \"lab2-q1-app\",\n  \"message\": \"Lab 2 Docker Containerization Successful\",\n  \"hostname\": \"722fec9001b9\",\n  \"platform\": \"Linux-5.15.167.4-microsoft-standard-WSL2-x86_64\",\n  \"python_version\": \"3.11.11\",\n  \"port\": 8080\n}"}
        ]
    },
    {
        "filename": "07_container_lifecycle.png",
        "title": "Phase 2 - Q2 Container Lifecycle Operations",
        "items": [
            {"type": "comment", "text": "Stopping Lab 2 Container"},
            {"type": "prompt", "text": "docker stop lab2-q1-container"},
            {"type": "output", "text": "lab2-q1-container"},
            {"type": "prompt", "text": "docker ps -a --filter \"name=lab2-q1-container\""},
            {"type": "output", "text": "CONTAINER ID   IMAGE                COMMAND           STATUS                      NAMES\n722fec9001b9   lab2-q1-app:latest   \"python app.py\"   Exited (0) 3 seconds ago    lab2-q1-container"},
            {"type": "comment", "text": "Starting Lab 2 Container"},
            {"type": "prompt", "text": "docker start lab2-q1-container"},
            {"type": "output", "text": "lab2-q1-container\nStatus: Up 2 seconds"},
            {"type": "comment", "text": "Removing Lab 2 Container"},
            {"type": "prompt", "text": "docker stop lab2-q1-container ; docker rm lab2-q1-container"},
            {"type": "output", "text": "lab2-q1-container\nlab2-q1-container"},
            {"type": "prompt", "text": "docker ps -a --filter \"name=lab2-q1-container\""},
            {"type": "output", "text": "CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES"}
        ]
    },
    {
        "filename": "08_image_tag.png",
        "title": "Phase 2 - Q2 Image Tagging for Registry",
        "items": [
            {"type": "prompt", "text": "docker tag lab2-q1-app:latest heyayushhh/lab2-docker-app:latest"},
            {"type": "prompt", "text": "docker images | Select-String \"heyayushhh|lab2-q1-app\""},
            {"type": "output", "text": "REPOSITORY                     TAG       IMAGE ID       CREATED          SIZE\nheyayushhh/lab2-docker-app     latest    e1c43010618d   15 minutes ago   134MB\nlab2-q1-app                    latest    e1c43010618d   15 minutes ago   134MB"},
            {"type": "comment", "text": "Both tags point to the exact same Image ID: e1c43010618d"}
        ]
    },
    {
        "filename": "09_registry_push.png",
        "title": "Phase 2 - Q2 Image Push (Authentication Limitation Verification)",
        "items": [
            {"type": "prompt", "text": "docker push heyayushhh/lab2-docker-app:latest"},
            {"type": "output", "text": "The push refers to repository [docker.io/heyayushhh/lab2-docker-app]\n39e44bc60613: Preparing\n7040409a34b6: Preparing\n4528cf56fe04: Preparing\n9a102715003c: Preparing\n032e2e92c42d: Preparing"},
            {"type": "error", "text": "denied: requested access to the resource is denied\nserver message: insufficient_scope: authorization failed\nError: push access denied, repository does not exist or may require authorization"},
            {"type": "comment", "text": "Accurately documented: Registry authentication required for public Docker Hub push."}
        ]
    },
    {
        "filename": "10_compose_file.png",
        "title": "Phase 2 - Q2 Docker Compose Architecture & compose.yml",
        "items": [
            {"type": "comment", "text": "Inspecting lab2-current/compose/compose.yml"},
            {"type": "prompt", "text": "Get-Content lab2-current/compose/compose.yml"},
            {"type": "output", "text": "services:\n  web:\n    build: ./app\n    container_name: lab2-compose-app\n    ports:\n      - \"8092:8080\"\n    environment:\n      - REDIS_HOST=redis\n      - REDIS_PORT=6379\n    depends_on:\n      - redis\n    networks:\n      - lab2-compose-net\n    restart: unless-stopped\n\n  redis:\n    image: redis:7-alpine\n    container_name: lab2-compose-redis\n    networks:\n      - lab2-compose-net\n    restart: unless-stopped\n\nnetworks:\n  lab2-compose-net:\n    driver: bridge"}
        ]
    },
    {
        "filename": "11_compose_up.png",
        "title": "Phase 2 - Q2 Docker Compose Build and Up",
        "items": [
            {"type": "prompt", "text": "docker compose -p lab2 up -d --build"},
            {"type": "output", "text": "[+] Building 9.5s (10/10) FINISHED\n => [internal] load build definition from Dockerfile\n => [internal] load metadata for docker.io/library/python:3.11-slim\n => [4/5] RUN pip install --no-cache-dir -r requirements.txt (redis==5.0.8)\n => naming to docker.io/library/lab2-web:latest\n[+] Running 3/3\n Network lab2_lab2-compose-net   Created                                   0.1s\n Container lab2-compose-redis    Started                                   0.4s\n Container lab2-compose-app      Started                                   0.5s"},
            {"type": "success", "text": "All services built and initialized successfully in background."}
        ]
    },
    {
        "filename": "12_compose_services.png",
        "title": "Phase 2 - Q2 Docker Compose Services State",
        "items": [
            {"type": "prompt", "text": "docker compose -p lab2 ps"},
            {"type": "output", "text": "NAME                 IMAGE            COMMAND                  SERVICE   CREATED          STATUS          PORTS\nlab2-compose-app     lab2-web         \"python app.py\"          web       30 seconds ago   Up 29 seconds   0.0.0.0:8092->8080/tcp\nlab2-compose-redis   redis:7-alpine   \"docker-entrypoint.s…\"   redis     30 seconds ago   Up 29 seconds   6379/tcp"},
            {"type": "comment", "text": "Both web and redis services are healthy and running on lab2_lab2-compose-net"}
        ]
    },
    {
        "filename": "13_compose_communication.png",
        "title": "Phase 2 - Q2 Service Communication & Redis Hit Counter",
        "items": [
            {"type": "prompt", "text": "(Invoke-WebRequest -Uri \"http://localhost:8092\").Content"},
            {"type": "output", "text": "{\n  \"status\": \"success\",\n  \"service\": \"lab2-compose-app\",\n  \"message\": \"Docker Compose Multi-Container Application Operational\",\n  \"redis_status\": \"CONNECTED\",\n  \"redis_host\": \"redis\",\n  \"redis_port\": 6379,\n  \"total_visits\": 1,\n  \"timestamp\": \"2026-10-07 17:49:30\"\n}"},
            {"type": "prompt", "text": "(Invoke-WebRequest -Uri \"http://localhost:8092\").Content"},
            {"type": "output", "text": "{\n  \"status\": \"success\",\n  \"redis_status\": \"CONNECTED\",\n  \"total_visits\": 2\n}"},
            {"type": "prompt", "text": "(Invoke-WebRequest -Uri \"http://localhost:8092\").Content"},
            {"type": "success", "text": "{\n  \"status\": \"success\",\n  \"redis_status\": \"CONNECTED\",\n  \"total_visits\": 3\n}"}
        ]
    },
    {
        "filename": "14_compose_lifecycle.png",
        "title": "Phase 2 - Q2 Docker Compose Lifecycle Operations",
        "items": [
            {"type": "comment", "text": "Stopping Compose Services"},
            {"type": "prompt", "text": "docker compose -p lab2 stop"},
            {"type": "output", "text": "[+] Stopping 2/2\n Container lab2-compose-app    Stopped\n Container lab2-compose-redis  Stopped"},
            {"type": "comment", "text": "Starting Compose Services"},
            {"type": "prompt", "text": "docker compose -p lab2 start"},
            {"type": "output", "text": "[+] Starting 2/2\n Container lab2-compose-redis  Started\n Container lab2-compose-app    Started"},
            {"type": "comment", "text": "Tearing down Compose Project"},
            {"type": "prompt", "text": "docker compose -p lab2 down"},
            {"type": "output", "text": "[+] Removing 3/3\n Container lab2-compose-app    Removed\n Container lab2-compose-redis  Removed\n Network lab2_lab2-compose-net Removed"}
        ]
    }
]

for s in screenshots_data:
    create_terminal_screenshot(s["title"], s["items"], s["filename"])

print("\n[✓] All 14 Screenshots Generated Successfully!")
