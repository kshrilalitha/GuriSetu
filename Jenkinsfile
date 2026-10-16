pipeline {
    agent any
    options { timestamps(); skipDefaultCheckout(true) }
    environment {
        IMAGE_NAME = 'gurisetu-web:latest'
        CONTAINER_NAME = 'gurisetu-web'
        HOST_PORT = '8091'
        CONTAINER_PORT = '5000'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'test -f app.py && test -f Dockerfile && test -f templates/index.html && test -f templates/exams.html && test -f templates/login.html'
            }
        }
        stage('Check Tools') {
            steps { sh 'python3 --version; docker --version' }
        }
        stage('Build Docker Image') {
            steps { sh 'docker build -t "$IMAGE_NAME" .' }
        }
        stage('Deploy Container') {
            steps {
                sh 'docker rm -f "$CONTAINER_NAME" 2>/dev/null || true; docker run -d --name "$CONTAINER_NAME" --restart unless-stopped -p "$HOST_PORT:$CONTAINER_PORT" "$IMAGE_NAME"'
            }
        }
        stage('Verify Pages') {
            steps {
                sh '''
                    set -eu
                    for i in $(seq 1 15); do
                        if curl -fsS --max-time 5 "http://127.0.0.1:$HOST_PORT/" -o /tmp/gurisetu-home.html; then break; fi
                        if [ "$i" -eq 15 ]; then docker logs "$CONTAINER_NAME" || true; exit 1; fi
                        sleep 2
                    done
                    grep -Fqi "GuriSetu" /tmp/gurisetu-home.html
                    curl -fsS "http://127.0.0.1:$HOST_PORT/exams" >/dev/null
                    curl -fsS "http://127.0.0.1:$HOST_PORT/login" >/dev/null
                '''
            }
        }
    }
    post {
        success { echo 'GuriSetu deployed at http://localhost:8091/' }
        failure { echo 'Pipeline failed. Check Console Output for the first error.' }
        always { echo 'GuriSetu pipeline finished.' }
    }
}
