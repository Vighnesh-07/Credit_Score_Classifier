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
                    // This pulls the code exactly like Step 1 in your lab document
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/main"]], 
                        userRemoteConfigs: [[url: "${env.REPO_URL}"]]
                    ])
                    
                    // Instead of renaming, we ensure we are on a branch
                    bat "git checkout -b ${env.BRANCH_NAME} || git checkout ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Lab 2 Tasks') {
            steps {
                // Step 4: echo content into Lab2.txt
                bat 'echo "This is the end..... of Lab1" >> Lab2.txt'
                
                // Step 5 & 7: git status and add
                bat "git status"
                bat "git add Lab2.txt"
                
                // Step 8: git commit
                bat 'git commit -m "Added Lab2.txt for Lab2 completion"'
            }
        }

        stage('Verification') {
            steps {
                // Step 12 & 14: git log and show
                bat "git log --oneline"
                bat "git show"
            }
        }
    }
}