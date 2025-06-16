pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('calculator-test-image')
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image('calculator-test-image').inside {
                        sh 'python -m unittest discover -s tests -p "test_*.py"'
                    }
                }
            }
        }
    }
}
