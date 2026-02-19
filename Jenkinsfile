pipeline {
    agent any 

    environment {
        // Defines the static name for your application image
        IMAGE_NAME = "credit-score-app"
        // Maps the host port 8081 to the container port 80
        PORT_MAPPING = "8081:80" 
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Pulls the Dockerfile and code from your Lab2 branch
                git branch: 'Lab2', url: 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Creates the image snapshot from the Dockerfile
                bat "docker build -t ${env.IMAGE_NAME} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                // Safely stops and removes old versions to prevent port errors
                bat "docker stop ${env.IMAGE_NAME} || rem"
                bat "docker rm ${env.IMAGE_NAME} || rem"
                
                // Launches the container in background mode
                bat "docker run -d -p ${env.PORT_MAPPING} --name ${env.IMAGE_NAME} ${env.IMAGE_NAME}"
            }
        }

        stage('Verify Container') {
            steps {
                // Proof of running state for your lab record
                bat "docker ps"
                echo "Application live at: http://localhost:8081"
            }
        }
    }

    post {
        always {
            echo "Experiment 7: Docker lifecycle stage completed."
        }
    }
}
