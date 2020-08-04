node{
    
    def git_commit = ""
    def author_email = ""
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
        py.test
    }
    
    stage("SonarQube"){
        withSonarQubeEnv('SonarQube') {
            sh "ls -l"
            sh "mvn sonar:sonar -X"
        }
    }
}