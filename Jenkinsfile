pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('aws-event-pipeline-creds')
        TF_WORKING_DIR = '.' // Root directory
        S3_BUCKET = 'event-pipeline-lambda-artifacts-dhruv'
        LAMBDA_DAILY = 'daily_summary'
        LAMBDA_PROCESSOR = 'processor'
    }

    options {
        // Extended timeout (40 minutes max)
        timeout(time: 40, unit: 'MINUTES')
        timestamps()
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '--- Checking out GitHub Repository ---'
                git branch: 'main', url: 'https://github.com/DHRUV222222/Event_Pipeline.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir("${TF_WORKING_DIR}") {
                    echo '=== Starting Terraform Init & Apply ==='
                    sh '''
                        echo ">>> Terraform Init Started"
                        date
                        terraform init -input=false -upgrade=false

                        echo ">>> Terraform Plan Started"
                        date
                        terraform plan -refresh=false -out=tfplan

                        echo ">>> Terraform Apply Started"
                        date
                        terraform apply -auto-approve tfplan

                        echo ">>> Terraform Completed Successfully"
                        date
                    '''
                }
            }
        }

        stage('Package Lambda') {
            steps {
                echo '--- Packaging Lambda Functions ---'
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
                echo '--- Uploading Lambda Packages to S3 ---'
                sh """
                    aws s3 cp lambda-src/daily_summary/daily_summary.zip s3://${S3_BUCKET}/daily_summary.zip
                    aws s3 cp lambda-src/processor/processor.zip s3://${S3_BUCKET}/processor.zip
                """
            }
        }

        stage('Update Lambda Functions') {
            steps {
                echo '--- Updating Lambda Functions ---'
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
            echo '✅ All stages executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
        always {
            echo '🧹 Cleaning up temporary files...'
        }
    }
}
