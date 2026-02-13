pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
        BRANCH_NAME = 'Lab2'
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
                bat "git status"
                bat "git add Lab2.txt"
                
                // Add identity configuration here
                bat 'git config user.email "vighnesh.waman@vit.edu.in"'
                bat 'git config user.name "Vighnesh Somnath Waman"'
                
                bat 'git commit -m "Added Lab2.txt for Lab2 completion"'
            }
        }

        stage('Verification') {
            steps {
                bat "git log --oneline"
                bat "git show"
            }
        }
    }
}