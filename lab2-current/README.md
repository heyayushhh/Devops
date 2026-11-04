# Lab 2 — Docker Containerization & Container Management

## Overview
This directory contains the implementation, real execution logs, evidence screenshots, and generated submission reports for **Lab 2 (10 Marks Total)**:
- **Q1 (5 Marks):** Application Containerization, Dockerfile specification, Image Build, Container Execution, and Docker Image Layer inspection.
- **Q2 (5 Marks):** Docker Container Lifecycle management, Image Tagging & Registry Push documentation, and Multi-Container Orchestration using Docker Compose (`web` + `redis`).

---

## Directory Structure
```
lab2-current/
├── app/
│   ├── app.py                     # Python HTTP REST service
│   ├── requirements.txt           # Minimal dependencies
│   └── Dockerfile                 # Production container definition
├── compose/
│   ├── compose.yml                # Multi-service Compose manifest (web + redis)
│   └── app/
│       ├── app.py                 # Multi-container app with Redis client
│       ├── requirements.txt       # redis==5.0.8
│       └── Dockerfile             # Compose container definition
├── screenshots/                   # 14 Real execution screenshots (PNG)
│   ├── 01_environment.png
│   ├── 02_dockerfile.png
│   ├── 03_docker_build.png
│   ├── 04_docker_image.png
│   ├── 05_docker_history_layers.png
│   ├── 06_container_running.png
│   ├── 07_container_lifecycle.png
│   ├── 08_image_tag.png
│   ├── 09_registry_push.png
│   ├── 10_compose_file.png
│   ├── 11_compose_up.png
│   ├── 12_compose_services.png
│   ├── 13_compose_communication.png
│   └── 14_compose_lifecycle.png
├── reports/
│   ├── Lab2_Q1_Docker_Containerization_Report.pdf
│   ├── Lab2_Q2_Docker_Container_Management_Report.pdf
│   └── Lab2_Tools_Documents.pdf
├── commands.txt                   # Complete sequential CLI commands run
├── generate_screenshots.py        # Screenshot builder
└── Lab2_Tools_Documents.zip       # Final submission archive
```

---

## Execution Summary

### Q1 — Docker Containerization (5 Marks)
1. **Dockerfile:** Built on `python:3.11-slim`, set working directory to `/app`, copied dependencies and source files, exposed port `8080`, and configured `python app.py` entrypoint.
2. **Build:** Built image `lab2-q1-app:latest` (ID: `e1c43010618d`, Size: 134 MB).
3. **Execution:** Launched container `lab2-q1-container` on port `8091:8080`.
4. **Verification:** Verified HTTP 200 JSON response confirming healthy container state.
5. **Layers Breakdown:** Inspected using `docker history`, validating base OS layer (126MB), dependency layer (8.11MB), app copy layer (1.48KB), and metadata layers (0B).

### Q2 — Container & Multi-Container Management (5 Marks)
1. **Container Lifecycle:** Demonstrated `docker stop`, `docker start`, and `docker rm` lifecycle operations on `lab2-q1-container`.
2. **Image Tagging:** Tagged `lab2-q1-app:latest` as `heyayushhh/lab2-docker-app:latest`.
3. **Registry Push:** Executed `docker push heyayushhh/lab2-docker-app:latest`. Honestly documented standard Docker Hub authentication limitation (`insufficient_scope: authorization failed`) without fabricating credentials.
4. **Docker Compose:** Configured two interconnected services (`web` and `redis`) on a private bridge network (`lab2-compose-net`).
5. **Inter-Service Communication:** Probed `http://localhost:8092` multiple times, confirming web service communicates with Redis via service name `redis:6379` and increments visit counter (`total_visits`: 1, 2, 3).
6. **Compose Lifecycle:** Demonstrated `docker compose stop`, `start`, and `down`.
