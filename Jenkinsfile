stages {
    stage('Setup Environment') {
        steps {
            script {
                bat '''
                    cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    playwright install chromium firefox webkit --with-deps
                '''
            }
        }
    }

    stage('Run Tests in Parallel') {
        parallel {
            stage('Test on Chromium') {
                steps {
                    script {
                        bat '''
                            cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                            call venv\\Scripts\\activate
                            pytest test_runner.py -v --browser=chromium --html=report_chromium.html --css=custom.css --self-contained-html
                        '''
                    }
                }
            }

            stage('Test on Firefox') {
                steps {
                    script {
                        bat '''
                            cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                            call venv\\Scripts\\activate
                            pytest test_runner.py -v --browser=firefox --html=report_firefox.html --css=custom.css --self-contained-html
                        '''
                    }
                }
            }

            stage('Test on WebKit') {
                steps {
                    script {
                        bat '''
                            cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenDemo0905"
                            call venv\\Scripts\\activate
                            pytest test_runner.py -v --browser=webkit --html=report_webkit.html --css=custom.css --self-contained-html
                        '''
                    }
                }
            }
        }
    }

    stage('Archive and Publish Reports') {
        steps {
            archiveArtifacts artifacts: 'report_*.html', allowEmptyArchive: false

            publishHTML([
                reportDir: '.',
                reportFiles: 'report_chromium.html',
                reportName: 'Chromium Test Report',
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])

            publishHTML([
                reportDir: '.',
                reportFiles: 'report_firefox.html',
                reportName: 'Firefox Test Report',
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])

            publishHTML([
                reportDir: '.',
                reportFiles: 'report_webkit.html',
                reportName: 'WebKit Test Report',
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])
        }
    }
}

post {
    always {
        echo 'Test execution completed'
    }
    success {
        echo 'All tests passed successfully!'
    }
    failure {
        echo 'Some tests failed. Check the reports.'
    }
}
