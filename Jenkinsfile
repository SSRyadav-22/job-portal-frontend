pipeline {
    agent any

    environment {
        APP_ID = "9xXf9kz_qwMyeEK-tHYeg" // YOUR CORRECT FRONTEND ID
    }

    parameters {
        string(name: 'DEPLOY_URL_CRED_ID', defaultValue: 'DEPLOY_URL', description: 'Credentials ID for the deployment URL (Secret Text)')
        string(name: 'DEPLOY_KEY_CRED_ID', defaultValue: 'DEPLOY_KEY', description: 'Credentials ID for the deployment API key (Secret Text)')
        string(name: 'VITE_CANDIDATES_ENDPOINT', defaultValue: 'VITE_CANDIDATES_ENDPOINT', description: 'Endpoint for candidates API (Secret Text)')
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
                  sh 'echo ".env created with VITE_CANDIDATES_ENDPOINT"'
                }
            }
        }

        stage('Install dependencies') {
            steps {
                // This uses Node.js, which is correct for the frontend
                sh 'npm install'
            }
        }

        stage('Run tests') {
            steps {
                // This runs Vitest, which is correct for the frontend
                sh 'npm test -- --run'
            }
        }

        stage('Build') {
            steps {
                // Create the production build
                sh 'npm run build'
            }
        }
    }    
    post {
        success {
            echo "✅ Tests passed, triggering deployment API..."
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
            // Mail code removed for brevity, will fail without App Password fix
        }

        failure {
            echo "❌ Pipeline failed, check console output for details."
            // Mail code removed for brevity
        }
    }
}
