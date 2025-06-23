pipeline {
    agent any

    environment {
        AWS_ENDPOINT = 'https://storage.yandexcloud.net'
        BUCKET = 'ib-builds'
        REPO_NAME = 'kirbalezin/bspb-ib'
    }

    parameters {
        string(name: 'RELEASE', defaultValue: 'release-2025-06-zero-client-private',  description: 'release name')
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    deleteDir()
                    currentBuild.displayName = RELEASE
                }
            }
        }

        stage('Find release file') {
            steps {
                withAWS(credentials: 'yc_ib_builds', endpointUrl: env.AWS_ENDPOINT) {
                    script {
                        def files = s3FindFiles(bucket: env.BUCKET, path: "${RELEASE}/", glob: '*.zip').findAll { !it.directory }

                        echo "Files: ${files}"

                        if (files.isEmpty()) {
                            echo "The release was not found"
                            def releases = s3FindFiles(bucket: env.BUCKET).findAll { it.directory }
                            echo "Avaliable releases: ${releases}"
                            sh 'exit 1'
                        } else {
                            def latestFile = files[0]
                            for (f in files) {
                                if (f.lastModified > latestFile.lastModified) {
                                    latestFile = f
                                }
                            }
                            echo "Latest file: ${latestFile.name} - Last Modified: ${new Date(latestFile.lastModified)}"
                            LATEST_FILE = latestFile.name
                        }
                    }
                }
            }
        }

        stage('Download release') {
            steps {
                script {
                    withAWS(credentials: 'yc_ib_builds', endpointUrl: env.AWS_ENDPOINT) {
                        s3Download(
                            bucket: env.BUCKET,
                            file: "${env.WORKSPACE}/${LATEST_FILE}",
                            path: "${RELEASE}/${LATEST_FILE}",
                            force: true
                        )
                    }
                }
            }
        }

        stage('Unzip release') {
            steps {
                script {
                    sh "unzip -o ${WORKSPACE}/${LATEST_FILE} -d ${WORKSPACE}/bspb/"
                }
            }
        }

        stage('Docker build') {
            steps {
                script {
                    RELEASE_NAME = LATEST_FILE - '.zip'
                    sh "echo ${RELEASE_NAME}"
                    docker.withServer('tcp://docker-dind:2375') {
                        DOCKER_IMAGE = docker.build("${env.REPO_NAME}:${RELEASE_NAME}")
                    }
                }
            }
        }

        stage('Docker push') {
            steps {
                script {
                    docker.withServer('tcp://docker-dind:2375') {
                        docker.withRegistry('', 'dhLogin') {
                            DOCKER_IMAGE.push()
                        }
                    }
                }
            }
        }
    }
}
