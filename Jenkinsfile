pipeline {
  agent any

  environment {
    IMAGE_NAME = "2024ht66529/aceestver"
    APP_VERSION = "${env.BRANCH_NAME}"
  }

  stages {

    stage('Docker Hub Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', 
                                          usernameVariable: 'DOCKER_USER', 
                                          passwordVariable: 'DOCKER_PASS')]) {
          sh '''
          echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
          '''
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME:$APP_VERSION .'
      }
    }

    stage('Run Tests in Container') {
      steps {
        sh 'docker run $IMAGE_NAME:$APP_VERSION pytest'
      }
    }

    stage('Push Image') {
      steps {
        sh '''
        docker tag $IMAGE_NAME:$APP_VERSION $IMAGE_NAME:stable
        docker push $IMAGE_NAME:$APP_VERSION
        docker push $IMAGE_NAME:stable
        '''
      }
    }
  

    stage('Deploy to Minikube') {
      steps {
        sh '''
        # Ensure kubectl is pointing to Minikube
        kubectl config use-context minikube

        # Apply Kubernetes manifests (Deployment + Service)
        kubectl apply -f k8s/base/deployment.yaml
        kubectl apply -f k8s/base/service.yaml

        # Wait for rollout to complete
        kubectl rollout status deployment/aceestver-deployment
        '''
      }
    }
  }
  post {
    failure {
      echo '❌ Build failed – rollback safe'
    }
    success {
      echo '✅ Build successful'
    }
  }
}
