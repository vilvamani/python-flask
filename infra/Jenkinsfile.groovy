#!groovy

properties([
    disableConcurrentBuilds(),
    buildDiscarder(logRotator(daysToKeepStr: '7', numToKeepStr: '10'))
])

current_branch = "${env.BRANCH_NAME}"

jenkins_common_branch = "develop"
jenkins_common_repo_url = "https://github.com/vilvamani/jenkins_common_library.git"
jenkins_common_checkout_dir = "jenkins_library"
jenkins_common_file = "jenkins_common_library.groovy"

params = [
    branch_checkout_dir: 'service',
    service: 'python-flask',
    branch: current_branch,
    repo_url: 'https://github.com/vilvamani/python-flask.git',
    dockerRepoName: 'vilvamani007',
    dockerImageName: 'python-flask',
    kubeDeploymentFile: './infra/k8s-deployment.yaml',
    kubeServiceFile: './infra/k8s-service.yaml',
    jenkins_slack_channel: "infra-development",
    skip_unit_test: false,
    skip_integration_test: true,
    skip_sonar: false,
    skip_artifactory: true,
    skip_docker_push: false,
    skip_kubernetes_deployment: false,
    skip_notification: false
]

node('python-slave') {

    step([$class: 'WsCleanup'])
    jenkinsLibrary = loadJenkinsCommonLibrary()
    jenkinsLibrary.defaultConfigs(params)
    timestamps {
        try {
            jenkinsLibrary.pythonFlaskBuild(params)
        } catch (NoSuchMethodError err) {
            currentBuild.result = 'FAILURE'
            throw err
        } catch (Exception err) {
            currentBuild.result = 'FAILURE'
            throw err
        } finally {
            jenkinsLibrary.sendSlack(params)
        }
    }
}

def loadJenkinsCommonLibrary() {
    dir(jenkins_common_checkout_dir) {
        git(url: jenkins_common_repo_url, branch: jenkins_common_branch)
            def jenkinsLibrary = load "${jenkins_common_file}"
            return jenkinsLibrary
    }
}