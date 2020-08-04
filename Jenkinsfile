node {
    def git_commit = ""
    def author_email = ""
    def customImage = ""
    def docker_image_name = "vilvamani007/python_flask_app"

    def mvnHome = tool 'M3'
    env.PATH = "${mvnHome}/bin:${env.PATH}"

    properties([buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '7', numToKeepStr: '10')), disableConcurrentBuilds(), [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]])

    try {
        stage("CleanUp WorkSpace") {
            cleanWs()
        }

        stage("Git Checkout") {
            git url: 'https://github.com/vilvamani/python-flask.git'
        }

        stage("Read Author") {
            git_commit = sh label: 'get last commit',
                returnStdout: true,
                script: 'git rev-parse --short HEAD~0'
            author_email = sh label: 'get last commit',
                returnStdout: true,
                script: 'git log -1 --pretty=format:"%ae"'
        }

        stage("Python UnitTest") {
            sh "pip3 install -r requirements.txt"
            sh "python3 -m pytest test_*.py --junit-xml='reports.xml' --cov-report html --cov-report xml --cov-report term --cov"
        }

        stage("Publish Report") {
            publishHTML(target: [
                allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'HTML_Report', reportTitles: 'Python UnitTest'
            ])
        }

        stage("SonarQube") {
            withSonarQubeEnv('SonarQube') {
                sh "mvn verify sonar:sonar"
            }
        }

        stage("Build Docker Image") {
            customImage = docker.build(docker_image_name)
        }

        stage("Regression Test - Postman Collection") {
            docker.image("${docker_image_name}:latest").withRun("-p 5000:5000") {
                sh 'newman run python-flask.postman_collection.json --reporters cli,junit --reporter-junit-export "newman/myreport.xml"'

                junit 'newman/myreport.xml'
            }
        }

        stage("Docker Push & CleanUp") {
            // This step should not normally be used in your script. Consult the inline help for details.
            withDockerRegistry(credentialsId: 'docker_hub', url: 'https://index.docker.io/v1/') {
                customImage.push("${env.BUILD_NUMBER}")
                customImage.push("${git_commit}")
                customImage.push("latest")
            }

            // Remove dangling Docker images
            sh "docker image prune --all --force"
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        currentBuild.displayName = "#" + (currentBuild.number + ' - ' + currentBuild.result)
        println "::: Catching the exception :::"
        println e
    } finally {
        //The finally block always executes. 
        if (currentBuild.result != 'FAILURE') {
            currentBuild.result = 'SUCCESS'
            currentBuild.displayName = "#" + (currentBuild.number + ' - ' + currentBuild.result)
        }
    }
}