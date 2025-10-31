pipeline {
    agent any

    environment {
        // PASTE YOUR NEW FRONTEND ID FROM THE PYTHON SCRIPT HERE
        APP_ID = "yi7ZEJXMAXYYxzfYB4tYO" 
    }

    parameters {
        string(name: 'DEPLOY_URL_CRED_ID', defaultValue: 'DEPLOY_URL', description: 'Credentials ID for the deployment URL (Secret Text)')
        string(name: 'DEPLOY_KEY_CRED_ID', defaultValue: 'DEPLOY_KEY', description: 'Credentials ID for the deployment API key (Secret Text)')
        string(name: 'VITE_CANDIDATES_ENDPOINT', defaultValue: 'VITE_CANDIDATES_ENDPOINT', description: 'Endpoint for candidates API used by the frontend (exported into .env)')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup .env') {
            steps {
                withCredentials([
                    string(credentialsId: params.VITE_CANDIDATES_ENDPOINT, variable: 'CANDIDATES_URL')
                ]) { 
                    sh "echo 'VITE_CANDIDATES_ENDPOINT=${CANDIDATES_URL}' > .env"
                    sh 'echo ".env file created successfully with real URL"'
                }
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'node -v && npm --version && (npm ci || npm install)'
            }
        }

        stage('Run tests') {
            steps {
                sh 'npm test -- --run'
            }
        }

        // ---------------------------------------------------
        // THIS IS THE MISSING STAGE THAT WILL FIX YOUR BUILD
        // ---------------------------------------------------
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
        // ---------------------------------------------------

    }    
    post {
        success {
            echo "✅ Build and tests passed, triggering deployment API..."
            withCredentials([
                string(credentialsId: params.DEPLOY_URL_CRED_ID, variable: 'DEPLOY_URL'),
                string(credentialsId: params.DEPLOY_KEY_CRED_ID, variable: 'DEPLOY_KEY')
            ]) {
                sh '''
                json_payload=$(printf '{"applicationId":"%s"}' "$APP_ID")
                curl -fS -X POST \
                    "$DEPLOY_URL" \
                    -H 'accept: application/json' \
                    -H 'Content-Type: application/json' \
                    -H "x-api-key: $DEPLOY_KEY" \
                    --data-binary "$json_payload" \
                    -w "\nHTTP %{http_code}\n"
                '''
            }
            mail to: 'xaioene@gmail.com', // Update this to your email
                 subject: "Jenkins Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Build #${env.BUILD_NUMBER} succeeded and deployed."
        }
        failure {
            echo "❌ Pipeline failed, sending error email..."
            mail to: 'xaioene@gmail.com', // Update this to your email
                 subject: "Jenkins Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Build #${env.BUILD_NUMBER} failed. Check console: ${env.BUILD_URL}"
        }
    }
}