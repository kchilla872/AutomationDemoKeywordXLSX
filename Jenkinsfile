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
        stage('Archive and Publish HTML Report') {
            steps {
                // Archive the HTML report so it can be downloaded
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

                // Publish the HTML report in Jenkins UI
                publishHTML(target: [
                    reportDir: '.',                // Directory where report.html is located
                    reportFiles: 'report.html',   // Report file name
                    reportName: 'Pytest HTML Report',
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    allowMissing: false
                ])
            }
        }
    }
    post {
        always {
            // Optionally archive again to ensure report is persisted on any build outcome
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}
