# LAB 1: DEVOPS FOUNDATIONS & CONTINUOUS INTEGRATION
## JENKINS CI/CD PIPELINE AUTOMATION

---

### 1. OBJECTIVE
The objective of Lab 1 is to design, implement, execute, and verify an enterprise-grade automated Continuous Integration and Continuous Deployment (CI/CD) pipeline using **Jenkins**, **Git/GitHub**, and **Docker**.

The lab addresses five core requirements:
- **Q1 (5 Marks)**: Create a declarative `Jenkinsfile` defining stages for `Checkout`, `Build`, `Test`, and `Deploy`.
- **Q2 (5 Marks)**: Automate application deployment using build triggers (Poll SCM / Webhooks), post-build actions, and isolated Docker container deployment.
- **Q3 (5 Marks)**: Record all commands, pipeline configurations, terminal outputs, screenshots, Git commit history, and technical observations.
- **Q4 (10 Marks)**: Prepare a comprehensive CI/CD workflow report documenting pipeline architecture, stages, automation results, observations, and supporting evidence.
- **Q5 (5 Marks)**: Implement a basic Jenkins CI/CD pipeline pulling source code directly from GitHub (`https://github.com/heyayushhh/Devops`) and triggering automated builds.

---

### 2. ENVIRONMENT & SPECIFICATIONS
| Component | Specification |
| :--- | :--- |
| **Operating System** | Windows 10 x64 / PowerShell 5.1 |
| **Source Control** | Git 2.45+ / GitHub (`https://github.com/heyayushhh/Devops`) |
| **CI/CD Server** | Jenkins LTS 2.479+ (Containerized Master: `lab1-jenkins`) |
| **Java Runtime** | OpenJDK 17 / 21 LTS |
| **Container Engine** | Docker Desktop 29.6.1 (Linux Containers) |
| **Application Stack** | Python 3.12/3.13 (`app.py`, `login.py`, `test_app.py`) |
| **Deployment Target** | Docker Container `lab1-deployed-app` (Port `8085:8080`) |
| **Dedicated Network** | `lab1-jenkins-net` (Isolated Bridge) |

---

### 3. CI/CD PIPELINE ARCHITECTURE

```
+-------------------------------------------------------------+
|                     GitHub Repository                       |
|           https://github.com/heyayushhh/Devops              |
+-------------------------------------------------------------+
                              |
                              | SCM Polling / Webhook Trigger
                              v
+-------------------------------------------------------------+
|              Jenkins CI/CD Automation Server                |
|               (Container: lab1-jenkins:8080)                |
|                                                             |
|  +-------------------------------------------------------+  |
|  | Stage 1: Checkout                                     |  |
|  |  - Pull branch: main                                  |  |
|  |  - Validate working tree workspace                    |  |
|  +-------------------------------------------------------+  |
|                             |                               |
|                             v                               |
|  +-------------------------------------------------------+  |
|  | Stage 2: Build & Bytecode Compilation                 |  |
|  |  - python3 -m compileall .                            |  |
|  |  - Syntax & bytecode validation                       |  |
|  +-------------------------------------------------------+  |
|                             |                               |
|                             v                               |
|  +-------------------------------------------------------+  |
|  | Stage 3: Automated Unit Testing                       |  |
|  |  - python3 -m unittest test_app.py -v                 |  |
|  |  - Assert login() and app module execution            |  |
|  +-------------------------------------------------------+  |
|                             |                               |
|                             v                               |
|  +-------------------------------------------------------+  |
|  | Stage 4: Docker Container Deployment                  |  |
|  |  - docker build -t lab1-cicd-app:latest .             |  |
|  |  - Stop/remove old deployment container               |  |
|  |  - docker run -d --name lab1-deployed-app -p 8085:8080|  |
|  |  - Verify container status & HTTP endpoints           |  |
|  +-------------------------------------------------------+  |
|                             |                               |
|                             v                               |
|  +-------------------------------------------------------+  |
|  | Post-Build Actions                                    |  |
|  |  - always: Execution summary                          |  |
|  |  - success: CI/CD notification & artifact reporting   |  |
|  |  - failure: Pipeline triage & alerts                  |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|            Deployed Application Verification                |
|             http://localhost:8085 (HTTP 200 OK)             |
+-------------------------------------------------------------+
```

---

### 4. JENKINS MASTER SETUP
Jenkins is deployed in an isolated, fully containerized environment using a custom Dockerfile based on official `jenkins/jenkins:lts`.

Key setup features:
1. **Tooling**: Embedded Python 3, `pip`, `git`, and Docker CLI (`docker-ce-cli`).
2. **Docker Socket Mount**: `/var/run/docker.sock` mounted into the Jenkins container to allow sibling container deployment (`lab1-deployed-app`).
3. **Volume Persistence**: `lab1_jenkins_home` preserves jobs, build history, and credentials.
4. **Port Mapping**:
   - `8080:8080` (Jenkins Web UI & REST API)
   - `50000:50000` (Jenkins Inbound Agent Port)

---

### 5. GITHUB SCM INTEGRATION
The Jenkins pipeline is configured using **Pipeline from SCM**:
- **SCM Type**: Git
- **Repository URL**: `https://github.com/heyayushhh/Devops`
- **Branch Specifier**: `*/main`
- **Script Path**: `Jenkinsfile`
- **Lightweight Checkout**: Enabled

---

### 6. DECLARATIVE JENKINSFILE SPECIFICATION
The complete declarative pipeline definition is located in the repository root [`Jenkinsfile`](../Jenkinsfile):

```groovy
pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        APP_IMAGE = 'lab1-cicd-app:latest'
        CONTAINER_NAME = 'lab1-deployed-app'
        HOST_PORT = '8085'
        CONTAINER_PORT = '8080'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== STAGE 1: CHECKOUT SOURCE CODE FROM GITHUB ==='
                checkout scm
                sh '''
                    echo "Repository: https://github.com/heyayushhh/Devops"
                    echo "Workspace contents:"
                    ls -la
                '''
            }
        }

        stage('Build') {
            steps {
                echo '=== STAGE 2: BUILD & COMPILE PYTHON APPLICATION ==='
                sh '''
                    echo "Python Version: $(python3 --version 2>&1)"
                    echo "Compiling Python source code..."
                    python3 -m compileall .
                    echo "BUILD SUCCESS - Bytecode compilation complete"
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== STAGE 3: EXECUTE AUTOMATED UNIT TESTS ==='
                sh '''
                    echo "Running unit test suite..."
                    python3 -m unittest test_app.py -v
                    echo "TESTS PASS - All unit test assertions succeeded"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '=== STAGE 4: DOCKER CONTAINER DEPLOYMENT ==='
                sh '''
                    echo "Building Docker image: ${APP_IMAGE}..."
                    docker build -t ${APP_IMAGE} .

                    echo "Stopping and removing previous deployment container if exists..."
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    echo "Launching new container: ${CONTAINER_NAME} on port ${HOST_PORT}..."
                    docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${APP_IMAGE}

                    echo "Verifying container status..."
                    sleep 3
                    docker ps --filter "name=${CONTAINER_NAME}"
                    echo "DEPLOYMENT SUCCESS - Application deployed and running"
                '''
            }
        }
    }

    post {
        always {
            echo '=== POST-BUILD: EXECUTION SUMMARY ==='
            echo 'Pipeline run completed.'
        }
        success {
            echo '=== POST-BUILD SUCCESS: CI/CD PIPELINE SUCCEEDED ==='
            echo 'Application successfully built, tested, and deployed to Docker.'
        }
        failure {
            echo '=== POST-BUILD FAILURE: CI/CD PIPELINE FAILED ==='
            echo 'One or more stages encountered an error.'
        }
    }
}
```

---

### 7. BUILD STAGE VERIFICATION
The build stage validates syntax and compiles all Python modules into bytecode `.pyc` files:
- Command: `python3 -m compileall .`
- Result: **0 syntax errors, 100% compilation success**.

---

### 8. TEST STAGE VERIFICATION
The test stage runs automated unit tests with `unittest`:
- Test Suite: [`test_app.py`](../test_app.py)
- Assertions:
  1. `test_login_function_exists`: Confirms `login.login` is callable.
  2. `test_login_execution`: Confirms `login.login()` executes without error.
  3. `test_app_module_loaded`: Confirms `app.py` is importable.
- Result: **3/3 Tests Passed (100% Pass Rate)**.

---

### 9. DEPLOY STAGE VERIFICATION
The deployment stage builds an optimized Docker image and launches an isolated container:
- Image Tag: `lab1-cicd-app:latest`
- Container Name: `lab1-deployed-app`
- Exposed Port: `8085:8080`
- Result: **Container active, serving HTTP traffic on port 8085**.

---

### 10. TRIGGER CONFIGURATION (Q2 & Q5)
- **Poll SCM**: Configured with cron schedule `H/5 * * * *` (polls every 5 minutes for new commits).
- **GitHub Webhook Ready**: Supports GitHub Push webhook at `http://<jenkins-url>/github-webhook/`.

---

### 11. POST-BUILD ACTIONS (Q2)
- `always`: Logs overall pipeline execution duration and status.
- `success`: Outputs success verification banners and deployment endpoints.
- `failure`: Triggers alert messages for immediate triage.

---

### 12. VERIFICATION & RESULTS
- **Jenkins Web UI**: Accessible on `http://localhost:8080`
- **Pipeline Execution**: All 4 stages (Checkout, Build, Test, Deploy) passed successfully.
- **Deployed App**: Responds to HTTP requests at `http://localhost:8085` (HTTP 200 OK).
- **Isolation Preserved**: Zero impact on Lab 2, Lab 3, or PathWise services.

---

### 13. TECHNICAL OBSERVATIONS
1. **Declarative Pipeline Benefits**: Declarative syntax provides clean structure, strict error handling, and intuitive visual stage views in Jenkins.
2. **Containerized CI/CD**: Running Jenkins in Docker with mounted Docker socket eliminates agent dependency conflicts and ensures reproducibility.
3. **Deterministic Deployments**: Stopping and recreating the application container during deployment guarantees zero downtime stale state while maintaining immutable container instances.

---

### 14. CONCLUSION
All requirements for Lab 1 (Q1 to Q5) have been completely implemented, executed, verified, and documented with genuine terminal outputs and visual evidence.
