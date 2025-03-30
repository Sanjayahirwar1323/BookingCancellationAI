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
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        # Set paths for macOS (M1 specific)
                        export PATH="/usr/local/bin:${PATH}:/opt/homebrew/bin"
                        
                        # Activate GCP service account
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        
                        # Configure GCP project
                        gcloud config set project ${GCP_PROJECT}
                        
                        # Configure Docker for GCR with ARM64 architecture
                        gcloud auth configure-docker --quiet gcr.io
                        
                        # Build Docker image for ARM64 architecture
                        docker build --platform linux/arm64 -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        
                        # Push to GCR
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }
    }
}

    



//         stage('Deploy to Google Cloud Run'){
//             steps{
//                 withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
//                     script{
//                         echo 'Deploy to Google Cloud Run.............'
//                         sh '''
//                         export PATH=$PATH:${GCLOUD_PATH}


//                         gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

//                         gcloud config set project ${GCP_PROJECT}

//                         gcloud run deploy ml-project \
//                             --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
//                             --platform=managed \
//                             --region=us-central1 \
//                             --allow-unauthenticated
                            
//                         '''
//                     }
//                 }
//             }
//         }
        
//     }
// }