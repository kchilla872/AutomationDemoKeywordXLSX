pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                        call venv\\Scripts\\activate
                        pip install -r requirements.txt
                        playwright install chromium --with-deps
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                        call venv\\Scripts\\activate
                        pytest test_runner.py --headed --slowmo=1000 --html=report.html --self-contained-html
                    '''
                }
            }
        }
        stage('Archive HTML Report') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}
