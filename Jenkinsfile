pipeline {
    agent none

    environment {
        REPO_NAME = 'kirbalezin/jenkins_test'
    }

    stages {
        stage('release info') {
            agent any
            steps {
                git branch: 'master', url: 'https://github.com/KirillBalezin/jenkins_test.git'
                script {
                    GIT_COMMIT_SHORT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim().take(7)
                    currentBuild.displayName = "$GIT_COMMIT_SHORT"
                }
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        DOCKER_IMAGE = docker.build("${REPO_NAME}:${GIT_COMMIT_SHORT}")
                    }
                }
            }
        }

        stage('Run Tests') {
            agent any
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.image("${REPO_NAME}:${GIT_COMMIT_SHORT}").inside {
                            sh 'python -m unittest discover -s tests -p "test_*.py"'
                        }
                    }
                }
            }
        }

        stage ('Send to Docker Hub') {
            agent any
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.withRegistry('', 'dhLogin') {
                            DOCKER_IMAGE.push()
                            DOCKER_IMAGE.push("latest")
                        }
                        sh "docker rmi ${REPO_NAME}:${GIT_COMMIT_SHORT} || true"
                        sh "docker rmi ${REPO_NAME}:latest || true"
                    }
                }
            }
        }

        stage ('variable') {
            agent any
            steps {
                script {
                    CHOICE_UPDATE = input(
                        message: 'Update container?',
                        ok: 'Continue',
                        parameters: [
                            choice(name: 'Действие', choices: ['Yes', 'No'])
                        ]
                    )
                }
            }
        }

        stage ('container update') {
            agent any
            when {
                expression { CHOICE_UPDATE == 'Yes' }
            }
            steps {
                script {
                    echo "update ...."
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Done post actions"
            }
        }
    }

}
