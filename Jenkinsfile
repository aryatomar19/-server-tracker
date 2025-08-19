pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "ap-south-1" // Change to your region
        AWS_ACCOUNT_ID = "331248920826"   // Change to your AWS account ID
        ECR_REPO_NAME = "trackingappcode" // Your ECR repo name
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/aryatomar19/-server-tracker'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t $docker build -t trackingappcode .
                    docker tag trackingappcode:latest 331248920826.dkr.ecr.ap-south-1.amazonaws.com/trackingappcode:latest
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 331248920826.dkr.ecr.ap-south-1.amazonaws.com
                    """
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh """
                    docker push 331248920826.dkr.ecr.ap-south-1.amazonaws.com/trackingappcode:latest
                    """
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    sh """
                    aws ecs update-service --cluster server-tracker-cluster --service server-tracker-service --force-new-deployment --region $AWS_DEFAULT_REGION
                    """
                }
            }
        }
    }
}
