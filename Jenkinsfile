pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                // Change 'myapp' to your github project name
                bat 'docker build -t Credit_Score_Classifier .' 
            }
        }
        stage('Run Container') {
            steps {
                // Runs container in background on port 8081 (to avoid conflict with Jenkins 8080)
                bat 'docker run -d -p 8081:80 Credit_Score_Classifier' 
            }
        }
    }
}
