pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('aws-event-pipeline-creds')
        TF_WORKING_DIR = 'infra'
        S3_BUCKET = 'event-pipeline-lambda-artifacts-dhruv'
        LAMBDA_DAILY = 'daily_summary'
        LAMBDA_PROCESSOR = 'processor'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/DHRUV222222/Event_Pipeline.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir("${TF_WORKING_DIR}") {
                    sh 'terraform init'
                    sh 'terraform plan -out=tfplan'
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }

        stage('Package Lambda') {
            steps {
                sh '''
                    cd lambda-src/daily_summary
                    zip -r daily_summary.zip app.py
                    cd ../processor
                    zip -r processor.zip app.py
                '''
            }
        }

        stage('Upload Lambda to S3') {
            steps {
                sh """
                    aws s3 cp lambda-src/daily_summary/daily_summary.zip s3://${S3_BUCKET}/daily_summary.zip
                    aws s3 cp lambda-src/processor/processor.zip s3://${S3_BUCKET}/processor.zip
                """
            }
        }

        stage('Update Lambda Functions') {
            steps {
                sh """
                    aws lambda update-function-code --function-name ${LAMBDA_DAILY} --s3-bucket ${S3_BUCKET} --s3-key daily_summary.zip
                    aws lambda update-function-code --function-name ${LAMBDA_PROCESSOR} --s3-bucket ${S3_BUCKET} --s3-key processor.zip
                """
            }
        }

        stage('Post-build Cleanup') {
            steps {
                echo 'Pipeline completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'All stages executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
