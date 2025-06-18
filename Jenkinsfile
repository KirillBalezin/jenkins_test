pipeline {
    agent none

    environment {
        REPO_NAME = 'kirbalezin/jenkins_test'
        CONTAINER_NAME = 'ladmin-calc-1'
        SERVER_IP = '10.128.0.17'
    }

    stages {
        stage('release info') {
            agent any
            steps {
                git branch: 'master', url: 'https://github.com/KirillBalezin/jenkins_test.git'
                script {
                    env.GIT_COMMIT_SHORT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim().take(7)
                    currentBuild.displayName = env.GIT_COMMIT_SHORT
                }
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        DOCKER_IMAGE = docker.build("${env.REPO_NAME}:${env.GIT_COMMIT_SHORT}")
                    }
                }
            }
        }

        stage('Run Tests') {
            agent any
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.image("${env.REPO_NAME}:${env.GIT_COMMIT_SHORT}").inside {
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
                    }
                }
            }
            post {
                always {
                    script {
                        sh "docker rmi ${env.REPO_NAME}:${env.GIT_COMMIT_SHORT} || true"
                        sh "docker rmi ${env.REPO_NAME}:latest || true"
                    }
                }
            }
        }

        stage ('variable') {
            agent none
            steps {
                script {
                    try {
                        timeout(time: 10, unit: 'MINUTES') {
                            env.CHOICE_UPDATE = input(
                                message: 'Update container?',
                                ok: 'Continue',
                                parameters: [
                                    choice(name: 'Choice', choices: ['Yes', 'No'])
                                ]
                            )
                        }
                    } catch(err) {
                        echo "Input timeout reached, defaulting to 'No'"
                        env.CHOICE_UPDATE = 'No'
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
ssh -o StrictHostKeyChecking=no ladmin@${env.SERVER_IP} <<ENDSSH
docker pull ${env.REPO_NAME}:${env.GIT_COMMIT_SHORT}
docker stop ${env.CONTAINER_NAME} || true
docker rm ${env.CONTAINER_NAME} || true
CALC_VERSION=${env.GIT_COMMIT_SHORT} docker compose up -d calc
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
                node {
                    echo "Done post actions"
                }
            }
        }
    }
}