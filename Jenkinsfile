#!/usr/bin/env groovy
import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException

def label = "slave-${UUID.randomUUID().toString()}"
def IMAGE_VERSION = ''

def getGitCredentials() {
  def co = checkout(scm)
  sh 'git config --local credential.helper "!p() { echo username=\\$GIT_USERNAME; echo password=\\$GIT_PASSWORD; }; p"'
  GIT_COMMIT = co.GIT_COMMIT
}


def slackNotifier(String buildResult) {
	
  currentBuild.displayName = "#" + (currentBuild.number + ' - ' + buildResult)
	
  if ( buildResult == "SUCCESS" ) {
    slackSend color: "good", message: "Deployment of ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} : <${BUILD_URL}|Successfull>"
  }
  else if( buildResult == "FAILURE" ) { 
    slackSend color: "danger", message: "Deployment of ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} : <${BUILD_URL}|Failed>"
  }
  else if( buildResult == "UNSTABLE" ) { 
    slackSend color: "warning", message: "Deployment of ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} : <${BUILD_URL}|Unstable"
  }
  else {
    slackSend color: "danger", message: "Deployment of ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} : <${BUILD_URL}|Unclear"	
  }
}


podTemplate(label: label, containers: [
    containerTemplate(name: 'jnlp', image: 'jenkins/jnlp-slave:4.7-1-alpine', args: '${computer.jnlpmac} ${computer.name}', runAsGroup: '1000', runAsUser: '1000'),
    containerTemplate(name: 'sonarqube', image: 'sonarsource/sonar-scanner-cli:4.6', command: 'cat', ttyEnabled: true, runAsGroup: '1000', runAsUser: '1000'),
    containerTemplate(name: 'maven', image: 'algoshack/k8s-docker-slave:maven', command: 'cat', ttyEnabled: true, runAsGroup: '1000', runAsUser: '1000'),
    containerTemplate(name: 'python', image: 'algoshack/k8s-docker-slave:python', command: 'cat', ttyEnabled: true, runAsGroup: '1000', runAsUser: '1000'),
    containerTemplate(name: 'kaniko', image: 'gcr.io/kaniko-project/executor:debug', command: '/busybox/cat', ttyEnabled: true, privileged: true, runAsGroup: '0', runAsUser: '0'),
    containerTemplate(name: 'kubectl', image: 'bitnami/kubectl', command: 'cat', ttyEnabled: true, runAsGroup: '1000', runAsUser: '1000'),
  ],
  volumes: [
    configMapVolume(configMapName: 'docker-config', mountPath: '/kaniko/.docker/'),
  ],
  envVars: [],
  annotations: []/*,
  runAsUser: '1000',
  runAsGroup: '1000'*/
) {
  timeout(time: 30, unit: 'MINUTES') {
    try {
      node(label) {
        properties([
          disableConcurrentBuilds(),
        ])
        container('python') {

          stage("CleanUp WorkSpace") {
            cleanWs()
          }

          stage('Git Checkout') {
            getGitCredentials()
            IMAGE_VERSION = "${GIT_COMMIT}"
          }

          stage("Read Author") {
            git_commit = sh label: 'get last commit', returnStdout: true, script: 'git rev-parse --short HEAD~0'
            author_email = sh label: 'get last commit', returnStdout: true, script: 'git log -1 --pretty=format:"%ae"'
          }
        }
        
        container('maven') {
          stage('SonarQube') {
            withSonarQubeEnv('SonarQube') {
              sh "mvn verify sonar:sonar"
            }
          }
        }

        stage('Create Docker images') {
          container(name: 'kaniko', shell: '/busybox/sh') {
            withEnv(['PATH+EXTRA=/busybox:/kaniko']) {
            sh """
              #!/busybox/sh
              cp newrelic/newrelic.jar ./newrelic.jar
              rm -rf newrelic newrelic-java.zip
              /kaniko/executor -f `pwd`/Dockerfile -c `pwd` --destination=vilvamani007/springboot:${IMAGE_VERSION}
            """
            }
          }
        }


        if (env.BRANCH_NAME == 'master') {
          stage("Kubernetes") {
            container('kubectl') {
              sh """
                kubectl apply -f https://raw.githubusercontent.com/vilvamani/springboot/master/infra/k8s-deployment.yaml
                kubectl apply -f https://raw.githubusercontent.com/vilvamani/springboot/master/infra/k8s-service.yaml
	          """
            }
          }
        }

        currentBuild.result = 'SUCCESS'
      }
    } 
    catch (FlowInterruptedException interruptEx) {
      echo "Job was cancelled"
      currentBuild.result = 'FAILURE'
      throw interruptEx
    }
    catch (Exception err) {
      currentBuild.result = 'FAILURE'
    }
    finally{
	  /* Use slackNotifier.groovy from shared library and provide current build result as parameter */
      slackNotifier(currentBuild.result)
    }
  }
}
