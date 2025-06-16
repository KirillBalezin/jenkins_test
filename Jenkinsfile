pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.build('calculator-test-image')
                    }
                }
            }
        }

        stage('say hi') {
            steps {
                script {
                    echo "hi"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.image('calculator-test-image').inside {
                            sh 'python -m unittest discover -s tests -p "test_*.py"'
                        }
                    }
                }
            }
        }
    }

}