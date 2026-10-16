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
            set -e

            echo "Checking GuriSetu pages..."

            docker exec gurisetu-web python -c "
import urllib.request

for path in ['/', '/exams', '/login']:
    response = urllib.request.urlopen(
        'http://127.0.0.1:5000' + path,
        timeout=5
    )
    print(path, response.status)
    assert response.status == 200
"

            echo "All GuriSetu pages verified successfully!"
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
