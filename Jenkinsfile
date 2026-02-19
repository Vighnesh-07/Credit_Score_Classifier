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
                // The '|| exit 0' tells Jenkins to ignore the error if the container doesn't exist
                bat "docker stop credit-score-app || exit 0"
                bat "docker rm credit-score-app || exit 0"
                
                // Now start the fresh container [cite: 626]
                bat "docker run -d -p 8081:80 --name credit-score-app credit-score-app"
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
