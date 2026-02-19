pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
        BRANCH_NAME = 'Lab2'
        // Using your project name as the image tag [cite: 620]
        IMAGE_NAME = 'credit-classifier-app' 
        // Define port: 8081 avoids conflict with Jenkins 8080 [cite: 627]
        PORT = '8081' 
    }

    stages {
        stage('Cleanup') {
            steps {
                deleteDir()
            }
        }

        stage('Setup Workspace') {
            steps {
                script {
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/main"]], 
                        userRemoteConfigs: [[url: "${env.REPO_URL}"]]
                    ])
                    bat "git checkout -b ${env.BRANCH_NAME} || git checkout ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Lab 2 Tasks') {
            steps {
                bat 'echo "This is the end..... of Lab1" >> Lab2.txt'
                bat 'git config user.email "vighnesh.waman@vit.edu.in"'
                bat 'git config user.name "Vighnesh Somnath Waman"'
                bat 'git add Lab2.txt'
                bat 'git commit -m "Lab2 tasks and Docker prep"'
            }
        }

        // --- NEW STAGES FOR EXPERIMENT 7 ---

        stage('Build Docker Image') {
            steps {
                // Creates a read-only snapshot (Image) from the Dockerfile [cite: 489, 575, 620]
                bat "docker build -t ${env.IMAGE_NAME} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                // Starts a live instance of the image (Container) [cite: 490, 579, 626]
                // -d runs in background; -p maps host port to container port [cite: 317-318, 626]
                bat "docker run -d -p ${env.PORT}:80 ${env.IMAGE_NAME}"
            }
        }
        
        stage('Verify Container') {
            steps {
                // Lists running containers to prove success [cite: 330, 639]
                bat "docker ps"
            }
        }
    }

    post {
        always {
            echo "Experiment 7: Docker lifecycle stage completed." [cite: 532]
        }
    }
}
