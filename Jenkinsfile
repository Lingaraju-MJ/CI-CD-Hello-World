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
        // no Sonar server yet — this stage only runs if SONAR_HOST_URL is set on the job
        stage('SonarQube') {
            when {
                expression { return env.SONAR_HOST_URL?.trim() }
            }
            steps {
                sh '''
                    sonar-scanner \
                        -Dsonar.host.url="$SONAR_HOST_URL" \
                        -Dsonar.token="$SONAR_TOKEN"
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
