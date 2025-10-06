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
                                pytest test_runner.py -v --browser chromium --headed --slowmo 1000 --html=report_chromium.html --self-contained-html
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
                                pytest test_runner.py -v --browser firefox --headed --slowmo 1000 --html=report_firefox.html --self-contained-html
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
                                pytest test_runner.py -v --browser webkit --headed --slowmo 1000 --html=report_webkit.html --self-contained-html
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
                    keepAll: true,
                    allowMissing: false
                ])

                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report_firefox.html',
                    reportName: 'Firefox Test Report',
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    allowMissing: false
                ])

                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report_webkit.html',
                    reportName: 'WebKit Test Report',
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    allowMissing: false
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
}