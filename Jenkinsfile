pipeline {
    agent any

    environment {
        IMAGE_NAME     = "2024ht66529/aceestver"
        APP_VERSION    = "stable"
        APP_PORT       = "9090"   // avoid Jenkins 8080 conflict
        KUBECONFIG     = "${env.HOME}/.kube/config"
        MINIKUBE_HOME  = "${env.HOME}/.minikube"
        PATH           = "/usr/local/bin:${env.PATH}" // ensure minikube/kubectl are visible
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

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
                sh '''
                    docker build -t $IMAGE_NAME:$APP_VERSION .
                '''
            }
        }

    stage('Run Tests in Container') {
            steps {
                sh '''
                    docker run $IMAGE_NAME:$APP_VERSION pytest
                '''
            }
        }

      stage('Push Image') {
            steps {
                sh '''
                    docker push $IMAGE_NAME:$APP_VERSION
                '''
            }
        }

       stage('Deploy to Minikube') {
            steps {
                sh '''
                    minikube delete --all --purge || true
                    minikube start --driver=docker --container-runtime=containerd --force
                    minikube update-context



                    echo "=== Cluster Info ==="
                    kubectl cluster-info
                    kubectl get nodes

                    kubectl apply -f k8s/base/deployment.yaml --validate=false
                    kubectl apply -f k8s/base/services.yaml --validate=false

                    kubectl rollout status deployment/aceestver --timeout=120s

                    echo "🌐 Setting up port-forward..."
                    nohup kubectl port-forward svc/aceestver-service $APP_PORT:5000 > /dev/null 2>&1 &
                    sleep 5
                    echo "🌐 Application is accessible at: http://127.0.0.1:$APP_PORT"
                '''
            }
        }
    }
    post {
        always {
            sh '''
                echo "📊 Cluster state snapshot:"
                kubectl get pods -A || true

                # Cleanup port-forward
                pkill -f "kubectl port-forward" || true
            '''
        }
        success {
            echo "✅ Build and rollout successful"
            sh '''
                echo "🌐 Final Service URL (summary): http://127.0.0.1:$APP_PORT"
            '''
        }
    }
}

