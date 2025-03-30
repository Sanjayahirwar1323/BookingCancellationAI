pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "hotelreservation-1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Sanjayahirwar1323/BookingCancellationAI.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR with Multi-Platform Support.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        # Enable Docker Buildx for multi-platform builds
                        docker buildx create --use || true

                        # Build and push in one step for both amd64 and arm64 architectures
                        docker buildx build \
                            --platform linux/amd64,linux/arm64 \
                            -t gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --push .
                        '''
                    }
                }
            }
        }

        // stage('Deploy to Google Cloud Run'){
        //     steps{
        //         withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
        //             script{
        //                 echo 'Deploy to Google Cloud Run.............'
        //                 sh '''
        //                 export PATH=$PATH:${GCLOUD_PATH}


        //                 gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

        //                 gcloud config set project ${GCP_PROJECT}

        //                 gcloud run deploy ml-project \
        //                     --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
        //                     --platform=managed \
        //                     --region=us-central1 \
        //                     --allow-unauthenticated
                            
        //                 '''
        //             }
        //         }
        //     }
        // }
        
    }
}