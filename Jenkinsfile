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
      # Reset Minikube to avoid stale cluster state
      minikube delete || true
      minikube start --driver=docker --container-runtime=containerd

      export KUBECONFIG=$HOME/.kube/config

      echo "Waiting for Kubernetes API server to become ready..."
      for i in {1..30}; do
        if kubectl cluster-info; then
          echo "✅ Kubernetes cluster is ready!"
          break
        fi
        echo "⏳ Still waiting... attempt $i"
        sleep 10
      done

      kubectl get nodes
      kubectl get pods -n kube-system

      # Try to start Minikube tunnel in background
      echo "🔌 Starting Minikube tunnel..."
      nohup minikube tunnel > /dev/null 2>&1 &
      sleep 5

      # Apply Deployment and Service manifests
      kubectl apply -f k8s/base/deployment.yaml
      kubectl apply -f k8s/base/services.yaml

      # Wait for rollout to finish
      kubectl rollout status deployment/aceestver || {
        echo "❌ Rollout failed, attempting rollback..."
        kubectl rollout undo deployment/aceestver

        echo "📜 Dumping pod logs for debugging..."
        for pod in $(kubectl get pods -n default -l app=aceestver -o jsonpath='{.items[*].metadata.name}'); do
          echo "---- Logs for pod: $pod ----"
          kubectl logs $pod -n default || true
          echo "---- Describe for pod: $pod ----"
          kubectl describe pod $pod -n default || true
        done

        exit 1
      }

      # Try to get service URL via tunnel
      echo "🌐 Application is accessible at (tunnel):"
      if ! minikube service aceestver-service --url; then
        echo "⚠️ Tunnel failed, falling back to port-forward..."
        nohup kubectl port-forward svc/aceestver-service 8080:5000 > /dev/null 2>&1 &
        echo "🌐 Application is accessible at: http://127.0.0.1:8080"
      fi
    '''
  }
}

post {
  success {
    echo '✅ Build and rollout successful'
    sh '''
      echo "🌐 Final Service URL (summary):"
      if ! minikube service aceestver-service --url; then
        echo "⚠️ Tunnel failed, fallback URL:"
        echo "http://127.0.0.1:8080"
      fi
    '''
  }
  failure {
    echo '❌ Build failed – rollback attempted'
  }
  always {
    echo '📊 Cluster state snapshot:'
    sh 'kubectl get pods -A'
  }
}
}
}