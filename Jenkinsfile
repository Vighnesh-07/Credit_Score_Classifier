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

        stage('Version Control Setup') {
            steps {
                script {
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/main"]], 
                        userRemoteConfigs: [[url: "${env.REPO_URL}"]]
                    ])
                    // Use 'bat' for Windows commands
                    bat "git branch -m ${env.BRANCH_NAME}"
                }
            }
        }

        stage('File Manipulation') {
            steps {
                // 'echo' works in Batch too
                bat 'echo "This is the end..... of Lab1" >> Lab2.txt'
            }
        }

        stage('Git Operations') {
            steps {
                script {
                    bat "git add Lab2.txt"
                    bat "git commit -m \"Automated commit: Added Lab2.txt via Jenkins\""
                }
            }
        }

        stage('Verification') {
            steps {
                bat "git status"
                bat "git log --oneline"
                bat "git show"
            }
        }
    }
}