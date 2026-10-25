
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Weekend_Project1',
                    url: 'https://github.com/RahulMurugesh-2674/Weekend_Projects.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t employee-api .'
            }
        }
    }
}
