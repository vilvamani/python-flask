node{    
    def git_commit = ""
    def author_email = ""
    def customImage = ""
    def mvnHome = tool 'M3'
    env.PATH = "${mvnHome}/bin:${env.PATH}"
    
    stage("CleanUp WorkSpace"){
        cleanWs()
    }
    
    stage("Git Checkout"){
        git url: 'https://github.com/vilvamani/python-flask.git'
    }
    
    stage("Read Author"){
        git_commit = sh label: 'get last commit', returnStdout: true, script: 'git rev-parse --short HEAD~0'
        author_email = sh label: 'get last commit', returnStdout: true, script: 'git log -1 --pretty=format:"%ae"'
    }
    
    stage("Python UnitTest"){
        sh "pip3 install -r requirements.txt"
        sh "python3 -m pytest test_*.py --junit-xml='reports.xml' --cov-report html --cov-report xml --cov-report term --cov"
    }

    stage("Publish Report"){
        publishHTML(target: [
            allowMissing: false, 
            alwaysLinkToLastBuild: true, 
            keepAll: true, 
            reportDir: 'htmlcov', 
            reportFiles: 'index.html', 
            reportName: 'HTML_Report', 
            reportTitles: 'Python UnitTest'
        ])
    }
    
    stage("SonarQube"){
        withSonarQubeEnv('SonarQube') {
            sh "mvn verify sonar:sonar"
        }
    }

    stage("Build Docker Image"){
        customImage = docker.build("my-image:${env.BUILD_ID}")
    }
}