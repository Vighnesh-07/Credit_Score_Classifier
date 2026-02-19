pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
        BRANCH_NAME = 'Lab2'
        IMAGE_NAME = 'credit-classifier-app' 
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

        stage('Build Docker Image') {
            steps {
                // Creates the image snapshot from the Dockerfile instructions
                bat "docker build -t ${env.IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                // Starts the container and maps port 8081 to internal port 80
                bat "docker run -d -p ${env.PORT}:80 ${env.IMAGE_NAME}"
            }
        }
        
        stage('Verify Container') {
            steps {
                // Proves the container is live and running
                bat "docker ps"
            }
        }
    }

    post {
        always {
            echo "Experiment 7: Docker lifecycle stage completed."
        }
    }
}
