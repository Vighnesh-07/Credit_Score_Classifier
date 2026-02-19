pipeline {
    agent any 

    environment {
        // Update these paths to match YOUR laptop's actual installation folders
        DOCKER_PATH = 'C:\\Program Files\\Docker\\Docker\\resources\\bin'
        IMAGE_NAME = 'credit-classifier-app'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                // Using the full path to ensure Docker is found [cite: 583, 620]
                bat """ "${env.DOCKER_PATH}\\docker.exe" build -t ${env.IMAGE_NAME} . """
            }
        }

        stage('Run Container') {
            steps {
                // -d runs in background, -p maps port 8081 to 80 [cite: 317, 540, 626]
                bat """ "${env.DOCKER_PATH}\\docker.exe" run -d -p 8081:80 ${env.IMAGE_NAME} """
            }
        }
        
        stage('Verify Container') {
            steps {
                // Lists running containers as proof for your lab report [cite: 331, 639]
                bat """ "${env.DOCKER_PATH}\\docker.exe" ps """
            }
        }
    }

    post {
        always {
            echo "Experiment 7: Docker lifecycle stage completed." [cite: 583]
        }
    }
}
