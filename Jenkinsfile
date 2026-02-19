pipeline {
    agent any 

    environment {
        // Replace 'myapp' with your project name [cite: 621]
        IMAGE_NAME = "Credit_Score_Classifier"
        // Maps Jenkins/Host port to Nginx/Container port [cite: 626-627]
        PORT_MAPPING = "8081:80" 
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Jenkins automatically pulls your Dockerfile and code here [cite: 633-635]
                git branch: 'Lab2', url: 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Creates a read-only snapshot (Image) from your Dockerfile [cite: 489, 620]
                bat "docker build -t ${env.IMAGE_NAME} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stops any existing container with the same name to prevent port conflicts
                bat "docker stop ${env.IMAGE_NAME} || rem"
                bat "docker rm ${env.IMAGE_NAME} || rem"
                
                // Starts a live instance (Container) in background mode [cite: 490, 626]
                bat "docker run -d -p ${env.PORT_MAPPING} --name ${env.IMAGE_NAME} ${env.IMAGE_NAME}"
            }
        }

        stage('Verify Container') {
            steps {
                // Lists running containers to prove the lifecycle is in 'Running' state [cite: 541, 639]
                bat "docker ps"
                echo "Verify at: http://localhost:8081" [cite: 640]
            }
        }
    }

    post {
        always {
            echo "Experiment 7: Docker lifecycle stage completed." [cite: 583]
        }
    }
}
