pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "331248920826"
        ECR_REPO_NAME = "trackingappcode"
        IMAGE_TAG = "latest"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/aryatomar19/-server-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .
                    docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region ${AWS_DEFAULT_REGION} \
                    | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh """
                    docker push ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    sh """
                    aws ecs update-service \
                        --cluster server-tracker-cluster \
                        --service server-tracker-service \
                        --force-new-deployment \
                        --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }
    }
}

