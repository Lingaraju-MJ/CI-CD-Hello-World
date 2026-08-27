pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff check .
                '''
            }
        }
        stage('Format') {
            steps {
                sh '''
                    . .venv/bin/activate
                    black --check .
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    python -m pytest test_app.py \
                        --junitxml=reports/junit.xml \
                        --cov=app \
                        --cov-fail-under=80 \
                        --cov-report=term \
                        --cov-report=xml
                '''
            }
        }
        stage('SonarQube') {
            steps {
                sh '''
                    export PATH="/opt/sonar-scanner/bin:$PATH"
                    set +x
                    export SONAR_TOKEN=$(cat /var/jenkins_home/.sonar_token)
                    set -x
                    sonar-scanner -Dsonar.host.url=http://sonarqube-hello-world:9000
                '''
            }
        }
        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    python3 -m zipfile -c "dist/hello-world-${BUILD_NUMBER}.zip" app.py
                '''
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
            }
        }
        stage('Run') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python app.py
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
        }
    }
}
