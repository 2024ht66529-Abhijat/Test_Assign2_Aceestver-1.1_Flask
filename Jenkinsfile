pipeline {
  agent any

  environment {
    IMAGE_NAME = "dockerhub-username/aceestver"
    APP_VERSION = "${env.BRANCH_NAME}"
  }

  /*triggers {
    pollSCM('H/2 * * * *')
  }

  stages {

    stage('Checkout') {
      steps { checkout scm }
    }
  */
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
/*
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('SonarQubeCloud') {
          withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
          sh 'sonar-scanner'
        } 
        }
      }
    }

stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('SonarQubeCloud') {
            script {
                def scannerHome = tool 'SonarScanner'
                sh "${scannerHome}/bin/sonar-scanner \
                  -Dsonar.projectKey=my-org_my-project \
                  -Dsonar.organization=my-org \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=https://sonarcloud.io \
                  -Dsonar.login=$SONAR_TOKEN"
            }
        }
    }
}

    stage('Quality Gate') {
      steps {
        waitForQualityGate abortPipeline: true
      }
    }
  */
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
