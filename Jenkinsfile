pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "hotelreservation-1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        DOCKER_PATH = "/usr/local/bin" // Standard Docker installation path on Mac
    }
    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Sanjayahirwar1323/BookingCancellationAI.git']])
                }
            }
        }
        stage('Setting up our Virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing dependencies............'
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
                        echo 'Building and Pushing Docker Image to GCR using Cloud Build.............'
                        sh '''
                        # Configure gcloud
                        export PATH=$PATH:${GCLOUD_PATH}:${DOCKER_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        
                        # Option 1: Use Google Cloud Build (recommended for M1 Macs)
                        gcloud builds submit --tag gcr.io/${GCP_PROJECT}/ml-hotelreservation:v1 .
                        
                        # Option 2: If you prefer local Docker build (keep as fallback)
                        # Uncomment these lines if you want to use local Docker instead of Cloud Build
                        # gcloud auth configure-docker --quiet
                        # docker build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/ml-hotelreservation:v1 .
                        # docker push gcr.io/${GCP_PROJECT}/ml-hotelreservation:v1
                        '''
                    }
                }
            }
        }
        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud run deploy ml-hotelreservation \
                        --image=gcr.io/${GCP_PROJECT}/ml-hotelreservation:v1 \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
