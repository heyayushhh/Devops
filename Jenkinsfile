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
