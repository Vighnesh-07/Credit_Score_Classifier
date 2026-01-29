pipeline {
    agent any

    environment {
        // Derived from your lab documentation 
        REPO_URL = 'https://github.com/Vighnesh-07/Credit_Score_Classifier.git'
        BRANCH_NAME = 'Lab2'
    }

    stages {
        stage('Cleanup') {
            steps {
                // Ensures a fresh start for the lab environment
                deleteDir()
            }
        }

        stage('Version Control Setup') {
            steps {
                script {
                    // Mirrors "git clone" and "git branch -m" from your lab 
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "*/main"]], 
                        userRemoteConfigs: [[url: "${env.REPO_URL}"]]
                    ])
                    sh "git branch -m ${env.BRANCH_NAME}"
                }
            }
        }

        stage('File Manipulation') {
            steps {
                // Replicates the echo command used in Step 4 of your lab [cite: 30]
                sh 'echo "This is the end..... of Lab1" >> Lab2.txt'
            }
        }

        stage('Git Operations') {
            steps {
                script {
                    // Automates the staging and committing steps [cite: 53, 60]
                    sh "git add Lab2.txt"
                    sh "git commit -m 'Automated commit: Added Lab2.txt via Jenkins'"
                }
            }
        }

        stage('Verification') {
            steps {
                // Performs the logging and status checks from your lab [cite: 87, 100, 113]
                sh "git status"
                sh "git log --oneline"
                sh "git show"
            }
        }
    }

    post {
        success {
            echo "Successfully replicated DevOps Lab 2 operations for ${env.BRANCH_NAME} branch."
        }
    }
}