pipeline {
  agent any

  environment {
    IMAGE_NAME = "2024ht66529/aceestver"
    APP_VERSION = "${env.BRANCH_NAME}"
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
