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
          # Start Minikube with explicit runtime
          minikube start --driver=docker --container-runtime=docker

          # Export kubeconfig so kubectl knows where to connect
          export KUBECONFIG=$(minikube kubeconfig)

          echo "Waiting for Kubernetes API server to become ready..."
          for i in {1..30}; do
            if kubectl cluster-info; then
              echo "✅ Kubernetes cluster is ready!"
              break
            fi
            echo "⏳ Still waiting... attempt $i"
            sleep 10
          done

          # Optional: verify nodes and system pods
          kubectl get nodes
          kubectl get pods -n kube-system
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
