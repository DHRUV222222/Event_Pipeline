pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Initialize Terraform') {
            steps {
                dir('infra') {
                    sh 'terraform init'
                }
            }
        }

        stage('Validate Terraform') {
            steps {
                dir('infra') {
                    sh 'terraform validate'
                }
            }
        }

        stage('Plan Terraform') {
            steps {
                dir('infra') {
                    sh 'terraform plan -out=tfplan'
                }
            }
        }

        stage('Apply Terraform') {
            steps {
                dir('infra') {
                    input message: "Approve to apply Terraform changes?"
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }
    }
}
