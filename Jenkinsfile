pipeline {
    agent none

    environment {
        REPO_NAME = 'kirbalezin/jenkins_test'
        CONTAINER_NAME = 'calc'
        SERVER_IP = '10.128.0.17'
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
                            sh 'python -m unittest discover -s tests'
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
            steps {
                script {
                    try {
                        timeout(time: 10, unit: 'SECONDS') {
                            CHOICE_UPDATE = input(
                                message: 'Update container?',
                                ok: 'Continue',
                                parameters: [
                                    choice(name: 'Действие', choices: ['Yes', 'No'])
                                ]
                            )
                        }
                    } catch(err) {
                        // Если таймаут случился — назначаем "No"
                        echo "Input timeout reached, defaulting to 'No'"
                        CHOICE_UPDATE = 'No'
                    }
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
                    sshagent(['ssh_key']) {
                        sh """
ssh -o StrictHostKeyChecking=no ladmin@${SERVER_IP} <<ENDSSH
docker pull ${REPO_NAME}:${GIT_COMMIT_SHORT}
docker stop ${CONTAINER_NAME} || true
docker rm ${CONTAINER_NAME} || true
CALC_VERSION=${GIT_COMMIT_SHORT} docker compose up -d calc
ENDSSH
                        """
                    }
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