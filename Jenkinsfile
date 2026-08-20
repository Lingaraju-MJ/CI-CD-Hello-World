pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
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
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest test_app.py
                '''
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
}
