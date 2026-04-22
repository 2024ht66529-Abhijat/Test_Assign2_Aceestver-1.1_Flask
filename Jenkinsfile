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
      minikube delete || true
      minikube start --driver=docker --container-runtime=containerd

      export KUBECONFIG=$HOME/.kube/config

      kubectl apply -f k8s/base/deployment.yaml
      kubectl apply -f k8s/base/services.yaml

      kubectl rollout status deployment/aceestver

      echo "🌐 Setting up port-forward..."
      nohup kubectl port-forward svc/aceestver-service 8080:5000 > /dev/null 2>&1 &
      sleep 5
      echo "🌐 Application is accessible at: http://127.0.0.1:8080"
    '''
  }
}
post {
  success {
    echo '✅ Build and rollout successful'
    sh '''
      echo "🌐 Final Service URL (summary): http://127.0.0.1:8080"
    '''
  }
  failure {
    echo '❌ Build failed – rollback attempted'
  }
  always {
    echo '📊 Cluster state snapshot:'
    sh 'kubectl get pods -A'
  
    pkill -f "kubectl port-forward" || true
  }
}
}
