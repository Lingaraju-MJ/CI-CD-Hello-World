pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest test_app.py'
            }
        }
        stage('Run') {
            steps {
                sh 'python app.py'
            }
        }
    }
}
